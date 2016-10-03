# -*- coding: utf-8 -*-
# ___________________________________________________________________________________
# | File Name: client.py                                                            |
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

from   __future__ import print_function
from   oslo_utils import importutils
from   urlparse   import urlparse
import requests, functools, logging
import sidecarclient, exception
try: import json
except ImportError: import simplejson as json

class HTTPClient(object):
    """
    # | Http client object
    """
    USER_AGENT = 'python-sidecarclient'
    timeout = None
    verify  = None

    def __init__(self, timeout=300, verify=False):
        """
        # | Initialization function
        # |
        # | Arguments:
        # |   <timeout>: Timeout in second
        # |   <verify>: Wheather https verify or not
        # | Returns: None
        """
        self.timeout = timeout
        self.verify  = verify

    def get(self, url, headers):
        """
        # | Method to make http request with gett method
        # |
        # | Arguments:
        # | <url>: Url to make the request
        # | <headers>: Headers need to be sent with the request
        # |
        # | Returns: Request header, body, status code
        """
        return self._do_curl(url, headers=headers, method="GET")

    def post(self, url, data, headers={}):
        """
        # | Method to make http request with POST method
        # |
        # | Arguments:
        # | <url>: Url to make the request
        # | <data>: Data to be sent with post request
        # | <headers>: Headers need to be sent with the request
        # |
        # | Returns: Request header, body, status code
        """
        return self._do_curl(url, data=data, headers=headers, method="post")

    def put(self, url, data, headers={}):
        """
        # | Method to make http request with put method
        # |
        # | Arguments:
        # | <url>: Url to make the request
        # | <data>: Data to be sent with put request
        # | <headers>: Headers need to be sent with the request
        # |
        # | Returns: Request header, body, status code
        """
        return self._do_curl(url, data=data, headers=headers, method="put")
   

    def delete(self, url, headers={}):
        """
        # | Function to make the http request with delete method in header
        # |
        # | Arguments:
        # |  <url>: Url to make the request
        # |  <headers> Any header need to send in header
        # |
        # | Returns: Dictionary containg headers, body and status code
        """
        return self._do_curl(url, headers=headers, method="delete")
       
    def _do_curl(self, url="", data={}, headers={}, method=""):
        """
        # | Function is responsible to make curl request
'       # |
        # | Arguments:
        # |   <url>: Url to make curl request
        # |   <data>: If any data need to be sent
        # |   <headers>: If any headerts need to be sent
        # |   <method>:  get | put|post|delete
        # |
        # | Returns: Dictionary conbtaing
        # |     <headers>, <body>, <status code>
        """
        headers['User-Agent']   = self.USER_AGENT
        headers['Content-Type'] = 'application/json'
        headers['Accept']       = 'application/json'
        if data:
            # | If any data is present, then try to
            # | convert them into json. On fail
            # | raise exception
            try:
                data = json.dumps(data)
            except Exception as e:
                raise exception.InvalidJSON("Unable to encode the data into JSON.")

        try:
            # | As per the given method request. But
            # | if it is not one of get, put, post or delete
            # | then throw error
            if method.lower()   == 'get':
                req = requests.get(url, headers=headers, timeout=self.timeout, verify=self.verify)
            elif method.lower() == 'post':
		req = requests.post(url, data = data, headers=headers, timeout=self.timeout, verify=self.verify)
            elif method.lower() == 'put':
                req = requests.put(url, data = data, headers=headers, timeout=self.timeout, verify=self.verify)
            elif method.lower() == 'delete':
                req = requests.delete(url, headers=headers, timeout=self.timeout, verify=self.verify)
            else:
		
                raise exception.NotSupported("%s method not supported" %(method))
        except requests.exceptions.ConnectionError as e:
            raise exception.ConnectionError("Unable to connect to %s" %(url))
        except requests.exceptions.Timeout as e:
            raise exception.TimeOut("connection to %s timeout." %(url))
       
        if int((req.status_code) / 100) not in (1, 2, 0) or req.status_code == 0:
            # If the code is not in 100 or 2000 like 201, 200,  then raise APIError
            raise exception.APIError(req.text, req.status_code)
            
        # | Okay now we have completed response
        # | Try to convert the response into dict
        try:
            response = json.loads(req.text)
        except Exception as e:

            if int((req.status_code) / 100) not in (1, 2):
                raise exception.APIError(req.text)
            response = None
        return {"headers": req.headers, "body": response, "status_code": req.status_code}

       
def _get_client_class_and_version(version):
    """
    # | Function to get the appropriate version
    # |
    # | Arguments: Version
    # |
    # | Returns: Null
    """
    return version, importutils.import_class("sidecarclient.v%s.client.Client" % version)

def Client(*args, **kwargs):
    """
    # | Client function to initalize the sidecar client
    # |
    # | Arguments: Version
    # |
    # | Returns: Null
    """
    version = sidecarclient.__version__
    api_version, client_class = _get_client_class_and_version(version)
    return client_class(*args, **kwargs)
