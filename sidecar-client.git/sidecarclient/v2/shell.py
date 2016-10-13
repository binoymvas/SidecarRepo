# -*- coding: utf-8 -*-
#  ________________________________________________________________________________
# | File Name: __init__.py                                                         |
# |                                                                                |
# | Package Name: python-sidecarclient                                             |
# |                                                                                |
# | Component Name: nova evacute                                                   |
# |                                                                                |
# | Software: Openstack                                                            |
# |________________________________________________________________________________|
# | The basic idea of python-sidecarclient is to handel the sidecar REST api       |
# |________________________________________________________________________________|
# | Copyright: 2016@nephoscale.com                                                 |
# |                                                                                |
# | Author: Binoy MV <binoymv@poornam.com>, Dinesh Patra<dinesh.p@poornam.com>     |
# | Email: info@nephocale.com                                                      |
# |                                                                                |
# | Websote: http://www.nephoscale.com                                             |
# |________________________________________________________________________________|

from __future__ import print_function
from sidecarclient.common import cliutils
import argparse
from prettytable import PrettyTable

#############################################
# evacuates-events-list                     #
#############################################
@cliutils.arg(
    '--id',
    default=None,
    metavar='<string>',
    help="id of the event"
)
@cliutils.arg(
    '--name',
    default=None,
    metavar='<string>',
    help="Name of the event"
)
@cliutils.arg(
    '--node-uuid',
    default=None,
    metavar='<string>',
    help="node uuid of the event"
)
@cliutils.arg(
    '--event-create-time',
    default=None,
    metavar='<string>',
    help="event create time"
)
@cliutils.arg(
    '--min-event-create-time',
    default=None,
    metavar='<string>',
    help="minimum event create time"
)
@cliutils.arg(
    '--max-event-create-time',
    default=None,
    metavar='<string>',
    help="maximum event create time"
)
@cliutils.arg(
    '--marker',
    default=None,
    metavar='<string>',
    help="last event id"
)
@cliutils.arg(
    '--limit',
    default=None,
    metavar='<number>',
    help="Maximum number of events to be displayed"
)
def do_evacuates_events_lists(obj, args):
    """ Listing and filtering the evacuates events """
    filter_options = {}
    if getattr(args, 'id', None):
        filter_options['id'] = args.id
    if getattr(args, 'name', None):
        filter_options['name'] = args.name
    if getattr(args, 'event_status', None):
        filter_options['event_status'] = args.event_status
    if getattr(args, 'node_uuid', None):
        filter_options['node_uuid'] = args.node_uuid
    if getattr(args, 'marker', None):
        filter_options['marker'] = args.marker
    if getattr(args, 'limit', None):
        filter_options['limit'] = args.limit
  
    sidecar = obj.get_sidecar_client()
    events_obj = sidecar.events.list(**filter_options)
    table = PrettyTable()
    table.field_names = [
        "id", 
        "name", 
        "event-status", 
        "nova-uuid", 
        "event-create-time", 
        "event-complete-time", 
        "vm-uuid-list", 
        "extra"
    ]
    for event in events_obj:
        table.add_row([
            event.id, 
            event.name, 
            event.event_status, 
            event.node_uuid, 
            event.event_create_time, 
            event.event_complete_time, 
            event.vm_uuid_list, 
            event.extra
        ])
    table.align='l'
    print(table)

####################################################
# evacuates-event-create                           #
###################################################
@cliutils.arg(
    '--name',
    default=None,
    metavar='<string>',
    help="Name of the event. It should be unique"
)
@cliutils.arg(
    '--node-uuid',
    default=None,
    metavar='<string>',
    help="Host id for which evacute will be done."
)
@cliutils.arg(
    '--vm-uuid-list',
    default=None,
    metavar='<string>',
    help="comma separated instance ids"
)
def do_evacuates_event_create(obj, args):
    """ Creating a new event """
    filter_options = {}
    if getattr(args, 'id', None):
        filter_options['id'] = args.id
    if getattr(args, 'name', None):
        filter_options['name'] = args.name
    if getattr(args, 'vm_uuid_list', None):
        a = args.vm_uuid_list.split(",")
        filter_options['vm_uuid_list'] = a
    if getattr(args, 'node_uuid', None):
        filter_options['node_uuid'] = args.node_uuid
    
    sidecar = obj.get_sidecar_client()
    event_obj = sidecar.events.create(**filter_options)
    table = PrettyTable()
    table.field_names = ["Field Name", "Value"]
    table.add_row(["id",                  event_obj.id])
    table.add_row(["name",                event_obj.name])
    table.add_row(["event-status",        event_obj.event_status])
    table.add_row(["node-uuid",           event_obj.node_uuid])
    table.add_row(["event-create-time",   event_obj.event_create_time])
    table.add_row(["event-complete-time", event_obj.event_complete_time])
    table.add_row(["vm-uuid-list",        event_obj.vm_uuid_list])
    table.add_row(["extra",               event_obj.extra])
    table.align = "l"
    print(table)



#####################################################
# evacuates-event-detail                           #
####################################################
@cliutils.arg(
    '--id',
    default=None,
    metavar='<string>',
    help="id of the event"
)
def do_evacuates_event_detail(obj, args):
    """ Getting the detail of an event """
    filter_options = {}
    if getattr(args, 'id', None):
        filter_options['id'] = args.id
    
    sidecar = obj.get_sidecar_client()
    event_obj = sidecar.events.detail(**filter_options)
    table = PrettyTable()
    table.field_names = ["Field Name", "Value"]
    table.add_row(["id",                  event_obj.id])
    table.add_row(["name",                event_obj.name])
    table.add_row(["event-status",        event_obj.event_status])
    table.add_row(["node-uuid",           event_obj.node_uuid])
    table.add_row(["event-create-time",   event_obj.event_create_time])
    table.add_row(["event-complete-time", event_obj.event_complete_time])
    table.add_row(["vm-uuid-list",        event_obj.vm_uuid_list])
    table.add_row(["extra",               event_obj.extra])
    table.align = "l"
    print(table)

#################################################
# Editing an given event evacuates-event-edit   #
################################################
@cliutils.arg(
    '--id',
    default=None,
    metavar='<string>',
    help="id of the event to be edited."
)
@cliutils.arg(
    '--name',
    default=None,
    metavar='<string>',
    help="Name of the event"
)
@cliutils.arg(
    '--node-uuid',
    default=None,
    metavar='<string>',
    help="Host id to be evacuted"
)
@cliutils.arg(
    '--event-status',
    default=None,
    metavar='<string>',
    help="event status either completed, or running."
)
@cliutils.arg(
    '--vm-uuid-list',
    default=None,
    metavar='<string>',
    help="Instance ids in comma separated."
)
def do_evacuates_event_edit(obj, args):
    """ Editing a given event """
    filter_options = {}

    # | Preparing the filter query
    if getattr(args, 'id', None):
        filter_options['id'] = args.id
    if getattr(args, 'name', None):
        filter_options['name'] = args.name
    if getattr(args, 'event_status', None):
        filter_options['event_status'] = args.event_status
    if getattr(args, 'node_uuid', None):
        filter_options['node_uuid'] = args.node_uuid
    if getattr(args, 'vm_uuid_list', None):
        a = args.vm_uuid_list.split(",")
        filter_options['vm_uuid_list'] = a
    sidecar = obj.get_sidecar_client()
    event_obj = sidecar.events.edit(**filter_options)
    event_obj = sidecar.events.detail(id=filter_options['id'])
    table = PrettyTable()
    table.field_names = ["Field Name", "Value"]
    table.add_row(["id",                  event_obj.id])
    table.add_row(["name",                event_obj.name])
    table.add_row(["event-status",        event_obj.event_status])
    table.add_row(["node-uuid",           event_obj.node_uuid])
    table.add_row(["event-create-time",   event_obj.event_create_time])
    table.add_row(["event-complete-time", event_obj.event_complete_time])
    table.add_row(["vm-uuid-list",        event_obj.vm_uuid_list])
    table.add_row(["extra",               event_obj.extra])
    table.align = "l"
    print(table)


####################################################
# evacuate-event-run                               #
####################################################
@cliutils.arg(
    '--id',
    default=None,
    metavar='<string>',
    help="id of the event to be run."
)

def do_evacuate_event_run(obj, args):
    """Run a evacuate event"""
    filter_options = {}
    if getattr(args, 'id', None):
        filter_options['id'] = args.id
    sidecar = obj.get_sidecar_client()
    event_obj = sidecar.events.evacuate_runEvent(**filter_options)

###################################################
# evacuate-healthcheck				  #
###################################################
def do_evacuate_healthcheck(obj, args=None):
    """Healthcheck Details for an event"""
    sidecar = obj.get_sidecar_client()
    event_obj = sidecar.events.evacuate_healthcheck()

#################################################
# evacuates-event-delete                        #
################################################
@cliutils.arg(
    '--id',
    default=None,
    metavar='<string>',
    help="id of the event to be delete."
)
def do_evacuates_event_delete(obj, args):
    """ Deleting a given evacuate event """
    filter_options = {}
    if getattr(args, 'id', None):
        filter_options['id'] = args.id
    sidecar = obj.get_sidecar_client()
    event_obj = sidecar.events.delete(**filter_options)

#################################################
# all-versions                                 #
################################################
def do_all_versions(obj, args=None):
    """ Getting version details """
    sidecar = obj.get_sidecar_client()
    version_obj = sidecar.versions.list()
    table = PrettyTable()
    table.field_names = ["version", "release-date", "status"]
    for v in version_obj:
        table.add_row([v.version, v.date, v.status])
    table.align = "l"
    print(table)

###################################################
# evacuate-healthcheck-status                     #
###################################################
def do_evacuate_healthcheck_status(obj, args=None):
    """Healthcheck Log Details for an event"""
    sidecar = obj.get_sidecar_client()
    log_data = sidecar.events.evacuate_healthcheck_status()
    table = PrettyTable()
    table.field_names = ["Hypervisor Name", "Down Since", "Event creationtime "]
    for log in log_data:
        table.add_row([log.hypervisor_name, log.down_since, log.event_creation_time])
    table.align = "l"
    print(table)
