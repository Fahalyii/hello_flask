# reservation.py

from flask import Blueprint, request, redirect, url_for, flash, jsonify, render_template
from flask_login import login_required, current_user
from models import db, Reservation, Table, Notification
from datetime import datetime
from flask_login import login_required

reservation_bp = Blueprint('reservation', __name__)

# Utility function: Send notification
def send_notification(user_id, message):
    notification = Notification(user_id=user_id, message=message)
    db.session.add(notification)
    db.session.commit()

# ✅ 1. Reserve a Table (Form POST)
@reservation_bp.route('/reserve/<int:restaurant_id>', methods=['POST'])
@login_required
def reserve_table(restaurant_id):
    table = Table.query.filter_by(restaurant_id=restaurant_id, is_available=True).first()

    if not table:
        flash("No available table at the moment", "danger")
        return redirect(url_for('restaurant.list_restaurants_page'))

    date_str = request.form.get('date')
    time_str = request.form.get('time')
    guest_count = request.form.get('guest_count')

    if not date_str or not time_str or not guest_count:
        flash('Missing reservation fields.', 'danger')
        return redirect(url_for('restaurant.list_restaurants_page'))

    try:
        new_reservation = Reservation(
            user_id=current_user.id,
            table_id=table.id,
            date=datetime.strptime(date_str, "%Y-%m-%d").date(),
            time=datetime.strptime(time_str, "%H:%M").time(),
            guest_count=int(guest_count),
            status='Confirmed'
        )

        table.is_available = False
        db.session.add(new_reservation)
        db.session.commit()

        # Optional: send notification if you still use it
        # send_notification(current_user.id, "Your reservation has been confirmed!")

        flash("Reservation created!", "success")
        return redirect(url_for('reservation.view_reservations'))

    except Exception as e:
        print(f"ERROR: {str(e)}")
        flash('Internal server error.', 'danger')
        return redirect(url_for('restaurant.list_restaurants_page'))



# ✅ 2. View All User Reservations (Page)
@reservation_bp.route('/reservations', methods=['GET'])
@login_required
def view_reservations():
    reservations = Reservation.query.filter_by(user_id=current_user.id).all()

    return render_template('reservations.html', reservations=reservations)


# ✅ 3. Modify Existing Reservation (Form POST)
@reservation_bp.route('/modify_reservation/<int:reservation_id>', methods=['POST'])
@login_required
def modify_reservation(reservation_id):
    reservation = Reservation.query.get(reservation_id)

    if not reservation:
        flash('Reservation not found.', 'danger')
        return redirect(url_for('reservation.view_reservations'))

    if reservation.user_id != current_user.id:
        flash('Unauthorized access.', 'danger')
        return redirect(url_for('reservation.view_reservations'))

    try:
        date_str = request.form.get('date')
        time_str = request.form.get('time')
        guest_count = request.form.get('guest_count')

        if not date_str or not time_str or not guest_count:
            flash('Missing fields.', 'danger')
            return redirect(url_for('reservation.view_reservations'))

        date = datetime.strptime(date_str, "%Y-%m-%d").date()
        time = datetime.strptime(time_str, "%H:%M").time()
        guest_count = int(guest_count)

        if guest_count <= 0:
            flash('Guest count must be greater than 0.', 'danger')
            return redirect(url_for('reservation.view_reservations'))

        reservation.date = date
        reservation.time = time
        reservation.guest_count = guest_count

        db.session.commit()
        send_notification(current_user.id, "Your reservation has been updated.")

        flash('Reservation updated successfully.', 'success')
        return redirect(url_for('reservation.view_reservations'))

    except Exception as e:
        print(f"ERROR: {str(e)}")
        flash('Internal server error.', 'danger')
        return redirect(url_for('reservation.view_reservations'))


# ✅ 4. Cancel Reservation (POST)
@reservation_bp.route('/cancel_reservation/<int:reservation_id>', methods=['POST'])
@login_required
def cancel_reservation(reservation_id):
    reservation = Reservation.query.get(reservation_id)

    if not reservation:
        flash('Reservation not found.', 'danger')
        return redirect(url_for('reservation.view_reservations'))

    if reservation.user_id != current_user.id:
        flash('Unauthorized access.', 'danger')
        return redirect(url_for('reservation.view_reservations'))

    try:
        reservation.status = 'Cancelled'

        # Mark table as available again
        table = reservation.table
        if table:
            table.is_available = True

        db.session.commit()
        send_notification(current_user.id, "Your reservation has been cancelled.")

        flash('Reservation cancelled successfully.', 'success')
        return redirect(url_for('reservation.view_reservations'))

    except Exception as e:
        print(f"ERROR: {str(e)}")
        flash('Internal server error.', 'danger')
        return redirect(url_for('reservation.view_reservations'))
