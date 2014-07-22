from flask.ext.wtf import Form
from wtforms import TextField, BooleanField, StringField, SubmitField
from wtforms.validators import Required

# class LoginForm(Form):
#     openid = TextField('openid', validators=[Required()])
#     remember_me = BooleanField('remember_me', default=False)

class QueryForm(Form):
    name = StringField('Name', validators=[Required()])
    email = StringField('Email', validators=[Required()])
    markets = StringField('Markets', validators=[Required()])
    submit = SubmitField('Submit')