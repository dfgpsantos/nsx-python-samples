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

nsxmgr = 'yournsxmanagerhere'

headers = {'Content-type': 'application/json'}

exportfile = 'gruouplist.csv'

class Group:

  def __init__(self,grouplist='none',groupid='none',page='none',ipmembers='none',cursor='',efectivemembers='none'):
    self.grouplist = grouplist
    self.groupid = groupid
    self.page = page
    self.ipmembers = ipmembers
    self.cursor = cursor
    self.efectivemembers = efectivemembers

  
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



nsxuser = input("Username:")

nsxpass = getpass.getpass("Password")


basic = HTTPBasicAuth(nsxuser, nsxpass)

cursorpage = ''

printresults = True

myfile = open(exportfile, "w")

myfile.write('Group Name;IP Addresses\n')

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
    myfile.write('{};{}\n'.format(groupname['display_name'],groupips['results']))

  if 'cursor' in results:
    cursorpage = results['cursor']
    myfile.close()
  else:
    printresults = False
    myfile.close()
