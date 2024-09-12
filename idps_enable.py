'''
Python Script to Enable and Configure IDPS Profile and Rules
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

  def enable(self):
    data = {'ids_enabled':'true', 'cluster':{'target_id':'c1da5ddb-6a0c-410f-8cd9-91040f49e030:domain-c1006'}}
    requests.patch('https://{}/policy/api/v1/infra/settings/firewall/security/intrusion-services/cluster-configs/c1da5ddb-6a0c-410f-8cd9-91040f49e030%3Adomain-c1006'.format(nsxmgr), auth=basic, verify=False, headers=headers, data=json.dumps(data))


class IdpsT1:

  def __init__(self,t1id):
    self.t1id = t1id

  def enable_idps(self):
    data = {'resource_type':'Infra', 'children':[{'resource_type':'ChildResourceReference', 'id':'{}'.format(self.t1id), 'target_type':'Tier1', 'children':[{'SecurityFeatures':{'resource_type':'SecurityFeatures', 'features':[{'feature':'IDPS', 'enable':'true'}, {'feature':'MALWAREPREVENTION', 'enable':'false'}, {'feature':'TLS', 'enable':'false'}, {'feature':'IDFW', 'enable':'false'}]}, 'resource_type':'ChildSecurityFeatures'}]}]}
    requests.patch('https://{}/policy/api/v1/infra'.format(nsxmgr), auth=basic, verify=False, headers=headers, data=json.dumps(data))


class IdpsGeneral:

  def __init__(self,name='0'):
    self.name = name

  def enable(self):
    data = {'auto_update':'true', 'ids_events_to_syslog':'true', 'oversubscription':'BYPASSED'}
    requests.patch('https://{}/policy/api/v1/infra/settings/firewall/security/intrusion-services'.format(nsxmgr), auth=basic, verify=False, headers=headers, data=json.dumps(data))

  def profile(self):
    data = {'display_name':'{}'.format(idpsprofilename), 'profile_severity':['CRITICAL', 'HIGH', 'MEDIUM', 'LOW', 'SUSPICIOUS'], 'pcap_config':{'pcap_enabled':'true', 'pcap_byte_count':10000, 'pcap_packet_count':5}}
    requests.put('https://{}/policy/api/v1/infra/settings/firewall/security/intrusion-services/profiles/{}'.format(nsxmgr,idpsprofilename), auth=basic, verify=False, headers=headers, data=json.dumps(data))

  def rule_create(self):
    data = {'resource_type':'Infra', 'children':[{'resource_type':'ChildResourceReference', 'id':'default', 'target_type':'Domain', 'children':[{'resource_type':'ChildIdsSecurityPolicy', 'marked_for_delete':'false', 'IdsSecurityPolicy':{'resource_type':'IdsSecurityPolicy', 'display_name':'Distributed IDPS', 'id':'Distributed_IDPS', 'marked_for_delete':'false', 'stateful':'true', 'locked':'false', 'category':'ThreatRules', 'sequence_number':5, 'children':[{'resource_type':'ChildIdsRule', 'marked_for_delete':'false', 'IdsRule':{'display_name':'Lateral Movement', 'id':'Lateral_Movement', 'resource_type':'IdsRule', 'marked_for_delete':'false', 'source_groups':['/infra/domains/default/groups/Threat_VM'], 'sequence_number':10, 'destination_groups':['/infra/domains/default/groups/Threat_VM'], 'services':['ANY'], 'action':'DETECT', 'direction':'IN_OUT', 'logged':'true', 'disabled':'false', 'notes':'', 'tag':'', 'ip_protocol':'IPV4_IPV6', 'sources_excluded':'false', 'ids_profiles':['/infra/settings/firewall/security/intrusion-services/profiles/Lateral-Profile'], 'oversubscription':'INHERIT_GLOBAL', 'scope':['/infra/domains/default/groups/Threat_VM']}}]}}]}]}
    requests.patch('https://{}/policy/api/v1/infra?enforce_revision_check=true'.format(nsxmgr), auth=basic, verify=False, headers=headers, data=json.dumps(data))


#Enable IDPS Features

tncluster = IdpsTn()

#Enabling IDPS at ESXi Clusters and Tier 1 Gateways

print('Enabling IDPS at the ESXi Cluster Level')

tncluster.enable()

time.sleep(10)

print('Enabling IDPS on T1s')

for tier1 in t1list:
  print('Configuring Tier-1 {}'.format(tier1))
  tier1gw = IdpsT1(tier1)
  tier1gw.enable_idps()
  time.sleep(3)

print('Enabling IDPS Auto Update and Syslog')

idpsdemo = IdpsGeneral()

idpsdemo.enable()

time.sleep(3)

print('Creating IDPS Profile')

idpsdemo.profile()

time.sleep(3)

print('Creating IDPS Distributed Rules')

idpsdemo.rule_create()


print('IDPS configurations have been finished')
