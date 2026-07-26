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
# META           "id": "ed215450-beb6-4ef6-b930-2bbe977199ee"
# META         }
# META       ]
# META     }
# META   }
# META }

# CELL ********************

# MAGIC %%sql
# MAGIC -- create or oreplace temporary view
# MAGIC CREATE OR REPLACE TEMPORARY VIEW bronze_wind_power AS
# MAGIC SELECT * 
# MAGIC FROM WinPowerAnalitics.lh_wind_power_bronze.dbo.wind_power

# METADATA ********************

# META {
# META   "language": "sparksql",
# META   "language_group": "synapse_pyspark"
# META }

# CELL ********************

# MAGIC %%sql
# MAGIC CREATE OR REPLACE TEMPORARY VIEW transformed_wind_power AS
# MAGIC SELECT
# MAGIC     production_id,
# MAGIC     date,
# MAGIC     turbine_name,
# MAGIC     capacity,
# MAGIC     location_name,
# MAGIC     latitude,
# MAGIC     region,
# MAGIC     status,
# MAGIC     responsible_department,
# MAGIC     wind_direction,
# MAGIC     ROUND(wind_speed, 2) AS wind_speed,
# MAGIC     ROUND(energy_produced, 2) AS energy_produced,
# MAGIC     DAY(date) AS day,
# MAGIC     MONTH(date) AS month,
# MAGIC     QUARTER(date) AS quarter,
# MAGIC     YEAR(date) AS year,
# MAGIC     REGEXP_REPLACE(time, '-', ':') AS time,
# MAGIC     CAST(SUBSTRING(time, 1, 2) AS INT) AS hour_of_day,
# MAGIC     CAST(SUBSTRING(time, 4, 2) AS INT) AS minute_of_hour,
# MAGIC     CAST(SUBSTRING(time, 7, 2) AS INT) AS second_of_minute,
# MAGIC     CASE
# MAGIC         WHEN CAST(SUBSTRING(time, 1, 2) AS INT) BETWEEN 5 AND 11 THEN 'Morning'
# MAGIC         WHEN CAST(SUBSTRING(time, 1, 2) AS INT) BETWEEN 12 AND 16 THEN 'Afternoon'
# MAGIC         WHEN CAST(SUBSTRING(time, 1, 2) AS INT) BETWEEN 17 AND 20 THEN 'Evening'
# MAGIC         ELSE 'Noght'
# MAGIC     END AS time_period
# MAGIC FROM bronze_wind_power


# METADATA ********************

# META {
# META   "language": "sparksql",
# META   "language_group": "synapse_pyspark"
# META }

# CELL ********************

# MAGIC %%sql
# MAGIC -- drop the wind_power table in the silver lakehouse if it exist
# MAGIC DROP TABLE IF EXISTS WinPowerAnalitics.lh_wind_power_silver.dbo.wind_power;

# METADATA ********************

# META {
# META   "language": "sparksql",
# META   "language_group": "synapse_pyspark"
# META }

# CELL ********************

# MAGIC %%sql
# MAGIC -- Create the new wind_power table in silver lakehouse
# MAGIC CREATE TABLE WinPowerAnalitics.lh_wind_power_silver.dbo.wind_power
# MAGIC USING delta
# MAGIC AS
# MAGIC SELECT * FROM transformed_wind_power;

# METADATA ********************

# META {
# META   "language": "sparksql",
# META   "language_group": "synapse_pyspark"
# META }
