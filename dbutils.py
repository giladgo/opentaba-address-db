import os
import pymongo

MONGO_URL = os.environ.get('MONGOHQ_URL')
RUNNING_LOCAL = False

if MONGO_URL:	# on Heroku, get a connection
    m_conn = pymongo.Connection(MONGO_URL)   
    db = m_conn[urlparse(MONGO_URL).path[1:]]
    RUNNING_LOCAL = False
else:			# work locally
    m_conn = pymongo.Connection('localhost', 27017)
    db = m_conn['opentaba-address-db']
    RUNNING_LOCAL = True
