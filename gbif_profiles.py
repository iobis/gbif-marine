import time
import psycopg2
from requests import get
import grequests

batch_size = 50
pool_size = 5

aphia_url = "http://www.marinespecies.org/aphia.php?p=soap&wsdl=1"
gbif_url = "http://api.gbif.org/v1/species/%s/speciesProfiles"

con = psycopg2.connect("dbname='gbif' user='postgres' password='postgres' host='localhost'") 
cur = con.cursor()

while True:

	# retrieve names from database

	print "Retrieving taxon keys from db..."
	
	cur.execute("select taxonkey from gbif.names where last_checked is null")
	rows = cur.fetchmany(batch_size)
	if (len(rows) == 0):
		break

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

		if r is None:

			print "Error processing response for taxon key %s..." % key

		else:

			data = r.json()
			results = data['results']

			# process species profiles

			if (len(results) > 0):

				irmng = False
				worms = False

				for result in results:

					if irmng == False and result["source"] == "Interim Register of Marine and Nonmarine Genera":
						irmng = True
						if "sourceTaxonKey" in result:
							v.append("irmng_id = " + str(result["sourceTaxonKey"]))
						if "marine" in result:
							if result["marine"]:
								v.append("irmng_marine = true")
						if "brackish" in result:
							if result["brackish"]:
								v.append("irmng_brackish = true")
						if "freshwater" in result:
							if result["freshwater"]:
								v.append("irmng_freshwater = true")
						if "terrestrial" in result:
							if result["terrestrial"]:
								v.append("irmng_terrestrial = true")
						if "extinct" in result:
							if result["extinct"]:
								v.append("irmng_extinct = true")

					elif worms == False and result["source"] == "World Register of Marine Species":
						worms = True
						if "sourceTaxonKey" in result:
							v.append("worms_id = " + str(result["sourceTaxonKey"]))
						if "marine" in result:
							if result["marine"]:
								v.append("worms_marine = true")
						if "brackish" in result:
							if result["brackish"]:
								v.append("worms_brackish = true")
						if "freshwater" in result:
							if result["freshwater"]:
								v.append("worms_freshwater = true")
						if "terrestrial" in result:
							if result["terrestrial"]:
								v.append("worms_terrestrial = true")
						if "extinct" in result:
							if result["extinct"]:
								v.append("worms_extinct = true")

		queries.append("update gbif.names set " + ",".join(v) + " where taxonkey = " + str(key) + ";")

	print "Committing to db..."

	query = "".join(queries)
	cur.execute(query)
	con.commit()
