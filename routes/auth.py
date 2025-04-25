from flask import Blueprint, render_template, request, redirect, url_for, flash
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import login_user, logout_user, login_required
from models import db, User

auth_bp = Blueprint('auth', __name__)



@auth_bp.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        # Get form data
        username = request.form.get('username')
        email = request.form.get('email')
        password = request.form.get('password')
        role = request.form.get('role')

        # Debug output
        print("Form Data:")
        print(f"Username: {username}")
        print(f"Email: {email}")
        print(f"Password: {password}")
        print(f"Role: {role}")

        # Validate fields
        if not username or not email or not password or not role:
            flash("All fields are required!", "danger")
            return redirect(url_for('auth.register'))

        # Check if email already exists
        if User.query.filter_by(email=email).first():
            flash("Email already registered. Please log in.", "warning")
            return redirect(url_for('auth.login'))

        # Hash password and create user
        hashed_password = generate_password_hash(password, method='pbkdf2:sha256', salt_length=16)
        new_user = User(name=username, email=email, password=hashed_password, role=role)

        # Save to DB
        db.session.add(new_user)
        db.session.commit()

        flash("Registration successful! Please login.", "success")
        return redirect(url_for('auth.login'))

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


