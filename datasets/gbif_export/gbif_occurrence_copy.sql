copy gbif.occurrence from '/Users/Pieterp/Desktop/gbif/name_export.txt' delimiter as '	' csv;

create index occurrence_ix_datasetkey on gbif.occurrence using btree(datasetkey);