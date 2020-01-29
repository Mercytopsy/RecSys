from flask_wtf import FlaskForm
from wtforms import validators, StringField, PasswordField, ValidationError, FileField
from wtforms.fields.html5 import EmailField
from werkzeug.security import check_password_hash
from flask_wtf.file import FileAllowed
from author.models import Author

class RegisterForm(FlaskForm):
    email = EmailField('Email address', [validators.InputRequired(), validators.Email()])
    password = PasswordField('Password', [
            validators.InputRequired(),
            validators.Length(min=4, max=80)
        ])
    confirm = PasswordField('Re-type Password', [
            validators.EqualTo('password', message='Passwords must match'),
    ])


    def validate_email(self, email):
        author = Author.query.filter_by(email=email.data).first()
        if author is not None:
            raise ValidationError('Email already in use, please use a different one.')


class LoginForm(FlaskForm):
    email = EmailField('Email', [validators.InputRequired(), validators.Email()])
    password = PasswordField('Password', [
            validators.Required(),
            validators.Length(min=4, max=80)
        ])

    def validate(self):
        rv = FlaskForm.validate(self)
        if not rv:
            return False

        author = Author.query.filter_by(
            email=self.email.data,
            ).first()

        if author:
            if not check_password_hash(author.password, self.password.data):
                self.password.errors.append('Incorrect email or password')
                return False
            return True
        else:
            self.password.errors.append('Incorrect email or password')
            return False


class PostForm(FlaskForm):
    image = FileField('Image', validators=[
        FileAllowed(['jpg', 'png'], 'We only accept JPG or PNG images')
    ])  