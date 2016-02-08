drop table if exists gbif.names;

create table gbif.names as
select
	distinct(scientificname) as name,
	cast(null as text) as scientificname,
	cast(null as text) as authority,
	cast(null as text) as rank,
	cast(null as text) as status,
	cast(null as text) as unacceptreason,
	cast(null as integer) as aphiaid,
	cast(null as integer) as valid_aphiaid,
	cast(null as text) as valid_name,
	cast(null as text) as valid_authority,
	cast(null as text) as kingdom,
	cast(null as text) as phylum,
	cast(null as text) as cls,
	cast(null as text) as ord,
	cast(null as text) as family,
	cast(null as text) as genus,
	cast(null as text) as match_type,
	cast(null as boolean) as marine,
	cast(null as boolean) as brackish,
	cast(null as boolean) as terrestrial,
	cast(null as boolean) as freshwater,
	cast(null as boolean) as extinct
from gbif.occurrence
order by name;