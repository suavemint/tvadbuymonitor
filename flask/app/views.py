from app import app, db
from flask import render_template, flash, redirect, session, url_for, request, g
# from flask.ext.login import login_user, logout_user, current_user, login_required
from forms import NameForm
from models import Users, Queries, AdBuys, ROLE_USER, ROLE_ADMIN
from wtforms import Form, TextField, validators

## Notes to self:
## 1. The app.config dict is a general-purpose place to store configuration variables used by the framework,
## + the extensions, or the application itself.

def send_email(in_query, target):
    import smtplib, date, datetime
    from email.MIMEMultipart import MIMEMultipart
    from email.MIMEText import MIMEText

    src = 'tvadbuymonitor@gmail.com'
    pw = 'B30ptimus!'

    msg = MIMEMultipart()
    msg['From'] = src
    msg['To'] = target
    msg['Subject'] = 'TV Ad Buy Summary for {}'.format(date.today().strftime('%m-%d-%Y'))
    message = 'Currently placeholder text; put the query results (new inserts) here.'
    msg.attach(MIMEText(message))

    server = smtplib.SMTP('smtp.gmail.com',587)
    server.ehlo()
    server.starttls()
    server.ehlo()
    server.login(src, pw)

    server.sendmail(src, target, msg.as_string())
    server.quit()


class MonitorRequestForm(Form):
    username = TextField('Name', [validators.Length(min=1, max=50)])
    email = TextField('Email', [validators.Length(min=11, max=20)])  # FIXME ??
    callsigns = TextField('Callsigns')

# ^^ May be obviated by NameForm() below... we'll see.

@app.route('/')
def index():
    form = NameForm()
    if form.validate_on_submit():
        user = Users.query.filter_by(name=form.name.data).first()
        if user is None:
            user = 'FIXME'
            # user = User(name = form.name.data, email=form.email.data, market)
            # db.session.add(user)
    # user = g.user  # Added user to the g object in before_request func. (far below)

    # Mock markets data; these will be used as a starting point
    # + for each users' comparisons for new ad data and alerts
    # + (i.e., I don't necessarily want all of Scott's alerts and v.v.).


    # What we want is a list of users and their subscriptions (so, two text fields,
    # + one for user name and one for markets followed), with a blank one for new
    # + email addresses and/or subscriptions. This blank one will allow for creation.

    # users = [{'name':'James', 'email':'james@0ptimus.com'},
             # {'name':'Scott', 'email':'scott@0ptimus.com'}]

    ## Super testing of user-db storage -- FIXME
    # james = User(name='James', email='james@0ptimus.com', role=ROLE_USER)
    # scott = models.User(name='Scott', email='scott@0ptimus.com', role=modles.ROLE_USER)

    ## Add me to db.session, for committing (adding a new row).
    ## NB: To add more than one row at once, use db.session.add_all([list of objects]).
    if 'james' not in Users.query().all():
        db.session.add(james)
        db.session.commit()


    return render_template('index.html',
                            title = 'Home',
                            user =  james,  ### FIXME
                            dmas = dmas)

