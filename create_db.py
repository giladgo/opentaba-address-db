import json
import pymongo
from optparse import OptionParser

import dbutils

parser = OptionParser()
parser.add_option("--force", dest="force", default=False, action="store_true", help="delete existing dbs")

(options, args) = parser.parse_args()

if not options.force:
	print "This script will delete the gushim. To make sure this isn't running by mistake, run this with --force"
	exit()

# print "Deleting db.gushim and db.plans"
dbutils.db.gushim.drop()

dbutils.db.gushim.create_index([('gush_id', 1)], unique=True)

bad_gushim = [30160, 30343, 30361, 0]

with open("data/gushim.js","r") as gushim_file:
	gushim_str = gushim_file.read()

gushim_str = gushim_str.replace("var gushim = ", "")
gushim = json.loads(gushim_str)
for g in gushim["features"]:
	if g["properties"]["Name"]:
		try:
			gush_id = int(g["properties"]["Name"])
		except ValueError:
			continue

		# some gushim are bad, so skip them
		if gush_id in bad_gushim:
			continue

		for ring in range(len(g["geometry"]["coordinates"])):
			newcoords = []
			for coord in g["geometry"]["coordinates"][ring]:
				#print coord[0], coord[1]
				newcoords.append([coord[0], coord[1]])

			g["geometry"]["coordinates"][ring] = newcoords

		print "inserting gush number ", gush_id, "number of coords", len(g["geometry"]["coordinates"][0])
		dbutils.db.gushim.insert({
			'gush_id'	: gush_id,
			'html_hash' : '',
			'last_checked_at': '',
			'gush_geo': g["geometry"]
		})

print "Inserted %d gushim" % (len(gushim["features"]))
print "Creating geo index..."
dbutils.db.gushim.create_index([("gush_geo", pymongo.GEOSPHERE)])


print "=== All done! ==="