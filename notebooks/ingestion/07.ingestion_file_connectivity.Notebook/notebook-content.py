# Fabric notebook source

# METADATA ********************

# META {
# META   "kernel_info": {
# META     "name": "synapse_pyspark"
# META   },
# META   "dependencies": {
# META     "lakehouse": {
# META       "default_lakehouse": "15ecebd5-cfde-4e08-8e7f-20de67bc7036",
# META       "default_lakehouse_name": "lh_silver",
# META       "default_lakehouse_workspace_id": "238170a0-2b5d-44e7-bbf4-11d6911490f6",
# META       "known_lakehouses": [
# META         {
# META           "id": "0e1c6eaf-72d2-46bd-8c84-a9c270f5f1ab"
# META         },
# META         {
# META           "id": "15ecebd5-cfde-4e08-8e7f-20de67bc7036"
# META         }
# META       ]
# META     }
# META   }
# META }

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

# # Ingestion del archivo "connectivity.json"
# 
# #### Paso 1: Leer el archivo JSON  usando "DataframeReader" de Spark

# CELL ********************

from pyspark.sql.types import StructType, StructField, IntegerType, StringType

# METADATA ********************

# META {
# META   "language": "python",
# META   "language_group": "synapse_pyspark"
# META }

# CELL ********************

connectivity_schema = StructType( fields= [
    StructField("ConnectivityID", IntegerType(), False),
    StructField("USB", StringType(), True),
    StructField("USBConnector", StringType(), True),
    StructField("Bluetooth", StringType(), True),
    StructField("NFC", StringType(), True),
    StructField("SIMCardSlot", StringType(), True)
    ])

# METADATA ********************

# META {
# META   "language": "python",
# META   "language_group": "synapse_pyspark"
# META }

# CELL ********************

path =  f"{bronze_foflder_path}/{file_date}/connectivity.json"

connectivity_df = spark.read \
                    .schema(connectivity_schema) \
                    .option("multiline", True) \
                    .json(path)


# METADATA ********************

# META {
# META   "language": "python",
# META   "language_group": "synapse_pyspark"
# META }

# MARKDOWN ********************

# #### Paso 2: Renombrar las columnas "SID", "PlatforM" y añadir las nuevas "ingestion_date" y "environtment"

# CELL ********************

connectivity_with_column_df = add_ingestion_date(connectivity_df, environment) \
                            .withColumnRenamed("ConnectivityID", "connectivity_id") \
                            .withColumnRenamed("USB", "usb") \
                            .withColumnRenamed("USBConnector", "usb_connector") \
                            .withColumnRenamed("Bluetooth", "luetooth") \
                            .withColumnRenamed("NFC", "fc") \
                            .withColumnRenamed("SIMCardSlot", "sim_card_slot")

# METADATA ********************

# META {
# META   "language": "python",
# META   "language_group": "synapse_pyspark"
# META }

# MARKDOWN ********************

# ### Paso 3: Escribir la salida en formato Delta

# CELL ********************

# MAGIC %%sql
# MAGIC DROP TABLE IF EXISTS connectivity

# METADATA ********************

# META {
# META   "language": "sparksql",
# META   "language_group": "synapse_pyspark"
# META }

# CELL ********************

connectivity_with_column_df.write.format("delta").mode("overwrite").saveAsTable(table_connectivity)

# METADATA ********************

# META {
# META   "language": "python",
# META   "language_group": "synapse_pyspark"
# META }

# CELL ********************

# MAGIC %%sql
# MAGIC SELECT * FROM connectivity LIMIT 5;

# METADATA ********************

# META {
# META   "language": "sparksql",
# META   "language_group": "synapse_pyspark"
# META }
