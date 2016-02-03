drop table if exists gbif.names;

create table gbif.names as
with taxa as (
	select scientificname, taxonkey
	from gbif.occurrence
	group by scientificname, taxonkey
	order by scientificname
)
select 
	taxa.*,
	cast(null as timestamp) as last_checked,
	cast(null as boolean) as worms_marine,
	cast(null as boolean) as worms_brackish,
	cast(null as boolean) as worms_terrestrial,
	cast(null as boolean) as worms_freshwater,
	cast(null as boolean) as worms_extinct,
	cast(null as integer) as worms_id,
	cast(null as boolean) as irmng_marine,
	cast(null as boolean) as irmng_brackish,
	cast(null as boolean) as irmng_terrestrial,
	cast(null as boolean) as irmng_freshwater,
	cast(null as boolean) as irmng_extinct,
	cast(null as integer) as irmng_id
from taxa;