# -*- coding: utf-8 -*-
# _______________________________________________________
# | File Name: validation.py                            |
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

import pecan, jsonschema, simplejson as json
from sidecar import exception
from simplejson import JSONDecodeError
from jsonschema import Draft4Validator, Draft3Validator

class Validation(object):
    """
    # | Class is used for validating the requests
    """
    def json_header(self):
        """
        # | Method to check wheather the request content type is json or not
        # |
        # | @Arguments: None
        # |
        # | Returns Booleanm
        """
        if not pecan.request.content_type or pecan.request.content_type != 'application/json':
            raise exception.NotJSONHeader()

    def json_data(self, schema_name, data):
        """
        # | Method to check wheather the requested json is valid or not 
        # |
        # | @Returns:
        # |     <schema_name> : Schema Name, it is the file name stored in sidecar/sche,a/
        # |     <data>: Json data need to be va;lidated
        # |
        # | @Returns: Returns Null. But on exception, raises error
        """
        try:
            json_data = json.loads(data)
        except JSONDecodeError as err:
            raise exception.BadData('Invalid json data provided')

        module = __import__('sidecar.schemas.'+schema_name, fromlist = ["*"])
        try:
            jsonschema.validate(json_data, module.schema)
        except jsonschema.ValidationError as e:
            raise exception.BadData(e.message)
        return json_data

