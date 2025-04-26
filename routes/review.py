from flask import Blueprint, request, redirect, url_for, flash
from flask_login import login_required, current_user
from models import db, Reservation, Review, Restaurant, Table
from datetime import datetime

review_bp = Blueprint('review', __name__, url_prefix='/review')

@review_bp.route('/submit/<int:reservation_id>', methods=['POST'])
@login_required
def submit(reservation_id):
    reservation = Reservation.query.get_or_404(reservation_id)

    # Check if the current user owns the reservation
    if reservation.user_id != current_user.id:
        flash("Unauthorized access.", "danger")
        return redirect(url_for('reservation.view_reservations'))

    # Check if already reviewed
    if reservation.review:
        flash("You already submitted a review.", "info")
        return redirect(url_for('reservation.view_reservations'))

    try:
        rating = int(request.form.get('rating'))

        # 💥 FIX: manually get restaurant_id through Table
        table = Table.query.get(reservation.table_id)
        if not table:
            flash("Table not found.", "danger")
            return redirect(url_for('reservation.view_reservations'))

        # Create the review
        review = Review(
            user_id=current_user.id,
            reservation_id=reservation.id,
            restaurant_id=table.restaurant_id,
            rating=rating,
            timestamp=datetime.utcnow()
        )

        db.session.add(review)
        db.session.commit()

        # Update restaurant average
        reviews = Review.query.filter_by(restaurant_id=table.restaurant_id).all()
        avg_rating = sum(r.rating for r in reviews) / len(reviews)

        restaurant = Restaurant.query.get(table.restaurant_id)
        db.session.commit()

        flash("Thanks for rating!", "success")
        return redirect(url_for('reservation.view_reservations'))

    except Exception as e:
        print("ERROR:", e)
        flash("Something went wrong.", "danger")
        return redirect(url_for('reservation.view_reservations'))
