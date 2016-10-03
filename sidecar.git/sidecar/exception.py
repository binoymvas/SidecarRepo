# -*- coding: utf-8 -*-
# _______________________________________________________
# | File Name: exception.py                             |
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

class InvalidJSON(Exception):
    code = 400
    pass

class NotJSONHeader(Exception):
    code = "400"
    title = "Bad Request"
    message = "Invalid Content Type in Header"
    pass

class BadData(Exception):
    code = 400
    title = "Bad Data"
    pass

class NotFound(Exception):
    code = 404
    title = "Not Found"
    pass

class Conflict(Exception):
    code = 409
    title = "Conflict"
    pass

class Forbidden(Exception):
    code = 403
    title = "Forbidden"

