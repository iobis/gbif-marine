import sys
from itertools import chain
from suds.client import Client
from pg import DB
import time

reload(sys)
sys.setdefaultencoding("utf8")
start_time = time.time()
url = "http://www.marinespecies.org/aphia.php?p=soap&wsdl=1"
client = Client(url)
db = DB(dbname="gbif", host="localhost", port=5432, user="postgres", passwd="postgres")

offset = 0
while True:

	names = db.query("select name from gbif.names where match_type is null limit 50 offset " + str(offset)).getresult()
	names = list(chain(*names))

	if (len(names) == 0):
			break

	scientificnames = client.factory.create("scientificnames")
	scientificnames.item = names
	scientificnames._arrayType = "xsd:string[]"

	try:
		results = client.service.matchAphiaRecordsByNames(scientificnames, True, True, False)
	except:
		e = sys.exc_info()[0]
		print "Error: " + str(e)
		results = []
		
	for i, r in enumerate(results):

		if (len(r) > 0):
			r = r[0]
			v = []
			if r.scientificname is not None: v.append("scientificname='" + r.scientificname.replace("'", "''") + "'")
			if r.authority is not None: v.append("authority='" + r.authority.replace("'", "''") + "'")
			if r.rank is not None: v.append("rank='" + r.rank + "'")
			if r.status is not None: v.append("status='" + r.status + "'")
			if r.unacceptreason is not None: v.append("unacceptreason='" + r.unacceptreason + "'")
			if r.AphiaID is not None: v.append("aphiaid=" + str(r.AphiaID))
			if r.valid_AphiaID is not None: v.append("valid_aphiaid=" + str(r.valid_AphiaID)) 
			if r.valid_name is not None: v.append("valid_name='" + r.valid_name.replace("'", "''") + "'")
			if r.valid_authority is not None: v.append("valid_authority='" + r.valid_authority.replace("'", "''") + "'")
			if r.kingdom is not None: v.append("kingdom='" + r.kingdom + "'")
			if r.phylum is not None: v.append("phylum='" + r.phylum + "'")
			if r.cls is not None: v.append("cls='" + r.cls + "'")
			if r.order is not None: v.append("ord='" + r.order + "'")
			if r.family is not None: v.append("family='" + r.family + "'")
			if r.genus is not None: v.append("genus='" + r.genus + "'")
			if r.match_type is not None: v.append("match_type='" + r.match_type + "'")
			if r.isMarine is not None: v.append("marine=cast(" + str(r.isMarine) + " as boolean)")
			if r.isBrackish is not None: v.append("brackish=cast(" + str(r.isBrackish) + " as boolean)")
			if r.isFreshwater is not None: v.append("freshwater=cast(" + str(r.isFreshwater) + " as boolean)")
			if r.isTerrestrial is not None: v.append("terrestrial=cast(" + str(r.isTerrestrial) + " as boolean)")
			if r.isExtinct is not None: v.append("extinct=cast(" + str(r.isExtinct) + " as boolean)")

			q = "update gbif.names set " + ",".join(v) + " where name='" + names[i].replace("'", "''") + "'"
			db.query(q.encode("utf-8"))
			print str(offset) + " " + names[i] + " " + str(time.time() - start_time)
		else:
			v = []
			v.append("match_type='none'")

			q = "update gbif.names set " + ",".join(v) + " where name='" + names[i].replace("'", "''") + "'"
			db.query(q.encode("utf-8"))

	offset = offset + 50