from flask import blueprints

def init_routes(app):
    from routes.auth import auth_bp
    from routes.restaurant import restaurant_bp
    from routes.reservation import reservation_bp

    app.register_blueprint(auth_bp)
    app.register_blueprint(restaurant_bp)
    app.register_blueprint(reservation_bp)
