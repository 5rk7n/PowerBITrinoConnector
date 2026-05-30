import re

with open('/app/Trino/Trino.pq', 'r') as f:
    content = f.read()

# Fix the incorrect escaping in SQL statements
content = content.replace("\\'", "'")

with open('/app/Trino/Trino.pq', 'w') as f:
    f.write(content)
