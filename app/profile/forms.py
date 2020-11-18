from flask_wtf import Form
from wtforms import TextField, SubmitField, StringField, IntegerField, RadioField
from wtforms.validators import Required
from flask_wtf import FlaskForm

class LoginForm(FlaskForm):
    username = TextField('login', validators = [Required()])
    password = StringField('pass', validators = [Required()])
    years = IntegerField('years')
    submit = SubmitField('Sign In')

class RegisterForm(FlaskForm):
    username = TextField('login', validators = [Required()])
    full_name = StringField('full_name')
    password = StringField('pass', validators = [Required()])
    city = StringField('city')
    avatar = StringField('avatar')
    phone = StringField('phone')
    risk_level = RadioField('risk level', choices=[(1, '1'), (2, '2'), (3, '3'), ])
    about = StringField('about')
    years = IntegerField('year')
    submit = SubmitField('Sign In')

class AddPost(FlaskForm):
    posttext = TextField('text')
    posthead = TextField('Head')
   
    submit = SubmitField('send')