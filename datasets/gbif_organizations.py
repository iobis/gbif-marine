import time
import psycopg2
from requests import get
import grequests
import sys
import traceback

batch_size = 50
pool_size = 5

gbif_url = "http://api.gbif.org/v1/organization/%s"

con = psycopg2.connect("dbname='gbif' user='postgres' password='postgres' host='localhost'") 
cur = con.cursor()

while True:

	# retrieve organization keys from database

	print "Retrieving dataset keys from db..."
	
	cur.execute("select key from gbif.organizations where last_checked is null")
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
			organization = r.json()

			# process organization

			v.append("url = '%s'" % urls[i])

			if ("endorsingNodeKey" in organization):
				v.append("endorsingnodekey = '%s'" % organization["endorsingNodeKey"].replace("'", "''"))
			if ("title" in organization):
				v.append("title = '%s'" % organization["title"].replace("'", "''"))
			if ("abbreviation" in organization):
				v.append("abbreviation = '%s'" % organization["abbreviation"])
			if ("description" in organization):
				v.append("description = '%s'" % organization["description"].replace("'", "''"))
			if ("city" in organization):
				v.append("city = '%s'" % organization["city"])
			if ("country" in organization):
				v.append("country = '%s'" % organization["country"])
			if ("homepage" in organization):
				if len(organization["homepage"]) > 0:
					v.append("homepage = '%s'" % organization["homepage"][0])

		except:
			print "Error processing response for organization %s" % key

		queries.append("update gbif.organizations set " + ",".join(v) + " where key = '" + str(key) + "';")

	if len(queries) > 0:
		print "Committing to db..."
		query = "".join(queries)
		cur.execute(query)
		con.commit()
