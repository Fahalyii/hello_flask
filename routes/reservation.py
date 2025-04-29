# reservation.py

from flask import Blueprint, request, redirect, url_for, flash, jsonify, render_template
from flask_login import login_required, current_user
from models import db, Reservation, Table, Notification, Restaurant
from datetime import datetime, date, time
from flask_login import login_required
from datetime import datetime
from models import Waitlist
from datetime import datetime, timedelta
from email_utils import send_email

reservation_bp = Blueprint('reservation', __name__)


from datetime import datetime, timedelta

def auto_cancel_expired_reservations(reservations):
    now = datetime.utcnow()
    for reservation in reservations:
        if reservation.status == 'Awaiting Payment' and reservation.payment_requested_at:
            if now - reservation.payment_requested_at > timedelta(minutes=5):
                reservation.status = 'Cancelled'
                if reservation.table:
                    reservation.table.is_available = True
    db.session.commit()


# Utility function: Send notification
def send_notification(user_id, message):
    notification = Notification(user_id=user_id, message=message)
    db.session.add(notification)
    db.session.commit()

# ✅ 1. Reserve a Table (Form POST)




@reservation_bp.route('/reserve/<int:restaurant_id>', methods=['POST'])
@login_required
def reserve_table(restaurant_id):
    from models import Reservation  # Just in case you didn't import it above

    date_str = request.form.get('date')
    time_str = request.form.get('time')
    guest_count = request.form.get('guest_count')

    if not date_str or not time_str or not guest_count:
        flash('Please fill in all fields: Date, Time, and Number of Guests.', 'danger')
        return redirect(request.referrer)

    try:
        reservation_date = datetime.strptime(date_str, "%Y-%m-%d").date()
        reservation_time = datetime.strptime(time_str, "%H:%M").time()
        guest_count = int(guest_count)

        # Step 1: Get total available seats for this restaurant
        restaurant = Restaurant.query.get(restaurant_id)
        total_seats = sum(table.capacity for table in restaurant.tables if table.is_available)

        # Step 2: Get all existing reservations for the same date
        existing_reservations = Reservation.query.filter_by(
            restaurant_id=restaurant_id,
            date=reservation_date
        ).filter(Reservation.status != 'Cancelled').all()

        # Step 3: Now calculate how many seats are already booked at the EXACT same time
        booked_seats = 0
        for res in existing_reservations:
            if res.time == reservation_time and res.status in ['Pending', 'Awaiting Payment', 'Confirmed']:
                booked_seats += res.guest_count

        available_seats = total_seats - booked_seats

        if available_seats >= guest_count:
            # Enough seats ➔ create normal reservation
            new_reservation = Reservation(
                user_id=current_user.id,
                restaurant_id=restaurant_id,
                date=reservation_date,
                time=reservation_time,
                guest_count=guest_count,
                status='Pending'
            )
            db.session.add(new_reservation)
            db.session.commit()

            flash("Reservation created successfully! Awaiting manager confirmation.", "success")
            return redirect(url_for('reservation.view_reservations'))
        else:
            # Not enough seats ➔ create reservation with "In the Waiting List" status
            waiting_reservation = Reservation(
                user_id=current_user.id,
                restaurant_id=restaurant_id,
                date=reservation_date,
                time=reservation_time,
                guest_count=guest_count,
                status='In the Waiting List'
            )
            db.session.add(waiting_reservation)
            db.session.commit()

            flash("No available seats at the selected time. You have been added to the waiting list.", "info")
            return redirect(url_for('reservation.view_reservations'))

    except Exception as e:
        print(f"ERROR in reserve_table: {str(e)}")
        flash('Internal server error. Please try again.', 'danger')
        return redirect(request.referrer)






# ✅ 2. View All User Reservations (Page)
# Main reservations page: only unfinished
@reservation_bp.route('/reservations', methods=['GET'])
@login_required
def view_reservations():
    reservations = Reservation.query.filter(
        Reservation.user_id == current_user.id,
        Reservation.status.in_(['Pending', 'Awaiting Payment', 'In the Waiting List'])
    ).all()
    return render_template('reservations.html', reservations=reservations)

# New history page: only finished
@reservation_bp.route('/reservation_history', methods=['GET'])
@login_required
def view_reservation_history():
    reservations = Reservation.query.filter(
        Reservation.user_id == current_user.id,
        Reservation.status.in_(['Confirmed', 'Cancelled'])
    ).all()
    return render_template('reservation_history.html', reservations=reservations)


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
    if reservation.table:
        reservation.table.is_available = False

    reservation.payment_requested_at = datetime.utcnow()

    db.session.commit()

    # 📨 Send notification in app
    send_notification(reservation.user_id, "Your reservation has been accepted. Please pay 1 riyal within 5 minutes.")

    # 📨 Send email notification
    user_email = reservation.user.email
    send_email(
        to=user_email,
        subject="Reservv - Payment Required for Your Reservation",
        body=f"""Hello {reservation.user.name},

Your reservation at {reservation.restaurant.name} has been accepted!

Please complete your payment within 5 minutes to confirm your reservation.

Thank you,
Reservv Team
"""
    )

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

    if reservation.table:
        reservation.table.is_available = True  # ✅ Check if a table exists before marking it available

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

@reservation_bp.route('/waitlist_dashboard')
@login_required
def view_waitlist():
    if current_user.role != "restaurant_manager":
        flash('Unauthorized access.', 'danger')
        return redirect(url_for('dashboard'))

    assigned_restaurant = Restaurant.query.filter_by(manager_id=current_user.id).first()
    waitlist_entries = Waitlist.query.filter_by(restaurant_id=assigned_restaurant.id, status='Waiting').all()

    return render_template('waitlist_dashboard.html', waitlist_entries=waitlist_entries)


@reservation_bp.route('/accept_waitlist_reservation/<int:reservation_id>', methods=['POST'])
@login_required
def accept_waitlist_reservation(reservation_id):
    reservation = Reservation.query.get_or_404(reservation_id)

    if current_user.role != "restaurant_manager":
        flash('Unauthorized access.', 'danger')
        return redirect(url_for('dashboard'))

    if reservation.status != 'In the Waiting List':
        flash('This reservation is not in the waiting list.', 'danger')
        return redirect(url_for('dashboard'))

    # 🚀 Find available table first
    available_tables = Table.query.filter_by(restaurant_id=reservation.restaurant_id, is_available=True).all()

    for table in available_tables:
        # Check if table is free at that date and time
        existing_reservation = Reservation.query.filter_by(
            table_id=table.id,
            date=reservation.date,
            time=reservation.time
        ).filter(Reservation.status != 'Cancelled').first()

        if not existing_reservation:
            # Assign this table
            reservation.table_id = table.id
            table.is_available = False  # Optional: if you want to lock table immediately
            break

    if not reservation.table_id:
        flash('No available tables at the selected time.', 'danger')
        return redirect(url_for('dashboard'))

    reservation.status = 'Awaiting Payment'
    reservation.payment_requested_at = datetime.utcnow()

    db.session.commit()

    flash('Reservation moved from waiting list. Awaiting customer payment.', 'success')
    return redirect(url_for('dashboard'))

