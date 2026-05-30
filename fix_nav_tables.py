import re

with open('/app/Trino/Trino.pq', 'r') as f:
    content = f.read()

# For TrinoNavTable
content = content.replace(
    'TargetResultSizeColumn = Table.AddColumn(TimeoutColumn,"TargetResultSize", each TargetResultSize),',
    'TargetResultSizeColumn = Table.AddColumn(TimeoutColumn,"TargetResultSize", each TargetResultSize),\n        OIDCDiscoveryEndpointColumn = Table.AddColumn(TargetResultSizeColumn,"OIDCDiscoveryEndpoint", each OIDCDiscoveryEndpoint),'
)
content = content.replace(
    'ItemKindColumn = Table.AddColumn(TargetResultSizeColumn,"ItemKind", each "Database"),',
    'ItemKindColumn = Table.AddColumn(OIDCDiscoveryEndpointColumn,"ItemKind", each "Database"),'
)
content = content.replace(
    'ItemKindColumn = Table.AddColumn(TargetResultSizeColumn,"ItemKind", each "Folder"),',
    'ItemKindColumn = Table.AddColumn(OIDCDiscoveryEndpointColumn,"ItemKind", each "Folder"),'
)
content = content.replace(
    'ItemKindColumn = Table.AddColumn(TargetResultSizeColumn,"ItemKind", each "Table"),',
    'ItemKindColumn = Table.AddColumn(OIDCDiscoveryEndpointColumn,"ItemKind", each "Table"),'
)

# And in Table.NavigationTableView arguments:
content = content.replace(
    '{"Url","NameKey","User","Retries","Timeout","TargetResultSize"}',
    '{"Url","NameKey","User","Retries","Timeout","TargetResultSize","OIDCDiscoveryEndpoint"}'
)
content = content.replace(
    '{"Url","Catalog","NameKey","User","Retries","Timeout","TargetResultSize"}',
    '{"Url","Catalog","NameKey","User","Retries","Timeout","TargetResultSize","OIDCDiscoveryEndpoint"}'
)
content = content.replace(
    '{"Url","Catalog","Schema","Table","User","Retries","Timeout","TargetResultSize"}',
    '{"Url","Catalog","Schema","Table","User","Retries","Timeout","TargetResultSize","OIDCDiscoveryEndpoint"}'
)

with open('/app/Trino/Trino.pq', 'w') as f:
    f.write(content)
