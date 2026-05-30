import re

with open('/app/Trino/Trino.pq', 'r') as f:
    content = f.read()

# We want to fetch the token only once in TrinoImpl and pass the `token` string downwards instead of `OIDCDiscoveryEndpoint`.
# Wait, actually, TrinoImpl is the top level entrypoint. Let's see how we can fetch the token once.

# First, let's revert all the OIDCDiscoveryEndpoint parameters inside PostStatement* and GetPage, GetAllPagesByNextLink, TrinoNavTable, etc.
# And instead pass `token` as an optional parameter down. Wait, we can just pass an `optional M2MToken as text` parameter downwards.
# Let's replace `OIDCDiscoveryEndpoint` with `M2MToken` in all those helper functions.

content = content.replace(
    'optional OIDCDiscoveryEndpoint as text',
    'optional M2MToken as text'
)

# Also update the columns in NavigationTable
content = content.replace(
    'OIDCDiscoveryEndpointColumn = Table.AddColumn(TargetResultSizeColumn,"OIDCDiscoveryEndpoint", each OIDCDiscoveryEndpoint),',
    'M2MTokenColumn = Table.AddColumn(TargetResultSizeColumn,"M2MToken", each M2MToken),'
)
content = content.replace(
    'OIDCDiscoveryEndpointColumn',
    'M2MTokenColumn'
)
content = content.replace(
    '"OIDCDiscoveryEndpoint"',
    '"M2MToken"'
)
content = content.replace(
    'OIDCDiscoveryEndpoint',
    'M2MToken'
)

# Now fix the top level entry `TrinoImpl` which STILL receives `optional OIDCDiscoveryEndpoint as text` as input from user!
# Oh wait, the parameter exposed to the user should be OIDCDiscoveryEndpoint!
# So TrinoImpl should take `optional OIDCDiscoveryEndpoint as text`.
content = content.replace(
    'TrinoImpl = (Host as text, Port as number, optional Catalog as text, optional User as text, optional Retries as number, optional Timeout as number, optional TargetResultSize as number, optional SQLQuery as text, optional M2MToken as text) as table =>',
    'TrinoImpl = (Host as text, Port as number, optional Catalog as text, optional User as text, optional Retries as number, optional Timeout as number, optional TargetResultSize as number, optional SQLQuery as text, optional OIDCDiscoveryEndpoint as text) as table =>'
)

# And inside TrinoImpl, we generate the M2MToken:
impl_logic_old = '''    let
        Url = Http & Host & ":" & Number.ToText(Port) & "/v1/statement",
        Table =
            if SQLQuery is null then
                TrinoNavTable(Url, Catalog, User, Retries, Timeout, TargetResultSize, M2MToken)
            else
                let
                    User = if User is null and (Extension.CurrentCredential()[AuthenticationKind]?) <> "UsernamePassword" then DefaultUser
                        else if User is null and (Extension.CurrentCredential()[AuthenticationKind]?) = "UsernamePassword" then Extension.CurrentCredential()[Username]
                        else User,'''

impl_logic_new = '''    let
        Url = Http & Host & ":" & Number.ToText(Port) & "/v1/statement",
        M2MToken = if (OIDCDiscoveryEndpoint <> null and Extension.CurrentCredential()[AuthenticationKind]? = "UsernamePassword") then GetM2MToken(OIDCDiscoveryEndpoint, Extension.CurrentCredential()[Username], Extension.CurrentCredential()[Password]) else null,
        Table =
            if SQLQuery is null then
                TrinoNavTable(Url, Catalog, User, Retries, Timeout, TargetResultSize, M2MToken)
            else
                let
                    User = if User is null and (Extension.CurrentCredential()[AuthenticationKind]?) <> "UsernamePassword" then DefaultUser
                        else if User is null and (Extension.CurrentCredential()[AuthenticationKind]?) = "UsernamePassword" then Extension.CurrentCredential()[Username]
                        else User,'''

content = content.replace(impl_logic_old, impl_logic_new)

# Now, in the helper functions, they are using M2MToken as an argument.
# But they have code like:
# authHeaders = if (M2MToken <> null and Extension.CurrentCredential()[AuthenticationKind]? = "UsernamePassword") then let clientId = Extension.CurrentCredential()[Username], clientSecret = Extension.CurrentCredential()[Password], token = GetM2MToken(M2MToken, clientId, clientSecret) in [#"X-Trino-User" = User, #"Authorization" = "Bearer " & token] else [#"X-Trino-User" = User],

content = re.sub(
    r'authHeaders = if \(M2MToken <> null and Extension\.CurrentCredential\(\)\[AuthenticationKind\]\? = "UsernamePassword"\) then let clientId = Extension\.CurrentCredential\(\)\[Username\], clientSecret = Extension\.CurrentCredential\(\)\[Password\], token = GetM2MToken\(M2MToken, clientId, clientSecret\) in \[#"X-Trino-User" = User, #"Authorization" = "Bearer " & token\] else \[#"X-Trino-User" = User\],',
    r'authHeaders = if (M2MToken <> null) then [#"X-Trino-User" = User, #"Authorization" = "Bearer " & M2MToken] else [#"X-Trino-User" = User],',
    content
)

content = re.sub(
    r'manualCredentials = if \(M2MToken <> null and Extension\.CurrentCredential\(\)\[AuthenticationKind\]\? = "UsernamePassword"\) then true else null,',
    r'manualCredentials = if (M2MToken <> null) then true else null,',
    content
)

with open('/app/Trino/Trino.pq', 'w') as f:
    f.write(content)
