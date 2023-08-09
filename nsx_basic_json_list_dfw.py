import requests

import json

from urllib3.exceptions import InsecureRequestWarning
requests.packages.urllib3.disable_warnings(category=InsecureRequestWarning)

from requests.auth import HTTPBasicAuth

basic = HTTPBasicAuth('userhere', 'passwordhere')

dfw_response = requests.get('https://nsxmanagerhere/policy/api/v1/infra/domains/default/security-policies', auth=basic, verify=False)

print(dfw_response.status_code)

dfw_json = dfw_response.json()

print(json.dumps(dfw_json, indent=4, separators=(", ", " = ")))

secpolseq = int()

secpolseq = 1

secpol_id_list = ["null"]

for secpol_list in dfw_json['results']:
  print("Option: ", secpolseq)
  print("Security Policy: ", secpol_list['display_name'])
  print("id: ", secpol_list['id'])
  print("path: ", secpol_list['path'])
  secpol_id_list.insert(secpolseq, secpol_list['id'])
  secpolseq += 1


print( "Select an option to view the rule list")
secpolsel = int(input("Option: "))

#print("Selected Option " + secpolsel)
print(secpol_id_list[secpolsel])

dfw_pol_url = ('https://nsx-41.corp.local/policy/api/v1/infra/domains/default/security-policies/')
dfw_id = secpol_id_list[secpolsel]

dfw_pol_rules = (dfw_pol_url+dfw_id)

dfw_response2 = requests.get(dfw_pol_rules, auth=basic, verify=False)
print(dfw_response2.status_code)

dfw_json2 = dfw_response2.json()

print(json.dumps(dfw_json2, indent=4, separators=(", ", " = ")))

rule_id_list = ["null"]

ruleseq = int()

ruleseq = 1

for dfwrule_list in dfw_json2['rules']:
  print("Option: ", ruleseq)
  print("Rule Name: ", dfwrule_list['display_name'])
  print("id: ", dfwrule_list['id'])
  print("Source: ", dfwrule_list['source_groups'])
  print("Destination: ", dfwrule_list['destination_groups'])
  print("Service: ", dfwrule_list['services'])
  print("Action: ", dfwrule_list['profiles'])
  print("Action: ", dfwrule_list['action'])
  print("Apply to: ", dfwrule_list['scope'])
  rule_id_list.insert(ruleseq, dfwrule_list['id'])
  ruleseq += 1
