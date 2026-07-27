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

# ## Transformacion de la tabla "device"

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

# #### Paso 1: Ler la tabla "device" usando "Spark.sql"

# CELL ********************

device_df = spark.sql("SELECT * FROM lh_silver.dbo.device")

# METADATA ********************

# META {
# META   "language": "python",
# META   "language_group": "synapse_pyspark"
# META }

# MARKDOWN ********************

# #### Paso 2: Eliminar columna "environment" del DataFrame

# CELL ********************

from pyspark.sql.functions import col

# METADATA ********************

# META {
# META   "language": "python",
# META   "language_group": "synapse_pyspark"
# META }

# CELL ********************

device_final_df = device_df.drop(col("environment"))

# METADATA ********************

# META {
# META   "language": "python",
# META   "language_group": "synapse_pyspark"
# META }

# CELL ********************

display(device_final_df.limit(5))

# METADATA ********************

# META {
# META   "language": "python",
# META   "language_group": "synapse_pyspark"
# META }

# MARKDOWN ********************

# #### paso 3: Escribir datos en el Lakehouse"lh_gold"

# CELL ********************

merge_condition = "tgt.device_id = src.device_id AND tgt.file_date = src.file_date"
# merge_delta_lake(device_final_df, "lh_gold","dbo","fact_device", gold_folder_path, merge_condition, "file_date")

merge_delta_lake(device_final_df, "fact_device", merge_condition, "file_date")

# METADATA ********************

# META {
# META   "language": "python",
# META   "language_group": "synapse_pyspark"
# META }

# CELL ********************

# MAGIC %%sql
# MAGIC SELECT file_date, count(1) from fact_device
# MAGIC GROUP BY file_date

# METADATA ********************

# META {
# META   "language": "sparksql",
# META   "language_group": "synapse_pyspark"
# META }

# CELL ********************


# METADATA ********************

# META {
# META   "language": "python",
# META   "language_group": "synapse_pyspark"
# META }
