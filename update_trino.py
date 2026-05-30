import re

with open('/app/Trino/Trino.pq', 'r') as f:
    content = f.read()

# 1. Update TrinoType definition
old_trinotype = r'''    optional SQLQuery as \(type text meta \[
        DataSource\.Path = false,
        Documentation\.FieldCaption = "SQL Query",
        Documentation\.FieldDescription = "The SQL query you want to execute to retrieve data\.",
        Documentation\.SampleValues = \{"select custkey,name from tpch\.sf1\.customer"\},
        Formatting\.IsMultiLine = true
    \]\)
    \)
    as table meta \['''

new_trinotype = '''    optional SQLQuery as (type text meta [
        DataSource.Path = false,
        Documentation.FieldCaption = "SQL Query",
        Documentation.FieldDescription = "The SQL query you want to execute to retrieve data.",
        Documentation.SampleValues = {"select custkey,name from tpch.sf1.customer"},
        Formatting.IsMultiLine = true
    ]),
    optional OIDCDiscoveryEndpoint as (type text meta [
        DataSource.Path = false,
        Documentation.FieldCaption = "OIDC Discovery Endpoint",
        Documentation.FieldDescription = "OIDC Discovery Endpoint for Client Credentials (m2m) authentication. If provided, Basic Auth credentials are used as Client ID and Client Secret.",
        Documentation.SampleValues = {"https://idp.example.com/.well-known/openid-configuration"}
    ])
    )
    as table meta ['''

content = re.sub(old_trinotype, new_trinotype, content)

# 2. Update TrinoImpl signature
content = content.replace(
    'TrinoImpl = (Host as text, Port as number, optional Catalog as text, optional User as text, optional Retries as number, optional Timeout as number, optional TargetResultSize as number, optional SQLQuery as text) as table =>',
    'TrinoImpl = (Host as text, Port as number, optional Catalog as text, optional User as text, optional Retries as number, optional Timeout as number, optional TargetResultSize as number, optional SQLQuery as text, optional OIDCDiscoveryEndpoint as text) as table =>'
)

# 3. Update TrinoImpl call to TrinoNavTable
content = content.replace(
    'TrinoNavTable(Url, Catalog, User, Retries, Timeout, TargetResultSize)',
    'TrinoNavTable(Url, Catalog, User, Retries, Timeout, TargetResultSize, OIDCDiscoveryEndpoint)'
)

with open('/app/Trino/Trino.pq', 'w') as f:
    f.write(content)
