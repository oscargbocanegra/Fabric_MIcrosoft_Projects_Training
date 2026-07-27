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

# # Ingestion del archivo "Category.csv"

# MARKDOWN ********************

# ### Paso 1: Leer el archivo CSV usando "DataframeReader" de Spark

# CELL ********************

from pyspark.sql.types import StructField, StructType, IntegerType, StringType

# METADATA ********************

# META {
# META   "language": "python",
# META   "language_group": "synapse_pyspark"
# META }

# CELL ********************

category_schema = StructType(fields=[
    StructField("CategoryID", IntegerType(), False),
    StructField("DeviceCategory", StringType(), True)
])

# METADATA ********************

# META {
# META   "language": "python",
# META   "language_group": "synapse_pyspark"
# META }

# CELL ********************

path =  f"{bronze_foflder_path}/{file_date}/category.csv"

category_df = spark.read \
                .option("header", True) \
                .option("delimiter", ";") \
                .schema(category_schema) \
                .csv(path)

# METADATA ********************

# META {
# META   "language": "python",
# META   "language_group": "synapse_pyspark"
# META }

# MARKDOWN ********************

# ### Paso 2: Cambiar el nombre de las columnas segun lo requerido

# CELL ********************

category_renamed_df = category_df.withColumnRenamed("CategoryID", "category_id") \
                                 .withColumnRenamed("DeviceCategory", "device_category")

# METADATA ********************

# META {
# META   "language": "python",
# META   "language_group": "synapse_pyspark"
# META }

# MARKDOWN ********************

# ### Paso 3: Agregar columnas "ingestion_date" y "environment" al DataFrame

# CELL ********************

category_final_df = add_ingestion_date(category_renamed_df, environment) \
                                    .withColumn("file_date", lit(file_date))

# METADATA ********************

# META {
# META   "language": "python",
# META   "language_group": "synapse_pyspark"
# META }

# MARKDOWN ********************

# ### Paso 4: Esscribir datos en LakeHouse en formato Delta

# CELL ********************

# MAGIC %%sql
# MAGIC DROP TABLE IF EXISTS category

# METADATA ********************

# META {
# META   "language": "sparksql",
# META   "language_group": "synapse_pyspark"
# META }

# CELL ********************

category_final_df.write.format("delta").mode("overwrite").saveAsTable(table_category)

# METADATA ********************

# META {
# META   "language": "python",
# META   "language_group": "synapse_pyspark"
# META }

# CELL ********************

# MAGIC %%sql
# MAGIC SELECT * from category
# MAGIC LIMIT 5;

# METADATA ********************

# META {
# META   "language": "sparksql",
# META   "language_group": "synapse_pyspark"
# META }
