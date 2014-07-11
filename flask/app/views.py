from app import app
from flask import render_template, flash, redirect
from forms import LoginForm

@app.route('/')
@app.route('/index')
def index():
    user = {'name':'James'}  # Mock user

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

    return render_template('index.html',
                            title = 'Index',
                            user =  user,
                            dmas = dmas)
    # return '''
    # <html><head><title>Test page</title></head>
    # <body>
    #     <h1> Hello, ''' + user['name'] + ''' </h1>
    # </body>
    # </html>
    # '''

@app.route('/login', methods=['GET','POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        flash('DEBUGGING OUTPUT: Login requested for OpenID="' + form.openid.data + '", remember_me=' + str(form.remember_me.data))
        return redirect('/index')
    return render_template('login.html',
                            title = 'Sign In',
                            form = form,
                            providers = app.config['OPENID_PROVIDERS'])