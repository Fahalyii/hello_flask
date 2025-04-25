from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_required, current_user
from models import db, Restaurant, Table

restaurant_bp = Blueprint('restaurant', __name__)

# View all restaurants (Public)
@restaurant_bp.route('/restaurants')
def view_restaurants():
    try:
        restaurants = Restaurant.query.all()
        return render_template('restaurants.html', restaurants=restaurants)
    except Exception as e:
        print(f"ERROR: {str(e)}")  # Debugging error
        flash("An error occurred while fetching restaurants.", "danger")
        return redirect(url_for('home'))

# Add a new restaurant (For Managers Only)
@restaurant_bp.route('/add_restaurant', methods=['GET', 'POST'])
@login_required
def add_restaurant():
    if current_user.role != "restaurant_manager":
        flash("You are not authorized to add a restaurant!", "danger")
        return redirect(url_for('restaurant.view_restaurants'))

    if request.method == 'POST':
        try:
            name = request.form['name']
            location = request.form['location']

            new_restaurant = Restaurant(name=name, location=location, manager_id=current_user.id)
            db.session.add(new_restaurant)
            db.session.commit()
            flash("Restaurant added successfully!", "success")
            return redirect(url_for('restaurant.restaurant_dashboard'))

        except Exception as e:
            print(f"ERROR: {str(e)}")  # Debugging error
            flash("An error occurred. Please try again.", "danger")
            return redirect(url_for('restaurant.add_restaurant'))

    return render_template('add_restaurant.html')

# View restaurant dashboard (For Managers Only)
@restaurant_bp.route('/dashboard')
@login_required
def restaurant_dashboard():
    if current_user.role != "restaurant_manager":
        flash("Unauthorized access!", "danger")
        return redirect(url_for('restaurant.view_restaurants'))

    restaurants = Restaurant.query.filter_by(manager_id=current_user.id).all()
    return render_template('restaurant_dashboard.html', restaurants=restaurants)

# Add a table to a restaurant (For Managers Only)
@restaurant_bp.route('/add_table/<int:restaurant_id>', methods=['POST'])
@login_required
def add_table(restaurant_id):
    if current_user.role != "restaurant_manager":
        flash("Unauthorized!", "danger")
        return redirect(url_for('restaurant.restaurant_dashboard'))

    try:
        capacity = request.form['capacity']
        new_table = Table(restaurant_id=restaurant_id, capacity=capacity, is_available=True)
        db.session.add(new_table)
        db.session.commit()

        flash("Table added successfully!", "success")
        return redirect(url_for('restaurant.restaurant_dashboard'))

    except Exception as e:
        print(f"ERROR: {str(e)}")  # Debugging error
        flash("An error occurred. Please try again.", "danger")
        return redirect(url_for('restaurant.restaurant_dashboard'))
