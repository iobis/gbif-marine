drop table if exists gbif.installations;

create table gbif.installations as
select
	installationkey as key,
	cast(null as text) as organizationkey,
	cast(null as text) as title,
	cast(null as text) as type,
	cast(null as text) as description,
	cast(null as text) as url,
	cast(null as timestamp) as last_checked
from gbif.datasets
where installationkey is not null
group by installationkey
order by installationkey;

create index installations_ix_key on gbif.installations using btree(key);