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

# # Ingestion del archivo "operation_system.json"

# MARKDOWN ********************

# ### Paso 1: Leer el archivo JSON  usando "DataframeReader" de Spark

# CELL ********************

from pyspark.sql.types import StructType, StructField, IntegerType, StringType

# METADATA ********************

# META {
# META   "language": "python",
# META   "language_group": "synapse_pyspark"
# META }

# CELL ********************

op_system_schema = StructType( fields= [
    StructField("OSID", IntegerType(), False),
    StructField("Platform", StringType(), True),
    StructField("OperatingSystem", StringType(), True),
    StructField("SoftwareExtras", StringType(), True)
    ])

# METADATA ********************

# META {
# META   "language": "python",
# META   "language_group": "synapse_pyspark"
# META }

# CELL ********************

path =  f"{bronze_foflder_path}/{file_date}/operationg_system.json"

op_system_df = spark.read \
                    .schema(op_system_schema) \
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

op_system_with_column_df = add_ingestion_date(op_system_df, environment) \
                            .withColumnRenamed("OSID", "os_id") \
                            .withColumnRenamed("Platfor", "platform")

# METADATA ********************

# META {
# META   "language": "python",
# META   "language_group": "synapse_pyspark"
# META }

# MARKDOWN ********************

# ### Paso 3: Eliminar columnas no deseadas del DataFrame

# CELL ********************

from pyspark.sql.functions import col

op_system_final_df = op_system_with_column_df.drop(col("OperatingSystem"), col("SoftwareExtras"))

# METADATA ********************

# META {
# META   "language": "python",
# META   "language_group": "synapse_pyspark"
# META }

# MARKDOWN ********************

# #### Paso 4: Escribir la salida en formato Delta

# CELL ********************

# MAGIC %%sql
# MAGIC DROP TABLE IF EXISTS operating_system

# METADATA ********************

# META {
# META   "language": "sparksql",
# META   "language_group": "synapse_pyspark"
# META }

# CELL ********************

op_system_final_df.write.format("delta").mode("overwrite").saveAsTable(table_operating_system)

# METADATA ********************

# META {
# META   "language": "python",
# META   "language_group": "synapse_pyspark"
# META }

# CELL ********************

# MAGIC %%sql
# MAGIC SELECT * FROM operating_system LIMIT 5;

# METADATA ********************

# META {
# META   "language": "sparksql",
# META   "language_group": "synapse_pyspark"
# META }
