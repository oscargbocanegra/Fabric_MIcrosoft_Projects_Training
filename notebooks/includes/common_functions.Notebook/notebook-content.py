# Fabric notebook source

# METADATA ********************

# META {
# META   "kernel_info": {
# META     "name": "synapse_pyspark"
# META   },
# META   "dependencies": {}
# META }

# CELL ********************

from pyspark.sql.functions import current_timestamp, lit

def add_ingestion_date(input_df, environment):
    output_df = input_df.withColumn("ingestion_date", current_timestamp()) \
                        .withColumn("environment", lit(environment))
    return output_df

# METADATA ********************

# META {
# META   "language": "python",
# META   "language_group": "synapse_pyspark"
# META }

# CELL ********************




def merge_delta_lake_cp(input_df, lh_gold_name, schema_name, table_name, gold_folder_path, merge_condition, partition_col):
    from delta.tables import DeltaTable

    if (spark._jsparkSession.catalog().tableExists(f"{lh_gold_name}.{schema_name}.{table_name}")):
        deltaTablePeople = DeltaTable.forPath(spark, f'{gold_folder_path}/{schema_name}/{table_name}')

        deltaTablePeople.alias('tgt') \
        .merge(
            input_df.alias('src'),
            merge_condition
        )\
        .whenMatchedUpdateAll() \
        .whenNotMatchedInsertAll() \
        .execute()

    else:
        input_df.write.format("delta") \
                            .mode("overwrite") \
                            .partitionBy(partition_col) \
                            .saveAsTable(table_name)


# METADATA ********************

# META {
# META   "language": "python",
# META   "language_group": "synapse_pyspark"
# META }

# CELL ********************

def merge_delta_lake(
    input_df,
    full_table_name,
    merge_condition,
    partition_col=None
):
    from delta.tables import DeltaTable

    if spark.catalog.tableExists(full_table_name):
        delta_table = DeltaTable.forName(spark, full_table_name)

        (
            delta_table.alias("tgt")
            .merge(
                input_df.alias("src"),
                merge_condition
            )
            .whenMatchedUpdateAll()
            .whenNotMatchedInsertAll()
            .execute()
        )

    else:
        writer = (
            input_df.write
            .format("delta")
            .mode("overwrite")
        )

        if partition_col:
            writer = writer.partitionBy(partition_col)

        writer.saveAsTable(full_table_name)

# METADATA ********************

# META {
# META   "language": "python",
# META   "language_group": "synapse_pyspark"
# META }
