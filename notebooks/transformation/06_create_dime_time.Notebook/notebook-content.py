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
# META         }
# META       ]
# META     }
# META   }
# META }

# MARKDOWN ********************

# ### Crear la Dimension "Time"

# MARKDOWN ********************

# #### Paso 1: Leer la tabla de hechos "fact_device" usando "spark.sql"

# CELL ********************

time_df = spark.sql("SELECT * FROM lh_gold.dbo.fact_device")

# METADATA ********************

# META {
# META   "language": "python",
# META   "language_group": "synapse_pyspark"
# META }

# CELL ********************

display(time_df.limit(10))

# METADATA ********************

# META {
# META   "language": "python",
# META   "language_group": "synapse_pyspark"
# META }

# MARKDOWN ********************

# #### Paso 2: Seleccionar la columna "release_announces"

# CELL ********************

from pyspark.sql.functions import col

time_selected_df = time_df.select(col("released_announced"))
display(time_selected_df.limit(5))

# METADATA ********************

# META {
# META   "language": "python",
# META   "language_group": "synapse_pyspark"
# META }

# MARKDOWN ********************

# #### Paso 3: Eliminar valores duplicados y hacer un orden ascendente

# CELL ********************

time_dup_and_order = time_selected_df.drop_duplicates(["released_announced"]) \
                                        .sort("released_announced", ascending = True)

display(time_dup_and_order.limit(5))

# METADATA ********************

# META {
# META   "language": "python",
# META   "language_group": "synapse_pyspark"
# META }

# MARKDOWN ********************

# #### Paso 4: cambiar el nombre de la columna "released_announced" a "date"

# CELL ********************

time_renamed = time_dup_and_order.withColumnRenamed("released_announced", "date")
display(time_renamed.limit(5))

# METADATA ********************

# META {
# META   "language": "python",
# META   "language_group": "synapse_pyspark"
# META }

# MARKDOWN ********************

# #### Paso 5: agregar columnas de "Time Intelligence" a la Dimencion "Time"

# CELL ********************

from pyspark.sql.functions import year, month, dayofmonth, date_format, quarter, concat, lit

time_final_df = time_renamed.withColumn("year", year("date")) \
                            .withColumn("month", month("date")) \
                            .withColumn("day", dayofmonth("date")) \
                            .withColumn("month_name", date_format("date", "MMMM")) \
                            .withColumn("day_name", date_format("date", "EEEE")) \
                            .withColumn("quarter", concat(lit("Q"), quarter("date")))

# METADATA ********************

# META {
# META   "language": "python",
# META   "language_group": "synapse_pyspark"
# META }

# CELL ********************

display(time_final_df.limit(10))

# METADATA ********************

# META {
# META   "language": "python",
# META   "language_group": "synapse_pyspark"
# META }

# MARKDOWN ********************

# #### Paso 6: Escribir los datos en el lh_gold

# CELL ********************

time_final_df.write.format("delta") \
                .mode("overwrite") \
                .saveAsTable("dim_time")

# METADATA ********************

# META {
# META   "language": "python",
# META   "language_group": "synapse_pyspark"
# META }

# CELL ********************

# MAGIC %%sql
# MAGIC SELECT * FROM dim_time;

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
