# Fabric notebook source

# METADATA ********************

# META {
# META   "kernel_info": {
# META     "name": "synapse_pyspark"
# META   },
# META   "dependencies": {
# META     "lakehouse": {
# META       "default_lakehouse": "07e48deb-91dd-484b-a26f-a3602d709745",
# META       "default_lakehouse_name": "lh_gold",
# META       "default_lakehouse_workspace_id": "238170a0-2b5d-44e7-bbf4-11d6911490f6",
# META       "known_lakehouses": [
# META         {
# META           "id": "07e48deb-91dd-484b-a26f-a3602d709745"
# META         },
# META         {
# META           "id": "15ecebd5-cfde-4e08-8e7f-20de67bc7036"
# META         }
# META       ]
# META     }
# META   }
# META }

# MARKDOWN ********************

# ### Transformacion de la tabla "display"

# CELL ********************

%run configurations

# METADATA ********************

# META {
# META   "language": "python",
# META   "language_group": "synapse_pyspark"
# META }

# CELL ********************

%run common_functions

# METADATA ********************

# META {
# META   "language": "python",
# META   "language_group": "synapse_pyspark"
# META }

# MARKDOWN ********************

# #### Paso 1: Leer tabla "display" usando Spark.sql

# CELL ********************

display_df = spark.sql("SELECT * FROM lh_silver.dbo.display")

# METADATA ********************

# META {
# META   "language": "python",
# META   "language_group": "synapse_pyspark"
# META }

# MARKDOWN ********************

# #### Paso 2: Eliminar la columna "environment" del DataFrame

# CELL ********************

from pyspark.sql.functions import col

display_drop_column_df = display_df.drop(col("environment"))

# METADATA ********************

# META {
# META   "language": "python",
# META   "language_group": "synapse_pyspark"
# META }

# CELL ********************

display(display_drop_column_df.limit(3))

# METADATA ********************

# META {
# META   "language": "python",
# META   "language_group": "synapse_pyspark"
# META }

# MARKDOWN ********************

# #### Paso 3: Transformar la columna "refresh_rate"

# CELL ********************

display_final_df = display_drop_column_df.na.fill({"refresh_rate": "unknown"})

# METADATA ********************

# META {
# META   "language": "python",
# META   "language_group": "synapse_pyspark"
# META }

# CELL ********************

merge_condition = "tgt.display_id = src.display_id AND tgt.file_date = src.file_date"

# merge_delta_lake(display_final_df, "lh_gold","dbo", "dim_display", gold_folder_path, merge_condition, "file_date")

merge_delta_lake(display_final_df, "dim_display", merge_condition, "file_date")

# METADATA ********************

# META {
# META   "language": "python",
# META   "language_group": "synapse_pyspark"
# META }

# CELL ********************

# MAGIC %%sql
# MAGIC SELECT file_date, count(1) FROM dim_display
# MAGIC GROUP BY file_date;

# METADATA ********************

# META {
# META   "language": "sparksql",
# META   "language_group": "synapse_pyspark"
# META }
