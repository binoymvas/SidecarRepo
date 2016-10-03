# -*- coding: utf-8 -*-
# ___________________________________________________________________________________
# | File Name: exception.py                                                         |
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
try: import json
except ImportError: import simplejson as json


class NotSupported(Exception):
    """ When some method not supported this exception will be raised"""
    code = 405
    title = "Not supported"
    pass

class APIError(Exception):
    """ This error will be raised when there will problem caused in API """

    code = title = message = None

    def __init__(self, error, code):
        """
        # | Intialization function
        # |
        # | Arguments: Error (string), and error code
        # |
        # | Returns: None
        """
        try:
            error = json.loads(error)
            error = error['error']
            super(APIError, self).__init__(error['message'])
            self.code    = error['code']
            self.title   = error['title']
            self.message = error['message']
        except Exception as e:
            super(APIError, self).__init__(error)
            self.code    = code
        
class CMDError(Exception):
    """ CMDError class """
    pass

class InvalidValue(Exception):
    """ When any invalid value is given, this exception will be raised """
    pass

class ConnectionError(Exception):
    """ When it is unable to connect any API, the error will be raised """
    pass

class TimeOut(Exception):
    """ When connection is timeout """
    pass

