from flask import blueprints

# __init__.py

# routes/__init__.py

def init_routes(app):
    from routes.auth import auth_bp
    from routes.restaurant import restaurant_bp
    from routes.reservation import reservation_bp
    from routes.waitlist import waitlist_bp
    from routes.notifications import notifications_bp
    from routes.review import review_bp

    # Register blueprints
    app.register_blueprint(review_bp)

    app.register_blueprint(auth_bp, url_prefix='/auth')
    app.register_blueprint(restaurant_bp)
    app.register_blueprint(reservation_bp)
    app.register_blueprint(waitlist_bp)
    app.register_blueprint(notifications_bp)
