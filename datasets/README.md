# datasets

This is a collection of scripts which compiles a list of marine datasets in GBIF. A file containing taxon lists for all datasets is required, but not incuded in this repository. Species profiles are retrieved from the GBIF API and checked for a WoRMS or IRMNG marine flag.

## How-to

#### gbif_export/gbif_occurrence_table.sql

This creates a table `occurrence` for the `name_export.txt` file provided by GBIF.

#### gbif_export/gbif_occurrence_copy.sql

This copies the `name_export.txt` file to database.

#### gbif_names.sql

This creates a `names` table from the `occurrence` table.

#### gbif_profiles.py

This queries the GBIF API for species profiles. The `names` table gets populated with WoRMS and IRMNG marine flags.

#### id_mapping.sql` and `id_mapping_copy.sql

This creates a table and copies the `id_mapping.csv` file to database.

#### gbif_datasets.sql

This creates a `datasets` table from the `occurrence` and `names` tables. Only datasets with marine taxa are included.

#### gbif_datasets.py

This queries the GBIF API for dataset information.

#### totalrecords.sql

This adds the total number of records to the datasets.

#### gbif_organizations.sql and gbif_organizations.py

This creates a `organizations` table from the `datasets` table and queries the GBIF API for publishing organization information.

#### gbif_nodes.sql and gbif_nodes.py

This creates a `nodes` table from the `organizations` table and queries the GBIF API for node information.

#### gbif_installations.sql and gbif_installations.py

This creates a `installations` table from the `datasets` table and queries the GBIF API for installation information.

#### obis.py

This marks OBIS datasets.

#### output_datasets.sql

This outputs the [datasets.csv](datasets.csv) and [datasets_sample.csv](datasets_sample.csv) tables.
