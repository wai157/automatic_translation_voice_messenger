from flask import Blueprint, render_template
from flask_login import current_user, login_required

router = Blueprint('home', __name__, url_prefix='/')


@router.route("/health", methods=["GET"], strict_slashes=False)
def heathcheck():
    return {"status": "ok"}

@router.route("/", methods=["GET"], strict_slashes=False)
@login_required
def home():
    return render_template("home.html")