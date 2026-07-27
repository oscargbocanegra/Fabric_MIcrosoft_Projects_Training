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

# # Ingestion del archivo "camera.json"

# MARKDOWN ********************

# ### Paso 1: Leer el archivo JSON usando "DataframeReader" de Spark

# CELL ********************

camera_schema = "CameraID INT, CameraResolution STRING, NumberofEffectivePixel STRING, \
                Aperture STRING, Zoom STRING, RecordableImageFormat STRING, \
                VideoRecording STRING, Flash STRING"

# METADATA ********************

# META {
# META   "language": "python",
# META   "language_group": "synapse_pyspark"
# META }

# CELL ********************

path =  f"{bronze_foflder_path}/{file_date}/camera.json"

camera_df = spark.read \
                .schema(camera_schema) \
                .json(path)

# METADATA ********************

# META {
# META   "language": "python",
# META   "language_group": "synapse_pyspark"
# META }

# MARKDOWN ********************

# ### Paso 2: Eliminar columnas no deseadas del DataFrame

# CELL ********************

# Opcion 1 para eliminar columnas
camera_droped_df = camera_df.drop("Aperture", "Zoom")

# Opcion 2 para eliminar columnas
# camera_droped2_df = camera_df.drop(camera_df["Aperture"], camera_df["Zoom"])

# Opcion 3 para eliminar columnas
# from pyspark.sql.functions import col
# camera_droped3_df = camera_df.drop(col("Aperture"), col("Zoom"))

# display(camera_droped_df.limit(5))

# METADATA ********************

# META {
# META   "language": "python",
# META   "language_group": "synapse_pyspark"
# META }

# MARKDOWN ********************

# ### Paso 3: Cambiar el nombre de las columnas y añadir "ingestion_date" y "environment"

# CELL ********************

camera_final_df = add_ingestion_date(camera_droped_df, environment) \
                        .withColumnRenamed("CameraID", "camera_id") \
                        .withColumnRenamed("CameraResolution", "camera_resolution") \
                        .withColumnRenamed("NumberOfEffectivePixel", "effective_pixel") \
                        .withColumnRenamed("RecordableImageFormat", "image_format") \
                        .withColumnRenamed("VideoRecording", "video_recording") \
                        .withColumnRenamed("Flash", "flash")


# METADATA ********************

# META {
# META   "language": "python",
# META   "language_group": "synapse_pyspark"
# META }

# MARKDOWN ********************

# ### Paso 4: Escribir la salida en un formato Delta

# CELL ********************

# MAGIC %%sql
# MAGIC DROP TABLE IF EXISTS camera

# METADATA ********************

# META {
# META   "language": "sparksql",
# META   "language_group": "synapse_pyspark"
# META }

# CELL ********************

camera_final_df.write.format("delta").mode("overwrite").saveAsTable(table_camera)

# METADATA ********************

# META {
# META   "language": "python",
# META   "language_group": "synapse_pyspark"
# META }

# CELL ********************

# MAGIC %%sql
# MAGIC SELECT * from camera LIMIT 5

# METADATA ********************

# META {
# META   "language": "sparksql",
# META   "language_group": "synapse_pyspark"
# META }
