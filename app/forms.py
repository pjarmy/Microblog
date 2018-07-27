from flask_wtf import FlaskForm
from wtforms import StringField, BooleanField, PasswordField, SubmitField, ValidationError, TextAreaField, DateTimeField
from wtforms.validators import DataRequired, EqualTo, Email, Length
from app.models import User

class LoginForm(FlaskForm):
    openid = StringField('openid', validators=[DataRequired()])
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember_me = BooleanField('remember_me', default=False)
    submit = SubmitField('Sign in')


class RegistrationForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    password2 = PasswordField(
        'Repeat Password', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Register')

    def validate_username(self, username):
        user = User.query.filter_by(nickname=username.data).first()
        if user is not None:
            raise ValidationError('Please use a different username.')

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user is not None:
            raise ValidationError('Please use a different email address.')

class EditForm(FlaskForm):
    nickname = StringField('nickname', validators=[DataRequired()])
    about_me = TextAreaField('about_me', validators=[Length(min=0, max=140)])
    last_seen = DateTimeField('lase_seen')

    def __init__(self, original_nickname, *args, **kwargs):
        FlaskForm.__init__(self, *args, **kwargs)
        self.original_nickname = original_nickname

    def validate(self):
        if not Form.validate(self):
            return False
        if self.nickname.data == self.original_nickname:
            return True
        user = User.query.filter_by(nickname = self.nickname.data).first()
        if user != None:
            self.nickname.errors.append('This nickname is already in user. Please choose another one.')
            return False
        return True


class PassChangeForm(FlaskForm):
    oldpass = StringField('Old Password', validators=[DataRequired()])
    newpass = PasswordField('New Password', validators=[DataRequired()])
    newpass2 = PasswordField('Repeat Password', validators=[DataRequired(), EqualTo('newpass')])
    submit = SubmitField('Change')

class PostForm(FlaskForm):
    post = StringField('post', validators=[DataRequired()])
