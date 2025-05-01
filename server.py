from flask import Flask, render_template, request, redirect
from flask_login import LoginManager, login_required, current_user
from flask_mail import Mail, Message

from config import Config
from database import db
from models import User, Restaurant, Review, Reservation, Waitlist
from sqlalchemy import func
from datetime import datetime, date
from email_utils import mail, init_mail  # ✅ Correct
from routes import init_routes  # ✅ Moved after app setup
from email_utils import mail, init_mail
from flask import request, render_template
from models import Restaurant

mail = Mail()


app = Flask(__name__)
app.config.from_object(Config)

# Init SQLAlchemy
db.init_app(app)
init_mail(app)

# Init Flask-Login
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'auth.login'



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
    rating_filter = request.args.get('rating', type=int)
    price_filter = request.args.get('price')
    sort_option = request.args.get('sort', 'recommended')

    query = Restaurant.query

    # Filter by Cuisine
    if cuisine and cuisine != "All Cuisines":
        query = query.filter(Restaurant.cuisine == cuisine)

    # Filter by Price
    if price_filter:
        try:
            price_filter = int(price_filter)
            if price_filter == 101:
                query = query.filter(Restaurant.price.cast(db.Integer) > 100)
            else:
                query = query.filter(Restaurant.price.cast(db.Integer) <= price_filter)
        except ValueError:
            pass

    restaurants = query.all()

    # Calculate average rating and review count for each restaurant
    for restaurant in restaurants:
        avg_rating = db.session.query(func.avg(Review.rating)).filter(Review.restaurant_id == restaurant.id).scalar()
        review_count = db.session.query(func.count(Review.id)).filter(Review.restaurant_id == restaurant.id).scalar()

        if avg_rating is not None:
            restaurant.rating = round(avg_rating, 1)
        else:
            restaurant.rating = None

        restaurant.review_count = review_count or 0

    # Filter by Rating (AFTER calculating)
    if rating_filter:
        restaurants = [r for r in restaurants if r.rating and r.rating >= rating_filter]

    # ✅ Sort Restaurants
    if sort_option == "highest_rated":
        restaurants.sort(key=lambda r: (r.rating or 0), reverse=True)
    elif sort_option == "most_popular":
        restaurants.sort(key=lambda r: (r.review_count or 0), reverse=True)
    elif sort_option == "price_low_high":
        restaurants.sort(key=lambda r: int(r.price) if r.price else 9999)
    elif sort_option == "price_high_low":
        restaurants.sort(key=lambda r: int(r.price) if r.price else 0, reverse=True)
    else:
        # recommended (default)
        restaurants.sort(key=lambda r: r.id)

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





@app.route('/book.html')
def claude_book():
    restaurant_id = request.args.get('id')
    if not restaurant_id:
        return redirect('/restaurants')  # ✅ redirect silently if no ID

    return render_template('book.html')


@app.route('/dashboard')
@login_required
def dashboard():
    from routes.reservation import auto_cancel_expired_reservations

    if current_user.role == "restaurant_manager":
        assigned_restaurant = Restaurant.query.filter_by(manager_id=current_user.id).first()

        if not assigned_restaurant:
            return render_template('wait_admin.html')

        # 🚀 Get fresh reservations now
        reservations = Reservation.query.filter(
            Reservation.restaurant_id == assigned_restaurant.id,
            Reservation.status.in_(['Pending', 'Awaiting Payment', 'Confirmed'])
        ).all()

        waiting_list_reservations = Reservation.query.filter(
            Reservation.restaurant_id == assigned_restaurant.id,
            Reservation.status == 'In the Waiting List'
        ).all()

        auto_cancel_expired_reservations(reservations)

        available_seats = sum(table.capacity for table in assigned_restaurant.tables if table.is_available)
        guest_sum = sum(reservation.guest_count for reservation in reservations)

        return render_template('manager_dashboard.html',
                               restaurant=assigned_restaurant,
                               reservations=reservations,
                               waiting_list_reservations=waiting_list_reservations,
                               available_seats=available_seats,
                               guest_sum=guest_sum)
    else:
        restaurants = Restaurant.query.limit(4).all()
        return render_template('index.html', restaurants=restaurants)





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

def send_email(to, subject, body):
    msg = Message(subject, recipients=[to])
    msg.body = body
    msg.sender = app.config['MAIL_USERNAME']
    mail.send(msg)

@app.route('/search_restaurants', methods=['GET'])
def search_restaurants():
    query = request.args.get('query', '')

    restaurants_query = Restaurant.query

    if query:
        search_pattern = f"%{query}%"
        restaurants_query = restaurants_query.filter(
            Restaurant.name.ilike(search_pattern) |
            Restaurant.location.ilike(search_pattern) |
            Restaurant.cuisine.ilike(search_pattern)
        )

    filtered_restaurants = restaurants_query.all()

    return render_template('restaurants.html',
                           restaurants=filtered_restaurants,
                           query=query)
