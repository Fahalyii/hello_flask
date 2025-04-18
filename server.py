from flask import Flask, render_template
from flask_login import LoginManager
from config import Config
from database import db
from routes import init_routes
from models import User, Restaurant
from flask import request, render_template


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
@app.route('/restaurants')
def restaurants():
    cuisine = request.args.get('cuisine')
    query = Restaurant.query

    if cuisine:
        query = query.filter(Restaurant.cuisine == cuisine)

    restaurants = query.all()
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

@app.route('/test')
def test():
    return render_template('test.html')

if __name__ == "__main__":
    app.run(debug=True)
