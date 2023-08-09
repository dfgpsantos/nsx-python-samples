import requests

import json

from urllib3.exceptions import InsecureRequestWarning
requests.packages.urllib3.disable_warnings(category=InsecureRequestWarning)

from requests.auth import HTTPBasicAuth

basic = HTTPBasicAuth('admin', 'VMware1!VMware1!')

response = requests.get('https://nsx-41.corp.local/policy/api/v1/infra/segments', auth=basic, verify=False)

print(response.status_code)

teste = response.json()

#print(json.dumps(teste, indent=4, separators=(", ", " = ")))

for i in teste['results']:
  print("segment: ", i['display_name'])
  print("id: ", i['id'])
  print("path: ", i['path'])
  print("subnet: ", i['subnets'])
