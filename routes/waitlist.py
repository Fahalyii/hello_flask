# waitlist.py

from flask import Blueprint, request, redirect, url_for, flash, render_template
from flask_login import login_required, current_user
from models import db, Waitlist, Restaurant
from flask_login import login_required

waitlist_bp = Blueprint('waitlist', __name__)

# ✅ 1. Join Waitlist
@waitlist_bp.route('/join_waitlist/<int:restaurant_id>', methods=['POST'])
@login_required
def join_waitlist(restaurant_id):
    restaurant = Restaurant.query.get(restaurant_id)

    if not restaurant:
        flash('Restaurant not found.', 'danger')
        return redirect(url_for('restaurant.list_restaurants_page'))

    # Check if user already in waitlist
    existing = Waitlist.query.filter_by(user_id=current_user.id, restaurant_id=restaurant_id, status="Waiting").first()

    if existing:
        flash('You are already on the waitlist for this restaurant.', 'warning')
        return redirect(url_for('restaurant.list_restaurants_page'))

    try:
        new_waitlist = Waitlist(
            user_id=current_user.id,
            restaurant_id=restaurant_id,
            status="Waiting"
        )

        db.session.add(new_waitlist)
        db.session.commit()

        flash('Successfully joined the waitlist.', 'success')
        return redirect(url_for('restaurant.list_restaurants_page'))

    except Exception as e:
        print(f"ERROR: {str(e)}")
        flash('Internal server error.', 'danger')
        return redirect(url_for('restaurant.list_restaurants_page'))
