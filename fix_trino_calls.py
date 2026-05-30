import re

with open('/app/Trino/Trino.pq', 'r') as f:
    content = f.read()

# Update PostStatement* functions to take OIDCDiscoveryEndpoint
old_post_statement_catalogs = 'PostStatementCatalogs = (url as text, optional Catalog as text, optional User as text, optional Retries as number, optional Timeout as number, optional TargetResultSize as number) as table =>'
new_post_statement_catalogs = 'PostStatementCatalogs = (url as text, optional Catalog as text, optional User as text, optional Retries as number, optional Timeout as number, optional TargetResultSize as number, optional OIDCDiscoveryEndpoint as text) as table =>'
content = content.replace(old_post_statement_catalogs, new_post_statement_catalogs)

old_post_statement_schemas = 'PostStatementSchemas = (url as text, Catalog as text, User as text, Retries as number, Timeout as number, optional TargetResultSize as number) as table  =>'
new_post_statement_schemas = 'PostStatementSchemas = (url as text, Catalog as text, User as text, Retries as number, Timeout as number, optional TargetResultSize as number, optional OIDCDiscoveryEndpoint as text) as table  =>'
content = content.replace(old_post_statement_schemas, new_post_statement_schemas)

old_post_statement_tables = 'PostStatementTables = (url as text, Catalog as text, Schema as text, User as text, Retries as number, Timeout as number, optional TargetResultSize as number) as table  =>'
new_post_statement_tables = 'PostStatementTables = (url as text, Catalog as text, Schema as text, User as text, Retries as number, Timeout as number, optional TargetResultSize as number, optional OIDCDiscoveryEndpoint as text) as table  =>'
content = content.replace(old_post_statement_tables, new_post_statement_tables)

old_post_statement_query_tables = 'PostStatementQueryTables = (url as text, Catalog as text, schema as text, table as text, User as text, Retries as number, Timeout as number, optional TargetResultSize as number) as table  =>'
new_post_statement_query_tables = 'PostStatementQueryTables = (url as text, Catalog as text, schema as text, table as text, User as text, Retries as number, Timeout as number, optional TargetResultSize as number, optional OIDCDiscoveryEndpoint as text) as table  =>'
content = content.replace(old_post_statement_query_tables, new_post_statement_query_tables)

old_post_statement_query_column_names = 'PostStatementQueryColumnNames = (url as text, Catalog as text, schema as text, table as text, User as text, Retries as number, Timeout as number, optional TargetResultSize as number) as table  =>'
new_post_statement_query_column_names = 'PostStatementQueryColumnNames = (url as text, Catalog as text, schema as text, table as text, User as text, Retries as number, Timeout as number, optional TargetResultSize as number, optional OIDCDiscoveryEndpoint as text) as table  =>'
content = content.replace(old_post_statement_query_column_names, new_post_statement_query_column_names)

old_get_all_pages = 'GetAllPagesByNextLink = (url as text, User as text, Retries as number, Timeout as number, optional TargetResultSize as number) as table =>'
new_get_all_pages = 'GetAllPagesByNextLink = (url as text, User as text, Retries as number, Timeout as number, optional TargetResultSize as number, optional OIDCDiscoveryEndpoint as text) as table =>'
content = content.replace(old_get_all_pages, new_get_all_pages)

old_get_page = 'GetPage = (url as text, User as text, Retries as number, Timeout as number, optional TargetResultSize as number) as table =>'
new_get_page = 'GetPage = (url as text, User as text, Retries as number, Timeout as number, optional TargetResultSize as number, optional OIDCDiscoveryEndpoint as text) as table =>'
content = content.replace(old_get_page, new_get_page)

# In GetPage, need to update its call:
content = content.replace(
    'page = if (nextLink <> null) then GetPage(nextLink,User,Retries,Timeout,TargetResultSize) else null',
    'page = if (nextLink <> null) then GetPage(nextLink,User,Retries,Timeout,TargetResultSize,OIDCDiscoveryEndpoint) else null'
)
content = content.replace(
    'GetAllPagesByNextLink(body[nextUri],User,Retries,Timeout,TargetResultSize)',
    'GetAllPagesByNextLink(body[nextUri],User,Retries,Timeout,TargetResultSize,OIDCDiscoveryEndpoint)'
)

# Also update TrinoNavTable, TrinoNavTableLeaf, TrinoNavTableLeafLeaf to pass OIDCDiscoveryEndpoint
content = content.replace(
    'TrinoNavTableLeaf = (url as text, Catalog as text, optional User as text, optional Retries as number, optional Timeout as number, optional TargetResultSize as number)  as table =>',
    'TrinoNavTableLeaf = (url as text, Catalog as text, optional User as text, optional Retries as number, optional Timeout as number, optional TargetResultSize as number, optional OIDCDiscoveryEndpoint as text)  as table =>'
)
content = content.replace(
    'TrinoNavTableLeafLeaf = (url as text, Catalog as text, Schema as text, optional User as text, optional Retries as number, optional Timeout as number, optional TargetResultSize as number)  as table =>',
    'TrinoNavTableLeafLeaf = (url as text, Catalog as text, Schema as text, optional User as text, optional Retries as number, optional Timeout as number, optional TargetResultSize as number, optional OIDCDiscoveryEndpoint as text)  as table =>'
)

# Update internal calls to PostStatementCatalogs, PostStatementSchemas, PostStatementTables, PostStatementQueryTables inside Nav tables
content = content.replace(
    'catalogs = PostStatementCatalogs(url,Catalog,User,Retries,Timeout,TargetResultSize),',
    'catalogs = PostStatementCatalogs(url,Catalog,User,Retries,Timeout,TargetResultSize,OIDCDiscoveryEndpoint),'
)
content = content.replace(
    'schemas = PostStatementSchemas(url,Catalog,User,Retries,Timeout,TargetResultSize),',
    'schemas = PostStatementSchemas(url,Catalog,User,Retries,Timeout,TargetResultSize,OIDCDiscoveryEndpoint),'
)
content = content.replace(
    'tables = PostStatementTables(url,Catalog,Schema,User,Retries,Timeout,TargetResultSize),',
    'tables = PostStatementTables(url,Catalog,Schema,User,Retries,Timeout,TargetResultSize,OIDCDiscoveryEndpoint),'
)

# And the Nav tables also pass fields via Table.NavigationTableView
# Wait, Table.NavigationTableView gets arguments dynamically from the list of fields. We need to add OIDCDiscoveryEndpoint.
content = content.replace(
    'OIDCDiscoveryEndpointColumn = Table.AddColumn(TargetResultSizeColumn,"OIDCDiscoveryEndpoint", each OIDCDiscoveryEndpoint),',
    '' # Wait, let's just add it correctly below
)

with open('/app/Trino/Trino.pq', 'w') as f:
    f.write(content)
