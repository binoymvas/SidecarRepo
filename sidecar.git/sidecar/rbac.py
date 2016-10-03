# -*- coding: utf-8 -*-
# _______________________________________________________
# | File Name: rbac.py                                  |
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

"""Access Control Lists (ACL's) control access the API server."""

from oslo_config import cfg
from oslo_policy import policy
from sidecar     import exception
import pecan

_ENFORCER = None
CONF = cfg.CONF

def _has_rule(name):
    """
    # | Function to check wheather it has rule or not
    # |
    # | Argumments:
    # |  <name>: Name of the event
    # |
    # | Returns Boolean
    """
    return name in _ENFORCER.rules.keys()

def enforce(policy_name, request):
    """Return the user and project the request should be limited to.
    :param request: HTTP request
    :param policy_name: the policy name to validate authz against.
    """
    global _ENFORCER
    if not _ENFORCER:
        _ENFORCER = policy.Enforcer(CONF)
        _ENFORCER.load_rules()

    rule_method =  policy_name
    headers = request.headers

    policy_dict = dict()
    policy_dict['roles'] = "demo".split(",")
    policy_dict['target.user_id'] = (headers.get('X-User-Id'))
    policy_dict['target.project_id'] = (headers.get('X-Project-Id'))

    # maintain backward compat with Juno and previous by allowing the action if
    # there is no rule defined for it
    if ((_has_rule('default') or _has_rule(rule_method)) and
            not _ENFORCER.enforce(rule_method, {}, policy_dict)):
        raise exception.Forbidden("Not allowed to perform this.")
       
# TODO(fabiog): these methods are still used because the scoping part is really
# convoluted and difficult to separate out.

def get_limited_to(headers):
    """Return the user and project the request should be limited to.
    :param headers: HTTP headers dictionary
    :return: A tuple of (user, project), set to None if there's no limit on
    one of these.
    """
    
    global _ENFORCER
    if not _ENFORCER:
        _ENFORCER = policy.Enforcer(CONF)
        _ENFORCER.load_rules()

    policy_dict = dict()
    policy_dict['roles'] = headers.get('X-Roles', "").split(",")
    policy_dict['target.user_id'] = (headers.get('X-User-Id'))
    policy_dict['target.project_id'] = (headers.get('X-Project-Id'))

    # maintain backward compat with Juno and previous by using context_is_admin
    # rule if the segregation rule (added in Kilo) is not defined
    rule_name = 'segregation' if _has_rule(
        'segregation') else 'context_is_admin'
    if not _ENFORCER.enforce(rule_name,
                             {},
                             policy_dict):
        return headers.get('X-User-Id'), headers.get('X-Project-Id')
    return None, None

def get_limited_to_project(headers):
    """Return the project the request should be limited to.
    :param headers: HTTP headers dictionary
    :return: A project, or None if there's no limit on it.
    """
    return get_limited_to(headers)[1]

