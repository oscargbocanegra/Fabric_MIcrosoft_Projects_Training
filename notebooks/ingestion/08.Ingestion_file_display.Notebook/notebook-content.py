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

# # Ingestion del archivo "display.csv"
# #### Paso 1: Leer el archivo CSV usando "DataframeReader" de Spark

# CELL ********************

from pyspark.sql.types import StructField, StructType, IntegerType, StringType

# METADATA ********************

# META {
# META   "language": "python",
# META   "language_group": "synapse_pyspark"
# META }

# CELL ********************

display_schema = StructType(fields=[
    StructField("DisplayID", IntegerType(), False),
    StructField("DisplayHole", StringType(), True),
    StructField("DisplayDiagonal", StringType(), True),
    StructField("Resolution", StringType(), True),
    StructField("DisplayType", StringType(), True),
    StructField("DisplayColorDepth", StringType(), True),
    StructField("DisplayIllumination", StringType(), True),
    StructField("DisplayRefreshRate", StringType(), True)
])

# METADATA ********************

# META {
# META   "language": "python",
# META   "language_group": "synapse_pyspark"
# META }

# CELL ********************

path =  f"{bronze_foflder_path}/{file_date}/display/display_*.csv"

display_df = spark.read \
                .option("header", True) \
                .option("delimiter", ";") \
                .schema(display_schema) \
                .csv(path)

# METADATA ********************

# META {
# META   "language": "python",
# META   "language_group": "synapse_pyspark"
# META }

# CELL ********************

display(display_df.count())

# METADATA ********************

# META {
# META   "language": "python",
# META   "language_group": "synapse_pyspark"
# META }

# MARKDOWN ********************

# #### Paso 2: Cambiar el nombre de las columnas segun lo requerido y Agregar columnas "ingestion_date" y "environment" al DataFrame

# CELL ********************

display_with_columns_df = add_ingestion_date(display_df, environment) \
                                    .withColumnRenamed("DisplayID", "display_id") \
                                    .withColumnRenamed("DisplayHole", "display_hole") \
                                    .withColumnRenamed("DisplayDiagonal", "diagonal") \
                                    .withColumnRenamed("Resolution", "resolution") \
                                    .withColumnRenamed("DisplayType", "type") \
                                    .withColumnRenamed("DisplayColorDepth", "color_depth") \
                                    .withColumnRenamed("DisplayIllumination", "ilumination") \
                                    .withColumnRenamed("DisplayRefreshRate", "refresh_rate")

# METADATA ********************

# META {
# META   "language": "python",
# META   "language_group": "synapse_pyspark"
# META }

# MARKDOWN ********************

# #### Paso 3: Eliminar las columnas no deseadas

# CELL ********************

from pyspark.sql.functions import col

display_drop_df = display_with_columns_df.drop(col("display_hole"),
                                                col("diagonal"),
                                                col("type"))

# METADATA ********************

# META {
# META   "language": "python",
# META   "language_group": "synapse_pyspark"
# META }

# MARKDOWN ********************

# #### Paso 4: Agregar columnas

# CELL ********************

display_final_df = add_ingestion_date(display_drop_df, environment) \
                                .withColumn("file_date", lit(file_date))

# METADATA ********************

# META {
# META   "language": "python",
# META   "language_group": "synapse_pyspark"
# META }

# MARKDOWN ********************

# #### Paso 5: Esscribir datos en LakeHouse en formato Delta

# CELL ********************

# MAGIC %%sql
# MAGIC DROP TABLE IF EXISTS display

# METADATA ********************

# META {
# META   "language": "sparksql",
# META   "language_group": "synapse_pyspark"
# META }

# CELL ********************

display_final_df.write.format("delta").mode("overwrite").saveAsTable(table_display)


# METADATA ********************

# META {
# META   "language": "python",
# META   "language_group": "synapse_pyspark"
# META }

# CELL ********************

# MAGIC %%sql
# MAGIC SELECT * from display
# MAGIC LIMIT 5;

# METADATA ********************

# META {
# META   "language": "sparksql",
# META   "language_group": "synapse_pyspark"
# META }
