from flask import Blueprint, render_template, redirect, flash, url_for, request
from flask_login import current_user, login_required
import requests

router = Blueprint('home', __name__, url_prefix='/')


@router.route("/", methods=["GET"], strict_slashes=False)
@login_required
def home():
    return render_template("home.html")


@router.route("/upload-audio", methods=["POST"], strict_slashes=False)
@login_required
def audio():
    test = request.files['audio']
    filename = "test.wav"
    test.save(filename)
    src_lang = "vi"
    print(test)
    url = "http://127.0.0.1:8080"
    response = requests.post(
        url,
        files={'file': open(filename, 'rb')},
        params={"lang": src_lang},
        timeout=15
    )
    # if os.path.exists(filename):
    # 	os.remove(filename)
    print(response.text)
    if response.status_code == 200:
        text = response.json()['text']
        print(text)
    return "Success", 200