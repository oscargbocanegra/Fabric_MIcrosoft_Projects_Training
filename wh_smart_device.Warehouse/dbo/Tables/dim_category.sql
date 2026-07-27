CREATE TABLE [dbo].[dim_category] (

	[category_id] int NULL, 
	[device_category] varchar(8000) NULL, 
	[ingestion_date] datetime2(6) NULL, 
	[file_date] varchar(2048) NULL
);