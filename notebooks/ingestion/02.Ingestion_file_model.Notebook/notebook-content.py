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

# # Ingestion del archivo "model.csv"
# #### Paso 1: Leer el archivo CSV usando "DataframeReader" de Spark

# CELL ********************

from pyspark.sql.types import StructField, StructType, IntegerType, StringType


# METADATA ********************

# META {
# META   "language": "python",
# META   "language_group": "synapse_pyspark"
# META }

# CELL ********************

model_schema = StructType(fields = [
            StructField("ModelID", IntegerType(), False),
            StructField("CategoryID", IntegerType(), True),
            StructField("Model", StringType(), True),
            StructField("Codename", StringType(), True),
            StructField("GeneraExtras", StringType(), True)
            ])

# METADATA ********************

# META {
# META   "language": "python",
# META   "language_group": "synapse_pyspark"
# META }

# CELL ********************

path = f"{bronze_foflder_path}/{file_date}/model.csv"

model_df = spark.read \
            .option("header", True) \
            .option("delimiter", ";") \
            .schema(model_schema) \
            .csv(path)

# METADATA ********************

# META {
# META   "language": "python",
# META   "language_group": "synapse_pyspark"
# META }

# MARKDOWN ********************

# #### Paso 2: Seleccionar las columnas requeridas

# CELL ********************

from pyspark.sql.functions import col

model_selected_df = model_df.select(
    col("ModelID"),
    col("CategoryID"),
    col("Model"),
    col("Codename")
)

# METADATA ********************

# META {
# META   "language": "python",
# META   "language_group": "synapse_pyspark"
# META }

# MARKDOWN ********************

# #### Paso 3: Cambiar el nombre de las columnas segun lo requerido

# CELL ********************

model_renamed_df = model_selected_df.withColumnRenamed("ModelId", "model_id") \
                                    .withColumnRenamed("CategoryID", "category_id") \
                                    .withColumnRenamed("Model", "model") \
                                    .withColumnRenamed("Codename", "code_name")

# METADATA ********************

# META {
# META   "language": "python",
# META   "language_group": "synapse_pyspark"
# META }

# MARKDOWN ********************

# #### Paso 4: Agregar columnas "ingestion_date", "enviroment"

# CELL ********************

model_final_df = add_ingestion_date(model_renamed_df, environment) \
                                .withColumn("file_date", lit(file_date))

# METADATA ********************

# META {
# META   "language": "python",
# META   "language_group": "synapse_pyspark"
# META }

# MARKDOWN ********************

# #### Paso 5: Escribir lps datps en el "lakehouse" en formato Delta

# CELL ********************

# MAGIC %%sql
# MAGIC DROP TABLE IF EXISTS model

# METADATA ********************

# META {
# META   "language": "sparksql",
# META   "language_group": "synapse_pyspark"
# META }

# CELL ********************

model_final_df.write.format("delta").mode("overwrite").saveAsTable(table_model)

# METADATA ********************

# META {
# META   "language": "python",
# META   "language_group": "synapse_pyspark"
# META }

# CELL ********************

# MAGIC %%sql
# MAGIC SELECT * from model
# MAGIC LIMIT 10;


# METADATA ********************

# META {
# META   "language": "sparksql",
# META   "language_group": "synapse_pyspark"
# META }
