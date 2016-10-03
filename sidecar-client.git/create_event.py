from sidecarclient import client
from novaclient import client as nova_client

sidecar = client.Client(
    auth_version = 2,
    username = "admin",
    password = "demo",
    endpoint = "http://198.100.181.67:9090/v2",
    auth_url = "http://198.100.181.67:35357/v2",
    endpoint_type="publicURL",
    region_name = "RegionOne",
    tenant_name = "admin",
    timeout = 10,
    insecure = False
)

"""
try:
    print " before connect"
    nova_conn=nova_client.Client(2, "admin","stack123","admin","http://198.100.181.74:35357/v2")
except Exception, e:
    print "sdfsdf", e

   
print "###############################################################"
print "# CREATING NEW EVENT                                          #"
print "###############################################################"

new_event = sidecar.events.create(
    name="test3786872368-7690-8",
    node_uuid="897897879jhkjk",
    vm_uuid_list = ["gvjhsdgvjs7678", "bcjhdhgbskjch786768"]
)
"""
#new_event = sidecar.events.evacuate_runEvent('15acc2ca8fb84c3ba731a86f6f70a475')
new_event = sidecar.events.evacuate_healthcheck()
"""
try:    
    nova_conn=nova_client.Client(2, "admin", "stack123", "admin", "http://198.100.181.74:35357/v2.0")
    service_list = nova_conn.hypervisors.list()
    print service_list
    print service_list.__dict__
except Exception, e:
    print 'error here----', e
"""
