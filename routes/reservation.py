# reservation.py

from flask import Blueprint, request, redirect, url_for, flash, jsonify, render_template
from flask_login import login_required, current_user
from models import db, Reservation, Table, Notification
from datetime import datetime, date, time
from flask_login import login_required
from datetime import datetime
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
        # 🔥 Parse date and time properly
        reservation_date = datetime.strptime(date_str, "%Y-%m-%d").date()
        reservation_time = datetime.strptime(time_str, "%H:%M").time()
        guest_count = int(guest_count)

        new_reservation = Reservation(
            user_id=current_user.id,
            table_id=table.id,
            restaurant_id=table.restaurant_id,
            date=reservation_date,
            time=reservation_time,
            guest_count=guest_count,
            status='Pending'
        )

        table.is_available = False
        db.session.add(new_reservation)
        db.session.commit()

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

@reservation_bp.route('/confirm_reservation/<int:reservation_id>', methods=['POST'])
@login_required
def confirm_reservation(reservation_id):
    reservation = Reservation.query.get_or_404(reservation_id)

    if current_user.role != "restaurant_manager":
        flash('Unauthorized access.', 'danger')
        return redirect(url_for('dashboard'))

    reservation.status = 'Awaiting Payment'
    reservation.table.is_available = False  # Optional: Keep table unavailable if confirmed

    db.session.commit()
    send_notification(reservation.user_id, "Your reservation has been accepted. Please pay 1 riyal within 5 minutes.")

    flash('Reservation accepted. Awaiting customer payment.', 'info')

    return redirect(url_for('dashboard'))


@reservation_bp.route('/reject_reservation/<int:reservation_id>', methods=['POST'])
@login_required
def reject_reservation(reservation_id):
    reservation = Reservation.query.get_or_404(reservation_id)

    if current_user.role != "restaurant_manager":
        flash('Unauthorized access.', 'danger')
        return redirect(url_for('manager.dashboard'))

    reservation.status = 'Cancelled'
    reservation.table.is_available = True  # Free the table
    db.session.commit()

    send_notification(reservation.user_id, "Your reservation has been rejected.")
    flash('Reservation rejected successfully.', 'success')
    return redirect(url_for('dashboard'))


@reservation_bp.route('/pay_reservation/<int:reservation_id>', methods=['POST'])
@login_required
def pay_reservation(reservation_id):
    reservation = Reservation.query.get_or_404(reservation_id)

    if reservation.user_id != current_user.id:
        flash('Unauthorized action.', 'danger')
        return redirect(url_for('reservation.view_reservations'))

    if reservation.status != 'Awaiting Payment':
        flash('Invalid payment attempt.', 'danger')
        return redirect(url_for('reservation.view_reservations'))

    try:
        # Simulate payment success
        reservation.status = 'Confirmed'
        db.session.commit()

        flash('Payment successful! Your reservation is now confirmed.', 'success')
        return redirect(url_for('reservation.view_reservations'))
    except Exception as e:
        print(f"ERROR: {str(e)}")
        flash('Payment failed. Try again.', 'danger')
        return redirect(url_for('reservation.view_reservations'))
