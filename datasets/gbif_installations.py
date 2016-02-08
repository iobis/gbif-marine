import time
import psycopg2
from requests import get
import grequests
import sys
import traceback

batch_size = 50
pool_size = 5

gbif_url = "http://api.gbif.org/v1/installation/%s"

con = psycopg2.connect("dbname='gbif' user='postgres' password='postgres' host='localhost'") 
cur = con.cursor()

while True:

	# retrieve installation keys from database

	print "Retrieving installation keys from db..."
	
	cur.execute("select key from gbif.installations where last_checked is null")
	rows = cur.fetchmany(batch_size)
	if (len(rows) == 0):
		sys.exit()

	# create list of urls

	print "Querying GBIF..."

	keys = []
	urls = []

	for row in rows:
		key = row[0]
		keys.append(key)
		urls.append(gbif_url % key)

	# initiate requests

	rs = (grequests.get(u) for u in urls)	

	# process responses

	responses = grequests.map(rs, size=pool_size)

	print "GBIF responses received..."

	queries = []

	for i, r in enumerate(responses):

		key = keys[i]
		v = []
		v.append("last_checked = '" + time.strftime("%Y/%m/%d %H:%M:%S") + "'")

		try:
			installation = r.json()

			# process organization

			v.append("url = '%s'" % urls[i])

			if ("organizationKey" in installation):
				v.append("organizationkey = '%s'" % installation["organizationKey"])
			if ("title" in installation):
				v.append("title = '%s'" % installation["title"].replace("'", "''"))
			if ("type" in installation):
				v.append("type = '%s'" % installation["type"])
			if ("description" in installation):
				v.append("description = '%s'" % installation["description"].replace("'", "''"))

		except:
			print "Error processing response for installation %s" % key
			traceback.print_exc()

		queries.append("update gbif.installations set " + ",".join(v) + " where key = '" + str(key) + "';")

	if len(queries) > 0:
		print "Committing to db..."
		query = "".join(queries)
		cur.execute(query)
		con.commit()
