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
try:
    import simplejson as json
except ImportError: 
    import json
import datetime
from novaclient import client as nova_client
CONF = cfg.CONF
LOG = log.getLogger(__name__)

class HostEvacuateController(RestController):
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

        # Getting the configuartion file and its details
        LOG.info("Getting the configuration file(/etc/sidecar/sidecar.conf")
        config_file = cfg.CONF.config_file[0]
        config = ConfigParser.ConfigParser()
        config.read(config_file)

        # Nova connection details
        LOG.info("Connecting with the the nova using the nova client")
        nova_username = config.get('keystone_authtoken', 'username', '')
        nova_version = config.get('keystone_authtoken', 'auth_version', '2')
        nova_password = config.get('keystone_authtoken', 'password', '')
        nova_auth_url = config.get('keystone_authtoken', 'auth_url', '')
        nova_auth_plugin = config.get('keystone_authtoken', 'auth_plugin', '')
        nova_tenant_name = config.get('keystone_authtoken', 'tenant_name', '')
        self.nova_conn = nova_client.Client(nova_version, nova_username, nova_password, nova_tenant_name, nova_auth_url, insecure=False)

        # Log, dead time and json file details
        LOG.info("Getting the details from the conf file")
        self.evacuate_deadtime = config.get('evacuate_details', 'dead_time', '180')
        self.failure_threshold = config.get('evacuate_details', 'failure_threshold', '300')
        self.shared_storage_flag = config.get('evacuate_details', 'shared_storage_flag', False)

        #Making the database connection
        LOG.info("Making the database connection.")
        self.evacuates = sql_model.Evacuate()

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
            logs = self.evacuates.list_log(kw)
            LOG.error("Got all the logs.")
            return {"logs": logs}
        except Exception as err:
            LOG.error("Error in getting all the logs.")
            return exception_handle(err)

    @expose(generic=True, template='json', content_type="application/json")
    def post(self, **kw):
        """
        # | Function to do the evacuation
        # | Arguments: None
        # |
        # | Returns: Json object
        """

        #Calling the event/health check depend on the parameter
        if 'id' in kw['event']:
            LOG.info("Calling the evacuate_event function.")
            self.evacuate_event(kw['event']['id'])
        else:
            LOG.info("Calling the evacuate_healthcheck function.")
            self.evacuate_healthcheck()

    def evacuate_healthcheck(self):
        """
        # | Function to handle the evacuation of the events via REST API call
        # |
        # | Arguments: NA
        # |
        # | Returns: Null
        """
        
        # | Getting the configuration values from the /etc/sidecar/sidecar.conf file
        dead_time = self.evacuate_deadtime
        current_time = datetime.datetime.utcnow()

        try:
            hypervisor_servers_list = self.nova_conn.hypervisors.list()
            LOG.info("Got the list of servers")
        except Exception, e:
            LOG.error(e)
            raise  Exception("Error in the hypervisor list.")

        # Checking each hypervisor to execute the evacuation.
        LOG.info("Checking each hypervisor to execute the evacuation.")	
        for hyper_visor in hypervisor_servers_list:
            LOG.info("Getting the details of the logs.")
            log_detail = self.evacuates.get_log_detail(hyper_visor.hypervisor_hostname)

            #Fetching the servers within each hypervisor
            LOG.info("Fetching the server list within the hypervisor " + hyper_visor.hypervisor_hostname)
            hype_vm_uuids  = self.nova_conn.hypervisors.search(hyper_visor.hypervisor_hostname, servers=True)
            if hasattr(hype_vm_uuids[0], 'servers'):
            
                # Getting the details and assigning to the variable (used to check in future)
                if len(log_detail) > 0:
                    log_id = log_detail.get("id")
                    hypervisor_name_log = log_detail.get("hypervisor_name")
                    down_since_log = log_detail.get("down_since")
                    evacuated_log = log_detail.get("evacuated")
                    event_id_log = log_detail.get("event_id")
                    prev_time_log = log_detail.get("prev_time")
                    creation_time_log = log_detail.get("creation_time")
                    prev_time_log = str(prev_time_log)+ '.000000'
                else:
                    down_since_log = 0
                    evacuated_log = False
                    prev_time_log = str(current_time)
                    event_id_log = 0
                
                # Creating or deleting the logs depend on the status of the hypervisor state
                LOG.info("Creating or deleting the logs depend on the status of the hypervisor state")	
                if hyper_visor.state == 'up':
                    # | If the hypervisor is up
                    # | then delete the log from the log details
                    #down_since_log = 0
                    #evacuated_log = False		
                    LOG.info("Since the hypervisor is up, we are deleting the log from the evacuation_log table and marking the event as completed.")
                    self.update_event_status(hyper_visor.hypervisor_hostname, 'completed')
                    
                elif hyper_visor.state == 'down':
                    # | if the hypervisor is down then calculating the down time
                    # | and updating the log table accordingly
                    LOG.info("Calculating the down time of the hypervisor " + str(hyper_visor.hypervisor_hostname))
                    diff = current_time - datetime.datetime.strptime(str(prev_time_log), "%Y-%m-%d %H:%M:%S.%f")
                    down_since_log = diff.total_seconds()
                    LOG.info("Hypervisor is down for "+ str(down_since_log) + "seconds.")
                
                    # Updating the log table with the down time
                    if len(log_detail):
                        update_logs = {'down_since': down_since_log,
                                       'evacuated': 'False', 
                                       'prev_time': str(prev_time_log),
                                       'hypervisor_name': hyper_visor.hypervisor_hostname
                               }
                        self.evacuates.update_log(hyper_visor.hypervisor_hostname, update_logs)
                        LOG.info("Updated the log table with new value of down time as "+ str(down_since_log))
                    else:
                        create_logs = {'hypervisor_name' : hyper_visor.hypervisor_hostname,
                                       'down_since': down_since_log,
                                       'evacuated': 'False', 
                                       'event_id':  123,
                                       'prev_time': str(current_time),
                                       'event_creation_time': str(current_time) 
                                       }
                        self.evacuates.createLog(create_logs)
                        LOG.info("Created entry the log table with new value of down time as "+ str(down_since_log))

                    # | Checking the down time 
                    # | If more dead time then proceed for the evacuation
                    LOG.info("Hypervisor is down since:" + str(down_since_log) + "and dead time is :"  + str(dead_time))
                    if int(down_since_log) >= int(dead_time):
                        LOG.info("Hypervisor is down for " + str(down_since_log))
                        LOG.info("Searching the events using the hyervisor name.")
                        search_event = {'name': hyper_visor.hypervisor_hostname, 'filter_out': True}
                        event_details = self.evacuates.list_events(search_event)
                        LOG.info("Got the list of hypervisors")

                        # | If list exists the proceeding with the status check
                        # | else creating the event  
                        if len(event_details) > 0:
                        
                            #Getting the details of event
                            for event_detail in event_details:
                                event_status = event_detail.get("event_status")
                                event_vm_list = event_detail.get("vm_uuid_list")
                                event_extra_list = event_detail.get("extra")
                                event_name = event_detail.get("name")
                                event_id  = event_detail.get("id")
                            
                                LOG.info("Status of the event is " + event_status)
                                if event_status == 'running':
                                    self.evacuate_instances(event_extra_list, event_id)
                                elif event_status == 'migrating':
                                    # Getting the server details with the hypervisor name
                                    hype_vm_uuids  = self.nova_conn.hypervisors.search(hyper_visor.hypervisor_hostname, servers=True)
                                    LOG.info("Found servers in the hypervisor with name" + hyper_visor.hypervisor_hostname)

                                    # If server list is 0 then evacuation is done and 
                                    # Deleting the event and log details
                                    if hasattr(hype_vm_uuids[0], 'servers'):
                                        LOG.info("If server list is not 0 then checking the status of the event.")
                                        self.check_status(event_id)
                                    else:
                                    
                                        # | If the event_status is scompleted and
                                        # | no furthur vms are present in node
                                        # | update the status as completed
                                        self.update_event_status(hyper_visor.hypervisor_hostname, 'completed')
                        else:     
                            LOG.info("Creating the event and starting the evacuation.")
                            event_id = self.create_evacuate(hyper_visor)
                            self.evacuate_event(event_id)
            else:
                LOG.info('No Servers are present within this hypervisor so updating the event with hypervisor name '+ hyper_visor.hypervisor_hostname)
                self.update_event_status(hyper_visor.hypervisor_hostname, 'completed')

    def check_status(self, event_id):
        """
        # | Function to check the status and update the event table accordingly
        # |
        # | Arguments:
        # |     <event_id>: id of the event
        # | Returns: Null
        """

        #Getting the details of the event using event id
        LOG.info('Going to change the status of the event depend on the threshold.')
        event_detail = self.evacuates.get_detail(event_id)
        creation_time = event_detail.get("event_create_time")
        current_time = datetime.datetime.utcnow()
        failure_threshold = self.failure_threshold
        creation_time = str(creation_time)+ '.000000'
        diff = current_time - datetime.datetime.strptime(str(creation_time), "%Y-%m-%d %H:%M:%S.%f")
        diff = diff.total_seconds()

        # | If the failure threshold is more 
        # | than the failure time then marking the event as failure
        if int(failure_threshold) <= int(diff):
            LOG.info('Changing the status to FAILURE.')	
            error_data = {'event_status' : 'failure', 'extra': 'NULL'}
            self.evacuates.update_event(event_id, error_data)

    def create_evacuate(self, hyper_visor):
        """
        # | Function to check the status and update the event table accordingly
        # |
        # | Arguments:
        # |     <event_id>: id of the event
        # | Returns: Null
        """

        # | searching the hypervisor and 
        # | getting the servers list
        vm_uuid_list = []
        try:
            servers_list = self.nova_conn.hypervisors.search(hyper_visor.hypervisor_hostname, servers=True)
        except Exception , e:
            LOG.error(e)		
            raise  Exception("Error in the hypervisor search.")

        LOG.info("Making the servers list")
        for server in servers_list[0].servers:
            vm_uuid_list.append(server['uuid'])
    
        # If the event is not created, then lets go for event creation
        create_data = {'name' : hyper_visor.hypervisor_hostname,
            'node_uuid': str(hyper_visor.id),
            'vm_uuid_list': vm_uuid_list
        }

        # | Creating the events
        event_id = self.evacuates.createEvent(create_data)
        LOG.info("Created the event with event id :" + str(event_id))
        return event_id

    def evacuate_event(self, event_id, targethost=None):
        """
        # | Function to do the event evacuation with the event id
        # |
        # | Arguments:
        # |     <event_id>: id of the event
        # |     <targethost>: Target host to which evacuation need to do 
        # | Returns: Null
        """

        # | Getting the server uuid list from table using event id
        # | for making the error list
        event_detail = self.evacuates.get_detail(event_id)
        hypervisor_name = event_detail.get("name")
        hype_vm_uuids  = self.nova_conn.hypervisors.search(hypervisor_name, servers=True)
        if hasattr(hype_vm_uuids[0], 'servers'):

            event_vm_list = event_detail.get("vm_uuid_list")
            error_vm_list = []

            #Looping through each server and do the evacuation.
            LOG.info("Looping through each server and do the evacuation.")
            for event_vm in event_vm_list:
                LOG.info("Started the evacuation if event with id:" + str(event_vm))
                state = self.do_evacuate(event_vm, targethost)
                LOG.info("State of the evacuation of  the server  with id:" + str(event_vm) + "is " + str(state))

                #If the status false then adding the vm list as error list
                if state == False:
                    error_vm_list.append(event_vm)
   
            # | if the error list is up then making the status as running
            # | else making as completed
            if len(error_vm_list) > 0:
                error_data = {'event_status' : 'running', 'extra': error_vm_list}
                self.evacuates.update_event(event_id, error_data)
                LOG.info("Made the status of event with id:" + str(event_id) + "to running.")

            elif len(error_vm_list) == 0:
                complete_data = {'event_status' : 'migrating', 'extra': 'NULL'}
                self.evacuates.update_event(event_id, complete_data)
                LOG.info("Made the status of event with id:" + str(event_id) + "to completed.")	
        else:
            update_event_status(hypervisor_name, 'completed')

    def update_event_status(self, hypervisor_name, status):
        """
        # | Function to do update the events
        # |
        # | Arguments:
        # |     <hostname>: host name
        # |     <status>: status of the event
        # | Returns: Null
        """

        #If the status is in completed state, then removeing the log and updating the event with completed status
        if status == 'completed':
            self.delete_log(hypervisor_name)
            search_event = {'name': hypervisor_name, 'filter_out': True}
            event_details = self.evacuates.list_events(search_event)
            LOG.info("Got the list of hypervisors")

            # | If list exists the proceeding with the status check
            # | else creating the event  
            if len(event_details) > 0:
            
                #Getting the details of event
                for event_detail in event_details:
                    event_id  = event_detail.get("id")                 
                    complete_data = {'event_status' : 'completed', 'extra': 'NULL'}
                    self.evacuates.update_event(event_id, complete_data)
                    LOG.info("Event with id " + event_id + "is completed.")

    def evacuate_instances(self, instances, event_id, targethost=None):
        """
        # | Function to do the instance evacuation
        # |
        # | Arguments:
        # | 	<instances>: list of instances
        # |     <event_id>: id of the event
        # |     <targethost>: Target host to which evacuation need to do 
        # | Returns: Null
        """

        # Doing evacuation of each instances and updating status
        error_vm_list = []
        for instance in instances:
            LOG.info("Started evacuating the instance with id "+ str(instance))
            state = self.do_evacuate(instance, targethost)
            if state == False:
                error_vm_list.append(instance)
   
        # Updating the status to running/completed depend on the vm list 
        if len(error_vm_list) > 0:
            run_data = {'event_status' : 'running', 'extra': error_vm_list}
            self.evacuates.update_event(event_id, run_data) 
            LOG.info("Updated the status of event with id " + str(event_id) + "to running")
            self.check_status(event_id)		
        elif len(error_vm_list) == 0:
            error_data = {'event_status' : 'migrating', 'extra': 'NULL'}
            self.evacuates.update_event(event_id, error_data)
            LOG.info("Updated the status of event with id " + str(event_id) + "to migrating")

    def do_evacuate(self, instance, targethost=None):
        """
        # | Function to do the evacuation
        # |
        # | Arguments:
        # |     <instance>:  instances
        # |     <targethost>: Target host to which evacuation need to do 
        # | Returns: Null
        """

        # | Doing the evacuation od the instances
        try:
            state = self.nova_conn.servers.evacuate(server=instance, host=targethost, on_shared_storage=self.shared_storage_flag)
            LOG.info("Done the evacuation of the instance with id" + str(instance))
            return True
        except Exception, e:
            LOG.info(e)
            return False

    	
    def delete_log(self, hypervisor_name):
        """
        # | Function to delete the event as well as the log entries
        # |
        # | Arguments:
        # |     <hypervisor_name>: Name of the hypervisor 
        # | Returns: Null
        """

        # | Doing the evacuation of the instances
        self.evacuates.delete_log(hypervisor_name)
        LOG.info("Log of hypervisor with name " + hypervisor_name + "is deleted.")

def exception_handle(e):
    """
    # | Function to handle the exception
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
