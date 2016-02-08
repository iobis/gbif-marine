drop table if exists gbif.nodes;

create table gbif.nodes as
select
	endorsingnodekey as key,
	cast(null as text) as title,
	cast(null as text) as organization,
	cast(null as text) as description,
	cast(null as text) as homepage,
	cast(null as text) as city,
	cast(null as text) as country,
	cast(null as double precision) as latitude,
	cast(null as double precision) as longitude,
	cast(null as text) as url,
	cast(null as timestamp) as last_checked
from gbif.organizations
where endorsingnodekey is not null
group by endorsingnodekey
order by endorsingnodekey;

create index nodes_ix_key on gbif.nodes using btree(key);