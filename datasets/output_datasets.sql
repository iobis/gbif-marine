select
	d.title as title,
	d.obis,
	d.records,
	d.totalrecords,
	round(cast(cast(d.records as double precision) / cast(d.totalrecords as double precision) as numeric), 2) as fraction,
	d.taxa,
	d.description as description,
	d.datasetkey as key,
	d.taxonomiccoverage,
	d.geographiccoverage,
	o.description as org_description,
	o.homepage as org_homepage,
	o.title as org_title,
	o.city as org_city,
	o.country as org_country,
	o.url as org_url,
	n.title as node_title,
	n.organization as node_organization,
	n.description as node_description,
	n.homepage as node_homepage,
	n.city as node_city,
	n.country as node_country,
	n.url as node_url
from gbif.datasets d
left join gbif.organizations o
on d.publishingorganizationkey = o.key
left join gbif.nodes n
on o.endorsingnodekey = n.key
order by d.records desc;

select 
	d.title as title,
	d.obis,
	d.records,
	d.totalrecords,
	round(cast(cast(d.records as double precision) / cast(d.totalrecords as double precision) as numeric), 2) as fraction,
	d.taxa,
	o.title as org_title,
	o.country as org_country,
	n.title as node_title
from gbif.datasets d
left join gbif.organizations o
on d.publishingorganizationkey = o.key
left join gbif.nodes n
on o.endorsingnodekey = n.key
where d.records > 1000
order by d.records desc;