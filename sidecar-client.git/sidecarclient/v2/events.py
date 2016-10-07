# -*- coding: utf-8 -*-
# ___________________________________________________________________________________
# | File Name: events.py                                                            |
# |                                                                                 |
# | Package Name: Python-Sidecarclient to handel the sidecar REST API               |
# |                                                                                 |
# | Version: 2.0                                                                    |
# |                                                                                 |
# | Sofatware: Openstack                                                            |
# |_________________________________________________________________________________|
# | Copyright: 2016@nephoscale.com                                                  |
# |                                                                                 |
# | Author: Binoy MV <binoymv@poornam.com>, Dinesh Patra<dinesh.p@poornam.com>      |
# |                                                                                 |
# | Author:  info@nephoscale.com                                                    |
# |_________________________________________________________________________________|
from __future__ import print_function
from sidecarclient import exception
import sidecarclient

class Event(object):
    """
    # | Class to provide Event Object
    """

    # | id: id of the event
    # |
    # | Default Value: None
    # |
    # | Type: String
    id = None

    # | name: Name of the event
    # |
    # | Default Value: None
    # |
    # | Type: String
    name = None

    # | vm_uuid_list: List containg instance ids
    # |
    # | Default Value: Empty List
    # |
    # | Type: List
    vm_uuid_list = None
    
    # | node_uuid: Id of the host taking part in evacuates
    # |
    # | Default Value: None
    # |
    # | Type: String
    node_uuid = None

    # | event_status: Status of the event
    # |
    # | Default Value: None
    # | 
    # | Type: String
    # |
    # | Allowed Values: created, running, completed
    event_status = None

    # | extra: Extra value for the event
    # |
    # | Default Value: {}
    # |
    # | Type: dictionary
    extra = None

    # | event_create_time: Event create time in yyy-mm-dd HH:ii:ss format
    # |
    # | Default Value: None
    # |
    # | Type: string
    event_create_time = None

    # | event_complete_time: Event create time in yyy-mm-dd HH:ii:ss format
    # |
    # | Default Value: None
    # |
    # | Type: string
    event_complete_time = None

    def __init__(self, event):
        """ Initialization Function """
        self.id            = event['id']
        self.name                = event['name']
        self.vm_uuid_list        = event['vm_uuid_list']
        self.node_uuid           = event['node_uuid']
        self.event_status        = event['event_status']
        self.extra               = event['extra']
        self.event_create_time   = event['event_create_time']
        self.event_complete_time = event['event_complete_time']

class ResultGenerator(object):
    """ Result Generator object """

    def __init__(self, event_list):
        # | Intialziation function
        # |
        # | Arguments: event_list
        # |
        # | Returns None        
        self._count = len(event_list['events'])
        self._events = event_list['events']
        self._position = 0

    def __iter__(self):
        return self

    def __len__(self):
        return self._count

    def __next__(self):
        return self.next()

    def next(self):
        if self._position < self._count:
            # | IF POSITION IS LESS THAN TOTAL ELEMT
            # | Continue the looping
            obj =  Event(self._events[self._position])
            self._position = self._position + 1
            return obj
        raise StopIteration() 

class EventsHttp(object):
    """
    # | Class to make api request
    """
    def __init__(self, obj):
        """ 
        # | Initialization function
        # |
        # | Arguments: 
        # | <obj>: Instabnce of the v2.client
        """
        if type(obj) != sidecarclient.v2.client.Client:
            raise exception.NotSupported("Not an instance of sidecarclient.")
        self._obj = obj

        
    def list(self, id=None, name=None, node_uuid=None, event_create_time=None,
        min_event_create_time=None, max_event_create_time=None, marker=None, limit=None, event_status=None):
        """
        # | Function to list the evenets
        # |
        # | Arguments: filter options
        # |     :id          <string>: event id
        # |     :name        <string>: name of the event
        # |     :node_uuid   <string>: Host id
        # |     :event_create_time <string in yyyy-mm-dd HH:ii::ss format>: Event create time
        # |     :min_event_create_time <strimg in yyyy-mm-dd HH:ii::ss format>: Minimum time when the event was created
        # |     :max_event_create_time <strimg in yyyy-mm-dd HH:ii::ss format>: Maximum time when the event was created
        # |     :marker <last event id>: Minimum time when the event was created
        # |     :limit  <integer>: Minimum time when the event was created
        # |
        # | Returns: Events generator object
        """
        self._obj.authenticate()
        headers = {"X-Auth-Token":self._obj.authenticated_token}
        url     = self._obj.sidecar_url + '/evacuates/events?'
                
        # | Createing filter options
        if id:
            url = url + "id=%s&" % (id)
        if name:
            url = url + "name=%s&" % (name)
        if event_status:
            url = url + "event_status=%s&" % (event_status)
        if node_uuid:
            url = url + "node_uuid=%s&" % (node_uuid)
        if event_create_time:
            url = url + "event_create_time=%s&" % (event_create_time)
        if min_event_create_time:
            url = url + "min_event_create_time=%s&" % (min_event_create_time)
        if max_event_create_time:
            url = url + "max_event_create_time=%s&" % (max_event_create_time)
        if marker:
            url = url + "marker=%s&" % (marker)
        if limit:
            url = url + "limit=%s&" % (limit)
 
        # | Make http request
        data = self._obj.http.get(url, headers)
        return ResultGenerator(data['body'])

    def create(self, vm_uuid_list=[], name=None, node_uuid=None):
        """
        # | Function to create a new event
        # |
        # | Arguments: filter options
        # |     :name         <string>:        name of the event
        # |     :node_uuid    <string>:        Host id
        # |     :vm_uuid_list <list of strings>list containg instance ids
        # |
        # | Returns: Event object
        """
        self._obj.authenticate()
        headers = {"X-Auth-Token":self._obj.authenticated_token}
        url = self._obj.sidecar_url + '/evacuates/events'        
        data = {
            "event": {
                "name": name,
                "vm_uuid_list": vm_uuid_list,
                "node_uuid": node_uuid
            }
        }
        data = self._obj.http.post(url,  data, headers)
        return Event(data['body']['event'])

    def detail(self, id):
        """
        # | Function to get the detail of an event
        # |
        # | Arguments:
        # |  :id <string> Event id
        # |
        # | Returns: Event Object
        """
        self._obj.authenticate()
        headers = {"X-Auth-Token":self._obj.authenticated_token}
        url = self._obj.sidecar_url + '/evacuates/events/%s' %(id)
        data = self._obj.http.get(url, headers)
        return Event(data['body']['event'])

    def edit(self, id = None, name=None, event_status=None, node_uuid=None, vm_uuid_list=[]):
        """
        # | Function to edit the event
        # |
        # | Arguments:
        # |     :id          <string>: event id
        # |     :name        <string>: name of the event
        # |     :node_uuid   <string>: Host id
        # |     :event_create_time <string in yyyy-mm-dd HH:ii::ss format>: Event create time
        # |     :event_status <string, either running, completed>
        # |
        # | Returns:
        # |   None
        """
        event_id = id
        self._obj.authenticate()
        headers = {"X-Auth-Token":self._obj.authenticated_token}
        url = self._obj.sidecar_url + '/evacuates/events/%s' %(id)
        data = {}
        data["event"] = {}

        # | Creating event list
        if name:
            data["event"]["name"] =  name
        if event_status:
            data["event"]["event_status"] = event_status
        if node_uuid:
            data["event"]["node_uuid"] = node_uuid
        if vm_uuid_list:
            data["event"]["vm_uuid_list"] = vm_uuid_list
        data = self._obj.http.put(url, data, headers)
    
    def delete(self, id):
        """
        # | Function to get the detail of an event
        # |
        # | Arguments:
        # |  :id <string> Event id
        # |
        # | Returns: Event Object
        """
        self._obj.authenticate()
        headers = {"X-Auth-Token":self._obj.authenticated_token}
        url = self._obj.sidecar_url + '/evacuates/events/%s' %(id)
        data = self._obj.http.delete(url, headers)

    def evacuate_runEvent(self, id = None):
        """
        # | Function to run a evacuate event
        # | 
        # | Arguments
        # |   :id  <string>: event id
        # | Returns:
        # |   None
        """
        self._obj.authenticate()
        headers = {"X-Auth-Token":self._obj.authenticated_token}
        url = self._obj.sidecar_url + '/evacuates/hostevacuate'
        data = {"event": {"id": id}}
        data = self._obj.http.post(url,  data, headers)

    def evacuate_healthcheck(self):
        """
        # | Function to execute and fetch the healthcheck details for all events
        # |
        # | Arguments
        # |   :id <string>: event_id
        # | Returns:
        #|   None
        """
        self._obj.authenticate()
        headers = {"X-Auth-Token":self._obj.authenticated_token}
        url = self._obj.sidecar_url + '/evacuates/hostevacuate'
        data = {"event": {"name": 'name',"vm_uuid_list": 'vm_uuid_list',"node_uuid": 'node_uuid'}}
        data = self._obj.http.post(url,  data, headers)
