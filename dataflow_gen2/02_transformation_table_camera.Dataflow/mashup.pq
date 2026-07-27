[StagingDefinition = [Kind = "FastCopy"]]
section Section1;
[DataDestinations = {[Definition = [Kind = "Reference", QueryName = "camera_DataDestination", IsNewTarget = true], Settings = [Kind = "Manual", AllowCreation = true, ColumnSettings = [Mappings = {[SourceColumnName = "camera_id", DestinationColumnName = "camera_id"], [SourceColumnName = "camera_resolution", DestinationColumnName = "camera_resolution"], [SourceColumnName = "effective_pixel", DestinationColumnName = "effective_pixel"], [SourceColumnName = "image_format", DestinationColumnName = "image_format"], [SourceColumnName = "video_recording", DestinationColumnName = "video_recording"], [SourceColumnName = "flash", DestinationColumnName = "flash"], [SourceColumnName = "ingestion_date", DestinationColumnName = "ingestion_date"]}], DynamicSchema = true, UpdateMethod = [Kind = "Replace"], TypeSettings = [Kind = "Table"]]]}]
shared camera = let
  Source = Lakehouse.Contents([HierarchicalNavigation = null, EnableVorder = true, OutputMetadataRefresh = true]),
  #"Navigation 1" = Source{[workspaceId = "238170a0-2b5d-44e7-bbf4-11d6911490f6"]}[Data],
  #"Navigation 2" = #"Navigation 1"{[lakehouseId = "15ecebd5-cfde-4e08-8e7f-20de67bc7036"]}[Data],
  #"Navigation 3" = #"Navigation 2"{[Id = "camera", ItemKind = "Table"]}[Data],
  #"Removed columns" = Table.RemoveColumns(#"Navigation 3", {"environment"})
in
  #"Removed columns";
shared camera_DataDestination = let
  Pattern = Lakehouse.Contents([CreateNavigationProperties = false, EnableFolding = false, HierarchicalNavigation = true, EnableVorder = true, OutputMetadataRefresh = true]),
  Navigation_1 = Pattern{[workspaceId = "238170a0-2b5d-44e7-bbf4-11d6911490f6"]}[Data],
  Navigation_2 = Navigation_1{[lakehouseId = "07e48deb-91dd-484b-a26f-a3602d709745"]}[Data],
  Navigation_3 = Navigation_2{[Id = "dbo", ItemKind = "Schema"]}[Data],
  TableNavigation = Navigation_3{[Id = "dim_camera", ItemKind = "Table"]}?[Data]?
in
  TableNavigation;
