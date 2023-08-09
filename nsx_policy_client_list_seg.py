#import pdb
#import pprint
import requests
#import json

import com.vmware
import com.vmware.nsx_policy
import com.vmware.nsx_policy_client
import com.vmware.nsx_policy.infra_client
import com.vmware.nsx_policy.model_client
#from com.vmware import nsx_policy_client
#from com.vmware import nsx_client


from vmware.vapi.bindings.struct import PrettyPrinter
from vmware.vapi.lib import connect
from vmware.vapi.security.user_password import \
    create_user_password_security_context
from vmware.vapi.stdlib.client.factories import StubConfigurationFactory

from urllib3.exceptions import InsecureRequestWarning
requests.packages.urllib3.disable_warnings(category=InsecureRequestWarning)

NSX='yournsxhere'
PASS='yourpassswordhere'
NSXUSER='youruserhere'

def main():
    session = requests.session()
    session.verify = False
    nsx_url = 'https://%s:%s' % (NSX, 443)
    connector = connect.get_requests_connector(
        session=session, msg_protocol='rest', url=nsx_url)
    stub_config = StubConfigurationFactory.new_std_configuration(connector)
    security_context = create_user_password_security_context(NSXUSER, PASS)
    connector.set_security_context(security_context)

    teste_seg2 = com.vmware.nsx_policy.infra_client.Segments(stub_config)
    teste_seg_result = teste_seg2.list()
#    print(teste_seg_result)

    for seg_list in teste_seg_result.results:
        print("Segment: ", seg_list.display_name)
        print("id: ", seg_list.id)
        print("path: ", seg_list.path)

if __name__ == "__main__":
    main()
