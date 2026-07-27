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

# ### Transformacion d ela tabla "physical_spects"

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

# #### Paso 1: Leer la tabla "physical_spects" usando Spark.sql

# CELL ********************

physical_spects_df = spark.sql("SELECT * FROM lh_silver.dbo.physical_specs")

# METADATA ********************

# META {
# META   "language": "python",
# META   "language_group": "synapse_pyspark"
# META }

# MARKDOWN ********************

# #### Paso 2: Eliminar la columna "Environment" del dataframe

# CELL ********************

from pyspark.sql.functions import col

physical_spects_drop_column_df = physical_spects_df.drop(col("environment"))

# METADATA ********************

# META {
# META   "language": "python",
# META   "language_group": "synapse_pyspark"
# META }

# CELL ********************

display(physical_spects_drop_column_df.limit(3))

# METADATA ********************

# META {
# META   "language": "python",
# META   "language_group": "synapse_pyspark"
# META }

# MARKDOWN ********************

# #### Paso 3: transformar la columna "Controler"

# CELL ********************

physical_spects_final_df = physical_spects_drop_column_df.replace("", "unknown")

# METADATA ********************

# META {
# META   "language": "python",
# META   "language_group": "synapse_pyspark"
# META }

# CELL ********************

display(physical_spects_final_df.limit(5))

# METADATA ********************

# META {
# META   "language": "python",
# META   "language_group": "synapse_pyspark"
# META }

# MARKDOWN ********************

# #### Paso 4: Escribir el lh_gold

# CELL ********************

merge_condition = "tgt.physicalSpec_id = src.physicalSpec_id AND tgt.file_date = src.file_date"
# merge_delta_lake(physical_spects_final_df, "lh_gold", "dbo", "dim_physical_spects", gold_folder_path, merge_condition, "file_date")

merge_delta_lake(physical_spects_final_df, "dim_physical_spects", merge_condition, "file_date")

# METADATA ********************

# META {
# META   "language": "python",
# META   "language_group": "synapse_pyspark"
# META }

# CELL ********************

# MAGIC %%sql
# MAGIC SELECT file_date, count(1) FROM dim_physical_spects
# MAGIC GROUP BY file_date;

# METADATA ********************

# META {
# META   "language": "sparksql",
# META   "language_group": "synapse_pyspark"
# META }
