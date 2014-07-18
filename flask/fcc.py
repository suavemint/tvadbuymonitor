import requests, json, unittest, os, csv

def return_zero_or_int(x):
    if x is None:
        return 0
    return int(float(x))

def create_database_testing():
  import sqlalchemy as sql
  # from datetime import datetime, date
  from datetime import datetime
  # import time

  # db = sql.create_engine('mysql+mysqldb:///adbuys.db')
  db = sql.create_engine('postgresql://postgres:password@localhost:5432/testdb')
  # db.echo = True
  metadata = sql.MetaData(db)

# Sample 'objects' object:

# {u'advertiser': None,
#   u'broadcasters': [u'KMTV-TV'],
#   u'candidate_type': u'Non-Candidate Issue Ads',
#   u'community_state': u'NE',
#   u'contract_end_date': u'2014-06-30',
#   u'contract_number': None,
#   u'contract_start_date': u'2014-06-30',
#   u'description': u'Non-Candidate Issue Ads, 06/30/14 on KMTV-TV (Omaha, NE)',
#   u'doc_source': u'FCC',
#   u'doc_status': u'Not loaded',
#   u'nielsen_dma': u'Omaha, NE',
#   u'nielsen_dma_id': 652,
#   u'num_spots': None,
#   u'resource_uri': u'/api/v1/politicalfile/1d9b7d31-f151-4116-b8c5-b69fea4250cf/',
#   u'source_file_uri': u'https://stations.fcc.gov/collect/files/35190/Political%20File/2014/Non-Candidate%20Issue%20Ads/DSCC%20IE%20523279%20%2814041354274449%29_.pdf',
#   u'total_spent': None,
#   u'updated_at': u'2014-06-30T09:40:09.912648',
#   u'upload_time': u'2014-06-30',
#   u'uuid_key': u'1d9b7d31-f151-4116-b8c5-b69fea4250cf'}

  adbuys = sql.Table('adbuys', metadata,
    sql.Column('adbuy_id', sql.Integer, primary_key=True),
    sql.Column('advertiser', sql.String),
    sql.Column('broadcasters', sql.String(50)),  # Will need to extract 'broadcasters' key by '','.join(broadcasters)' for broadcasters = resp['objects']['broadcasters']
    sql.Column('candidate_type', sql.String(50)),
    sql.Column('community_state', sql.String(2)),
    sql.Column('contract_end_date', sql.Date),
    sql.Column('contract_number', sql.String, default=0),
    # sql.Column('contract_start_date', sql.String),
    sql.Column('contract_start_date', sql.Date),
    sql.Column('description', sql.String(200)),
    sql.Column('doc_source', sql.String(20)),
    sql.Column('doc_status', sql.String(20)),
    sql.Column('nielsen_dma', sql.String(50)),
    sql.Column('nielsen_dma_id', sql.Integer),
    sql.Column('num_spots', sql.SmallInteger, default=0),
    sql.Column('resource_uri', sql.String(200)),
    sql.Column('source_file_uri', sql.String(400)),
    sql.Column('total_spent', sql.Integer, default=0),
    sql.Column('updated_at', sql.DateTime),
    sql.Column('upload_time', sql.String),
    sql.Column('uuid_key', sql.String(40)),
    sql.Column('last_refreshed_datetime', sql.DateTime, default=null)
    )

  adbuys.create(checkfirst=True)

  i = adbuys.insert()
  d = {}
  # data = get_adbuys_by_city('Miami','Orlando')
  # data = get_adbuys_by_city('Omaha', 'Lincoln', 'Miami', 'Orlando')
  data = get_adbuys_by_city()
  # print data


  # if data is None:
  #     print 'No data to insert.'
  #   # import sys;sys.exit(1)
  #     continue
  pas_data_to_insert = [x for x in data if x != None if data != None]  # FIXME: These two lines are logically redundant...

  if pas_data_to_insert is not None:

    # print pas_data_to_insert[1]; import sys; sys.exit(1)

    for a in pas_data_to_insert:
      # print a
      for l in a:
        # print 'TESTING'; print 50*'='
        d = dict(advertiser= l['advertiser'],
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
        # print d
        # import sys; sys.exit(1)
        i.execute(d)
        # i.execute(adbuys.insert(d))

def run(stmt):


  rs = stmt.execute()
  for r in rs:
    print r

def query_database_testing():
    '''
    Some queries that work (assuming date-type columns for timestamps):

    1.
    For the total spend on ad buys since the (contracts that start at) start of 2014 in FL:
    select sum(total_spent) from adbuys where community_state = 'FL' and 'contract_start_date' > '2014-01-01';

    2.
    For the total number of ad spots purchased (so counting rows returned) from KMTV after 2014:
    select count(*) from adbuys where broadcasters like 'KMTV' and 'contract_start_date' > '2012-01-01';

    '''
    import sqlalchemy as sql
    from sqlalchemy.orm import sessionmaker
    # Now, let's test the recovery of the data; let's find if there are any ads in the stations of interest:
    # a_stations = ['KETV','KMT','WOWT','CW','KPTM']# in Omaha:

    db = sql.create_engine('postgresql://postgres:password@localhost:5432/testdb')
    # db.echo = 'debug'
    metadata = sql.MetaData(db)

    # Set up Session factory instance, and make instance for this db (buys.db)
    Session = sessionmaker(bind=db)
    session = Session()

    adbuys = sql.Table('adbuys', metadata, autoload=True)

    query_nonzero_buy = lambda x: x['total_spent']

    a = session.query(adbuys).filter(adbuys.c.broadcasters.contains('KLKN')).all()
    print(a)
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


if __name__ == '__main__':
  # print 'Work in progress..'
  create_database_testing()
  # query_database_testing()

