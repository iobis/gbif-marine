import time
import psycopg2
from requests import get
import grequests
import sys
import traceback

batch_size = 50
pool_size = 5

gbif_url = "http://api.gbif.org/v1/node/%s"

con = psycopg2.connect("dbname='gbif' user='postgres' password='postgres' host='localhost'") 
cur = con.cursor()

while True:

	# retrieve organization keys from database

	print "Retrieving node keys from db..."
	
	cur.execute("select key from gbif.nodes where last_checked is null")
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
			node = r.json()

			# process node

			v.append("url = '%s'" % urls[i])

			if "title" in node:
				v.append("title = '%s'" % node["title"].replace("'", "''"))
			if "organization" in node:
				v.append("organization = '%s'" % node["organization"].replace("'", "''"))
			if "city" in node and node["city"]:
				v.append("city = '%s'" % node["city"].replace("'", "''"))
			if "country" in node:
				v.append("country = '%s'" % node["country"].replace("'", "''"))
			if "description" in node and node["description"]:
				v.append("description = '%s'" % node["description"].replace("'", "''"))
			if "homepage" in node:
				if len(node["homepage"]) > 0 and node["homepage"][0]:
					v.append("homepage = '%s'" % node["homepage"][0])
			if "latitude" in node:
				v.append("latitude = %s" % node["latitude"])
			if "longitude" in node:
				v.append("longitude = %s" % node["longitude"])

		except:
			print "Error processing response for node %s" % key

		queries.append("update gbif.nodes set " + ",".join(v) + " where key = '" + str(key) + "';")

	if len(queries) > 0:
		print "Committing to db..."
		query = "".join(queries)
		cur.execute(query)
		con.commit()
