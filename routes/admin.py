# admin.py

from flask import Blueprint, jsonify, request
from models import db, User, Restaurant
from routes.auth import token_required  # correct

admin_bp = Blueprint('admin', __name__)

# ✅ Secure admin check
def is_admin():
    return request.current_user.role == 'admin'

@admin_bp.route('/admin/users')
@token_required
def view_users():
    if not is_admin():
        return jsonify({"status": "error", "message": "Unauthorized"}), 403

    users = User.query.all()
    user_list = [{
        "id": user.id,
        "name": user.name,
        "email": user.email,
        "role": user.role
    } for user in users]

    return jsonify(user_list), 200

@admin_bp.route('/admin/restaurants')
@token_required
def view_restaurants():
    if not is_admin():
        return jsonify({"status": "error", "message": "Unauthorized"}), 403

    restaurants = Restaurant.query.all()
    rest_list = [{
        "id": res.id,
        "name": res.name,
        "location": res.location,
        "cuisine": res.cuisine,
        "manager_id": res.manager_id
    } for res in restaurants]

    return jsonify(rest_list), 200

@admin_bp.route('/admin/delete_user/<int:user_id>', methods=['POST'])
@token_required
def delete_user(user_id):
    if not is_admin():
        return jsonify({"status": "error", "message": "Unauthorized"}), 403

    user = User.query.get(user_id)
    if not user:
        return jsonify({"status": "error", "message": "User not found"}), 404

    try:
        db.session.delete(user)
        db.session.commit()
        return jsonify({"status": "success", "message": "User deleted successfully."}), 200
    except Exception as e:
        print(f"ERROR: {str(e)}")
        return jsonify({"status": "error", "message": "Internal server error."}), 500

@admin_bp.route('/admin/delete_restaurant/<int:restaurant_id>', methods=['POST'])
@token_required
def delete_restaurant(restaurant_id):
    if not is_admin():
        return jsonify({"status": "error", "message": "Unauthorized"}), 403

    restaurant = Restaurant.query.get(restaurant_id)
    if not restaurant:
        return jsonify({"status": "error", "message": "Restaurant not found"}), 404

    try:
        db.session.delete(restaurant)
        db.session.commit()
        return jsonify({"status": "success", "message": "Restaurant deleted successfully."}), 200
    except Exception as e:
        print(f"ERROR: {str(e)}")
        return jsonify({"status": "error", "message": "Internal server error."}), 500
