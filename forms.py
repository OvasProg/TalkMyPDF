from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import ValidationError, DataRequired, Email
import re

# Custom validator to reject non-Latin characters in email
def valid_email(form, field):
    email = field.data

    if re.search(r"[^\x00-\x7F]", email):
        raise ValidationError("Email must contain only Latin letters and symbols.")

# Custom validator for password strength and allowed characters
def strong_password(form, field):
    password = field.data

    if re.search(r"[^\x00-\x7F]", password):
        raise ValidationError("Password must contain only Latin letters and symbols.")
    if len(password) < 8:
        raise ValidationError("Password must be at least 8 characters long.")
    if (((not re.search(r"[a-z]", password) or
            not re.search(r"[A-Z]", password)) or
            not re.search(r"[0-9]", password)) or
            not re.search(r"[!@#$%^&*(),.?\":{}|<>]", password)):
        raise ValidationError("Password must include at least one lowercase letter, "
                              "one uppercase letter, one digit, and one special character.")

class LoginForm(FlaskForm):
    email = StringField(label='Email', validators=[DataRequired(), Email(), valid_email])
    password = PasswordField(label='Password', validators=[DataRequired(), strong_password])
    submit = SubmitField('Login')

class SignUpForm(FlaskForm):
    email = StringField(label='Email', validators=[DataRequired(), Email(), valid_email])
    password = PasswordField(label='Password', validators=[DataRequired(), strong_password])
    submit = SubmitField('Sign Up')