from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_required, current_user
from models import db, Reservation, Table

reservation_bp = Blueprint('reservation', __name__)

# Reserve a table
@reservation_bp.route('/reserve/<int:table_id>', methods=['POST'])
@login_required
def reserve_table(table_id):
    table = Table.query.get(table_id)
    if not table or not table.is_available:
        flash("Table not available!", "danger")
        return redirect(url_for('restaurant.view_restaurants'))

    new_reservation = Reservation(user_id=current_user.id, table_id=table.id)
    table.is_available = False
    db.session.add(new_reservation)
    db.session.commit()

    flash("Table reserved successfully!", "success")
    return redirect(url_for('reservation.view_reservations'))

# View reservations
@reservation_bp.route('/reservations')
@login_required
def view_reservations():
    reservations = Reservation.query.filter_by(user_id=current_user.id).all()
    return render_template('reservations.html', reservations=reservations)
