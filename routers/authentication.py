from flask import Blueprint, render_template, redirect, flash, url_for
from flask_bcrypt import Bcrypt
from flask_login import login_user, LoginManager, logout_user, login_required
from routers.forms import LoginForm, RegisterForm
from sqlalchemy.exc import IntegrityError
from models import db, User, Room
from datetime import datetime

router = Blueprint('authentication', __name__, url_prefix='/auth')

bcrypt = Bcrypt()
login_manager = LoginManager()
login_manager.session_protection = "strong"
login_manager.login_view = "authentication.login"
login_manager.login_message_category = "info"

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


@router.route("/login", methods=("GET", "POST"), strict_slashes=False)
def login():
    form: LoginForm = LoginForm()
    if form.validate_on_submit():
        try:
            user = User.query.filter_by(username=form.username.data).first()
            if user is None:
                flash("Invalid Username or password!", "error")
                return redirect(url_for('authentication.login'))
            if bcrypt.check_password_hash(user.password, form.password.data):
                login_user(user)
                return redirect(url_for('home.home'))
            else:
                flash("Invalid Username or password!", "error")
        except Exception as e:
            print(e)
            flash(e, "error")

    return render_template("auth.html", form=form,)


@router.route("/register", methods=("GET", "POST"), strict_slashes=False)
def register():
    form: RegisterForm = RegisterForm()
    if form.validate_on_submit():
        try:
            password = form.password.data
            username = form.username.data
            new_user = User(
                username=username,
                password=bcrypt.generate_password_hash(password),
            )
            db.session.add(new_user)
            new_room = Room(
                id = f"{username}-{username}",
            )
            new_room.users.append(new_user)
            db.session.add(new_room)
            db.session.commit()
            flash(f"Account Succesfully created", "success")
            return redirect(url_for("authentication.login"))
        except IntegrityError:
            db.session.rollback()
            flash(f"User already exists!", "warning")
        except Exception as e:
            print(e)
            db.session.rollback()
            flash(f"An error occured!", "error")
        
    return render_template("auth.html", form=form)

@router.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for('authentication.login'))
