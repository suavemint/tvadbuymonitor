from app import app, db
from flask import render_template, flash, redirect, session, url_for, request, g
# from flask.ext.login import login_user, logout_user, current_user, login_required
from forms import NameForm
from models import User, ROLE_USER, ROLE_ADMIN

## Notes to self:
## 1. The app.config dict is a general-purpose place to store configuration variables used by the framework,
## + the extensions, or the application itself.

@app.route('/')
# @app.route('/index')
# @login_required
def index():
    form = NameForm()
    if form.validate_on_submit():
        user = User.query.filter_by(name=form.name.data).first()
        if user is None:
            user = User(name = form.name.data, email=form.email.data, market)
            db.session.add(user)
    # user = g.user  # Added user to the g object in before_request func. (far below)

    # Mock markets data; these will be used as a starting point
    # + for each users' comparisons for new ad data and alerts
    # + (i.e., I don't necessarily want all of Scott's alerts and v.v.).
    dmas = [{
                'number':362,
                'name': 'Omaha',
                'markets': {'stations':['KETV', 'KMT', 'WOWT', 'CW', 'KPTM']},
                'body':'Omaha data'
                },
            {
                'number':400,
                'name': 'Lincoln',
                'markets': {'stations':['KHGI','KLKN','KOLN', 'KHAS', 'KNOP', 'KFXL']},
                'body':'Lincoln data'
            }]  # Fake array of DMAs / markets

    # What we want is a list of users and their subscriptions (so, two text fields,
    # + one for user name and one for markets followed), with a blank one for new
    # + email addresses and/or subscriptions. This blank one will allow for creation.

    # users = [{'name':'James', 'email':'james@0ptimus.com'},
             # {'name':'Scott', 'email':'scott@0ptimus.com'}]

    ## Super testing of user-db storage -- FIXME
    james = User(name='James', email='james@0ptimus.com', role=ROLE_USER)
    # scott = models.User(name='Scott', email='scott@0ptimus.com', role=modles.ROLE_USER)

    ## Add me to db.session, for committing (adding a new row).
    ## NB: To add more than one row at once, use db.session.add_all([list of objects]).
    if james not in User.query().all():
        db.session.add(james)
        db.session.commit()


    return render_template('index.html',
                            title = 'Home',
                            user =  james,  ### FIXME
                            dmas = dmas)

