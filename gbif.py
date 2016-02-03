import time
import psycopg2
from requests import get

aphia_url = "http://www.marinespecies.org/aphia.php?p=soap&wsdl=1"
gbif_url = "http://api.gbif.org/v1/species/%s/speciesProfiles"

con = psycopg2.connect("dbname='gbif' user='postgres' password='postgres' host='localhost'") 
cur = con.cursor()

while True:

	print "Retrieving taxon keys from db..."

	cur.execute("select taxonkey from gbif.names where last_checked is null")
	rows = cur.fetchmany(100)
	if (len(rows) == 0):
		break

	print "Querying GBIF..."

	for res in rows:

		key = res[0]
		url = gbif_url % key
		r = get(url)
		data = r.json()
		results = data['results']

		v = []
		v.append("last_checked = '" + time.strftime("%Y/%m/%d %H:%M:%S") + "'")

		if (len(results) > 0):

			print key

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

		cur.execute("update gbif.names set " + ",".join(v) + " where taxonkey = " + str(key))

	print "Committing to db..."

	con.commit()
