'''
Python Script to Deploy the Malware-Prevention SVMs
'''

import requests

import json

import time

from urllib3.exceptions import InsecureRequestWarning
requests.packages.urllib3.disable_warnings(category=InsecureRequestWarning)

from requests.auth import HTTPBasicAuth

basic = HTTPBasicAuth('userhere', 'passwordhere')

nsxmgr = 'nsxmanagerhere'

headers = {'Content-type': 'application/json'}

t1list = ['Tier-1-gateway-mars','Tier-1-gateway-VDI','Tier-1-gateway-Production','Tier-1-gateway-01','Tier-1-gateway-Development']

malwareprofilename = 'MalwareProfile'


class MpSvm:

  def __init__(self,mpsvmstatus='unknown'):
    self.mpsvmstatus = mpsvmstatus

  def status(self):
    mpsvmstatuscall = requests.get('https://{}/api/v1/malware-prevention/compute-collection/c1da5ddb-6a0c-410f-8cd9-91040f49e030%3Adomain-c1006/status'.format(nsxmgr), auth=basic, verify=False)
    self.mpsvmstatus = mpsvmstatuscall.json()
    return self.mpsvmstatus

  def deploy(self):
    data = {'cluster_svm_property':{'storage_id':'', 'network_id':'dvportgroup-1038', 'ip_allocation_type':'STATIC', 'ip_pool_id':'6a526407-2032-4838-80c9-5926080a57b0'}, 'svm_config':{'ssh_key':'---- BEGIN SSH2 PUBLIC KEY ----\nComment: \'rsa-key-20240604\'\nAAAAB3NzaC1yc2EAAAADAQABAAABAQCO2zaHggtTIjd0V9HXElGgKnggJDy8RbHv\n2seqpLCORVfVeb2llTc2zEedz1nBtp6oggA2Ks0ZV6+THQpwvSzTOhGPu23TmBuO\nh4okTLZSHPQBiFVFWG833rlxr9g8+Vt1MFFhnj/1VkKx7+6TJIr8bNoB6zmfj+4R\niije91QqK2bClhdlELrayKH4kxL4HVcWXl1++2bbTjKLuwenixKqrxiH805Yu1mD\nJbMvvgdmiD10gyEfKlpu4BV0scynKwBqbsGE4xw7Q90u6+dX13e1JIEAU0Z4uvtZ\nl2TvYdvB+wseqiW5iAiai9fs8EUEqF64V2v+QFd+tzWQMLx+sp6h\n---- END SSH2 PUBLIC KEY ----'}, 'ovf_spec_name':'NSX-SVM-4.2.0.0.0.24114048', 'compute_collection_id':'c1da5ddb-6a0c-410f-8cd9-91040f49e030:domain-c1006', 'sub_cluster_svm_property_list':[]}
    requests.post('https://{}/api/v1/malware-prevention/compute-collection/c1da5ddb-6a0c-410f-8cd9-91040f49e030%3Adomain-c1006/svm-deployment'.format(nsxmgr), auth=basic, verify=False, headers=headers, data=json.dumps(data))



class AtpT1:

  def __init__(self,t1id):
    self.t1id = t1id

  def enable_idps_mp(self):
    data = {'resource_type':'Infra', 'children':[{'resource_type':'ChildResourceReference', 'id':'{}'.format(self.t1id), 'target_type':'Tier1', 'children':[{'SecurityFeatures':{'resource_type':'SecurityFeatures', 'features':[{'feature':'IDPS', 'enable':'true'}, {'feature':'MALWAREPREVENTION', 'enable':'true'}, {'feature':'TLS', 'enable':'false'}, {'feature':'IDFW', 'enable':'false'}]}, 'resource_type':'ChildSecurityFeatures'}]}]}
    requests.patch('https://{}/policy/api/v1/infra'.format(nsxmgr), auth=basic, verify=False, headers=headers, data=json.dumps(data))


class MpGeneral:

  def __init__(self,name='0'):
    self.name = name

  def profile(self):
    data = {'display_name':'{}'.format(malwareprofilename), 'file_type':['DOCUMENT', 'EXECUTABLE', 'MEDIA', 'ARCHIVE', 'DATA', 'SCRIPT', 'OTHER'], 'detection_type':'SIGNATURE_AND_SANDBOXING_BASED'}
    requests.put('https://{}/policy/api/v1/infra/settings/firewall/security/malware-prevention-service/profiles/MalwareProfile'.format(nsxmgr), auth=basic, verify=False, headers=headers, data=json.dumps(data))

  def rule_create(self):
    data = {'resource_type':'Infra', 'children':[{'resource_type':'ChildResourceReference', 'id':'default', 'target_type':'Domain', 'children':[{'resource_type':'ChildIdsSecurityPolicy', 'marked_for_delete':'false', 'IdsSecurityPolicy':{'resource_type':'IdsSecurityPolicy', 'display_name':'Distributed-Malware', 'id':'Distributed-Malware', 'marked_for_delete':'false', 'stateful':'true', 'locked':'false', 'category':'ThreatRules', 'sequence_number':10, 'children':[{'resource_type':'ChildIdsRule', 'marked_for_delete':'false', 'IdsRule':{'display_name':'Distributed-Malware', 'id':'Distributed-Malware', 'resource_type':'IdsRule', 'marked_for_delete':'false', 'source_groups':['ANY'], 'sequence_number':10, 'destination_groups':['ANY'], 'services':['ANY'], 'action':'DETECT', 'direction':'IN_OUT', 'logged':'false', 'disabled':'false', 'notes':'', 'tag':'', 'ip_protocol':'IPV4_IPV6', 'ids_profiles':['/infra/settings/firewall/security/malware-prevention-service/profiles/MalwareProfile'], 'scope':['/infra/domains/default/groups/ATP']}}]}}]}]}
    requests.patch('https://{}/policy/api/v1/infra?enforce_revision_check=true'.format(nsxmgr), auth=basic, verify=False, headers=headers, data=json.dumps(data))


#Deploy Malware Prevention SVM

mpsvm = MpSvm()

#Deploying Malware Prevention SVM

print('Deploying Malware Prevention SVM')

mpsvm.deploy()

time.sleep(20)

print('Getting Malware Prevention SVM deployment status')

mpsvmstatus = mpsvm.status()

while mpsvmstatus['compute_collection_deployment_status'] != 'DEPLOYMENT_SUCCESSFUL':
  print('Cluster level MP SVM status is {}'.format(mpsvmstatus['compute_collection_deployment_status']))
  time.sleep(20)
  mpsvmstatus = mpsvm.status()

print('Cluster level MP SVM status is {}'.format(mpsvmstatus['compute_collection_deployment_status']))

print('Deploying Malware Prevention and IDPS on T1s')

for tier1 in t1list:
  print('Configuring Tier-1 {}'.format(tier1))
  tier1gw = AtpT1(tier1)
  tier1gw.enable_idps_mp()
  time.sleep(3)

print('Creating Malware Prevention Profile')

mpdemo = MpGeneral()

mpdemo.profile()

time.sleep(3)

print('Creating Malware Prevention Distributed Rules')

mpdemo.rule_create()


print('Malware Prevention configurations have been finished')
