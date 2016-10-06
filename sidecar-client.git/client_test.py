from sidecarclient import client

sidecar = client.Client(
	
    username = "admin",
    password = "5d6baead492b",
    auth_url = "https://api.stage1.nephoscale.com:35357/v2",
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
"""
new_event = sidecar.events.create(
    name="test786872368-7690",
    node_uuid="897897879jhkjk",
    vm_uuid_list = ["gvjhsdgvjs7678", "bcjhdhgbskjch786768"]
)
print "# id:%s" %(new_event.id)
print "# name:%s" %(new_event.name)
print "# node_uuid:%s" %(new_event.node_uuid)
print "# vm_uuid_list:%s" %(new_event.vm_uuid_list)
print "# extra:%s" %(new_event.extra)
print "# event_create_time:%s" %(new_event.event_create_time)
print "# event_complete_time:%s" %(new_event.event_complete_time)
print "###############################################################"
print "# EVENT DETAIL WITH ID %s                                     #" % (new_event.id)
print "###############################################################"
event_detail =  sidecar.events.detail(id=new_event.id)
print "# id:%s" %(event_detail.id)
print "# name:%s" %(event_detail.name)
print "# node_uuid:%s" %(event_detail.node_uuid)
print "# vm_uuid_list:%s" %(event_detail.vm_uuid_list)
print "# extra:%s" %(event_detail.extra)
print "# event_create_time:%s" %(event_detail.event_create_time)
print "# event_complete_time:%s" %(event_detail.event_complete_time)
print "###############################################################"
print "# Edit event WITH ID %s                                       #" % (new_event.id)
print "###############################################################"
event_detail =  sidecar.events.edit(id=new_event.id, name="Hello098765")
print "###############################################################"
print "# EVENT DETAIL WITH ID %s                                     #" % (new_event.id)
print "###############################################################"
event_detail =  sidecar.events.detail(id=new_event.id)
print "# id:%s" %(event_detail.id)
print "# name:%s" %(event_detail.name)
print "# node_uuid:%s" %(event_detail.node_uuid)
print "# vm_uuid_list:%s" %(event_detail.vm_uuid_list)
print "# extra:%s" %(event_detail.extra)
print "# event_create_time:%s" %(event_detail.event_create_time)
print "# event_complete_time:%s" %(event_detail.event_complete_time)
print "###############################################################"
print "# DELETE EVENT WITH ID %s                                     #" % (new_event.id)
print "###############################################################"
sidecar.events.delete(id=new_event.id)

"""
