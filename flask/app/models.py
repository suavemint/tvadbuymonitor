from app import db

ROLE_USER = 0
ROLE_ADMIN = 1

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), index=True, unique=True)
    email = db.Column(db.String(120), index=True, unique=True)
    role = db.Column(db.SmallInteger, default=ROLE_USER)
    watching = db.relationship('Watcher', backref='',lazy='dynamic')

    def __repr__(self):
        return '<User %r>' % self.name

# This db is the source file, from which users' queries will be polled at
# + set interval(s).
class Watcher(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    number = db.Column(db.SmallInteger, unique=True)


class AdBuys(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    station = db.Column(db.String(7))
    file_upload_date = db.Column(db.Date)
    contract_start_date = db.Column(db.Date)
    contract_end_date = db.Column(db.Date)
    tv_market = db.Column(db.String(30))
    tv_market_id = db.Column(db.Integer)
    ad_type = db.Column(db.String(24))
    fcc_folder = db.Column(db.String(70))
    fcc_file_name = db.Column(db.String(120))
    is_invalid = db.Column(db.String(1))
    is_invoice = db.Column(db.String(1))
    total_spent_raw = db.Column(db.Integer)
    num_spots_raw = db.Column(db.Integer)
    contract_number = db.Column(db.Integer)

