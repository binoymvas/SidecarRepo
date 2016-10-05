# _______________________________________________________________________
# | File Name: views.py                                                 |
# |                                                                     |
# | This file is for handling the views of support ticket display       |
# |_____________________________________________________________________|
# | Start Date: Aug 31th, 2016                                          |
# |                                                                     |
# | Package: Openstack Horizon Dashboard [liberity]                     |
# |                                                                     |
# | Copy Right: 2016@nephoscale                                         |
# |_____________________________________________________________________|

from openstack_dashboard.dashboards.sidecar.events import tabs as event_tabs
from django.utils.translation import ugettext_lazy as _
from openstack_dashboard.dashboards.sidecar.events import tables
from django.core.urlresolvers import reverse
from django.core.urlresolvers import reverse_lazy
from django.http import  HttpResponseRedirect
from django.shortcuts import render
from horizon import views
from horizon import tabs
from horizon import exceptions
from horizon.utils import memoized
from django.conf import settings
import requests
import json

class IndexView(tabs.TabbedTableView):
    """
    # | IndexView for showing ticket list 
    # |
    # | Code is in tabs.py 
    """
    tab_group_class = event_tabs.MyEventsTab
    template_name   = "sidecar_dashboard/events/index.html"
    page_title      = "My Events"

def get_event_detail(request, **kwargs):
    print " in the get_event_details"
    print kwargs, 'kwargs'

    pecan_evacuate_url = getattr(settings, 'EVACUATE_URL', '')
    header = {'X-Auth-Token': request.user.token.id, 'Content-Type': 'application/json'}
    args = {}
    response =  requests.get(pecan_evacuate_url + '/details/'+ kwargs['event_id'], params=args, auth=('user', 'pass'), headers=header)
    event_data = json.loads(response.text)
    context = {
        "page_title": _("Event Details: %s") % event_data['event']['name'],
        "events": event_data['event']
    }
    return render(request, 'sidecar_dashboard/events/event_detail.html', context)
