'''
Python Script to export VM Details
'''

import getpass

import requests

import json

import time

from urllib3.exceptions import InsecureRequestWarning
requests.packages.urllib3.disable_warnings(category=InsecureRequestWarning)

from requests.auth import HTTPBasicAuth

nsxmgr = 'yournsxmanagerhere'

headers = {'Content-Type': 'application/json', 'Accept': 'application/json'} 

exportfile = 'vmlist.csv'

true = "true"

false = "false"


class VirtualMachineList:

  def __init__(self,vmlist='none',page='none',cursor='',vms='none'):
    self.vmlist = vmlist
    self.page = page
    self.cursor = cursor

  
  def list(self):

    allvms = requests.get('https://{}/api/v1/fabric/virtual-machines?page_size=5&cursor={}'.format(nsxmgr,self.cursor), auth=basic, verify=False)
    self.vmlist = allvms.json()
    return self.vmlist



class Search:

  def __init__(self,vmdetails='none',vmexternalid='none',vmidonhost='none',vmhostid='none',vminfo='none'):
    self.vmexternalid = vmexternalid
    self.vmidonhost = vmidonhost
    self.vmhostid = vmhostid
    self.vminfo = vminfo
    self.vmdetails = vmdetails


  def vm_info(self):
    vmdata = {'primary':{'resource_type':'VirtualNetworkInterface','filters':[{'field_names':'owner_vm_id','value':'{}'.format(self.vmexternalid),'case_sensitive':'true'},{'field_names':'vm_local_id_on_host','value':'{}'.format(self.vmidonhost),'case_sensitive':'true'},{'field_names':'host_id','value':'{}'.format(self.vmhostid),'case_sensitive':'true'}]},'related':[{'resource_type':'LogicalPort OR SegmentPort OR VpcSubnetPort','join_condition':'attachment.id:lport_attachment_id','alias':'segmentPort'},{'resource_type':'VirtualMachine','join_condition':'external_id:owner_vm_id','alias':'VirtualMachine','filters':[{'field_names':'!tags.tag','value':'NSX_POLICY_INTERNAL','case_sensitive':'true'}]}],'context':'projects:ALL','data_source':'ALL'}
    vminfo = requests.post('https://{}/policy/api/v1/search/aggregate'.format(nsxmgr), headers=headers, auth=basic, verify=False, data=json.dumps(vmdata))
    self.vmdetails = vminfo.json()
    return self.vmdetails['results']



nsxuser = input("Username:")
#nsxuser = 'userhere'

nsxpass = getpass.getpass("Password")
#nsxpass = 'passwordhere'

basic = HTTPBasicAuth(nsxuser, nsxpass)

cursorpage = ''

printresults = True

myfile = open(exportfile, "w")

myfile.write('VM Name;Interface Count;Interface Names\n')

myfile.close()

while printresults:
  
  myfile = open(exportfile, "a")

  myvms = VirtualMachineList(cursor=cursorpage)
  results = myvms.list()
  vmslist = results['results']

  for virtual_machine in vmslist:
    virtual_machine_display_name = virtual_machine['display_name']
    print(virtual_machine_display_name)
    virtual_machine_external_id = virtual_machine['external_id']
    virtual_machine_host_id = virtual_machine['host_id']
    virtual_machine_local_id_on_host = virtual_machine['local_id_on_host']
    thisvm = Search(vmexternalid=virtual_machine_external_id,vmhostid=virtual_machine_host_id,vmidonhost=virtual_machine_local_id_on_host)
    vm_results = thisvm.vm_info()
    myfile.write('{};'.format(virtual_machine_display_name))
    if len(vm_results) != 0:
      vm_int_results = vm_results[0]
      vm_int_count = vm_int_results['related'][0]['result_count']
      print(vm_int_count)
      myfile.write('{};'.format(vm_int_count))
      if vm_int_count != 0:
        portindex = 0
        while vm_int_count != 0:
          vm_int_details = vm_int_results['related'][0]['results'][portindex]
          print(vm_int_details['display_name'])
          myfile.write('{} '.format(vm_int_details['display_name']))
          portindex += 1
          vm_int_count -= 1

    myfile.write('\n')    

  myfile.close()

  if 'cursor' in results:
    cursorpage = results['cursor']
  else:
    printresults = False


  










