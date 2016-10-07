# -*- coding: utf-8 -*-
# _______________________________________________________
# | File Name: RootController.py                        |
# |                                                     |
# | Package Name: Python-Sidecar REST API               |
# |                                                     |
# | Version: 2.0                                        |
# |                                                     |
# | Sofatware: Openstack                                |
# |_____________________________________________________|
# | Copyright: 2016@nephoscale.com                      |
# |                                                     |
# | Author:  info@nephoscale.com                        |
# |_____________________________________________________|

from pecan         import expose
from pecan.rest    import RestController
from sidecar       import rbac
from sidecar.model import sidecar_model as sql_model
from sidecar       import exception, rbac
from oslo_log      import log
from oslo_config   import cfg
import pecan, sidecar.validation as validation, ConfigParser, collections
try:   import simplejson as json
except ImportError: import json

CONF = cfg.CONF
LOG = log.getLogger(__name__)

class EventController(RestController):
    """
    # | Class to handel the REST API part of events in Evacuate 
    # | During post and put, we need a 307 redirection, which is
    # | Difficult if we handel it with index_GET, index_POST, etc.
    # | So AS per the doc http://pecan.readthedocs.io/en/latest/rest.html#url-mapping
    # | We have inherited this class from RestController    
    """
    def __init__(self, data=None):
        """
        # | Constructor function
        # | 
        # | Arguments: None
        # |
        # | Return Ttype: Void
        """
        self.evacuates = sql_model.Evacuate()

    @expose(generic=True, template='json')
    def get(self, event_id):
        """
        # | Method to get get detail of an event
        # |
        # | Arguments: event id
        # |
        # | Returns: Dictonary
        """
        try:
            rbac.enforce('get_detail', pecan.request) 
            result = self.evacuates.get_detail(event_id)
            return { "event": result }
        except Exception as e:
            return exception_handle(e)
     
    @expose(generic=True, template='json')
    def get_all(self, **kw):
        """
        # | Function to list the events
        # |
        # | @Arguments:
        # |     <kw>: Url query parameters
        # |
        # | @Returns: Json response
        """
        try:
            rbac.enforce('list_events', pecan.request)
            events = self.evacuates.list_events(kw)
            return {"events": events}
        except Exception as err:
            return exception_handle(err)
       
    @expose(generic=True, template='json', content_type="application/json")
    def post(self):
        """
        # | Function to create a new event
        # |
        # | Arguments: None
        # |
        # | Returns: Json object
        """
        try:
            rbac.enforce('create_event', pecan.request)
            valid = validation.Validation()
            valid.json_header()
            json_data = valid.json_data('create_event', pecan.request.body_file.read())
            data = json_data['event']
            new_event_id = self.evacuates.createEvent(data)
            pecan.response.status = 201
            return { "event": self.evacuates.get_detail(new_event_id)}
        except Exception as e:
            return exception_handle(e)
              
    @expose(generic=True, template='json', content_type="application/json")
    def put(self, event_id):
        """
        # | Function to handel the edit part of an event
        # |
        # | Arguments:
        # | <event_id>: The event id which will be edited
        # | 
        # | Returns: Dictionary
        """
        try:
            rbac.enforce('edit_event', pecan.request)
            valid = validation.Validation()
            valid.json_header()
            json_data = valid.json_data('edit_event', pecan.request.body_file.read())
            self.evacuates.update_event(event_id, json_data['event'])
            pecan.response.status = 204
        except Exception as e:
            print e.message
            return exception_handle(e)
          
    @expose(generic=True, template='json',  content_type="application/json")
    def delete(self, event_id):
        """
        # | Function to handel the delete event via REST API call
        # |
        # | Arguments:
        # |     <event_id>: id of the event
        # |
        # | Returns: Null
        """
        try:
            rbac.enforce('delete_event', pecan.request)
            self.evacuates.delete_event(event_id)
            pecan.response.status = 204
            return {}
        except Exception as e:
            return exception_handle(e)
     
def exception_handle(e):
    """
    # | Function to handel the exception
    # |
    # | Arguments: None
    # |
    # | Returns: error
    """
    LOG.error(e.message)
    if hasattr(e, 'code') and hasattr(e, 'title'):
        # If code is present, then it is a cutom exception
        # made by us
        return send_error(e.code, e.title, e.message)
    return send_error(500, 'Internal Server Error', 'Unknown error occured')

def send_error(code, title, message):
    """
    # | Functon to retun the exception
    # |
    # | Arguments: 
    # | <code>: Error code  
    # | <title>: Http tile
    # | <message>: Exception message
    # |
    # | Returns: Dictionary
    """
    pecan.response.status = code
    error =  collections.OrderedDict()
    error["code"]    = code
    error["title"]   = title
    error["message"] = message
    return { "error": error }
