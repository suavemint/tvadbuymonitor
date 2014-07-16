from flask.ext.wtf import Form
from wtforms import TextField, BooleanField, StringField, SubmitField
from wtforms.validators import Required

# class LoginForm(Form):
#     openid = TextField('openid', validators=[Required()])
#     remember_me = BooleanField('remember_me', default=False)

class NameForm(Form):
    name = StringField('Name', validators=[Required()])
    email = StringField('Email', validators=[Required()])
    market = StringField('Market', validators=[Required()])
    submit = SubmitField('Submit')