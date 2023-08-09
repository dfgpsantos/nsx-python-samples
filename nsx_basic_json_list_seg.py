import requests

import json

from urllib3.exceptions import InsecureRequestWarning
requests.packages.urllib3.disable_warnings(category=InsecureRequestWarning)

from requests.auth import HTTPBasicAuth

basic = HTTPBasicAuth('userhere', 'passwordhere')

response = requests.get('https://NSXMANAGERHERE/policy/api/v1/infra/segments', auth=basic, verify=False)

print(response.status_code)

teste = response.json()

#print(json.dumps(teste, indent=4, separators=(", ", " = ")))

for i in teste['results']:
  print("segment: ", i['display_name'])
  print("id: ", i['id'])
  print("path: ", i['path'])
  print("subnet: ", i['subnets'])
