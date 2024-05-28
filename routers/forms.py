from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import InputRequired, Length, EqualTo, Regexp


class LoginForm(FlaskForm):
    username = StringField(validators=[InputRequired(), Length(max=16)])
    password = PasswordField(validators=[InputRequired(), Length(min=8)])
    submit = SubmitField('Log In')


class RegisterForm(FlaskForm):
    username = StringField(
        validators=[
            InputRequired(),
            Length(max=16, message="Please provide a valid name"),
            Regexp(
                regex=r"[A-Za-z0-9_.]*$",
                message="Usernames must have only letters, numbers, dots, or underscores",
            ),
        ]
    )
    password = PasswordField(
        validators=[
            InputRequired(),
            Length(min=8),
            Regexp(
                regex=r"^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[^\da-zA-Z]).{8,}$",
                message="Passwords must have at least 8 characters, one uppercase letter, one lowercase letter, one digit, and one special character",
            ),
        ]
    )
    confirm_password = PasswordField(
        validators=[
            InputRequired(),
            EqualTo("password", message="Passwords must match!"),
        ]
    )
    submit = SubmitField('Register')