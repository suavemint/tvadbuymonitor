from app import db

ROLE_USER = 0
ROLE_ADMIN = 1

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), index=True, unique=True)
    email = db.Column(db.String(120), index=True, unique=True)
    role = db.Column(db.SmallInteger, default=ROLE_USER)
    watching = db.relationship('Watcher', backref='watched',lazy='dynamic')

    def __repr__(self):
        return '<User %r>' % self.name

# This db is the source file, from which users' queries will be polled at
# + set interval(s).

# Should probably work a selection for each user, by DMA of interest, for an update
# + check.

# We'll start with a single-market check.


# Add a Watcher item with the syntax: w = models.Watcher(market='Omaha', watched=u)
class Watcher(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    market = db.Column(db.String(40), unique=True)
    watch = db.Column(db.Integer, db.ForeignKey('user.id'))
    date_added = db.Column(db.Date)

    def __repr__(self):
        return '<Watcher %r by %r>' % (self.market, self.watch)


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

    def __repr__(self):
        return '<AdBuy: %s; %s; %s; %s; %s; %s; %s; %s; %s; %s; %s; %s; %s; %s; %s>' % \
        (self.id, self.station, self.file_upload_date, self.contract_start_date, self.contract_end_date,\
         self.tv_market, self.tv_market_id, self.ad_type, self.fcc_folder, self.fcc_file_name, self.is_invalid,\
         self.is_invoice, self.total_spent_raw, self.num_spots_raw, self.contract_number)

