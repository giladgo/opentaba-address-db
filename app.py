import os
import json
from bson import json_util
from urlparse import urlparse
import urllib2
import urllib
import contextlib


from flask import Flask
from flask import abort, redirect, url_for, make_response, request

app = Flask(__name__)

import dbutils
    
if dbutils.RUNNING_LOCAL:
	app.debug = True # since we're local, keep debug on



#### Helpers ####

# convert dictionary to JSON. json_util.default adds automatic mongoDB result support
def _to_json(mongo_obj):
	return json.dumps(mongo_obj, ensure_ascii=False, default=json_util.default)


def _resp(data):
	r = make_response(_to_json(data))
	r.headers['Access-Control-Allow-Origin'] = "*"
	r.headers['Content-Type'] = "application/json; charset=utf-8"
	return r


@app.route('/locate/<addr>')
def locate(addr):
	url = "http://nominatim.openstreetmap.org/search?" +  urllib.urlencode({"q" : addr.encode('utf8'), "format": "json"})
	with contextlib.closing(urllib2.urlopen(url)) as wwwfile:
		o = json.load(wwwfile)

	if not o:
		return _resp("ERROR")

	coords = []
	lon = float(o[0]['lon'])
	lat = float(o[0]['lat'])

	gush = dbutils.db.gushim.find_one( { "gush_geo": { "$geoIntersects": {"$geometry": {"type":"Point", "coordinates": [lon, lat]}} } }  )


	if gush:
		return _resp({ "gush_id": gush['gush_id'], "lon": lon, "lat": lat})
	else:
		abort(404)


#### MAIN ####

if __name__ == '__main__':
    # Bind to PORT if defined, otherwise default to 5000.
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)



