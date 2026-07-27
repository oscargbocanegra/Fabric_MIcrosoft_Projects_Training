CREATE TABLE [dbo].[dim_physical_spects] (

	[physicalSpec_id] int NULL, 
	[width] varchar(8000) NULL, 
	[height] varchar(8000) NULL, 
	[depth] varchar(8000) NULL, 
	[bounding_volume] varchar(8000) NULL, 
	[ram_capacity] varchar(8000) NULL, 
	[non_volatile_memory_capacity] varchar(8000) NULL, 
	[CellularController] varchar(8000) NULL, 
	[nominal_battery_capacity] varchar(8000) NULL, 
	[estimated_battery_life] varchar(8000) NULL, 
	[ingestion_date] datetime2(6) NULL, 
	[file_date] varchar(2048) NULL
);