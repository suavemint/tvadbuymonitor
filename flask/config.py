import os

CSRF_ENABLED = True
SECRET_KEY = 'this-is-a-secret'

# OPENID_PROVIDERS = [
    # {'name': 'Google', 'url':'https://www.google.com/accounts/o8/id'}]

psql_loc =  'postgresql://postgres:password@localhost:5432/testdb'
basedir = os.path.abspath(os.path.dirname(__file__))

# SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir, 'app.db')
SQLALCHEMY_DATABASE_URI = psql_loc
# SQLALCHEMY_MIGRATE_REPO = os.path.join(basedir, 'db_repository')