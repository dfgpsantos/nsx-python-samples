#import pdb
#import pprint
import requests
#import json

import com.vmware
#import com.vmware.nsx_policy
#import com.vmware.nsx_policy.infra_client
#import com.vmware.nsx_policy.model_client
from com.vmware import nsx_policy_client
from com.vmware import nsx_client


from vmware.vapi.bindings.struct import PrettyPrinter
from vmware.vapi.lib import connect
from vmware.vapi.security.user_password import \
    create_user_password_security_context
from vmware.vapi.stdlib.client.factories import StubConfigurationFactory
from vmware.vapi.bindings.stub import ApiClient

from urllib3.exceptions import InsecureRequestWarning
requests.packages.urllib3.disable_warnings(category=InsecureRequestWarning)

NSX='yournsxhere'
NSXPASS='yourpasswordhere'
NSXUSER='youruserhere'

def get_nsx_client(ip, username=NSXUSER, password=NSXPASS,
                   is_policy=False):
    session = requests.session()
    session.verify = False
    requests.packages.urllib3.disable_warnings()
    nsx_url = 'https://%s:%s' % (ip, 443)
    connector = connect.get_requests_connector(
        session=session, msg_protocol='rest', url=nsx_url)
    stub_config = StubConfigurationFactory.new_std_configuration(connector)
    security_context = create_user_password_security_context(username,
                                                             password)
    connector.set_security_context(security_context)
    if is_policy:
        stub_factory = nsx_policy_client.StubFactory(stub_config)
    else:
        stub_factory = nsx_client.StubFactory(stub_config)
    return ApiClient(stub_factory)

if __name__ == '__main__':
  nsx_client = get_nsx_client(NSX, username=NSXUSER, password=NSXPASS)
  segments_list = nsx_client.LogicalSwitches.list()

  for seg in segments_list.results:
    print(seg.display_name)
    print(seg.id)
    print(seg.transport_zone_id)
