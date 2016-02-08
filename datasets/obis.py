import psycopg2
import sys

con = psycopg2.connect("dbname='gbif' user='postgres' password='postgres' host='localhost'") 
cur = con.cursor()

with open("obis.csv") as f:
	keys = f.readlines()

for key in keys:
	print key.strip()
	cur.execute("update gbif.datasets set obis = true where datasetkey = '%s'" % key.strip())

con.commit()