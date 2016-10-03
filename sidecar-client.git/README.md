# python-sidecarclient version 2

## Install


```shell
python setup.py install
```

## obj = sidecarclient.client.Client(**args)

Function to get the instance of sidecarclient

|SL.NO.| Argument nAME | Required                                     | Default Value | Description                   |
|:-----|:--------------|:---------------------------------------------|:--------------|:------------------------------|
|1     | username      |True, if user_id or auth_token is not given   | None          | Keystone admin username       |
|2     | user_id       |True, if user_name or auth_token is not given | None          | Keystone admin user id        |
|3     | password      |True, if auth_token is not given              | None          | Keystone admin password       |
|4     | tenant_id     |True, if auth_version is 2 and tenant_name is None,  and user credential is provided. | None     | Keystone admin tenant id      |
|5     | tenant_name   |True, if auth_version is 2 and tenant_id   is None,  and user credential is provided. | None     | Keystone admin tenant name    |
|6     | auth_url      |True                                          | None          | Keystone authentication url   |
|7     | auth_version  |Optional                                      | 2             | Keystone auth version, value must be either 2 or 3     |
|8     | project_id    |True, if auth_version is 3 and project_name is None | None    | Keystone admin project id      |
|9     | project_name  |True, if auth_version is 3 and project_id is None   | None    | Keystone admin project name    |
|10    | project_domain_id    |True, if auth_version is 3 and project_domain_name is None | None    | Keystone admin project's domain id      |
|11    | project_domain_name  |True, if auth_version is 3 and project_domain_id is None,    | None    | Keystone admin project's domain name    |
|12    | user_domain_id    |True, if auth_version is 3 and user_domain_name is None,  and user credential is provided. | None    | Keystone admin user's domain id      |
|13    | user_domain_name  |True, if auth_version is 3 and user_domain_id is None, and user credential is provided.   | None    | Keystone admin user's domain name    |
|14    | aith_token    |True, if no user credential is there                         | None    | Keystone admin user's token id      |
|15    | user_domain_name  |True, if auth_version is 3 and user_domain_id is None   | None    | Keystone admin user's domain name    |
|16    | endpoint  |True  | None    | sidecar endpoint. After user got token from keystone, if user has this endpoint, with given endpint_type and region_name    |
|17    | endpoint_type    |Optional | 'publicURL'    | against which ednpoint type we need to check. In version 3, its `internal`, `admin`, `public`, in version 2.0 it is `publicURL`, `adminURL`, `internalURL`|
|18    | region_name     |True      | None  | Against which region, the endpoint should b echecked.    |
|19    | timeout         |Optional  | 300   | Maximum seconds to wait for the result      |
|20    | insecure        |Optional  | False | wheather HTTPS should be verified or not |


## Listing events
> obj.events.list(**arg)

>> Diffrent filtering options are:

|SL.NO.| Argument Name         | Required     | Default Value | Description                                             |
|:-----|:----------------------|:-------------|:--------------|:--------------------------------------------------------|
|1     | id                    | optional     | None          | id of the event to be filtered                          |
|2     | name                  | optional     | None          | name of the event to be filtered                        |
|3     | node_uuid             | optional     | None          | filter the events on the basis of node_uuid             |
|4     | event_create_time     | optional     | None          | filter the events on the basis of event_create_time in (yyyy-mm-dd HH:ii:ss format)    |
|5     | min_event_create_time | optional     | None          | filter the events on the basis of min event_create_time in (yyyy-mm-dd HH:ii:ss format)     |
|6     | max_event_create_time | optional     | None          | filter the events on the basis of max event_create_time in (yyyy-mm-dd HH:ii:ss format)     |
|7     | marker                | optional     | None          | last event id                                           |
|8     | limit                 | optional     | None          | maximum number of events to be displayed                |

> It outputs a resultGenerator object.
> len(ticket_list) = Number of results fetched
> On looping the ResultGenerator object, it provides an event object. The Event object has following properties.

|SL.NO.| Argument Name         | Data Type     | Default Value | Description                                            |
|:-----|:----------------------|:-------------|:--------------|:--------------------------------------------------------|
|1     | id                    | string       | None          | id of the event                                         |
|2     | name                  | string       | None          | name of the event                                       |
|3     | node_uuid             | string       | None          | HOST id on which the event is occuring                  |
|4     | event_create_time     | string (yyyy-mm-dd HH:ii::ss format) | None |  event create time                       |
|5     | event_complete_time   | string (yyyy-mm-dd HH:ii::ss format) | None |  event complete time                     |
|6     | event_status          | string ('created', 'running', 'completed') | None |  event status                      |
|7     | vm_uuid_list          | list conating, instance ids  | empty list  |  the instances, which took part in the evacuation   |
|8     | extra                 | json                         | None |  any meta data                                  |


## Creating a new event
> obj.events.create(**arg)

>> Diffrent parameters required:

|SL.NO.| Argument Name         | Data Type    | Default Value | Description                                            |
|:-----|:----------------------|:-------------|:--------------|:--------------------------------------------------------| 
|1     | name                  | string       | None          | name of the event                                       |
|2     | node_uuid             | string       | None          | HOST id on which the event is occuring                  | 
|3     | vm_uuid_list (optional) | list conating, instance ids  | empty list  |  the instances, which took part in the evacuation   | 

It returns an *Event* object of newly created event.

## Getting detail of an event
> obj.events.detail(id)

For getting detail of an event only event id need to be passed.

It returns an *Event* Object.

## Editing an event
> obj.events.detail(id, **args)

Diffrent arguments:

|SL.NO.| Argument Name         | Data Type     | Required     | Description                                            |
|:-----|:----------------------|:-------------|:--------------|:--------------------------------------------------------|
|1     | id                    | string       | True          | id of the event  to be edited                           |
|2     | name                  | string       | optional      | name of the event                                       |
|3     | node_uuid             | string       | optional      | HOST id on which the event is occuring                  | 
|4     | event_status          | string ('created', 'running', 'completed') | optional |  event status                  |
|5     | vm_uuid_list          | list conating, instance ids  | optional  |  the instances, which took part in the evacuation   |

>> Returns: None

## deleting an event
> obj.events.delete(id)
> For deleting an event only  event id is required. But the event status must be `completed`
> returns None

## Example:

```python

from sidecarclient import client

sidecar = client.Client(
    auth_version = 2,
    username = "admin",
    password = "demo",
    endpoint = "http://controller:9090/v2",
    auth_url = "http://controller:35357/v2",
    endpoint_type="publicURL",
    region_name = "regionOne",
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
```


# python-sidecarclient version 2 CMD

## Command Name: sidecar

### Arguments:

|CMD Parameter name        | openrc param           | sidecarclient equivalent variable    |
|:------------------------:|------------------------|:-------------------------------------|
| --os-username            | OS_USER_NAME           | username                             |
| --os-password            | OS_USER_PASSWORD       | password                             |
| --os-user-id             | OS_USER_ID             | user_id                              |
| --os-tenant-name         | OS_TENANT_NAME         | tenant_name                          |
| --os-tenant-id           | OS_TENANT_ID           | tenant_id                            |
| --os-project-name        | OS_PROJECT_NAME        | project_name                         |
| --os-project-id          | OS_PROJECT_ID          | project_id                           |
| --os-project-domain-name | OS_PROJECT_DOMAIN_NAME | project_domain_name                  |
| --os-project-domain-id   | OS_PROJECT_DOMAIN_ID   | project_domain_id                    |
| --os-user-domain-id      | OS_USER_DOMAIN_ID      | user_domain_id                       |
| --os-user-domain-name    | OS_USER_DOMAIN_NAME    | user_domain_name                     |
| --os-auth-token          | OS_AUTH_TOKEN          | auth_token                           |
| --os-auth-url            | OS_AUTH_URL            | auth_url                             |
| --os-endpoint            | OS_ENDPOINT            | endpoint                             |
| --os-enpoint-type        | OS_ENDPOINT_TYPE       | endpoint_type                        |
| --os-region-name         | OS_REGION_NAME         | region_name                          |
| --os-insecure            | OS_INSECURE            | insecure                             |
| --os-timeout             | OS_TIMEOUT             | timeout                              |
| --os-auth-version        | OS_AUTH_VERSION        | auth_version                         |


<pre>
root@controller:/usr/local/lib/python2.7/dist-packages/sidecar# sidecar help
usage: sidecar [--version] [--debug] [--os-auth-token OS_AUTH_TOKEN]
               [--os-user-id OS_USER_ID] [--os-username OS_USERNAME]
               [--os-password OS_PASSWORD] [--os-tenant-name OS_TENANT_NAME]
               [--os-tenant-id OS_TENANT_ID]
               [--os-project-name OS_PROJECT_NAME]
               [--os-project-id OS_PROJECT_ID] [--os-auth-url OS_AUTH_URL]
               [--os-region-name OS_REGION_NAME]
               [--os-auth-version OS_AUTH_VERSION] [--os-timeout OS_TIMEOUT]
               [--os-insecure OS_INSECURE]
               [--os-user-domain-id OS_USER_DOMAIN_ID]
               [--os-user-domain-name OS_USER_DOMAIN_NAME]
               [--os-project-domain-id OS_PROJECT_DOMAIN_ID]
               [--os-project-domain-name OS_PROJECT_DOMAIN_NAME]
               <subcommand> ...

SIDECAR SHELL PROGRAM

Positional arguments:
  <subcommand>
    all-versions                Getting version details
    evacuates-event-create      Creating a new event
    evacuates-event-delete      Deleting a given evacuate event
    evacuates-event-detail      Getting the detail of an event
    evacuates-event-edit        Editing a given event
    evacuates-events-list       Listing and filtering the evacuates events
    bash-completion             Prints all the commands to stdout
    help                        Show help for the <command>

Optional arguments:
  --version                     show program's version number and exit
  --debug                       Print debugging output.
  --os-auth-token OS_AUTH_TOKEN
                                Defaults to env[OS_AUTH_TOKEN].
  --os-user-id OS_USER_ID       keystone admin user id. defaults to OS_USER_ID
  --os-username OS_USERNAME     keystone admin username, defaults to
                                OS_USERNAME
  --os-password OS_PASSWORD     Openstack admin password, defaults to
                                OS_PASSWORD
  --os-tenant-name OS_TENANT_NAME
                                Defaults to env[OS_TENANT_NAME].
  --os-tenant-id OS_TENANT_ID   Defaults to env[OS_TENANT_ID].
  --os-project-name OS_PROJECT_NAME
                                Defaults to env[OS_PROJECT_NAME].
  --os-project-id OS_PROJECT_ID
                                Defaults to env[OS_PROJECT_ID].
  --os-auth-url OS_AUTH_URL     Keystone auth url. defaults to OS_AUTH_URL
  --os-region-name OS_REGION_NAME
                                Defaults to env[OS_REGION_NAME].
  --os-auth-version OS_AUTH_VERSION
                                Which os auth version should be used, either 2
                                or 3. Default OS_AUTH_VERSION
  --os-timeout OS_TIMEOUT       Maximum time to wait for result.
  --os-insecure OS_INSECURE     Wheather https should be verified or not.
                                Defaults to False
  --os-user-domain-id OS_USER_DOMAIN_ID
                                Admin user's domain id, Default
                                OS_USER_DOMAIN_ID
  --os-user-domain-name OS_USER_DOMAIN_NAME
                                Admin user's domain name, Default
                                OS_USER_DOMAIN_NAME
  --os-project-domain-id OS_PROJECT_DOMAIN_ID
                                Admin project's domain id, Default
                                OS_PROJECT_DOMAIN_ID
  --os-project-domain-name OS_PROJECT_DOMAIN_NAME
                                Admin user's domain id, Default
                                OS_USER_DOMAIN_NAME

See "sidecar help COMMAND" for help on a specific command.

</pre>
