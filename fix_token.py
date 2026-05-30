import re

with open('/app/Trino/Trino.pq', 'r') as f:
    content = f.read()

get_m2m_token_fn = """
GetM2MToken = (oidcDiscoveryUrl as text, clientId as text, clientSecret as text) as text =>
    let
        // 1. Fetch token_endpoint from OIDC Discovery Endpoint
        oidcResponse = Web.Contents(oidcDiscoveryUrl),
        oidcJson = Json.Document(oidcResponse),
        tokenEndpoint = oidcJson[token_endpoint],

        // 2. Request Token using client credentials
        TokenResponse = Web.Contents(tokenEndpoint, [
            Content = Text.ToBinary(Uri.BuildQueryString([
                grant_type = "client_credentials",
                client_id = clientId,
                client_secret = clientSecret
            ])),
            Headers=[
                #"Content-Type" = "application/x-www-form-urlencoded",
                #"Accept" = "application/json"
            ],
            ManualCredentials = true
        ]),
        TokenJson = Json.Document(TokenResponse),
        AccessToken = TokenJson[access_token]
    in
        AccessToken;

"""

content = content.replace(
    '//////////////////////\n// HELPER FUNCTIONS //\n//////////////////////',
    '//////////////////////\n// HELPER FUNCTIONS //\n//////////////////////\n' + get_m2m_token_fn
)

with open('/app/Trino/Trino.pq', 'w') as f:
    f.write(content)
