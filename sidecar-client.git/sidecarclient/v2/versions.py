# -*- coding: utf-8 -*-
# ___________________________________________________________________________________
# | File Name: versions.py                                                          |
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
import sidecarclient

class Version(object):
    """ version object """

    # | version: version name
    # | TYpe string
    # | default value: v2
    version = None

    # | date: relasing date of the version
    # | Type: date time string
    # | Default Value: None
    date = None

    # | status: status of the version
    # | Type: string
    # | Default Value: None
    status = None

    def __init__(self, version=None, date=None, status=None):
        """
        Initialization function
        """
        self.version = version
        self.date    = date
        self.status  = status


class VersionsHttp(object):
    """ class to connect to version service """
    
    def __init__(self, obj):
        """
        # | Initialization function to connect to version api
        # |
        # | Arguments:
        # |     <obj>: instance of sidecarclient.v2.client.Client:
        # |
        # | Returns: None
        """
        if type(obj) != sidecarclient.v2.client.Client:
            raise exception.NotSupported("Not an instance of sidecarclient.")
        self._obj = obj

    def list(self):
        """
        # | Function to list the versions
        # |
        # | Arguments: None
        # |
        # | Returns: List of Version object
        """
        self._obj.authenticate()
        headers = {"X-Auth-Token":self._obj.authenticated_token}
        url = self._obj.sidecar_url
        data = self._obj.http.get(url, headers)
        result = []
        for version in data["body"]:
            result.append(Version(version=version, date=data['body'][version]['date'], status=data['body'][version]['status']))
        return result
