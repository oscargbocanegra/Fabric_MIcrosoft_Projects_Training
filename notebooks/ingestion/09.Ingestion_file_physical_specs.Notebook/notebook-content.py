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

# # Ingestion del archivo "physical_specs.json"
# #### Paso 1: Leer el archivo CSV usando "DataframeReader" de Spark

# CELL ********************

from pyspark.sql.types import StructField, StructType, IntegerType, StringType

# METADATA ********************

# META {
# META   "language": "python",
# META   "language_group": "synapse_pyspark"
# META }

# CELL ********************

physical_specs_schema = StructType(fields=[
    StructField("PhysicalSpecID", IntegerType(), False),
    StructField("Width", StringType(), True),
    StructField("Height", StringType(), True),
    StructField("Depth", StringType(), True),
    StructField("BoundingVolume", StringType(), True),
    StructField("RAMCapacity", StringType(), True),
    StructField("NonVolatileMemoryCapacity", StringType(), True),
    StructField("CellularController", StringType(), True),
    StructField("NominalBatteryCapacity", StringType(), True),
    StructField("EstimatedBatteryLife", StringType(), True)
])

# METADATA ********************

# META {
# META   "language": "python",
# META   "language_group": "synapse_pyspark"
# META }

# CELL ********************

path =  f"{bronze_foflder_path}/{file_date}/physical_specs"

physical_specs_df = spark.read \
                        .schema(physical_specs_schema) \
                        .option("multiline", True) \
                        .json(path)

# METADATA ********************

# META {
# META   "language": "python",
# META   "language_group": "synapse_pyspark"
# META }

# MARKDOWN ********************

# #### Paso 2: Cambiar el nombre de las columnas segun lo requerido y Agregar columnas "ingestion_date" y "environment" al DataFrame

# CELL ********************

physical_specs_with_columns_df = add_ingestion_date(physical_specs_df, environment) \
                                    .withColumnRenamed("PhysicalSpecID", "physicalSpec_id") \
                                    .withColumnRenamed("Width", "width") \
                                    .withColumnRenamed("Height", "height") \
                                    .withColumnRenamed("Depth", "depth") \
                                    .withColumnRenamed("BoundingVolume", "bounding_volume") \
                                    .withColumnRenamed("Mass", "mass") \
                                    .withColumnRenamed("RAMCapacity", "ram_capacity") \
                                    .withColumnRenamed("NonVolatileMemoryCapacity", "non_volatile_memory_capacity") \
                                    .withColumnRenamed("NominalBatteryCapacity", "nominal_battery_capacity") \
                                    .withColumnRenamed("EstimatedBatteryLife", "estimated_battery_life")

# METADATA ********************

# META {
# META   "language": "python",
# META   "language_group": "synapse_pyspark"
# META }

# MARKDOWN ********************

# #### Paso 3: Eliminar las columnas no deseadas

# CELL ********************

from pyspark.sql.functions import col

physical_specs_drop_df = physical_specs_with_columns_df.drop(col("BoundingVolume"),
                                                            col("NonVolatileMemoryCapacity"),
                                                            col("EstimatedBatteryLife"))

# METADATA ********************

# META {
# META   "language": "python",
# META   "language_group": "synapse_pyspark"
# META }

# MARKDOWN ********************

# #### Paso 4: Agregar columnas file_date, environment 

# CELL ********************

physical_specs_final_df = add_ingestion_date(physical_specs_drop_df, environment) \
                                    .withColumn("file_date", lit(file_date))

# METADATA ********************

# META {
# META   "language": "python",
# META   "language_group": "synapse_pyspark"
# META }

# MARKDOWN ********************

# ### Paso 5: Esscribir datos en LakeHouse en formato Delta

# CELL ********************

# MAGIC %%sql
# MAGIC DROP TABLE IF EXISTS physical_specs

# METADATA ********************

# META {
# META   "language": "sparksql",
# META   "language_group": "synapse_pyspark"
# META }

# CELL ********************

physical_specs_final_df.write.format("delta").mode("overwrite").saveAsTable(table_physical_specs)

# METADATA ********************

# META {
# META   "language": "python",
# META   "language_group": "synapse_pyspark"
# META }

# CELL ********************

# MAGIC %%sql
# MAGIC SELECT * from physical_specs
# MAGIC LIMIT 5;

# METADATA ********************

# META {
# META   "language": "sparksql",
# META   "language_group": "synapse_pyspark"
# META }
