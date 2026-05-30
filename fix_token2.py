import re

with open('/app/Trino/Trino.pq', 'r') as f:
    content = f.read()

# Make sure oidcJson accesses the "token_endpoint" correctly, it should be a string key
content = content.replace(
    'tokenEndpoint = oidcJson[token_endpoint],',
    'tokenEndpoint = oidcJson[#"token_endpoint"],'
)
content = content.replace(
    'AccessToken = TokenJson[access_token]',
    'AccessToken = TokenJson[#"access_token"]'
)

with open('/app/Trino/Trino.pq', 'w') as f:
    f.write(content)
