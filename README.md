# gbif-marine

Retrieves species profiles and dataset information from the GBIF API.

## How-to

1. `gbif_export/gbif_names.sql`

This creates a table `occurrence` for the `name_export.txt` file provided by GBIF.

2. `gbif_export/gbif_occurrence_copy`

This copies the `name_export.txt` file to database.

3. `gbif_names.sql`

This creates a `names` table from the `occurrence` table.

4. `gbif_profiles.py`

This queries the GBIF API for species profiles. The `names` table gets populated with WoRMS and IRMNG marine flags.

5. `gbif_datasets.sql`

This creates a `datasets` table from the `occurrence` and `names` tables. Only datasets with marine taxa are included.

6. `gbif_datasets.py`

This queries the GBIF API for dataset information.

7. `gbif_organizations.sql`

This creates a `organizations` table from the `datasets` table.

8. `gbif_organizations.py`

This queries the GBIF API for publishing organization information.

9. `obis.py`

This marks OBIS datasets.

10. `output_datasets.sql`

This outputs the [datasets.csv](datasets.csv) and [datasets_sample.csv](datasets_sample.csv) tables.
