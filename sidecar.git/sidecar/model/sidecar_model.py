# -*- coding: utf-8 -*-
# _______________________________________________________
# | File Name: sidecar_model.py                         |
# |                                                     |
# | Package Name: Python-Sidecar MODEL API              |
# |                                                     |
# | Version: 2.0                                        |
# |                                                     |
# | Sofatware: Openstack                                |
# |_____________________________________________________|
# | Copyright: 2016@nephoscale.com                      |
# |                                                     |
# | Author:  info@nephoscale.com                        |
# |_____________________________________________________|

#importing the packages
from oslo_config        import cfg
from oslo_log           import log
from oslo_db.sqlalchemy import models
from sqlalchemy.ext     import declarative
from sqlalchemy         import *
from sqlalchemy.sql     import select
from sqlalchemy         import Table, Column, Integer, String, MetaData, ForeignKey, DATETIME, Enum
from sidecar            import exception
from sqlalchemy.orm     import sessionmaker
from sqlalchemy.dialects.postgresql import UUID
try:   
    import simplejson as json
except ImportError: 
    import json
import sqlalchemy, ConfigParser, enum, uuid, datetime, collections

CONF = cfg.CONF
LOG = log.getLogger(__name__)

# READ THE CONNECTION VARIABLE
try:
    config_file = cfg.CONF.config_file[0]
    config = ConfigParser.ConfigParser()
    config.read(config_file) 
    sql_connection = config.get('database', 'connection', '')   
    LOG.info("Getting the db configuration and ding the connection.)")
except Exception as e:
    LOG.error(str(e))
    sql_connection = ''

class Evacuate():
    """
    # | Evacuate model
    """
    metadata = MetaData()
    engine   = create_engine(sql_connection, pool_recycle=3600)
    conn     = engine.connect()
    
    #Creating the tables
    evacuate_events = Table('evacuate_events', metadata,
        Column('id',                  String(100),       primary_key=True,  unique=True, nullable=False),  # Event id column
        Column('name',                String(100),       default='',        nullable=False),
        Column('event_status',        Enum('created', 'completed', 'running', 'failure', 'migrating'), default='created', nullable=True),
        Column('event_create_time',   DATETIME,         default='0000-00-00 00:00:00', nullable=False),
        Column('event_complete_time', DATETIME,         default='0000-00-00 00:00:00', nullable=True),
        Column('node_uuid',           Text),
        Column('vm_uuid_list',        Text),
        Column('extra',               Text)
    )

    #Creating a configuration table
    evacuation_log   = Table('evacuation_log', metadata,
         Column('id',                  Integer(),       primary_key=True,  unique=True, nullable=False),  # Log id column
         Column('hypervisor_name',     String(200),       default='',        unique=True, nullable=False),
         Column('down_since',          Float(),       default='0',        nullable=True),
         Column('evacuated',           Enum('True', 'False'), default='False', nullable=True),
         Column('event_id',            String(100),       default='',        nullable=False),
         Column('prev_time',           DATETIME,          default='0000-00-00 00:00:00', nullable=False),
         Column('event_creation_time', DATETIME,          default='0000-00-00 00:00:00', nullable=False)
    )

    metadata.create_all(engine)
    LOG.info("Created the tables.)")
    
    def createEvent(self, kw):
        """
        name createEvent
        Params: event data
        Return : Json data
        """

        #Setting the parameters for the event creation
        unique_id = uuid.uuid4().hex
        arg = {
            "id": unique_id,
            "name": kw['name'],
            "event_status": "created",
            "event_create_time": datetime.datetime.now(),
            "node_uuid": kw["node_uuid"],
            "vm_uuid_list": json.dumps(kw["vm_uuid_list"])
        }
        #Inserting the data
        ins = self.evacuate_events.insert().values(arg)
        result = self.conn.execute(ins)
        LOG.info("Event created with id " + str(unique_id))
        return unique_id

    def get_detail(self, uuid):
        """
        # | Function to get the detail of an event
        # |
        # | Arguments:
        # |  <uuid>: Id of the event
        # |
        # | Returns: Json
        """

        #Getting the detail of the event
        get_data_select = select([self.evacuate_events]).where(self.evacuate_events.c.id == uuid)
        get_data = self.conn.execute(get_data_select)
        LOG.info("Getting the event details")

        #Raise exception if no event is present else fetching the one
        if not get_data.rowcount:
            LOG.error("No event with id " + uuid + " found.")
            raise exception.NotFound("No event with id " + uuid + " found.")
        data = get_data.fetchone()
        result = collections.OrderedDict()
        result["id"]                  = uuid
        result["name"]                = data["name"]
        result["event_status"]        = data["event_status"]
        result["event_create_time"]   = data["event_create_time"]
        result["event_complete_time"] = data["event_complete_time"]
        result["node_uuid"]           = data["node_uuid"]
        result["vm_uuid_list"]        = None
        result['extra']               = None
        
        # If the proper data is there 
        # then convert them into json
        if data["vm_uuid_list"]:
            result["vm_uuid_list"] = json.loads(data["vm_uuid_list"])
        if data['extra']:
            result['extra'] = json.loads(data['extra'])        
        return result

    def list_events(self, args={}):
        """
        # | Method to list the events
        # |
        # | Arguments: Distionary containg the flter values
        # |
        # | Returns Distionary
        """

        #Setting the allowed args for the serach
        allowed_args = [
            'id',
            'name',
            'event_status',
            'node_uuid', 
            'event_create_time', 
            'min_event_create_time',
            'max_event_create_time', 
            'marker',
            'limit',
            'filter_out'
        ]
        valid_args = {}
        for arg in args:
            # | For each given argument
            # | If it matches with allowed argument
            # | Then treat it as valid arg
            if arg in allowed_args:
                valid_args[arg] = args[arg]

        # Okay Bow lets start our query builder
        get_event_list = select([self.evacuate_events])
            
        for key in valid_args:
            if type(valid_args[key])==bool:
                val = valid_args[key]
            else:
                val = valid_args[key].strip()
       
            if not val:
                continue;
            if key == "id":
                get_event_list = get_event_list.where(self.evacuate_events.c.id == val)
            if key == "name":
                get_event_list = get_event_list.where(self.evacuate_events.c.name.like('%' + val + '%'))
            if key == "event_status":
                get_event_list = get_event_list.where(self.evacuate_events.c.event_status.like('%' + val + '%'))
            if key == 'node_uuid':
                get_event_list = get_event_list.where(self.evacuate_events.c.node_uuid == val)
            if key == 'event_create_time':
                get_event_list = get_event_list.where(self.evacuate_events.c.event_create_time == val)
            if key == 'min_event_create_time':
                get_event_list = get_event_list.where(self.evacuate_events.c.event_create_time >= val)
            if key == 'max_event_create_time':
                get_event_list = get_event_list.where(self.evacuate_events.c.event_create_time <= val)
            if key == 'filter_out':
                get_event_list = select([self.evacuate_events]).where(not_(or_(self.evacuate_events.c.event_status == 'failure', self.evacuate_events.c.event_status == 'completed')))
        
        LOG.info("Created the query with filter options.")
        get_event_list = get_event_list.order_by(desc(self.evacuate_events.c.event_create_time))
        # As per the documentaion in
        # https://specs.openstack.org/openstack/api-wg/guidelines/pagination_filter_sort.html
        # we need to add pagination  only after the filtering. So lets just filter out it.
        #
        # Point to be noted, though it is a bad idea to fetch all the data from db (in worst case when
        # there is no filter option), for time being we have done this way. Later we need to use sqlAlchemy
        try:
            result = self.conn.execute(get_event_list)
        except Exception as e:
            LOG.error(str(e))
            return []

        #Getting the values are setting it in list
        event_list = []
        for row in result:
            event_data = collections.OrderedDict()
            event_data['id']                  = row['id']
            event_data['name']                = row['name']
            event_data['event_status']        = row['event_status']
            event_data['event_create_time']   = row['event_create_time']
            event_data['event_complete_time'] = row['event_complete_time']
            event_data['node_uuid']           = row['node_uuid']
            vm_uuid_list = []
            if row['vm_uuid_list']:
                vm_uuid_list = json.loads(row['vm_uuid_list'])
            event_data['vm_uuid_list']        = vm_uuid_list
            event_data['extra']               = row['extra']
            event_list.append(event_data)
 
        first_index = 0
        if 'marker' in valid_args:
            marker = valid_args['marker']
            if marker is not None:
                for (marker_index, event) in enumerate(event_list):
                    if event['id'] == marker:
                        # we start pagination after the marker
                        first_index = marker_index + 1
                        break        
        limit = 30

        # Checking for the limit. If the given
        # Limit is not positive then, return emepty result
        if "limit" in valid_args:
            if not valid_args["limit"].isnumeric():
                return []
            if not valid_args["limit"] > 0:
                return []
            limit = valid_args["limit"].strip()
        limit = int(float(limit))

        event_list = event_list[first_index:limit]
        LOG.info("Sending back the result.")
        return event_list
 
    def update_event(self, event_id, data):
        """
        # | Method to update an events
        # |
        # | Arguments:
        # |     <uuid>: event id
        # |     <data>: Dictionary containg diffrent update sections
        # |
        # | Returns: None
        """

        #Getting the details of event using event id
        event_detail = self.get_detail(event_id)
        if "name" in data:
            # | If name is the parameter check for 
            # | the conflict
            name_check = select([self.evacuate_events]).where(
                and_(
                    self.evacuate_events.c.name == data['name'],
                    self.evacuate_events.c.id != event_id
                ))
            name_exist = self.conn.execute(name_check).rowcount
            if name_exist:
                LOG.error("There is already an event named " + data['name'])
                raise exception.Conflict("There is already an event named " + data['name'])

        #Updating the event status
        if 'event_status' in data:
            if data['event_status'] == 'completed':
                data['event_complete_time'] = datetime.datetime.now()
            else:
                data['event_complete_time'] = '0000-00-00 00:00:00'

        if 'vm_uuid_list' in data:
            data['vm_uuid_list'] = json.dumps(data['vm_uuid_list'])

        if 'extra' in data:
            data['extra'] = json.dumps(data['extra'])

        #Updating the data
        update = self.evacuate_events.update().where(self.evacuate_events.c.id == event_id).values(data)
        self.conn.execute(update)
        LOG.info("Event is updated succesfully.")
 
    def delete_event(self, event_id):
        """
        # | Function to delete an event
        # |
        # | Arguments:
        # |     <event_id>: id of the event
        # |
        # | Returns: None
        """

        # | A vent can be deleted, only if it's status completed
        # | Otherwise by deleting it will make error
        event_detail = self.get_detail(event_id)
        if event_detail['name']:
            self.delete_log(event_detail['name'])
        #if event_detail['event_status'] != 'completed':
        #raise exception.Forbidden("Events with completed status only can be deleted.")
        query = self.evacuate_events.delete().where(self.evacuate_events.c.id == event_id)
        self.conn.execute(query)
        LOG.info("Event is deleted succesfully.")

    def createLog(self, kw):
        """
        # | Function to delete an event
        # |
        # | Arguments:
        # |     <kw>: dictionary with values
        # |
        # | Returns: None
        """

        #Setting the dictionary to insert 
        arg = {
            "hypervisor_name": kw['hypervisor_name'],
            "down_since": kw['down_since'],
            "evacuated": "False",
            "event_id": kw['event_id'],
            "prev_time": kw['prev_time'],
            "event_creation_time": datetime.datetime.now()
        }

        #Inserting the data
        ins = self.evacuation_log.insert().values(arg)
        result = self.conn.execute(ins)
        LOG.info("Log is created succesfully.")
        return result

    def get_log_detail(self, name):
        """
        # | Function to get the detail of a log event
        # |
        # | Arguments:
        # |  <hypervisor_name>: Name of the hypervisor
        # |
        # | Returns: Json
        """
	
        #Searching the database and gettign the details
        get_data_select = select([self.evacuation_log]).where(self.evacuation_log.c.hypervisor_name == name)
        get_data = self.conn.execute(get_data_select)
        LOG.info("Got details of the log")
    
        #Checking the row count and returning the result
        if not get_data.rowcount:
            result = []
            LOG.error("No log entry with hypervisor name " + name + " found.")
            return result
            
        #Fecthing the detail from the table.
        data = get_data.fetchone()
        result = collections.OrderedDict()
        result["hypervisor_name"]     = name
        result["down_since"]          = data["down_since"]
        result["evacuated"]           = data["evacuated"]
        result["event_id"]            = data["event_id"]
        result["prev_time"]           = data["prev_time"]
        result["event_creation_time"] = data["event_creation_time"]	
        LOG.info("Return back the results.")
        return result

    def list_log(self, args={}):
        """
        # | Method to list the event logs
        # |
        # | Arguments: 
        # |   <args>: Dictionary
        # |
        # | Returns 
        """

        # Okay Bow lets start our query builder
        get_log_list = select([self.evacuation_log])
        LOG.info("Created the query to get the list of logs.")
        get_log_list = get_log_list.order_by(desc(self.evacuation_log.c.event_creation_time))
        try:
            result = self.conn.execute(get_log_list)
        except Exception as e:
            LOG.error(str(e))
            return []

        #Getting the values are setting it in list
        log_list = []
        for row in result:
            log_data = collections.OrderedDict()
            log_data['id']                  = row['id']
            log_data['name']                = row['hypervisor_name']
            log_data['down_since']          = row['down_since']
            log_data['evacuated']   	    = row['evacuated']
            log_data['event_id'] 	    = row['event_id']
            log_data['prev_time'] 	    = row['prev_time']
            log_data['event_creation_time'] = row['event_creation_time']
            log_list.append(log_data)
        return log_list

    def update_log(self, hypervisor_name, data):
        """
        # | Method to update a log
        # |
        # | Arguments:
        # |     <uuid>: log id
        # |     <data>: Dictionary containg diffrent update sections
        # |
        # | Returns: None
        """
        #log_detail = self.get_log_detail(hypervisor_name)

        #Checking that hypervisor name is in the data
        if "hypervisor_name" in data:
            
            # | If hypervisor_name is the parameter check for 
            # | the conflict
            name_check = select([self.evacuation_log]).where(self.evacuation_log.c.hypervisor_name == data['hypervisor_name'])
            name_exist = self.conn.execute(name_check).rowcount
            if name_exist:
                #Updating the data
                update = self.evacuation_log.update().where(self.evacuation_log.c.hypervisor_name == hypervisor_name).values(data)
                self.conn.execute(update)
                LOG.info("Log updated succesfully.")

    def delete_log(self, hypervisor_name):
        """
        # | Function to delete a log entry
        # |
        # | Arguments:
        # |     <hypervisor_name>: Name of the hypervisor for which the event is takign place
        # |
        # | Returns: None
        """

        #Setting the delete query
        query = self.evacuation_log.delete().where(self.evacuation_log.c.hypervisor_name == hypervisor_name)
        self.conn.execute(query)
        LOG.info("Log is deleted succesfully.")