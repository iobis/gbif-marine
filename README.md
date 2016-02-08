# gbif-marine

This is a collection of scripts which compiles a list of marine datasets in GBIF. A file containing taxon lists for all datasets is required, but not incuded in this repository. Species profiles are retrieved from the GBIF API and checked for a WoRMS or IRMNG marine flag.

## How-to

1. `gbif_export/gbif_names.sql`

 This creates a table `occurrence` for the `name_export.txt` file provided by GBIF.

2. `gbif_export/gbif_occurrence_copy.sql`

 This copies the `name_export.txt` file to database.

3. `gbif_names.sql`

 This creates a `names` table from the `occurrence` table.

4. `gbif_profiles.py`

 This queries the GBIF API for species profiles. The `names` table gets populated with WoRMS and IRMNG marine flags.

5. `gbif_datasets.sql`

 This creates a `datasets` table from the `occurrence` and `names` tables. Only datasets with marine taxa are included.

6. `gbif_datasets.py`

 This queries the GBIF API for dataset information.

7. `totalrecords.sql`

 This adds the total number of records to the datasets.

8. `gbif_organizations.sql`

 This creates a `organizations` table from the `datasets` table.

9. `gbif_organizations.py`

 This queries the GBIF API for publishing organization information.

10. `gbif_nodes.sql`

 This creates a `nodes` table from the `organizations` table.

11. `gbif_nodes.py`

 This queries the GBIF API for node information.

12. `obis.py`

 This marks OBIS datasets.

13. `output_datasets.sql`

 This outputs the [datasets.csv](datasets.csv) and [datasets_sample.csv](datasets_sample.csv) tables.
