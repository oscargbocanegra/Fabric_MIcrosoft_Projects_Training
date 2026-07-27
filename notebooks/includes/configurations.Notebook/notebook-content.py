# Fabric notebook source

# METADATA ********************

# META {
# META   "kernel_info": {
# META     "name": "synapse_pyspark"
# META   },
# META   "dependencies": {
# META     "lakehouse": {
# META       "default_lakehouse": "0e1c6eaf-72d2-46bd-8c84-a9c270f5f1ab",
# META       "default_lakehouse_name": "lh_bronze",
# META       "default_lakehouse_workspace_id": "238170a0-2b5d-44e7-bbf4-11d6911490f6",
# META       "known_lakehouses": [
# META         {
# META           "id": "0e1c6eaf-72d2-46bd-8c84-a9c270f5f1ab"
# META         }
# META       ]
# META     }
# META   }
# META }

# CELL ********************

# Welcome to your new notebook
# Type here in the cell editor to add code!
bronze_foflder_path = "abfss://SmartDeviceAnaliticsWS@onelake.dfs.fabric.microsoft.com/lh_bronze.Lakehouse/Files/smart-device/bronze-data"
# environment = "Development"
# environment_prod = "Production"
# file_date = "2025-07-07"

table_camera = "camera"
table_brand = "brand"
table_operating_system = "operating_system"
table_connectivity = "connectivity"
table_category = "category"
table_device = "device"
table_model = "model"
table_display = "display"
table_physical_specs = "physical_specs"


# METADATA ********************

# META {
# META   "language": "python",
# META   "language_group": "synapse_pyspark"
# META }

# CELL ********************

gold_folder_path = "abfss://SmartDeviceAnaliticsWS@onelake.dfs.fabric.microsoft.com/lh_gold.Lakehouse/Tables"

# METADATA ********************

# META {
# META   "language": "python",
# META   "language_group": "synapse_pyspark"
# META }
