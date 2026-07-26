# Fabric notebook source

# METADATA ********************

# META {
# META   "kernel_info": {
# META     "name": "synapse_pyspark"
# META   },
# META   "dependencies": {
# META     "lakehouse": {
# META       "default_lakehouse": "ed215450-beb6-4ef6-b930-2bbe977199ee",
# META       "default_lakehouse_name": "lh_wind_power_bronze",
# META       "default_lakehouse_workspace_id": "72b953c8-af36-4642-9f3c-77a89bf45813",
# META       "known_lakehouses": [
# META         {
# META           "id": "ed215450-beb6-4ef6-b930-2bbe977199ee"
# META         },
# META         {
# META           "id": "65c2e49a-0770-460c-8884-98859d69e3a9"
# META         }
# META       ]
# META     }
# META   }
# META }

# CELL ********************

from pyspark.sql.functions import round,col, dayofmonth, month, year, to_date, quarter, substring, when,regexp_replace

# METADATA ********************

# META {
# META   "language": "python",
# META   "language_group": "synapse_pyspark"
# META }

# CELL ********************

# Welcome to your new notebook
# Type here in the cell editor to add code!
bronze_table_path = "abfss://WinPowerAnalitics@onelake.dfs.fabric.microsoft.com/lh_wind_power_bronze.Lakehouse/Tables/dbo/wind_power"

# load the wind_power table into a DataFrame
df = spark.read.format("delta").load(bronze_table_path)

# METADATA ********************

# META {
# META   "language": "python",
# META   "language_group": "synapse_pyspark"
# META }

# CELL ********************

# Clean an read data
df_trandformed = (df
.withColumn("wind_speed", round(col("wind_speed"), 2))
.withColumn("energy_produced", round(col("energy_produced"), 2))
.withColumn("day", dayofmonth(col("date")))
.withColumn("month", month(col("date")))
.withColumn("quarter", quarter(col("date")))
.withColumn("year", year(col("date")))
.withColumn("time",regexp_replace(col("time"), "-", ":"))
.withColumn("hour_of_day", substring(col("time"), 1,2).cast("int"))
.withColumn("minute_of_hour", substring(col("time"), 4,2).cast("int"))
.withColumn("second_of_minute", substring(col("time"), 7,2).cast("int"))
.withColumn("time_period", when((col("hour_of_day") >= 5) & (col("hour_of_day") < 12 ), "Morning")
                            .when((col("hour_of_day") >= 12) & (col("hour_of_day") < 17 ), "Afternoon")
                            .when((col("hour_of_day") >= 17) & (col("hour_of_day") < 21 ), "Evening")
                            .otherwise("Night")
    )
)

# METADATA ********************

# META {
# META   "language": "python",
# META   "language_group": "synapse_pyspark"
# META }

# CELL ********************

silver_table_path = "abfss://WinPowerAnalitics@onelake.dfs.fabric.microsoft.com/lh_wind_power_silver.Lakehouse/Tables/dbo/wind_power"

# METADATA ********************

# META {
# META   "language": "python",
# META   "language_group": "synapse_pyspark"
# META }

# CELL ********************

# save the transformed silver table
df_trandformed.write.format("delta").mode("overwrite").save(silver_table_path)

# METADATA ********************

# META {
# META   "language": "python",
# META   "language_group": "synapse_pyspark"
# META }
