import re

with open('/app/Trino/Trino.pq', 'r') as f:
    content = f.read()

# We need to add the Auth headers dynamically. If OIDCDiscoveryEndpoint is present, we will generate a bearer token.

auth_header_logic = """
        authHeaders = if (OIDCDiscoveryEndpoint <> null and Extension.CurrentCredential()[AuthenticationKind]? = "UsernamePassword") then
            let
                clientId = Extension.CurrentCredential()[Username],
                clientSecret = Extension.CurrentCredential()[Password],
                token = GetM2MToken(OIDCDiscoveryEndpoint, clientId, clientSecret)
            in
                [#"X-Trino-User" = User, #"Authorization" = "Bearer " & token]
        else
            [#"X-Trino-User" = User],
        manualCredentials = if (OIDCDiscoveryEndpoint <> null and Extension.CurrentCredential()[AuthenticationKind]? = "UsernamePassword") then true else false,
"""

# Now replace the occurrences of Web.Contents where it passes headers.

# 1. In TrinoImpl for SQL Query execution
content = re.sub(
    r'(\s+)isRetry = if iteration > 0 then true else false,\n(\s+)response = Web\.Contents\(Url,\n(\s+)\[\n(\s+)Content = Text\.ToBinary\(SQLQuery\)\n\s+,Headers = \[#"X-Trino-User" = User\]',
    r'\1isRetry = if iteration > 0 then true else false,\n\1authHeaders = if (OIDCDiscoveryEndpoint <> null and Extension.CurrentCredential()[AuthenticationKind]? = "UsernamePassword") then let clientId = Extension.CurrentCredential()[Username], clientSecret = Extension.CurrentCredential()[Password], token = GetM2MToken(OIDCDiscoveryEndpoint, clientId, clientSecret) in [#"X-Trino-User" = User, #"Authorization" = "Bearer " & token] else [#"X-Trino-User" = User],\n\1manualCredentials = if (OIDCDiscoveryEndpoint <> null and Extension.CurrentCredential()[AuthenticationKind]? = "UsernamePassword") then true else null,\n\2response = Web.Contents(Url,\n\3[\n\4Content = Text.ToBinary(SQLQuery)\n\4,Headers = authHeaders\n\4,ManualCredentials = manualCredentials',
    content
)

# 2. In PostStatementCatalogs
content = re.sub(
    r'(\s+)isRetry = if iteration > 0 then true else false,\n(\s+)response = Web\.Contents\(url,\n(\s+)\[\n(\s+)Content = Text\.ToBinary\("show catalogs"\)\n\s+,Headers = \[#"X-Trino-User" = User\]',
    r'\1isRetry = if iteration > 0 then true else false,\n\1authHeaders = if (OIDCDiscoveryEndpoint <> null and Extension.CurrentCredential()[AuthenticationKind]? = "UsernamePassword") then let clientId = Extension.CurrentCredential()[Username], clientSecret = Extension.CurrentCredential()[Password], token = GetM2MToken(OIDCDiscoveryEndpoint, clientId, clientSecret) in [#"X-Trino-User" = User, #"Authorization" = "Bearer " & token] else [#"X-Trino-User" = User],\n\1manualCredentials = if (OIDCDiscoveryEndpoint <> null and Extension.CurrentCredential()[AuthenticationKind]? = "UsernamePassword") then true else null,\n\2response = Web.Contents(url,\n\3[\n\4Content = Text.ToBinary("show catalogs")\n\4,Headers = authHeaders\n\4,ManualCredentials = manualCredentials',
    content
)

# 3. In PostStatementSchemas
content = re.sub(
    r'(\s+)isRetry = if iteration > 0 then true else false,\n(\s+)response = Web\.Contents\(url,\n(\s+)\[\n(\s+)Content = Text\.ToBinary\("select schema_name from """ & Catalog & """\.information_schema\.schemata"\)\n\s+,Headers = \[#"X-Trino-User" = User\]',
    r'\1isRetry = if iteration > 0 then true else false,\n\1authHeaders = if (OIDCDiscoveryEndpoint <> null and Extension.CurrentCredential()[AuthenticationKind]? = "UsernamePassword") then let clientId = Extension.CurrentCredential()[Username], clientSecret = Extension.CurrentCredential()[Password], token = GetM2MToken(OIDCDiscoveryEndpoint, clientId, clientSecret) in [#"X-Trino-User" = User, #"Authorization" = "Bearer " & token] else [#"X-Trino-User" = User],\n\1manualCredentials = if (OIDCDiscoveryEndpoint <> null and Extension.CurrentCredential()[AuthenticationKind]? = "UsernamePassword") then true else null,\n\2response = Web.Contents(url,\n\3[\n\4Content = Text.ToBinary("select schema_name from """ & Catalog & """.information_schema.schemata")\n\4,Headers = authHeaders\n\4,ManualCredentials = manualCredentials',
    content
)

# 4. In PostStatementTables
content = re.sub(
    r'(\s+)isRetry = if iteration > 0 then true else false,\n(\s+)response = Web\.Contents\(url, \n(\s+)\[\n(\s+)Content = Text\.ToBinary\("select table_name, table_schema from """ & Catalog & """\.information_schema\.tables where table_schema = \'" & Schema & "\'"\)\n\s+,Headers = \[#"X-Trino-User" = User\]',
    r'\1isRetry = if iteration > 0 then true else false,\n\1authHeaders = if (OIDCDiscoveryEndpoint <> null and Extension.CurrentCredential()[AuthenticationKind]? = "UsernamePassword") then let clientId = Extension.CurrentCredential()[Username], clientSecret = Extension.CurrentCredential()[Password], token = GetM2MToken(OIDCDiscoveryEndpoint, clientId, clientSecret) in [#"X-Trino-User" = User, #"Authorization" = "Bearer " & token] else [#"X-Trino-User" = User],\n\1manualCredentials = if (OIDCDiscoveryEndpoint <> null and Extension.CurrentCredential()[AuthenticationKind]? = "UsernamePassword") then true else null,\n\2response = Web.Contents(url, \n\3[\n\4Content = Text.ToBinary("select table_name, table_schema from """ & Catalog & """.information_schema.tables where table_schema = \'" & Schema & "\'")\n\4,Headers = authHeaders\n\4,ManualCredentials = manualCredentials',
    content
)

# 5. In PostStatementQueryColumnNames
content = re.sub(
    r'(\s+)isRetry = if iteration > 0 then true else false,\n(\s+)response = Web\.Contents\(url, \n(\s+)\[\n(\s+)Content = Text\.ToBinary\("select column_name from """ & Catalog & """\.information_schema\.columns where table_schema = \'" & schema & "\' and table_name = \'" & table & "\' order by ordinal_position"\)\n\s+,Headers = \[#"X-Trino-User" = User\]',
    r'\1isRetry = if iteration > 0 then true else false,\n\1authHeaders = if (OIDCDiscoveryEndpoint <> null and Extension.CurrentCredential()[AuthenticationKind]? = "UsernamePassword") then let clientId = Extension.CurrentCredential()[Username], clientSecret = Extension.CurrentCredential()[Password], token = GetM2MToken(OIDCDiscoveryEndpoint, clientId, clientSecret) in [#"X-Trino-User" = User, #"Authorization" = "Bearer " & token] else [#"X-Trino-User" = User],\n\1manualCredentials = if (OIDCDiscoveryEndpoint <> null and Extension.CurrentCredential()[AuthenticationKind]? = "UsernamePassword") then true else null,\n\2response = Web.Contents(url, \n\3[\n\4Content = Text.ToBinary("select column_name from """ & Catalog & """.information_schema.columns where table_schema = \'" & schema & "\' and table_name = \'" & table & "\' order by ordinal_position")\n\4,Headers = authHeaders\n\4,ManualCredentials = manualCredentials',
    content
)

# 6. In PostStatementQueryTables
# Wait, this one has two parts:
# First the column name string (using PostStatementQueryColumnNames).
# Second, the Web.Contents triggering query using column names.
content = re.sub(
    r'(\s+)isRetry = if iteration > 0 then true else false,\n(\s+)response = Web\.Contents\(url, \n(\s+)\[\n(\s+)Content = Text\.ToBinary\("select " & ColumnNameStringSelectString & " from """ & Catalog & """\.""" & schema & """\.""" & table & """"\)\n\s+,Headers = \[#"X-Trino-User" = User\]',
    r'\1isRetry = if iteration > 0 then true else false,\n\1authHeaders = if (OIDCDiscoveryEndpoint <> null and Extension.CurrentCredential()[AuthenticationKind]? = "UsernamePassword") then let clientId = Extension.CurrentCredential()[Username], clientSecret = Extension.CurrentCredential()[Password], token = GetM2MToken(OIDCDiscoveryEndpoint, clientId, clientSecret) in [#"X-Trino-User" = User, #"Authorization" = "Bearer " & token] else [#"X-Trino-User" = User],\n\1manualCredentials = if (OIDCDiscoveryEndpoint <> null and Extension.CurrentCredential()[AuthenticationKind]? = "UsernamePassword") then true else null,\n\2response = Web.Contents(url, \n\3[\n\4Content = Text.ToBinary("select " & ColumnNameStringSelectString & " from """ & Catalog & """.""" & schema & """.""" & table & """")\n\4,Headers = authHeaders\n\4,ManualCredentials = manualCredentials',
    content
)

# 7. In GetPage
content = re.sub(
    r'(\s+)isRetry = if iteration > 0 then true else false,\n(\s+)response = Web\.Contents\(url, \n(\s+)\[\n(\s+)Headers = \[#"X-Trino-User" = User\]',
    r'\1isRetry = if iteration > 0 then true else false,\n\1authHeaders = if (OIDCDiscoveryEndpoint <> null and Extension.CurrentCredential()[AuthenticationKind]? = "UsernamePassword") then let clientId = Extension.CurrentCredential()[Username], clientSecret = Extension.CurrentCredential()[Password], token = GetM2MToken(OIDCDiscoveryEndpoint, clientId, clientSecret) in [#"X-Trino-User" = User, #"Authorization" = "Bearer " & token] else [#"X-Trino-User" = User],\n\1manualCredentials = if (OIDCDiscoveryEndpoint <> null and Extension.CurrentCredential()[AuthenticationKind]? = "UsernamePassword") then true else null,\n\2response = Web.Contents(url, \n\3[\n\4Headers = authHeaders\n\4,ManualCredentials = manualCredentials',
    content
)


with open('/app/Trino/Trino.pq', 'w') as f:
    f.write(content)
