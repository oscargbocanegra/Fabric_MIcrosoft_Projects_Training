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

# MARKDOWN ********************

# **### Ingestion del archivo "device.csv"**

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

# #### Paso 1: Leer el archivo CSV usando "DataframeReader"
# <mark>[Documentacion Spark](https://spark.apache.org/docs/latest/api/python/reference/index.html)</mark>

# CELL ********************

from pyspark.sql.types import StructType, StructField, IntegerType, DateType

# METADATA ********************

# META {
# META   "language": "python",
# META   "language_group": "synapse_pyspark"
# META }

# CELL ********************

device_schema = StructType(fields=
    [
    StructField("DeviceID", IntegerType(), False),
    StructField("BrandID", IntegerType(), True),
    StructField("ModelID", IntegerType(), True),
    StructField("DisplayID", IntegerType(), True),
    StructField("CameraID", IntegerType(), True),
    StructField("ConnectivityID", IntegerType(), True),
    StructField("OSID", IntegerType(), True),
    StructField("PhysicalSpecID", IntegerType(), True),
    StructField("ReleasedYear", IntegerType(), True),
    StructField("ReleasedAnnounced", DateType(), True)
    ] 
)


# METADATA ********************

# META {
# META   "language": "python",
# META   "language_group": "synapse_pyspark"
# META }

# CELL ********************

#path = "Files/smart-device/bronze-data/2025-07-07/device.csv"
path =  f"{bronze_foflder_path}/{file_date}/device.csv"

device_df = spark.read \
            .option("header", True) \
            .schema(device_schema) \
            .csv(path)

# METADATA ********************

# META {
# META   "language": "python",
# META   "language_group": "synapse_pyspark"
# META }

# CELL ********************

# device_df.printSchema()

# METADATA ********************

# META {
# META   "language": "python",
# META   "language_group": "synapse_pyspark"
# META }

# MARKDOWN ********************

# ### Paso 2: Seleccionar las columnas Requeridas

# CELL ********************

# Opcion 1 para seleccionar columnas de un DataFrame

device_selected_df = device_df.select("DeviceID","BrandID","ModelID","DisplayID","CameraID","ConnectivityID","OSID","PhysicalSpecID","ReleasedAnnounced")

# display(device_selected_df.limit(10))

# METADATA ********************

# META {
# META   "language": "python",
# META   "language_group": "synapse_pyspark"
# META }

# CELL ********************

# Opcion 2 para seleccionar columnas de un DataFrame

device_selected_df = device_df.select( \
                        device_df.DeviceID,
                        device_df.BrandID,
                        device_df.ModelID,
                        device_df.DisplayID,
                        device_df.CameraID,
                        device_df.ConnectivityID,
                        device_df.OSID,
                        device_df.PhysicalSpecID,
                        device_df.ReleasedAnnounced)

# display(device_selected_df.limit(10))

# METADATA ********************

# META {
# META   "language": "python",
# META   "language_group": "synapse_pyspark"
# META }

# CELL ********************

# Opcion 3 para seleccionar columnas de un DataFrame

device_selected_df = device_df.select( \
                    device_df["DeviceID"],
                    device_df["BrandID"],
                    device_df["ModelID"],
                    device_df["DisplayID"],
                    device_df["CameraID"],
                    device_df["ConnectivityID"],
                    device_df["OSID"],
                    device_df["PhysicalSpecID"],
                    device_df["ReleasedAnnounced"])

# display(device_selected_df.limit(10))

# METADATA ********************

# META {
# META   "language": "python",
# META   "language_group": "synapse_pyspark"
# META }

# CELL ********************

# Opcion 4 para seleccionar columnas de un DataFrame
from pyspark.sql.functions import col

device_selected_df = device_df.select( \
                    col("DeviceID"),
                    col("BrandID"),
                    col("ModelID"),
                    col("DisplayID"),
                    col("CameraID"),
                    col("ConnectivityID"),
                    col("OSID"),
                    col("PhysicalSpecID"),
                    col("ReleasedAnnounced"))

# display(device_selected_df.limit(10))

# METADATA ********************

# META {
# META   "language": "python",
# META   "language_group": "synapse_pyspark"
# META }

# MARKDOWN ********************

# ### Paso 3: Cambiar el nombre de las columnas segun lo requerido

# CELL ********************

# Opcion 1 para renombrar columnas

device_renamed_df = device_selected_df \
                    .withColumnRenamed("DeviceID", "device_id") \
                    .withColumnRenamed("BrandID", "brand_id") \
                    .withColumnRenamed("ModelID", "model_id") \
                    .withColumnRenamed("DisplayID", "display_id") \
                    .withColumnRenamed("CameraID", "camera_id") \
                    .withColumnRenamed("ConnectivityID", "connectivity_id") \
                    .withColumnRenamed("OSID", "os_id") \
                    .withColumnRenamed("PhysicalSpecID", "PhysicalSpec_id") \
                    .withColumnRenamed("ReleasedAnnounced", "released_announced")

# METADATA ********************

# META {
# META   "language": "python",
# META   "language_group": "synapse_pyspark"
# META }

# CELL ********************

# Opcion 2 para renombrar columnas

device_renamed2_df = device_selected_df \
                    .withColumnsRenamed({
                        "DeviceID":"device_id",
                        "BrandID":"brand_id",
                        "ModelID":"model_id",
                        "DisplayID":"display_id",
                        "CameraID":"camera_id",
                        "ConnectivityID":"connectivity_id",
                        "OSID":"os_id",
                        "PhysicalSpecID":"PhysicalSpec_id",
                        "ReleasedAnnounced":"released_announced"})

# METADATA ********************

# META {
# META   "language": "python",
# META   "language_group": "synapse_pyspark"
# META }

# MARKDOWN ********************

# ### Paso 5: Agregar columnas "ingestion_date" y "environment"

# CELL ********************

# Opcion 1 para agregar columnas
device_final_df = add_ingestion_date(device_renamed_df, environment) \
                            .withColumn("file_date", lit(file_date))


# Opcion 2 para agregar columnas

# from pyspark.sql.functions import current_timestamp, lit
# device_final2_df = device_renamed_df \
#                         .withColumns( {"ingestion_date":current_timestamp(),
#                                         "environment":lit(environment_dev)})

# METADATA ********************

# META {
# META   "language": "python",
# META   "language_group": "synapse_pyspark"
# META }

# MARKDOWN ********************

# ### Paso 5: Escribir los datos en el "lakehouse" en formato "Delta"

# CELL ********************

# MAGIC %%sql
# MAGIC DROP TABLE IF EXISTS device

# METADATA ********************

# META {
# META   "language": "sparksql",
# META   "language_group": "synapse_pyspark"
# META }

# CELL ********************

device_final_df.write.format("delta").mode("overwrite").saveAsTable(table_device)

# METADATA ********************

# META {
# META   "language": "python",
# META   "language_group": "synapse_pyspark"
# META }

# CELL ********************

# MAGIC %%sql
# MAGIC SELECT * from device
# MAGIC LIMIT 10;

# METADATA ********************

# META {
# META   "language": "sparksql",
# META   "language_group": "synapse_pyspark"
# META }
