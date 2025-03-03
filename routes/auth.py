from flask import Blueprint, render_template, request, redirect, url_for, flash
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import login_user, logout_user, login_required
from models import db, User

auth_bp = Blueprint('auth', __name__)

# User Registration
@auth_bp.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        try:
            name = request.form.get('name')
            email = request.form.get('email')
            password = request.form.get('password')
            role = request.form.get('role')

            print(f"DEBUG: Name={name}, Email={email}, Password={password}, Role={role}")  # Debugging

            if not name or not email or not password or not role:
                flash("All fields are required!", "danger")
                return redirect(url_for('auth.register'))

            hashed_password = generate_password_hash(password, method='sha256')
            new_user = User(name=name, email=email, password=hashed_password, role=role)
            db.session.add(new_user)
            db.session.commit()

            flash("Registration successful, please login", "success")
            return redirect(url_for('auth.login'))

        except Exception as e:
            print(f"ERROR: {str(e)}")  # Debugging error
            flash("An error occurred. Please try again.", "danger")
            return redirect(url_for('auth.register'))

    return render_template('register.html')

# User Login
@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        user = User.query.filter_by(email=email).first()

        if user and check_password_hash(user.password, password):
            login_user(user)
            return redirect(url_for('home'))

        flash("Invalid credentials", "danger")

    return render_template('login.html')

# User Logout
@auth_bp.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('auth.login'))


