[StagingDefinition = [Kind = "FastCopy"]]
section Section1;
shared OneDriveConnection = "https://jguwipaed-my.sharepoint.com/personal/schmisu_jguwipaed_onmicrosoft_com/Documents/" meta [IsParameterQuery = true, IsParameterQueryRequired = false, Type = type text];
shared BKPF = "sap_bkpf_document_header.csv" meta [IsParameterQuery = true, IsParameterQueryRequired = false, Type = type text];
[DataDestinations = {[Definition = [Kind = "Reference", QueryName = "load_bkpf_DataDestination", IsNewTarget = true], Settings = [Kind = "Automatic", TypeSettings = [Kind = "Table"]]]}]
shared load_bkpf = let
  Source = Csv.Document(Web.Contents(OneDriveConnection & BKPF), [Delimiter = ",", QuoteStyle = QuoteStyle.None]),
  #"Promoted headers" = Table.PromoteHeaders(Source, [PromoteAllScalars = true])
in
  #"Promoted headers";
shared BSEG = "sap_bseg_line_items.csv" meta [IsParameterQuery = true, IsParameterQueryRequired = false, Type = type text];
shared LFA1 = "sap_lfa1_vendor_master.csv" meta [IsParameterQuery = true, IsParameterQueryRequired = false, Type = type text];
[DataDestinations = {[Definition = [Kind = "Reference", QueryName = "load_bseg_DataDestination", IsNewTarget = true], Settings = [Kind = "Automatic", TypeSettings = [Kind = "Table"]]]}]
shared load_bseg = let
  Query = Csv.Document(Web.Contents(OneDriveConnection & BSEG), [Delimiter = ",", QuoteStyle = QuoteStyle.None]),
  #"Promoted headers" = Table.PromoteHeaders(Query, [PromoteAllScalars = true])
in
  #"Promoted headers";
[DataDestinations = {[Definition = [Kind = "Reference", QueryName = "load_lfa1_DataDestination", IsNewTarget = true], Settings = [Kind = "Automatic", TypeSettings = [Kind = "Table"]]]}]
shared load_lfa1 = let
  Query = Csv.Document(Web.Contents(OneDriveConnection & LFA1), [Delimiter = ",", QuoteStyle = QuoteStyle.None]),
  #"Promoted headers" = Table.PromoteHeaders(Query, [PromoteAllScalars = true])
in
  #"Promoted headers";
shared load_bkpf_DataDestination = let
  Pattern = Lakehouse.Contents([CreateNavigationProperties = false, EnableFolding = false]),
  Navigation_1 = Pattern{[workspaceId = "4401777b-4041-493e-81bc-efb3c0cc5c44"]}[Data],
  Navigation_2 = Navigation_1{[lakehouseId = "f245663a-76de-4021-a6dd-6a806d27f57b"]}[Data],
  TableNavigation = Navigation_2{[Id = "BKPF", ItemKind = "Table"]}?[Data]?
in
  TableNavigation;
shared load_lfa1_DataDestination = let
  Pattern = Lakehouse.Contents([CreateNavigationProperties = false, EnableFolding = false]),
  Navigation_1 = Pattern{[workspaceId = "4401777b-4041-493e-81bc-efb3c0cc5c44"]}[Data],
  Navigation_2 = Navigation_1{[lakehouseId = "f245663a-76de-4021-a6dd-6a806d27f57b"]}[Data],
  TableNavigation = Navigation_2{[Id = "LFA1", ItemKind = "Table"]}?[Data]?
in
  TableNavigation;
shared load_bseg_DataDestination = let
  Pattern = Lakehouse.Contents([CreateNavigationProperties = false, EnableFolding = false]),
  Navigation_1 = Pattern{[workspaceId = "4401777b-4041-493e-81bc-efb3c0cc5c44"]}[Data],
  Navigation_2 = Navigation_1{[lakehouseId = "f245663a-76de-4021-a6dd-6a806d27f57b"]}[Data],
  TableNavigation = Navigation_2{[Id = "BSEG", ItemKind = "Table"]}?[Data]?
in
  TableNavigation;
