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
 
import pecan, json, event, host_evacuation
from pecan         import expose, redirect
from oslo_config   import cfg
from sidecar       import rbac

class EvacuateController:
    """
    # | Evacutes controller
    """
    events = event.EventController()
    hostevacuate = host_evacuation.HostEvacuateController()

class V2Controller(object):
    """
    # | Version 2 controller.
    """
    evacuates = EvacuateController()

    @expose(generic=True, template='json')
    def index(self):
        """
        # | Index function for the version 2
        # |
        # | @Arguments: Void
        # |
        # | @Returns: Dictionary containg the version info
        """
        return  {"v2": {"date":"2016-08-07T00:00:00", "status":"current"}}

class RootController(object):
    """
    | # Root Controller Class
    """
    v2 = V2Controller()

    def __init__(self):
        """
        # | Constructor function
        # | 
        # | Arguments: None
        # |
        # | Return Ttype: Void
        """
    
    @expose(generic=True, template='json')
    def index(self):
        """
        # | Index function of the rest api
        # |
        # | Arguments: None
        # |
        # | Returns JSON
        """
        return {"versions": [self.v2.index()]}

