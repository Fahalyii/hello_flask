# notifications.py

from flask import Blueprint, render_template
from flask_login import login_required, current_user
from models import Notification

notifications_bp = Blueprint('notifications', __name__)

# ✅ 1. View User Notifications
@notifications_bp.route('/notifications', methods=['GET'])
@login_required
def get_user_notifications():
    notifications = Notification.query.filter_by(user_id=current_user.id).order_by(Notification.created_at.desc()).all()

    return render_template('notifications.html', notifications=notifications)
