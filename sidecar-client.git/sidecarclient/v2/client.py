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
from __future__ import print_function
import sidecarclient
from sidecarclient    import exception
from sidecarclient    import client
from sidecarclient.v2 import events, versions
from urlparse         import urlparse
try: import json
except ImportError: import simplejson as json

class Client(object):
    """
    # | Version2 client class 2 use the the sidecar client
    """
    
    # | username: Keystone admin user name
    # | Type: string
    # | Required: True if auth_token is None
    # | Default Value: None
    username = None

    # | username: Keystone admin user id
    # | Type: string
    # | Required: True if auth_token and username is None
    # | Default Value: None
    user_id = None

    # | password: Keystone user password
    # | Type: String
    # | Required: True if auth_token is None
    # | Default Value: None
    password = None

    # | auth_url: Keystone admin authentication url
    # | Type: String
    # | Required: True
    # | Default Value: None
    auth_url = None

    # | auth_token: Authentication token
    # | Type: string
    # | Required: True if username and password is not given
    # | Default Value: None
    auth_token = None

    # | tenant_id: Openstack admin tenant id
    # | Type: string
    # | Required: True, if auth_version is 2 and tenant_name is not there
    # | Default None
    tenant_id = None

    # | tenant_name: Openstack admin tenant name
    # | Type: string
    # | Required: True, if auth_version is 2 and tenant_id is not provided
    # | Default None
    tenant_name = None

    # | project_id: Openstack admin project id
    # | Type: string
    # | Required: True, if auth_version is 3 and project_name is not there
    # | Default None
    project_id = None

    # | project_name: Openstack admin project name
    # | Type: string
    # | Required: True, if auth_version is 3 and project_name is not provided
    # | Default None
    project_name = None

    # | project_domain_id: Openstack admin project domain id
    # | Type: string
    # | REquired True, if auth_version is 3 and project_domain_name is not defined
    # | Default Value: None
    projejct_domain_id = None

    # | project_domain_name: Openstack admin project domain name
    # | Type: string
    # | REquired True, if auth_version is 3 and project_domain_id is not defined
    # | Default Value: None
    project_domain_name = None

    # | user_domain_id: Openstack admin user domain id
    # | Type: String
    # | Required True, if auth_version is 3 and user_domain_name is none
    # | Default Value: None
    user_domain_id=None

    # | user_domain_id: Openstack admin user domain name
    # | Type: String
    # | Required True, if auth_version is 3 and user_domain_id is none
    # | Default Value: None
    user_domain_name=None

    # | endpoint: sidecar endpoint url. After authentication, against this endpoint will be checked
    # | Type: url string
    # | Required: True
    # | Default Value: None
    #endpoint = None

    # | endpoint_type: Endpoint type to be checked
    # | Type: String
    # | Required: True
    # | Default Value: publicURL
    endpoint_type = 'publicURL'

    # | region_name: region name of the endpoint to be checked during authentication
    # | TYpe: string
    # | Required: True
    # | Default Value: None
    region_name = None

    # | auth_version: auth version to be used
    # | Type: numeric, either of 2 or 3
    # | Required: True
    # | default: 2
    auth_version = 2

    # | timeout: timeout in seconds to wait for http connection
    # | Type: numeric
    # | Required: Optional
    # | Default Value: 300
    timeout = 300

    # | insecure: whather verify for https connection or not
    # | Type: Boolean
    # | Required: Optional
    # | Default Value: False
    insecure=False

    """
    EXCEPT ABOVE ARGUMENTS, AFTER THE OBJECT CREATED, SUCCESSFULLY, FOLLOWING
    PROPERTIES ALSO GENERATED
    """
    
    # | events: events Object
    # | Type: instance of sidecarclient.v2.events.EventsHttp object
    # | Default Value: None
    events = None

    # | versions: versions object
    # | Type: Instance of sidecarclient.v2.versions.VersionsHttp object
    # | Default Value: None
    versions = None

    # | http: http instance, which is responsible for curl requies
    # | Type: Instance of sidecarclient.HTTPConnection
    # | Default Value: None
    http = None

    # | sidecar_url: sidecar_url, evaluted from endpoint parameter
    # | Type: String
    # | Default Value: None
    sidecar_url = None

    # | authenticated_token: authenticated token only after authenticateion
    # | Type: string
    # | default value: None
    authenticated_token = None

    def __init__(self, username = None, user_id=None, password=None,  auth_url=None, auth_token=None, tenant_id=None, tenant_name=None, project_name=None, project_id=None,project_domain_id=None, project_domain_name=None, user_domain_id=None, user_domain_name=None, region_name=None, insecure=False, timeout=300):

        self.username            = username
        self.password            = password
        self.user_id             = user_id
        self.auth_url            = auth_url
        self.auth_token          = auth_token
        self.tenant_id           = tenant_id
        self.tenant_name         = tenant_name
        self.project_name        = project_name
        self.project_id          = project_id
        #self.endpoint           = endpoint
        self.endpoint_type       = 'publicURL'
        self.region_name         = region_name
        self.insecure            = insecure
        self.timeout             = timeout
        self.user_domain_id      = user_domain_id
        self.user_domain_name    = user_domain_name
        self.project_domain_id   = project_domain_id
        self.project_domain_name = project_domain_name
        
        # | Auth Url validation
        try:
            u = urlparse(self.auth_url)
            self.auth_url = "%s://%s" % (u.scheme, u.netloc)
        except Exception as e:
            raise exception.InvalidValue("Invalid value given for auth_url")
        
        # | Auth version validation
        version_check = urlparse(auth_url)
        self.auth_version = int(version_check.path[2:3])
        if self.auth_version == 2:
            self.auth_url = self.auth_url + '/v2.0'
        elif self.auth_version == 3:
            self.auth_url = self.auth_url + '/v3'
        else:
            raise exception.InvalidValue("Invalid value given for auth_version. It must be either 2 or 3")
    
        self.http     = client.HTTPClient(timeout=self.timeout, verify=self.insecure)
        self.events   = events.EventsHttp(self)
        self.versions = versions.VersionsHttp(self)

    def authenticate(self):
        """
        # | Function to manage the authentication
        # |
        # | Arguments: None
        # |
        # | Returns: None
        """
        if self.authenticated_token:
            # | If already a token is authenticated, no need to go for authentication
            pass

        if self.auth_version == 2:
            # | If auth version is 2 
            # | Then do v2 authenticateion
            self.v2auth()
        else:
            self.v3auth()

    def v2auth(self):
        """
        # | Function to do version 2 authentication
        # |
        # | Arguments: None
        # | 
        # | Returns: None
        """
        url = self.auth_url + "/tokens"
        headers = {}
        body = {"auth":{}}

        if self.tenant_id:
            # | If tenant id is defined then
            # | store it in credential
            body['auth']['tenant_id'] = self.tenant_id
        
        if 'tenant_id' not in body['auth']:
            # | As ids have priority over name
            # | so only if tenant_id is there 
            # | ask for tenant_name
            if self.tenant_name:
                body['auth']['tenantName']  = self.tenant_name

        pwd_cred = {}
        token_cred = {}

        if self.auth_token:
            # | If auth token is defined
            token_cred = {"id": self.auth_token}

        if self.user_id:
            # | If user id is defined, store
            # | it in  password credentials
            pwd_cred['user_id'] = self.user_id

        if 'user_id' not in pwd_cred:
            # | If user id not there, then
            # | look for password credential
            if self.username:
                pwd_cred['username'] = self.username
        pwd_cred['password'] = self.password
        if token_cred:
            # | Generally give priority
            # | to token ids
            body['auth']['token'] = token_cred
        else:
            # | If token is not there, then work for
            # | passwordCredentials
            body['auth']['passwordCredentials'] = pwd_cred
        auth = self.http.post(url, body)
        # | As our http is handling the error so we  do need to worry
        # | about the response. At this point anyway we will get success code
        access = auth["body"]
        is_alright = False
        for point in access['access']['serviceCatalog']:
            if point['name'] == 'sidecar':
                for p in point['endpoints']:
                    if (p['region'] != '') and (p['publicURL'] != ''):
                        self.endpoint = p['publicURL']
                        # Enpoint validation
                        try:
                            u = urlparse(self.endpoint)
                            self.sidecar_url = "%s://%s" % (u.scheme, u.netloc) + '/v2'
                        except Exception as e:
                            raise exception.InvalidValue("Invalid value given for endpoint")
                        is_alright = True
	    
        if not is_alright:
            raise exception.InvalidValue("region_name, endpoint_type and endpoint mismatch in sidecar service")
        self.authenticated_token = access['access']['token']['id']


    def v3auth(self):
        """
        # | Function to do version 2 authentication
        # |
        # | Arguments: None
        # | 
        # | Returns: None
        """
        url = self.auth_url + "/auth/tokens"
        headers = {}
        body = {"auth":{"identity":{}, "scope":{"project": {"domain":{}}}}}

        if self.project_id:
            # | If project id is defined then
            # | store it in  scope
            body['auth']["scope"]["project"]["id"] = self.project_id
        
        if 'id' not in body['auth']["scope"]["project"]:
            # | As ids have priority over name
            # | so only if project_id is not there 
            # | ask for project_name
            if self.project_name:
                body['auth']["scope"]["project"]["name"]  = self.project_name

        if self.project_domain_id:
            # | Adding the admin project domain id.
            body['auth']["scope"]["project"]["domain"]["id"] = self.project_domain_id

        if not self.project_domain_id:
            # | If no domain id is there
            # | then provide name
            body['auth']["scope"]["project"]["domain"]["name"] = self.project_domain_name
    
        if self.auth_token:
            # | if auth token is there
            # | it has more priority
            body['auth']["identity"]["methods"] = ["token"]
            body['auth']["identity"]["token"] = {}
            body['auth']["identity"]["token"]["id"] = self.auth_token

        if not self.auth_token:
            # | If auth token is not there then do it by 
            # | token
            body['auth']["identity"]["methods"] = ["password"]
            body['auth']["identity"]['password'] = {}
            body['auth']["identity"]['password']["user"] = {"domain":{}}
            body['auth']["identity"]['password']["user"]['password'] = self.password
            if self.user_id:
                body['auth']["identity"]['password']["user"]['id'] = self.user_id
            if not self.user_id:
                body['auth']["identity"]['password']["user"]['name'] = self.username
            if self.user_domain_id:
                body['auth']["identity"]['password']["user"]["domain"]["id"] = self.user_domain_id
            else:
                body['auth']["identity"]['password']["user"]["domain"]["name"] = self.user_domain_name

        auth = self.http.post(url, body)
       
        # | As our http is handling the error so we  do need to worry
        # | about the response. At this point anyway we will get success code
        access = auth["body"]
       
        is_alright = False
        for point in access['token']['catalog']:
	    if point['name'] == 'sidecar':
                for p in point['endpoints']:
                    if (p['region'] != '') and (p['publicURL'] != ''):
                        self.endpoint = p['publicURL']
                        # Enpoint validation
                        try:
                            u = urlparse(self.endpoint)
                            self.sidecar_url = "%s://%s" % (u.scheme, u.netloc) + '/v2'
                        except Exception as e:
                            raise exception.InvalidValue("Invalid value given for endpoint")
                        is_alright = True
        if not is_alright:
            raise exception.InvalidValue("region_name, endpoint_type and endpoint mismatch in sidecar service")
        self.authenticated_token = auth['headers']['X-Subject-Token']
