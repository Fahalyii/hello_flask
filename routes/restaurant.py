# restaurant.py

from flask import Blueprint, request, jsonify, render_template, redirect, url_for, flash
from flask_login import login_required, current_user
from models import db, Restaurant, Table
from flask_login import login_required

restaurant_bp = Blueprint('restaurant', __name__)

# ✅ 1. User-Friendly Page (HTML)
@restaurant_bp.route('/restaurants', methods=['GET'])
def list_restaurants_page():
    cuisine = request.args.get('cuisine')
    query = Restaurant.query

    if cuisine:
        query = query.filter(Restaurant.cuisine == cuisine)

    restaurants = query.all()

    return render_template('restaurants.html', restaurants=restaurants)


# ✅ 2. API Endpoint (JSON list for developers or dashboard)
@restaurant_bp.route('/api/restaurants', methods=['GET'])
def list_restaurants_api():
    try:
        restaurants = Restaurant.query.all()

        restaurants_list = []
        for res in restaurants:
            restaurants_list.append({
                "id": res.id,
                "name": res.name,
                "location": res.location,
                "cuisine": res.cuisine,
                "image": res.image,
                "menu_image": res.menu_image
            })

        return jsonify(restaurants_list)

    except Exception as e:
        print(f"ERROR: {str(e)}")
        return jsonify({"status": "error", "message": "Internal server error."}), 500


# ✅ 3. Add New Restaurant (Only for Restaurant Managers)
@restaurant_bp.route('/add_restaurant', methods=['POST'])
@login_required
def add_restaurant():
    if current_user.role != "restaurant_manager":
        return jsonify({"status": "error", "message": "Unauthorized"}), 403

    try:
        name = request.form.get('name')
        location = request.form.get('location')
        cuisine = request.form.get('cuisine')

        new_restaurant = Restaurant(
            name=name,
            location=location,
            cuisine=cuisine,
            manager_id=current_user.id
        )

        db.session.add(new_restaurant)
        db.session.commit()

        flash('Restaurant added successfully.', 'success')
        return redirect(url_for('restaurant.list_restaurants_page'))

    except Exception as e:
        print(f"ERROR: {str(e)}")
        flash('Failed to add restaurant.', 'danger')
        return redirect(url_for('restaurant.list_restaurants_page'))


# ✅ 4. Restaurant Dashboard (Only for Restaurant Managers)
@restaurant_bp.route('/restaurant_dashboard')
@login_required
def restaurant_dashboard():
    if current_user.role != "restaurant_manager":
        flash('Unauthorized access.', 'danger')
        return redirect('/')

    restaurants = Restaurant.query.filter_by(manager_id=current_user.id).all()

    return render_template('restaurant_dashboard.html', restaurants=restaurants)


# ✅ 5. View Single Restaurant Details (for frontend API)
@restaurant_bp.route('/api/restaurant/<int:restaurant_id>', methods=['GET'])
def get_restaurant_api(restaurant_id):
    r = Restaurant.query.get(restaurant_id)
    if not r:
        return jsonify({"status": "error", "message": "Not found"}), 404

    # No need to add 'images/' manually because your database already stores "images/xxx.jpg"
    image_filename = r.menu_image or r.image
    if image_filename:
        image_url = url_for('static', filename=image_filename)
    else:
        image_url = url_for('static', filename='images/default_restaurant.jpg')

    return jsonify({
        "status": "success",
        "restaurant": {
            "id": r.id,
            "name": r.name,
            "location": r.location,
            "cuisine": r.cuisine,
            "image": image_url
        }
    })





# ✅ 6. Add New Table to Restaurant (Only for Manager)
@restaurant_bp.route('/add_table/<int:restaurant_id>', methods=['POST'])
@login_required
def add_table(restaurant_id):
    if current_user.role != "restaurant_manager":
        return jsonify({"status": "error", "message": "Unauthorized"}), 403

    try:
        capacity = int(request.form.get('capacity'))

        new_table = Table(
            restaurant_id=restaurant_id,
            capacity=capacity,
            is_available=True
        )

        db.session.add(new_table)
        db.session.commit()

        flash('Table added successfully.', 'success')
        return redirect(url_for('restaurant.restaurant_dashboard'))

    except Exception as e:
        print(f"ERROR: {str(e)}")
        flash('Failed to add table.', 'danger')
        return redirect(url_for('restaurant.restaurant_dashboard'))

