import re

with open('/app/Trino/Trino.pq', 'r') as f:
    content = f.read()

# Update Authentication to replace UsernamePassword with Key type labeled Client ID / Secret?
# The user wants "repurpose the key authentication from username/password to client-id/clien-secret".
# But wait, Key type only has KeyLabel. There's no SecretLabel. We need UsernamePassword to prompt for two fields.
# We will change UsernamePassword labels to say Client ID and Client Secret, if the user leaves them empty we can change resources, but let's change the properties in the array.
content = re.sub(
    r'UsernamePassword = \[\s*UsernameLabel = Extension.LoadString\("UsernameLabelText"\),\s*PasswordLabel = Extension.LoadString\("PasswordLabelText"\)\s*\],',
    'UsernamePassword = [\n            UsernameLabel = "Username / Client ID",\n            PasswordLabel = "Password / Client Secret",\n            Label = "Basic / Client Credentials"\n        ],',
    content
)

with open('/app/Trino/Trino.pq', 'w') as f:
    f.write(content)
