#Enable NDR 

import requests

import json

import time

from urllib3.exceptions import InsecureRequestWarning
requests.packages.urllib3.disable_warnings(category=InsecureRequestWarning)

from requests.auth import HTTPBasicAuth

basic = HTTPBasicAuth('admin', 'VMware123!VMware123!')

nsxmgr = 'nsx-mgr.vcf.sddc.lab'

headers = {'Content-type': 'application/json'}

class Ndr:

  def __init__(self,ndrstatus='unknown',precheckstatus='unknown'):
    self.ndrstatus = ndrstatus
    self.precheckstatus = precheckstatus

  def status(self):
    ndrscall = requests.get('https://{}/napp/api/v1/platform/features/ndr/status'.format(nsxmgr), auth=basic, verify=False)
    self.ndrstatus = ndrscall.json()
    return self.ndrstatus


  def prechecks_enable(self):
    requests.post('https://{}/napp/api/v1/platform/features/ndr/pre-checks'.format(nsxmgr), auth=basic, verify=False)

  def prechecks_status(self):
    pcscall = requests.get('https://{}/napp/api/v1/platform/features/ndr/pre-checks/status'.format(nsxmgr), auth=basic, verify=False)
    self.precheckstatus = pcscall.json()
    return self.precheckstatus


  def enable(self):
    data = {'action': 'DEPLOY'}
    requests.post('https://{}/napp/api/v1/platform/features/ndr'.format(nsxmgr), auth=basic, verify=False, headers=headers, data=json.dumps(data))


#Enable NDR

ndr = Ndr()


#Enabling the pre-checks

ndr.prechecks_enable()

checkpc = [0,0,0]

#Validating the pre-checks are met

while checkpc != [1,1,1]:
  ndr.prechecks_status()
  pcsresults = ndr.precheckstatus['results']
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

print('NDR Pre-Checks done! Activating NDR')

#Enable NDR

ndr.enable()

checkndr = ndr.status()

#Check if NDR has been enabled

while checkndr['status'] != 'DEPLOYMENT_SUCCESSFUL':
  print('NDR status is {}'.format(checkndr['status']))
  time.sleep(60)
  checkndr = ndr.status()

print('NDR Deployment Successful')
