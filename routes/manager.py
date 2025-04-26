# routes/manager.py

from flask import Blueprint, render_template
from flask_login import login_required, current_user
from models import Restaurant

manager_bp = Blueprint('manager', __name__)

@manager_bp.route('/dashboard')
@login_required
def dashboard():
    if not current_user.is_authenticated:
        return "Access denied22."  # Not logged in (extra safe)

    if current_user.role is None or current_user.role.lower() != 'manager':
        return "Access denied33."  # Not a manager

    if not current_user.restaurant_id:
        return render_template('wait_admin.html')
    else:
        restaurant = Restaurant.query.get(current_user.restaurant_id)
        return render_template('manager_dashboard.html', restaurant=restaurant)
