drop table if exists gbif.organizations;

create table gbif.organizations as
select
	publishingorganizationkey as key,
	count(*) as datasets,
	sum(records) as records,
	cast(null as text) as endorsingnodekey,
	cast(null as text) as title,
	cast(null as text) as abbreviation,
	cast(null as text) as description,
	cast(null as text) as homepage,
	cast(null as text) as city,
	cast(null as text) as country,
	cast(null as text) as url,
	cast(null as timestamp) as last_checked
from gbif.datasets
where publishingorganizationkey is not null
group by publishingorganizationkey
order by publishingorganizationkey;

create index organizations_ix_key on gbif.organizations using btree(key);