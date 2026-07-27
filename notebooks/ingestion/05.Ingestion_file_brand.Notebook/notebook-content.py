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

# # Ingestion del archivo "brand.csv"

# MARKDOWN ********************

# #### Paso 1: Leer el archivo JSON usando "DataframeReader" de Spark

# CELL ********************

brand_schema = "BrandID INT, Brand STRING, HardwareDesigner STRING, Manufacturer STRING"

# METADATA ********************

# META {
# META   "language": "python",
# META   "language_group": "synapse_pyspark"
# META }

# CELL ********************

path =  f"{bronze_foflder_path}/{file_date}/brand.json"

brand_df = spark.read \
                .schema(brand_schema) \
                .json(path)

# METADATA ********************

# META {
# META   "language": "python",
# META   "language_group": "synapse_pyspark"
# META }

# MARKDOWN ********************

# #### Paso 2: Agregar columnas "ingestion_date" y "environment"

# CELL ********************

brand_final_df = add_ingestion_date(brand_df, environment) \
                    .withColumnRenamed("BrandID","brand_id") \
                    .withColumnRenamed("Brand","brand") \
                    .withColumnRenamed("HardwareDesigner","hardware_designer") \
                    .withColumnRenamed("Manufacturer","manufacturer")

# METADATA ********************

# META {
# META   "language": "python",
# META   "language_group": "synapse_pyspark"
# META }

# MARKDOWN ********************

# #### Paso 3: Escribir en el lakehouse en formato Delta

# CELL ********************

# MAGIC %%sql
# MAGIC DROP TABLE IF EXISTS brand

# METADATA ********************

# META {
# META   "language": "sparksql",
# META   "language_group": "synapse_pyspark"
# META }

# CELL ********************

brand_final_df.write.format("delta").mode("overwrite").saveAsTable(table_brand)

# METADATA ********************

# META {
# META   "language": "python",
# META   "language_group": "synapse_pyspark"
# META }

# CELL ********************

# MAGIC %%sql
# MAGIC SELECT * FROM brand LIMIT 5

# METADATA ********************

# META {
# META   "language": "sparksql",
# META   "language_group": "synapse_pyspark"
# META }
