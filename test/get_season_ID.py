import gzip
import json
import os
import urllib.request
from chicken_dinner.pubgapi import PUBG

req = urllib.request.Request(
    url='https://api.pubg.com/shards/steam/seasons',
    headers={
        'Authorization': f'Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJqdGkiOiI2NzNlZGFhMC1hOWZlLTAxM2EtY2I4Ni0wMTM2YWI5NGY3N2IiLCJpc3MiOiJnYW1lbG9ja2VyIiwiaWF0IjoxNjUxMjQ1ODc2LCJwdWIiOiJibHVlaG9sZSIsInRpdGxlIjoicHViZyIsImFwcCI6ImZyb3plbmRvZyJ9.mdDyb3P1KCBcNIk5xKeu7B7IWOIIaWpAc9JKL7TGyiY',
        'Accept': 'application/vnd.api+json'
    }
)

file_name = f'seasonID.json'
file_path = os.path.join('./seasonID', file_name)
with urllib.request.urlopen(req) as response, open(file_path, 'w') as write_file:
    json_data = json.loads(
        # gzip.decompress(response.read())
        response.read()
    )
    write_file.write(
        json.dumps(json_data, indent=4)
    )
    print('saved.')