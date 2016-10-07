# File Name: tabs.py
#
# @Software: Openstack Horizon
#
# @version: Liberity
#
# @Package: Sidecar 
#
# Start Date: 31th Aug 2016
from django.utils.translation import ugettext_lazy as _
from horizon import tabs, exceptions
from openstack_dashboard.dashboards.sidecar.events import tables
from django.core.urlresolvers import reverse_lazy, reverse
from horizon.utils import memoized
from django.conf import settings
from sidecarclient import client
from django.conf import settings
from pprint import pprint
import requests
import json
class EventListingTab(tabs.TableTab):
    """ 
    Class to Display the Evacuation Events
    """
    name = _("Evacuation Events Tab")
    slug = "evacuation_events_listing"
    table_classes = (tables.EventListTable, )
    template_name = ("horizon/common/_detail_table.html")
    preload = False
    #_has_more_data = False
    #_has_prev_data = False
 
    def get_events_data(self):
        """
        # | Function to get the ticket list for the given user
        # |
        # | @Arguments: None
        # |
        # | @Return Type: Dictionary
        """
        try:

            #Configuring all the access settings
            #Values are taken from settings.py file
            sidecar = client.Client(
                  auth_version = getattr(settings, "SC_AUTH_VERSION"),
                  username = getattr(settings, "SC_USERNAME"),
                  password = getattr(settings, "SC_PASSWORD"),
                  auth_url = getattr(settings, "SC_AUTH_URL"),
                  region_name = getattr(settings, "SC_REGION_NAME"),
                  tenant_name = getattr(settings, "SC_TENANT_NAME"),
                  timeout = getattr(settings, "SC_TIMEOUT"),
                  insecure = getattr(settings, "SC_INSECURE")
            )
            
            #Getting the field name from the post
            args = {}
            field_name = self.request.POST.get('events__eventfilter__q_field', 'default_value')
            if field_name == 'node_uuid':
                args['node_uuid'] = self.request.POST['events__eventfilter__q']
            elif field_name == 'event_create_time':
                args['event_create_time'] = self.request.POST['events__eventfilter__q']
            elif field_name == 'vm_uuid_list':
                args['vm_uuid_list'] = self.request.POST['events__eventfilter__q']
            elif field_name == 'id':
                args['id'] = self.request.POST['events__eventfilter__q']
            elif field_name == 'name':
                args['name'] = self.request.POST['events__eventfilter__q']
            elif field_name == 'event_status':
                args['event_status'] = self.request.POST['events__eventfilter__q']

            #Fetching the event list and returning it
            events = sidecar.events.list(**args)
            return events
        except Exception, e:
	    
            exceptions.handle(self.request, "Unable to fetch events.....")
            return []

class Event:
    name = uuid = event_status = event_create_time = event_complete_time = node_uuid = vm_uuid_list = extra = None

def obj_dic(dict_values):
    for values in dict_values:
        value = Event()
        value.id = values['id']
        value.event_status = values['event_status']
        value.node_uuid = values['node_uuid']
        value.name = values['name']
        value.event_complete_time = values['event_complete_time']
        #value.uuid = values['uuid']
        value.event_create_time = values['event_create_time']
        value.vm_uuid_list = values['vm_uuid_list']
        value.extra = values['extra']
        yield value

class EvacuationEventsTab(tabs.TabGroup):
    slug = "evacuation_events_tab"
    tabs = (EventListingTab,)
    sticky = True

