from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField
from wtforms.validators import InputRequired, Email, Length, EqualTo


class LoginForm(FlaskForm):
    emailid = StringField('emailid', validators=[InputRequired(), Email(), Length(min=6, max=40)])
    pwd = PasswordField('pwd', validators=[InputRequired(), Length(min=6, max=25)])


class RegisterForm(FlaskForm):
    name = StringField('name',validators=[InputRequired()])
    emailid = StringField('emailid', validators=[InputRequired(), Email(), Length(min=6, max=40)])
    pwd = PasswordField('pwd', validators=[InputRequired(), Length(min=6, max=25)])
    cpwd = PasswordField('cpwd',validators=[InputRequired(),EqualTo('password', message='Passwords must match.')])

    def validate(self):
        """ initial_validation = super(RegisterForm, self).validate()
        if not initial_validation:
            return False """
        
        return True


class ChangePasswordForm(FlaskForm):
    password = PasswordField('pwd',validators=[InputRequired(), Length(min=6, max=25)])
    confirm = PasswordField('cpwd',validators=[InputRequired(),EqualTo('password', message='Passwords must match.')])