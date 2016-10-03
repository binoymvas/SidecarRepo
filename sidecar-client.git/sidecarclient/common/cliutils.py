# -*- coding: utf-8 -*-
# ___________________________________________________________________________________
# | File Name: cliutils.py                                                          |
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
import getpass, inspect, os, sys, textwrap
from oslo_utils import encodeutils
from oslo_utils import strutils
import prettytable, six
from six import moves

class MissingArgs(Exception):
    """
     Class to tell missing arguments exception
    """
    def __init__(self, missing):
        self.missing = missing
        msg = _("Missing arguments: %s") % ", ".join(missing)
        super(MissingArgs, self).__init__(msg)


def validate_args(fn, *args, **kwargs):
    """
    # | Function to validate the arguments
    # |
    # | Arguments:
    # | <fn>: Function (action) name
    # | <arg>: arguments supplied
    # | <kwargs>: If any other argument supplied
    """
    argspec = inspect.getargspec(fn)
    num_defaults = len(argspec.defaults or [])
    required_args = argspec.args[:len(argspec.args) - num_defaults]
    def isbound(method):
        return getattr(method, '__self__', None) is not None
    if isbound(fn):
        required_args.pop(0)
    missing = [arg for arg in required_args if arg not in kwargs]
    missing = missing[len(args):]
    if missing:
        raise MissingArgs(missing)


def arg(*args, **kwargs):
    """
    # | Decorator for creating cli command arguments for a action
    # | 
    # | Example:
    # |   @arg("id", help="Id of the evacuate-events")
    # |   def  do_evacuates_events_list():
    # |      pass
    # |
    # | The above example will add id as argument to evacuates-events-list
    """
    def _decorator(func):
        """
        # | Add argument to function
        """
        add_arg(func, *args, **kwargs)
        return func
    return _decorator


def env(*args, **kwargs):
    """Returns the first environment variable set.

    If all are empty, defaults to '' or keyword arg `default`.
    """
    for arg in args:
        value = os.environ.get(arg)
        if value:
            return value

    # Default value return None, so that we do not
    # need to validate. Directly we can pass them to
    # sidecar client
    return kwargs.get('default', None)


def add_arg(func, *args, **kwargs):
    """
    # | Registering arguments for a function
    # | 
    # | Arguments:
    # |     <func>: Function name
    # |     <args>: Arguments
    # |     <kwargs>: Additional arg
    # |
    # | Returns: None
    """
    if not hasattr(func, 'arguments'):
        # | If the function has no argument attr, then
        # | add the property
        func.arguments = []

    if (args, kwargs) not in func.arguments:
        # | If the argument is not registed then add it
        func.arguments.insert(0, (args, kwargs))


