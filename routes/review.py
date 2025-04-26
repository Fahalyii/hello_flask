from flask import Blueprint, request, redirect, url_for, flash
from flask_login import login_required, current_user
from models import db, Review, Reservation
from datetime import datetime

review_bp = Blueprint('review', __name__, url_prefix='/review')

@review_bp.route('/submit/<int:reservation_id>', methods=['POST'])
@login_required
def submit(reservation_id):
    reservation = Reservation.query.get_or_404(reservation_id)

    if reservation.user_id != current_user.id:
        flash("Unauthorized access.", "danger")
        return redirect(url_for('reservation.view_reservations'))

    if reservation.status != 'Confirmed':
        flash("You can only review confirmed reservations.", "danger")
        return redirect(url_for('reservation.view_reservations'))

    rating = int(request.form.get('rating'))
    comment = request.form.get('comment', '')

    new_review = Review(
        user_id=current_user.id,
        reservation_id=reservation.id,
        restaurant_id=reservation.restaurant_id,  # ✅ Corrected here
        rating=rating,
        comment=comment,
        timestamp=datetime.utcnow()
    )

    db.session.add(new_review)
    db.session.commit()

    flash("Thank you for your feedback!", "success")
    return redirect(url_for('reservation.view_reservations'))
