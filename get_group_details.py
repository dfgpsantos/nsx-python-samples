'''
Python Script to export Group Effective IP Memebers
'''

import getpass

import requests

import json

import time

from urllib3.exceptions import InsecureRequestWarning
requests.packages.urllib3.disable_warnings(category=InsecureRequestWarning)

from requests.auth import HTTPBasicAuth

nsxmgr = 'lm-paris.corp.local'

headers = {'Content-type': 'application/json'}

exportfile = 'gruouplist.csv'

class Group:

  def __init__(self,grouplist='none',groupid='none',page='none',ipmembers='none',cursor='',efectivemembers='none',vms='none'):
    self.grouplist = grouplist
    self.groupid = groupid
    self.page = page
    self.ipmembers = ipmembers
    self.cursor = cursor
    self.efectivemembers = efectivemembers
    self.vms = vms

  
  def list(self):

    allgroups = requests.get('https://{}/policy/api/v1/infra/domains/default/groups?page_size=5&cursor={}'.format(nsxmgr,self.cursor), auth=basic, verify=False)
    self.grouplist = allgroups.json()
    return self.grouplist


  def members(self):
    groupmembers = requests.get('https://{}/policy/api/v1/infra/domains/default/groups/{}/members/vifs'.format(nsxmgr,groupid), auth=basic, verify=False)
    self.efectivemembers = groupmembers.json()
    return self.groupmembers

  def ipaddresses(self):
    groupipaddresses = requests.get('https://{}/policy/api/v1/infra/domains/default/groups/{}/members/ip-addresses'.format(nsxmgr,self.groupid), auth=basic, verify=False)
    self.ipmembers = groupipaddresses.json()
    return self.ipmembers
#    return self.ipmembers
  
  def vmlistname(self):
    vmlist = requests.get('https://{}/policy/api/v1/infra/domains/default/groups/{}/members/virtual-machines'.format(nsxmgr,self.groupid), auth=basic, verify=False)
    self.vms = vmlist.json()
    return self.vms['results']


class VM:

  def __init__(self,vmid,vmdetails='none'):
    self.vmid = vmid


  def vm_info(self):
    vminfo = requests.get('https://{}/policy/api/v1/fabric/virtual-machines?external_id={}'.format(nsxmgr,self.vmid), auth=basic, verify=False)
    vmdetails = vminfo.json()
    return self.vmdetails



nsxuser = input("Username:")
#nsxuser = 'xxxx'

nsxpass = getpass.getpass("Password")
#nsxpass = 'xxxx'

basic = HTTPBasicAuth(nsxuser, nsxpass)

cursorpage = ''

printresults = True

myfile = open(exportfile, "w")

myfile.write('Group Name;IP Addresses;VMs\n')

myfile.close()

while printresults:
  
  myfile = open(exportfile, "a")

  mygroups = Group(cursor=cursorpage)
  results = mygroups.list()
  grouplist = results['results']

  for groupname in grouplist:
    print(groupname['display_name'])
    mygroupvar = groupname['id']
    mygroupid = Group(groupid=mygroupvar)
    groupips = mygroupid.ipaddresses()
    print(groupips['results'])
#    print('{};{}'.format(groupname['display_name'],groupips['results']))
    myfile.write('{};{};'.format(groupname['display_name'],groupips['results']))
    vmsingroup = mygroupid.vmlistname()
    for hostid in vmsingroup:
      print(hostid['display_name'])
      myfile.write('{} '.format(hostid['display_name']))
    myfile.write('\n')

  if 'cursor' in results:
    cursorpage = results['cursor']
    myfile.close()
  else:
    printresults = False
    myfile.close()
