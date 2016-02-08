import time
import psycopg2
from requests import get
import grequests
import sys

batch_size = 50
pool_size = 5

gbif_url = "http://api.gbif.org/v1/dataset/%s"

con = psycopg2.connect("dbname='gbif' user='postgres' password='postgres' host='localhost'") 
cur = con.cursor()

while True:

	# retrieve dataset keys from database

	print "Retrieving dataset keys from db..."
	
	cur.execute("select datasetkey from gbif.datasets where last_checked is null")
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
			dataset = r.json()

			# process dataset

			if ("publishingOrganizationKey" in dataset):
				v.append("publishingorganizationkey = '%s'" % dataset["publishingOrganizationKey"])
			if ("doi" in dataset):
				v.append("doi = '%s'" % dataset["doi"])
			if ("type" in dataset):
				v.append("type = '%s'" % dataset["type"])
			if ("title" in dataset):
				v.append("title = '%s'" % dataset["title"].replace("'", "''"))
			if ("description" in dataset):
				v.append("description = '%s'" % dataset["description"].replace("'", "''"))
			if ("pubDate" in dataset):
				v.append("pubdate = '%s'" % dataset["pubDate"])
			if ("taxonomicCoverages" in dataset):
				if (len(dataset["taxonomicCoverages"]) > 0):
					cov = []
					for coverage in dataset["taxonomicCoverages"]:
						if "description" in coverage:
							cov.append(coverage["description"].replace("'", "''"))
					v.append("taxonomiccoverage = '%s'" % ";".join(cov))
			if ("geographicCoverages" in dataset):
				if (len(dataset["geographicCoverages"]) > 0):
					cov = []
					for coverage in dataset["geographicCoverages"]:
						if "description" in coverage:
							cov.append(coverage["description"].replace("'", "''"))
					v.append("geographiccoverage = '%s'" % ";".join(cov))

		except:
			print "Error processing response for dataset %s" % key

		queries.append("update gbif.datasets set " + ",".join(v) + " where datasetkey = '" + str(key) + "';")

	if len(queries) > 0:
		print "Committing to db..."
		query = "".join(queries)
		cur.execute(query)
		con.commit()
