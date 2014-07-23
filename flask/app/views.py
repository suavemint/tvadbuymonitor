from app import app, db
from flask import render_template, flash, redirect, session, url_for, request, g
# from flask.ext.login import login_user, logout_user, current_user, login_required
from forms import QueryForm
from models import Users, Queries, AdBuys
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

@app.route('/')
def index():
    from datetime import date, timedelta
    from sqlalchemy import and_, desc
    # from sqlalchemy.sql.expression import in_

    f = lambda x: date.strftime(x, '%Y-%m-%d')

    today = date.today()
    yesterday = today - timedelta(1)

    form = QueryForm()

    queries = Queries.query.all()

    user_id_j = Users.query.filter(Users.name=='james').first().id

    user_specific_callsigns = Queries.query.filter(Queries.user_id==user_id_j)\
                                     .first().query_text.split(',')
    # print user_specific_callsigns
    # print queries[0]
    users = Users.query.all()

    # j_callsigns = Queries.query.filter(Query.user_id == Users.query.filter()).filter()

    # j_id = Users.query.filter(Users.name=='james')[0].id
    # print 15*'='
    # # print j_id
    # for x in j_id:
    #     print x.id
    # print 15*'='

    # print Queries.query.filter(Queries.user_id = Users.name==)

    test_dict = {}

    for user in users:
        user_name = user.name
        user_id = user.id
        user_specific_queries = Queries.query.filter(Queries.user_id==user_id)
        for q in user_specific_queries:
            # test_dict[user_name] =
            pass

    # adbuys = AdBuys.query.all()
    # adbuys = AdBuys.query.filter(AdBuys.upload_time > f(yesterday))
    adbuys = AdBuys.query.filter(and_(AdBuys.upload_time > f(yesterday),\
                                      AdBuys.broadcasters.in_(user_specific_callsigns)))
    # adbuys = AdBuys.query.filter(AdBuys.broadcasters in user_specific_callsigns)

    # adbuys = AdBuys.query.filter(AdBuys.broadcasters.in_(['WKOW','non'])).order_by(desc(AdBuys.updated_at))

    # print 15*'='
    # print adbuys.first()
    # print 15*'='
    test_dict = {u.name:q.query_text.split(',') for u in users for q in Queries.query.filter()}

    return render_template('index.html',
                            title = 'Home',
                            users = users,
                            queries =  queries,
                            adbuys = adbuys,
                            form = form)


