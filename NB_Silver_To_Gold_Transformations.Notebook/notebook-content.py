# Fabric notebook source

# METADATA ********************

# META {
# META   "kernel_info": {
# META     "name": "synapse_pyspark"
# META   },
# META   "dependencies": {
# META     "lakehouse": {
# META       "default_lakehouse": "65c2e49a-0770-460c-8884-98859d69e3a9",
# META       "default_lakehouse_name": "lh_wind_power_silver",
# META       "default_lakehouse_workspace_id": "72b953c8-af36-4642-9f3c-77a89bf45813",
# META       "known_lakehouses": [
# META         {
# META           "id": "65c2e49a-0770-460c-8884-98859d69e3a9"
# META         },
# META         {
# META           "id": "d317d879-0e7a-444e-bd79-1dd480ddab3e"
# META         }
# META       ]
# META     }
# META   }
# META }

# CELL ********************

from pyspark.sql.window import Window
from pyspark.sql.functions import row_number

# METADATA ********************

# META {
# META   "language": "python",
# META   "language_group": "synapse_pyspark"
# META }

# CELL ********************

# Path to wind_power table in Silver Lakehouse
silver_table_path = "abfss://WinPowerAnalitics@onelake.dfs.fabric.microsoft.com/lh_wind_power_silver.Lakehouse/Tables/dbo/wind_power"

# Load the wind_power table into a DataFrame
df = spark.read.format("delta").load(silver_table_path)

# METADATA ********************

# META {
# META   "language": "python",
# META   "language_group": "synapse_pyspark"
# META }

# CELL ********************

# Create the Date Dimension Table
date_dim = df.select("date", "day", "month", "quarter", "year").distinct() \
                .withColumnRenamed("date", "date_id")

# Create the Time Dimension Table
time_dim = df.select("time", "hour_of_day", "minute_of_hour", "second_of_minute", "time_period").distinct() \
                .withColumnRenamed("time", "time_id")

# Create the Turbine Dimension Table
turbine_dim = df.select("turbine_name", "capacity", "location_name", "latitude", "longitude", "region").distinct() \
                .withColumn("turbine_id", row_number().over(Window.orderBy("turbine_name", "capacity", "location_name", "latitude", "longitude", "region")))

# Create the Operational Status Dimension Table
operational_status_dim = df.select("status", "responsible_department").distinct() \
                .withColumn("status_id", row_number().over(Window.orderBy("status", "responsible_department")))

# METADATA ********************

# META {
# META   "language": "python",
# META   "language_group": "synapse_pyspark"
# META }

# CELL ********************

# Join the dimension tables to the original DataFrame
df = df.join(turbine_dim, ["turbine_name", "capacity", "location_name", "latitude", "longitude", "region"], "left") \
        .join(operational_status_dim, ["status", "responsible_department"], "left")

# METADATA ********************

# META {
# META   "language": "python",
# META   "language_group": "synapse_pyspark"
# META }

# CELL ********************

# Create the Fact table
fact_table = df.select("production_id", "date", "time", "turbine_id", "status_id", "wind_speed", "wind_direction", "energy_produced") \
                .withColumnRenamed("date", "date_id") \
                .withColumnRenamed("time", "time_id")

# METADATA ********************

# META {
# META   "language": "python",
# META   "language_group": "synapse_pyspark"
# META }

# CELL ********************

# Paths to the Gold tables
gold_date_dim_path = "abfss://WinPowerAnalitics@onelake.dfs.fabric.microsoft.com/lh_wind_power_gold.Lakehouse/Tables/dbo/dim_date"
gold_time_dim_path = "abfss://WinPowerAnalitics@onelake.dfs.fabric.microsoft.com/lh_wind_power_gold.Lakehouse/Tables/dbo/dim_time"
gold_turbine_dim_path = "abfss://WinPowerAnalitics@onelake.dfs.fabric.microsoft.com/lh_wind_power_gold.Lakehouse/Tables/dbo/dim_turbine"
gold_operational_status_dim_path = "abfss://WinPowerAnalitics@onelake.dfs.fabric.microsoft.com/lh_wind_power_gold.Lakehouse/Tables/dbo/dim_operational_status"
gold_fact_table_path = "abfss://WinPowerAnalitics@onelake.dfs.fabric.microsoft.com/lh_wind_power_gold.Lakehouse/Tables/dbo/fact_wind_power"

# METADATA ********************

# META {
# META   "language": "python",
# META   "language_group": "synapse_pyspark"
# META }

# CELL ********************

# Save the tables in the Gold Lakehouse
date_dim.write.format("delta").mode("overwrite").save(gold_date_dim_path)
time_dim.write.format("delta").mode("overwrite").save(gold_time_dim_path)
turbine_dim.write.format("delta").mode("overwrite").save(gold_turbine_dim_path)
operational_status_dim.write.format("delta").mode("overwrite").save(gold_operational_status_dim_path)
fact_table.write.format("delta").mode("overwrite").save(gold_fact_table_path)

# METADATA ********************

# META {
# META   "language": "python",
# META   "language_group": "synapse_pyspark"
# META }
