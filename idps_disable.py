'''
Python Script to Disable and Remove IDPS Profile and Rules
'''

import requests

import json

import time

from urllib3.exceptions import InsecureRequestWarning
requests.packages.urllib3.disable_warnings(category=InsecureRequestWarning)

from requests.auth import HTTPBasicAuth

basic = HTTPBasicAuth('admin', 'VMware123!VMware123!')

nsxmgr = 'nsx-mgr.vcf.sddc.lab'

headers = {'Content-type': 'application/json'}

t1list = ['Tier-1-gateway-mars','Tier-1-gateway-VDI','Tier-1-gateway-Production','Tier-1-gateway-01','Tier-1-gateway-Development']

idpsprofilename = 'Lateral-Profile'

class IdpsTn:

  def __init__(self,name=0):
    self.name = name

  def disable(self):
    data = {'ids_enabled':'false', 'cluster':{'target_id':'c1da5ddb-6a0c-410f-8cd9-91040f49e030:domain-c1006'}}
    requests.patch('https://{}/policy/api/v1/infra/settings/firewall/security/intrusion-services/cluster-configs/c1da5ddb-6a0c-410f-8cd9-91040f49e030%3Adomain-c1006'.format(nsxmgr), auth=basic, verify=False, headers=headers, data=json.dumps(data))


class IdpsT1:

  def __init__(self,t1id):
    self.t1id = t1id

  def disable_idps(self):
    data = {'resource_type':'Infra', 'children':[{'resource_type':'ChildResourceReference', 'id':'{}'.format(self.t1id), 'target_type':'Tier1', 'children':[{'SecurityFeatures':{'resource_type':'SecurityFeatures', 'features':[{'feature':'IDPS', 'enable':'false'}, {'feature':'MALWAREPREVENTION', 'enable':'false'}, {'feature':'TLS', 'enable':'false'}, {'feature':'IDFW', 'enable':'false'}]}, 'resource_type':'ChildSecurityFeatures'}]}]}
    requests.patch('https://{}/policy/api/v1/infra'.format(nsxmgr), auth=basic, verify=False, headers=headers, data=json.dumps(data))


class IdpsGeneral:

  def __init__(self,name='0'):
    self.name = name

  def disable(self):
    data = {'auto_update':'false', 'ids_events_to_syslog':'false', 'oversubscription':'BYPASSED'}
    requests.patch('https://{}/policy/api/v1/infra/settings/firewall/security/intrusion-services'.format(nsxmgr), auth=basic, verify=False, headers=headers, data=json.dumps(data))

  def profile_delete(self):
    requests.delete('https://{}/policy/api/v1/infra/settings/firewall/security/intrusion-services/profiles/{}'.format(nsxmgr,idpsprofilename), auth=basic, verify=False, headers=headers)

  def rule_delete(self):
    data = {'resource_type':'Infra', 'children':[{'resource_type':'ChildResourceReference', 'id':'default', 'target_type':'Domain', 'children':[{'resource_type':'ChildIdsSecurityPolicy', 'marked_for_delete':'true', 'IdsSecurityPolicy':{'resource_type':'IdsSecurityPolicy', 'id':'Distributed_IDPS', 'marked_for_delete':'true', 'children':[]}}]}]}
    requests.patch('https://{}/policy/api/v1/infra?enforce_revision_check=true'.format(nsxmgr), auth=basic, verify=False, headers=headers, data=json.dumps(data))


#Disabling IDPS Features



print('Deleting IDPS Distributed Rules')

idpsdemo = IdpsGeneral()

idpsdemo.rule_delete()

time.sleep(3)



print('Deleting IDPS Profile')

idpsdemo.profile_delete()

time.sleep(3)



print('Disabling IDPS Auto Update and Syslog')

idpsdemo.disable()

time.sleep(3)



#Disabling IDPS at ESXi Clusters and Tier 1 Gateways



print('Disabling IDPS on T1s')

for tier1 in t1list:
  print('Configuring Tier-1 {}'.format(tier1))
  tier1gw = IdpsT1(tier1)
  tier1gw.disable_idps()
  time.sleep(3)



print('Disabling IDPS at the ESXi Cluster Level')

tncluster = IdpsTn()

tncluster.disable()

time.sleep(10)



print('IDPS configurations have been finished')
