from sidecarclient import client

sidecar = client.Client(
    auth_version = 2,
    username = "admin",
    password = "5d6baead492b",
    #endpoint = "https://api.stage1.nephoscale.com:9090/v2",
    auth_url = "https://api.stage1.nephoscale.com:5000/v2.0",
    #endpoint_type="publicURL",
    region_name = "stage1",
    tenant_name = "admin",
    timeout = 10,
    insecure = False
)

print "###############################################################"
print "# LISTING EVENTS                                              #"
print "###############################################################"
events = sidecar.events.list()
print "#Total event count %d:" % (len(events))
for event in events:
    print "#======================="
    print "# id:%s" %(event.id)
    print "# name:%s" %(event.name)
    print "# node_uuid:%s" %(event.node_uuid)
    print "# vm_uuid_list:%s" %(event.vm_uuid_list)
    print "# extra:%s" %(event.extra)
    print "# event_create_time:%s" %(event.event_create_time)
    print "# event_complete_time:%s" %(event.event_complete_time)
print "###############################################################"
print "# CREATING NEW EVENT                                          #"
print "###############################################################"
for i in xrange(66, 100):
    new_event = sidecar.events.create(
        name="event" + str(i),
        node_uuid="84444iiiii4897879jk" + str(i),
        vm_uuid_list = ["g4sdgvjs7678", "bchgbskjch7867658"]
    )

