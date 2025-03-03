from flask import Flask, render_template
from flask_login import LoginManager
from database import db, app
from routes import init_routes
from models import User

# Initialize Flask-Login
login_manager = LoginManager()
login_manager.init_app(app)
init_routes(app)

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

@app.route("/")
def home():
    return render_template("index.html")

if __name__ == "__main__":
    app.run(debug=True)
