drop table if exists gbif.occurrence;

create table gbif.occurrence (
	datasetkey varchar(36),
	kingdom varchar(50),
	family varchar(50),
	scientificname text,
	taxonkey integer,
	records integer
)