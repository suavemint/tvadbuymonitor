import requests, json, unittest, os, csv
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, String, Integer
from sqlalchemy.sql.functions import current_timestamp
from datetime import date

psql_loc =  'postgresql://postgres:password@localhost:5432/testdb'

Base = declarative_base()

class Users(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True)
    name = Column(String)
    email = Column(String)

    def __repr__(self):
        return '<User: id = {0}, name = {1}, email = {2}>'.format(self.id, self.name, self.email)

    def __init__(self, name, email):
        self.name = name
        self.email = email

class Queries(Base):
    from sqlalchemy import ForeignKey
    from sqlalchemy.orm import sessionmaker, relationship, backref

    __tablename__ = 'queries'

    id = Column(Integer, primary_key=True)
    query_text = Column(String, unique=True)
    # user_id = relationship(Users, backref=backref('query', order_by=id))
    user_id = Column(Integer, ForeignKey('users.id'))

    def __repr__(self):
        return '<Query: id = {0}, text = {1}, user_id = {2}>'.format(self.id, self.query_text, self.user_id)

    def __init__(self, query_text, user_id):
        self.query_text = query_text
        self.user_id = user_id

class AdBuys(Base):
    from sqlalchemy import Column, Integer, String, Date, DateTime, SmallInteger
    from sqlalchemy.orm import sessionmaker, relationship, backref

    __tablename__ = 'adbuys'

    id = Column(Integer, primary_key=True)
    #adbuy_id = Column('adbuy_id', Integer, primary_key=True)
    advertiser = Column('advertiser', String)
    broadcasters = Column('broadcasters', String(50))  # Will need to extract 'broadcasters' key by '','.join(broadcasters)' for broadcasters = resp['objects']['broadcasters']
    candidate_type = Column('candidate_type', String(50))
    community_state = Column('community_state', String(2))
    contract_end_date = Column('contract_end_date', Date)
    contract_number = Column('contract_number', String, default=0)
    # Column('contract_start_date', String),
    contract_start_date = Column('contract_start_date', Date)
    description = Column('description', String(200))
    doc_source = Column('doc_source', String(20))
    doc_status = Column('doc_status', String(20))
    nielsen_dma = Column('nielsen_dma', String(50))
    nielsen_dma_id = Column('nielsen_dma_id', Integer)
    num_spots = Column('num_spots', SmallInteger, default=0)
    resource_uri = Column('resource_uri', String(200))
    source_file_uri = Column('source_file_uri', String(400))
    total_spent = Column('total_spent', Integer, default=0)
    updated_at = Column('updated_at', DateTime)
    upload_time = Column('upload_time', String)
    uuid_key = Column('uuid_key', String(40))
    last_refreshed_datetime = Column('last_refreshed_datetime', DateTime, default=current_timestamp(),
                                                                          onupdate=current_timestamp())  # FIXME: add this to be refreshed every time the row is accessed
                                                                                       # + see http://waynesimmerson.ca/Article/learn-test-driven-development-flask-part-2
                                                                                       # + for detail on how to set this up in SQLA.
    has_user_been_alerted = Column('has_user_been_alerted', SmallInteger, default=0)

    def __repr__(self):
        print '<AdBuy: id={0}, community_state={1}, nielsen_dma_id={2}, num_spots={3}, total_spent={4}>'.format(\
            self.id, self.community_state, self.nielsen_dma_id, self.num_spots, self.total_spent)

    def __init__(self, advertiser, broadcasters, candidate_type, community_state, contract_end_date,\
                 contract_number, contract_start_date, description, doc_source, doc_status, nielsen_dma, nielsen_dma_id, \
                 num_spots, resource_uri, source_file_uri, total_spent, updated_at, upload_time, uuid_key):
        # self.id = id
        # self.adbuy_id = adbuy_id
        self.advertiser = advertiser
        self.broadcasters = broadcasters
        self.candidate_type = candidate_type
        self.community_state = community_state
        self.contract_end_date = contract_end_date
        self.contract_number = contract_number
        self.contract_start_date = contract_start_date
        self.description = description
        self.doc_source = doc_source
        self.doc_status = doc_status
        self.nielsen_dma = nielsen_dma
        self.nielsen_dma_id = nielsen_dma_id
        self.num_spots = num_spots
        self.resource_uri = resource_uri
        self.source_file_uri = source_file_uri
        self.total_spent = total_spent
        self.updated_at = updated_at
        self.upload_time = upload_time
        self.uuid_key = uuid_key
        # Two default-valued params:
        self.last_refreshed_datetime = date.today()
        self.has_user_been_alerted = 0

####
# End table classes
####

def create_session_and_bind_engine(psql_loc=psql_loc,echo=False):
    from sqlalchemy import create_engine
    from sqlalchemy.orm import sessionmaker

    Session = sessionmaker()
    db = create_engine(psql_loc, echo=echo)
    Session.configure(bind=db)
    session = Session()
    # session = Session.configure(bind=db)
    Base.metadata.create_all(db)

    return session

def return_zero_or_int(x):
    '''
    x: Int, Float, None -> Int
    '''

    if x is None:
        return 0
    return int(float(x))

def create_users_table():
    # import sqlalchemy as sql
    from datetime import datetime
    from sqlalchemy import create_engine
    from sqlalchemy.orm import sessionmaker

    # s = create_session_and_bind_engine()

    if False:
        Session = sessionmaker()
        db = create_engine(psql_loc)
        Session.configure(bind=db)
        session = Session()

    # Set up engine and metadata:
    session = create_session_and_bind_engine()

    # metadata = MetaData(db)
    # Base.metadata.create_all(db)

    # # Create users table:
    # users = Table('users', metadata,
    #             Column('id', Integer, primary_key=True),
    #             Column('email', String(100)))

    # users.create(checkfirst=True)
    # j = users.insert()
    # j.execute({'email':'james@0ptimus.com'})
    james = Users(name='james', email='james@0ptimus.com')
    scott = Users(name='scott', email='scott@0ptimus.com')
    session.add_all([james,scott])
    # session.add(scott)
    session.commit()

def create_queries_table():
    from sqlalchemy import create_engine
    from sqlalchemy.orm import sessionmaker
    # from datetime import datetime

    # Create Session, bind engine, and make new Session object()
    # TODO: This is likely abstractable to just one Session, to reduce
    # + code repetition and binding times.

    if False:
        Session = sessionmaker()
        db = create_engine(psql_loc)
        Session.configure(bind=db)
        session = Session()

    session = create_session_and_bind_engine()
    # print(session)

    # Before we completely abstract away the query strings and users and such, let's try to make
    # + a sample query, replete with FK to james.id:
    test_james = session.query(Users).filter(Users.name == 'james').first()
    # test_james = session.query(Users).filter_by(Users.name='james').first()
    # test_james = Users.query.filter_by(name='james').first()
    # print(15*'=')
    # print(test_james)
    # print(15*'=')
    # test_james = Users.query.with_entities(Users.id)
    # test_query = Queries(query_text='from adbuys select * where broadcasters like "KETV%"', user_id=test_james.id)
    test_query = Queries(query_text='KETV,KMT,WOWT,CW,KPTM,KHGI,KLKN,KOLN,KHAS,KNOP,KFXL', user_id=test_james.id)

    # And save our test query to the queries table.
    session.add(test_query)
    session.commit()

    # And now, test that the query string is both extant and retrievable:
    check_exists = session.query(Queries).all()
    print('Seeing if the Queries table was written to: {}'.format(check_exists))

def create_adbuys_table():
    # import sqlalchemy as sql
    from datetime import datetime
    from sqlalchemy.orm import sessionmaker
    from sqlalchemy import create_engine

    # db = create_engine(psql_loc)

    db = create_engine(psql_loc)
    Session = sessionmaker(bind=db)
    session = Session()

    Base.metadata.create_all(db)
    # adbuys.create(checkfirst=True)
    d = {}

    # The below is the current, correct way to retrieve the PAS data:
    # i = adbuys.insert()  # <- comment out to save on time, if already existing.
    data = get_adbuys_by_city()

    # Column('user_id'), Integer, )
    # print data


    # if data is None:
    #     print 'No data to insert.'
    #   # import sys;sys.exit(1)
    #     continue
    pas_data_to_insert = [x for x in data if x != None if data != None]  # FIXME: These two lines are logically redundant...

    # if pas_data_to_insert is not None:

    # print pas_data_to_insert[1]; import sys; sys.exit(1)

    for a in pas_data_to_insert:
      # print a
      if a is not None:
          for l in a:
            # print 'TESTING'; print 50*'='
            d = AdBuys(advertiser= l['advertiser'],
                 broadcasters= ','.join(l['broadcasters']),
                 candidate_type= l['candidate_type'],
                 community_state= l['community_state'],
                 # contract_end_date= datetime.strptime(l['contract_end_date'], '%Y-%m-%d'),
                 contract_end_date= l['contract_end_date'],
                 contract_number= l['contract_number'],
                 # contract_start_date= datetime.strptime(l['contract_start_date'], '%Y-%m-%d'),
                 contract_start_date= l['contract_start_date'],
                 description= l['description'],
                 doc_source= l['doc_source'],
                 doc_status= l['doc_status'],
                 nielsen_dma= l['nielsen_dma'],
                 nielsen_dma_id= l['nielsen_dma_id'],
                 num_spots= l['num_spots'],
                 resource_uri= l['resource_uri'],
                 source_file_uri= l['source_file_uri'],
                 total_spent = return_zero_or_int( l['total_spent'] ),
                 # t = l['total_spent']
                 # if t not None:
                    # total_spent = int(t)
                 # updated_at= datetime.strptime(l['updated_at'].split('.')[0], '%Y-%m-%dT%H:%M:%S'),
                 updated_at = l['updated_at'],
                 # upload_time= datetime.strptime(l['upload_time'], '%Y-%m-%d'),
                 upload_time= l['upload_time'],
                 uuid_key= l['uuid_key']
                 )

            # i.execute(d)
            session.add(d)
    session.commit()

def delete_all_tables():
    # TODO: Add in functionality to find all tables related to a Session (or session), and DROP them.
    pass

def query_database():
    '''
    Some queries that work (assuming date-type columns for timestamps):

    1.
    For the total spend on ad buys since the (contracts that start at) start of 2014 in FL:
    select sum(total_spent) from adbuys where community_state = 'FL' and 'contract_start_date' > '2014-01-01';

    2.
    For the total number of ad spots purchased (so counting rows returned) from KMTV after 2014:
    select count(*) from adbuys where broadcasters like 'KMTV' and 'contract_start_date' > '2012-01-01';

    '''
    # import sqlalchemy as sql
    from sqlalchemy import create_engine, Table, MetaData
    from sqlalchemy.orm import sessionmaker, relationship, backref
    # Now, let's test the recovery of the data; let's find if there are any ads in the stations of interest:
    # a_stations = ['KETV','KMT','WOWT','CW','KPTM']# in Omaha:

    db = create_engine(psql_loc)
    # db.echo = 'debug'
    metadata = MetaData(db)

    # Set up Session factory instance, and make instance for this db (buys.db)
    Session = sessionmaker(bind=db)
    session = Session()

    adbuys = Table('adbuys', metadata, autoload=True)

    # query_nonzero_buy = lambda x: x['total_spent']

    ## Per user, create a list of broadcasters' callsigns:
    broadcaster_list = ['KETV','KMT','WOWT','CW','KPTM','KHGI','KLKN','KOLN','KHAS','KNOP','KFXL']
    queries_list = []



    for b in broadcaster_list:
        queries_list.append(session.query(adbuys).filter(adbuys.c.broadcasters.contains(b)).all())
    # queries_list = [i for i in session.query(adbuys).filter(adbuys.c.broadcasters.contains(j)).order_by(adbuys.c.broadcasters) for j in broadcaster_list]

    # a = session.query(adbuys).filter(adbuys.c.broadcasters.contains('KLKN')).all()
    # print(a)
    for x in queries_list:
        print(x)
    # aa = a.all()


    # for x in session.query('select * from adbuys where broadcasters = "KLKN"'):
    #   print x


    # print type(aa)

    # a = adbuys.select((adbuys.c.broadcasters.contains('KETV')) | \
    #                   (adbuys.c.broadcasters.contains('KMT')) | \
    #                   (adbuys.c.broadcasters.contains('WOWT')) | \
    #                   (adbuys.c.broadcasters.contains('CW')) | \
    #                   (adbuys.c.broadcasters.contains('KPTM')))

    # print(a)

    # b = adbuys.select((adbuys.c.broadcasters.contains('KHGI')) | \
    #                   (adbuys.c.broadcasters.contains('KLKN')) | \
    #                   (adbuys.c.broadcasters.contains('KOLN')) | \
    #                   (adbuys.c.broadcasters.contains('KHAS')) | \
    #                   (adbuys.c.broadcasters.contains('KNOP')) | \
    #                   (adbuys.c.broadcasters.contains('KFXL')))
    # run(a)
    # run(b)

def generate_query_from_string(db, in_string):
    query_root = 'select * from {0} where '.format(db)
    query_string_of_only_ors = ''
    for s in in_string.split(','):
        query_string_of_only_ors += "broadcasters like '{}%' or".format(s)
    return query_string_of_only_ors[:-3]


def add_buys_to_db_testing(a):
    pass


def convert_cities_to_dmas(args):
    import csv
    # print('convert_cities_to_dmas received arguments {}'.format(args))
    in_f = csv.reader(open('dma_codes.csv'), dialect='excel')
    out_list = []
    in_f.next()
    for l in in_f:
    # print l
        for a in args:
          if isinstance(a, str):
          # print a
            if a.lower() in l[1].lower():
              out_list.append(l[0])

    # in_f.close()

    # If just a one-element list (empty or otherwise), just return string.
    if len(out_list) < 2:
        return str(out_list)
    return out_list



    # def get_adbuys_by_city(*args):
def get_adbuys_by_city(args=''):
    from csv import reader

    FCC_URL = 'http://data.fcc.gov/mediabureau/v01/tv/facility/search/'
    PAS_URL = 'http://politicaladsleuth.com/api/v1/politicalfile/?apikey=5f05db9ef8cb4ac1bd4b766c4f29ff64'

    PAS_KEY = '5f05db9ef8cb4ac1bd4b766c4f29ff64'
    # pas_order_by = '&order_by=updated_at'  # NB: prepend a minus (-) to sort in descending (so &order_by=-updated_at)

    # omaha_ne_markets = {'KETV':'ABC',
    #                     'KMT' :'CSB Omaha',
    #                     'WOWT':'NBC Omaha',
    #                     'CW'  :'KXVO',
    #                     'KPTM':'FOX Omaha'}

    # lincoln_ne_markets = {'KHGI':'ABC Lincoln Hastings',
    #                       'KLKN':'ABC Lincoln',
    #                       'KOLN':'CBS',
    #                       'KHAS':'NBC',
    #                       'KNOP':'NBC North Platte',
    #                       'KFXL':'Fox'}

    # test_req_by_callsign = requests.get(FCC_URL+'KETV'+'.json')
    # ^ The FCC responds with just text, not a response that is directly taken as JSON (.json() method fails).
    # So explicitly load this string into JSON format v.
    #json_response = json.loads(test_req_by_callsign.text)

    ##
    ## PAS Start:
    ##
    pas_params = {
                'format'              : 'json',
                'limit'               : 500,
                'contract_start_date__gte' : '2012-01-01',
                'order_by'            : 'updated_at'
               }

    out_dict = []
    # print('Testing cities {}...'.format(args))
    # dmas = convert_cities_to_dmas(args)
    dmas = []
    f = reader(open('zip_dmas.csv'))
    f.next()
    for l in f:
        zipc, dma, descr = l
        dmas.append(dma)
    # print('Testing dmas {}...'.format(dmas))

    # for city in dmas:  # TODO: Catch responses that give an empty 'objects' list.
    for city in set(dmas):
        print city,
        # print('Working on dma {}...'.format(city))
        #print callsign
        # dma = convert_cities_to_dmas(city)  #NB: want to keep the DMA as a string for search properties.
        # print(city, dma)
        pas_call = requests.get(PAS_URL + '&nielsen_dma_id={}'.format(city), params=pas_params)
        # print('PAS API call: {}'.format(pas_call.text))
        # print('Results of PAS API call: {}'.format(pas_call.text))
        # pas_call = requests.get(PAS_URL+'&q='+callsign, params=pas_params)
        if pas_call.text:
          pas_call = json.loads(pas_call.text)
          out_dict.append(pas_call['objects'])
          # print(pas_call['objects'])
        else:
          raise Exception('Cannot load ad-buy data into database. Content: {}'.format(pas_call))
    return out_dict


# if __name__ == '__main__':
    # print 'Work in progress..'
    # create_adbuys_database()
    # query_database_testing()

