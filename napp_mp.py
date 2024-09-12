'''
Python Script to enable Malware-Prevention
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

class MalwarePrevention:

  def __init__(self,mpstatus='unknown',ccstatus='unknown',precheckstatus='unknown'):
    self.mpstatus = mpstatus
    self.ccstatus = ccstatus
    self.precheckstatus = precheckstatus

  def status(self):
    mpscall = requests.get('https://{}/napp/api/v1/platform/features/malware-prevention/status'.format(nsxmgr), auth=basic, verify=False)
    self.mpstatus = mpscall.json()
    return self.mpstatus


  def cloud_connector_config(self):
    data = {'fqdn':'nsx.west.us.lastline.com', 'region':'west.us', 'region_name':'United States 1'}
    requests.patch('https://{}/napp/api/v1/platform/features/cloud-connector/config'.format(nsxmgr), auth=basic, verify=False, headers=headers, data=json.dumps(data))

  def cloud_connector_check(self):
    ccstatus = requests.get('https://{}/napp/api/v1/platform/features/cloud-connector/config'.format(nsxmgr), auth=basic, verify=False)
    self.ccstatus = ccstatus.json()
    return self.ccstatus

  def prechecks_enable(self):
    requests.post('https://{}/napp/api/v1/platform/features/malware-prevention/pre-checks'.format(nsxmgr), auth=basic, verify=False)

  def prechecks_status(self):
    pcscall = requests.get('https://{}/napp/api/v1/platform/features/malware-prevention/pre-checks/status'.format(nsxmgr), auth=basic, verify=False)
    self.precheckstatus = pcscall.json()
    return self.precheckstatus

  def enable(self):
    data = {'action': 'DEPLOY'}
    requests.post('https://{}/napp/api/v1/platform/features/malware-prevention'.format(nsxmgr), auth=basic, verify=False, headers=headers, data=json.dumps(data))


#Enable MalwarePrevention


mpsvc = MalwarePrevention()


#Configuring and enabling the pre-checks

print('Running Pre-Checks for Malware Prevention')


mpsvc.cloud_connector_config()


mpcc_config = mpsvc.cloud_connector_check()
print('MP Cloud Connector is using {} with fqdn {}'.format(mpcc_config['region_name'],mpcc_config['fqdn']))


mpsvc.prechecks_enable()

checkpc = [0,0,0,0]

#Validating the pre-checks are met

while checkpc != [1,1,1,1]:
  mpsvc.prechecks_status()
  pcsresults = mpsvc.precheckstatus['results']
  pcscounter = 0

  for check in pcsresults:
    if check['status'] != 'SUCCESS':
      print('{} is {}'.format(check['id'],check['status']))
      pcscounter = pcscounter + 1
    else:
      print('{} is {}'.format(check['id'],check['status']))
      checkpc[pcscounter] = 1
      pcscounter = pcscounter + 1
  time.sleep(10)

print('Malware Prevention Pre-Checks done! Activating Malware-Prevention')

#Enable Malware Prevention

mpsvc.enable()

checkmpsvc = mpsvc.status()

#Check if Malware-Prevention has been enabled

while checkmpsvc['status'] != 'DEPLOYMENT_SUCCESSFUL':
  print('Malware Prevention status is {}'.format(checkmpsvc['status']))
  time.sleep(30)
  checkmpsvc = mpsvc.status()

print('Malware-Prevention Deployment Successful')
