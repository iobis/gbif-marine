drop table if exists gbif.datasets;

create table gbif.datasets as
select
	datasetkey,
	sum(records) as records,
	cast(null as text) as publishingorganizationkey,
	cast(null as text) as doi,
	cast(null as text) as type,
	cast(null as text) as title,
	cast(null as text) as description,
	cast(null as timestamp) as pubdate,
	cast(null as text) as taxonomiccoverage,
	cast(null as text) as geographiccoverage,
	cast(null as timestamp) as last_checked	
from gbif.occurrence
inner join gbif.names
on occurrence.taxonkey = names.taxonkey
where names.worms_marine = true or names.irmng_marine = true
group by datasetkey
order by datasetkey;

create index datasets_ix_datasetkey on gbif.datasets using btree(datasetkey);