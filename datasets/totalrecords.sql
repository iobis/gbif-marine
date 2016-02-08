alter table gbif.datasets add column totalrecords integer;

update gbif.datasets
set totalrecords = sub.records
from (
	select d.datasetkey, sum(o.records) as records
	from gbif.datasets d
	left join gbif.occurrence o
	on d.datasetkey = o.datasetkey
	group by d.datasetkey
) as sub
where datasets.datasetkey = sub.datasetkey;