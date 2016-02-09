drop table if exists gbif.datasets;

create table gbif.datasets as
select
	datasetkey,
	sum(records) as records,
	count(distinct(occurrence.taxonkey)) as taxa,
	ids.obis as obis_id,
	cast(null as text) as publishingorganizationkey,
	cast(null as text) as installationkey,
	cast(null as text) as url,
	cast(null as text) as doi,
	cast(null as text) as type,
	cast(null as text) as title,
	cast(null as text) as description,
	cast(null as timestamp) as pubdate,
	cast(null as text) as taxonomiccoverage,
	cast(null as text) as geographiccoverage,
	cast(null as timestamp) as last_checked,
	cast(null as boolean) as obis
from gbif.occurrence
inner join gbif.names
on occurrence.taxonkey = names.taxonkey
left join gbif.ids
on occurrence.datasetkey = ids.gbif
where
	(names.worms_marine is true or names.irmng_marine is true)
	and names.worms_extinct is not true
	and names.irmng_extinct is not true
group by datasetkey, obis_id
order by datasetkey;

create index datasets_ix_datasetkey on gbif.datasets using btree(datasetkey);