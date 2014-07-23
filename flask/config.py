import os

# The next two lines are for the Flask-WTF extension.
CSRF_ENABLED = True
SECRET_KEY = 'this-is-a-secret'

# OPENID_PROVIDERS = [
    # {'name': 'Google', 'url':'https://www.google.com/accounts/o8/id'}]
basedir = os.path.abspath(os.path.dirname(__file__))

# SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir, 'app.db')
SQLALCHEMY_DATABASE_URI = 'postgresql://postgres:password@localhost:5432/testdb'
# SQLALCHEMY_MIGRATE_REPO = os.path.join(basedir, 'db_repository')