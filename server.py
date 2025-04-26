from flask import Flask, render_template
from flask_login import LoginManager
from config import Config
from database import db
from routes import init_routes
from models import User, Restaurant, Review
from flask import request, render_template
from flask_login import login_required, current_user
from sqlalchemy import func

app = Flask(__name__)
app.config.from_object(Config)

# Init SQLAlchemy
db.init_app(app)

# Init Flask-Login
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'auth.login'
from flask import request, render_template
from models import Restaurant


@app.route('/search')
def search_restaurants():
    query = request.args.get('query', '').strip()
    if query:
        restaurants = Restaurant.query.filter(
            Restaurant.name.ilike(f'%{query}%') |
            Restaurant.cuisine.ilike(f'%{query}%') |
            Restaurant.location.ilike(f'%{query}%')
        ).all()
    else:
        restaurants = Restaurant.query.all()

    return render_template('restaurants.html', restaurants=restaurants)
from sqlalchemy import func

@app.route('/restaurants')
def restaurants():
    cuisine = request.args.get('cuisine')
    query = Restaurant.query

    if cuisine:
        query = query.filter(Restaurant.cuisine == cuisine)

    restaurants = query.all()

    # Calculate average ratings for each restaurant
    for restaurant in restaurants:
        avg_rating = db.session.query(func.avg(Review.rating)).filter(Review.restaurant_id == restaurant.id).scalar()
        if avg_rating:
            restaurant.rating = round(avg_rating, 1)  # round to 1 decimal place
        else:
            restaurant.rating = None  # No reviews yet

    return render_template('restaurants.html', restaurants=restaurants)

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))



# Register all routes (Blueprints)
init_routes(app)

# Routes
@app.route("/")
def home():
    restaurants = Restaurant.query.limit(4).all()
    return render_template("index.html", restaurants=restaurants)

@app.route('/aboutUs')
def aboutUs():
    return render_template('aboutUs.html')

@app.route('/restaurant')
def restaurant():
    return render_template('restaurant.html')
@app.route('/login')
def login():
    return render_template('login.html')

@app.route('/register')
def register():
    return render_template('register.html')
@app.route('/test')
def test():
    return render_template('test.html')



@app.route('/ClaudeBookGPT.html')
def claude_book():
    return render_template('ClaudeBookGPT.html')


@app.route('/dashboard')
@login_required
def dashboard():
    if current_user.role == "restaurant_manager":
        assigned_restaurant = Restaurant.query.filter_by(manager_id=current_user.id).first()

        if not assigned_restaurant:
            return render_template('wait_admin.html')

        reservations = []
        for table in assigned_restaurant.tables:
            for reservation in table.reservations:
                reservations.append(reservation)

        available_seats = sum(table.capacity for table in assigned_restaurant.tables if table.is_available)

        # 🔥 NEW: calculate guest_sum in backend
        guest_sum = sum(reservation.guest_count for reservation in reservations)

        return render_template('manager_dashboard.html',
                               restaurant=assigned_restaurant,
                               reservations=reservations,
                               available_seats=available_seats,
                               guest_sum=guest_sum)
    else:
        return render_template('index.html')


@app.route('/restaurant/<int:restaurant_id>')
def restaurant_details(restaurant_id):
    restaurant = Restaurant.query.get_or_404(restaurant_id)
    reviews = Review.query.filter_by(restaurant_id=restaurant_id).order_by(Review.timestamp.desc()).all()
    avg_rating = db.session.query(func.avg(Review.rating)).filter(Review.restaurant_id == restaurant_id).scalar()

    if avg_rating:
        avg_rating = round(avg_rating, 1)
    else:
        avg_rating = "N/A"

    return render_template('restaurant_details.html',
                           restaurant=restaurant,
                           reviews=reviews,
                           avg_rating=avg_rating)


if __name__ == "__main__":
    app.run(debug=True)
