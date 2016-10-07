# -*- coding: utf-8 -*-
# _______________________________________________________
# | File Name: app.py                                   |
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

import logging
from oslo_config import cfg
from oslo_log import log
from paste import deploy
from pecan import make_app
import pecan
import os, socket, sys, oslo_i18n
import model  
import config as api_config
LOG = log.getLogger(__name__)
CONF = cfg.CONF
OPTS = [
    cfg.StrOpt('host',
               default="controller",
               help='Name of this node, which must be valid in an AMQP '
               'key. Can be an opaque identifier. For ZeroMQ only, must '
               'be a valid host name, FQDN, or IP address.'),
    cfg.IntOpt('http_timeout',
               default=600,
               help='Timeout seconds for HTTP requests. Set it to None to '
                    'disable timeout.'),
]
cfg.CONF.register_opts(OPTS)


CLI_OPTS = [
    cfg.StrOpt('os-username',
               deprecated_group="DEFAULT",
               default=os.environ.get('OS_USERNAME', 'admin'),
               help='User name to use for OpenStack service access.'),
    cfg.StrOpt('os-password',
               deprecated_group="DEFAULT",
               secret=True,
               default=os.environ.get('OS_PASSWORD', 'demo'),
               help='Password to use for OpenStack service access.'),
    cfg.StrOpt('os-tenant-id',
               deprecated_group="DEFAULT",
               default=os.environ.get('OS_TENANT_ID', '895dd72055d646b8a6af64d441cb6f33'),
               help='Tenant ID to use for OpenStack service access.'),
    cfg.StrOpt('os-tenant-name',
               deprecated_group="DEFAULT",
               default=os.environ.get('OS_TENANT_NAME', 'admin'),
               help='Tenant name to use for OpenStack service access.'),
    cfg.StrOpt('os-cacert',
               default=os.environ.get('OS_CACERT'),
               help='Certificate chain for SSL validation.'),
    cfg.StrOpt('os-auth-url',
               deprecated_group="DEFAULT",
               default=os.environ.get('OS_AUTH_URL',
                                      'http://198.100.181.66:5000/v2.0'),
               help='Auth URL to use for OpenStack service access.')
]

cfg.CONF.register_cli_opts(CLI_OPTS, group="service_credentials")


# Registering diffrent workers
API_OPT = cfg.IntOpt('workers',
                     default=1,
                     min=1,
                     deprecated_group='DEFAULT',
                     deprecated_name='api_workers',
                     help='Number of workers for api, default value is 1.')
cfg.CONF.register_opt(API_OPT, 'api')

NOTI_OPT = cfg.IntOpt('workers',
                      default=1,
                      min=1,
                      deprecated_group='DEFAULT',
                      deprecated_name='notification_workers',
                      help='Number of workers for notification service, '
                           'default value is 1.')
cfg.CONF.register_opt(NOTI_OPT, 'notification')

COLL_OPT = cfg.IntOpt('workers',
                      default=1,
                      min=1,
                      deprecated_group='DEFAULT',
                      deprecated_name='collector_workers',
                      help='Number of workers for collector service. '
                           'default value is 1.')
cfg.CONF.register_opt(COLL_OPT, 'collector')

LOG = log.getLogger(__name__)
oslo_i18n.enable_lazy()
logging.basicConfig(level=logging.INFO)
log.register_options(cfg.CONF)
log_levels = (cfg.CONF.default_log_levels + ['stevedore=INFO', 'sidecar=INFO'])
log.set_defaults(default_log_levels=log_levels)
argv = []
cfg.CONF(argv[1:], project='sidecar', validate_default_values=True, version="1.0", default_config_files=None)


OPTS = [
    cfg.StrOpt(
        'api_paste_config',
        default="/etc/sidecar/api_paste.ini",
        help="Configuration file for WSGI definition of API."
    ),
]

API_OPTS = [
    cfg.BoolOpt(
        'pecan_debug',
        default=False,
        help='Toggle Pecan Debug Middleware.'
    ),
    cfg.IntOpt(
        'default_api_return_limit',
        min=1,
        default=100,
        help='Default maximum number of items returned by API request.'
    ),
]

CONF.register_opts(OPTS)
CONF.register_opts(API_OPTS, group='api')

def get_pecan_config():
    """
    # | Get pecan config files
    # |
    # | Arguments: None
    # |
    # | Returns None
    """
    # Set up the pecan configuration
    filename = api_config.__file__.replace('.pyc', '.py')
    return pecan.configuration.conf_from_file(filename)

def setup_app(pecan_config=None, extra_hooks=None):

    if not pecan_config:
        pecan_config = get_pecan_config()

    pecan.configuration.set_config(dict(pecan_config), overwrite=True)

    # NOTE(sileht): pecan debug won't work in multi-process environment
    pecan_debug = CONF.api.pecan_debug
    if CONF.api.workers and CONF.api.workers != 1 and pecan_debug:
        pecan_debug = False
        LOG.warning(_LW('pecan_debug cannot be enabled, if workers is > 1, '
                        'the value is overrided with False'))
    app_hooks = []
    app = pecan.make_app(
        pecan_config.app.root,
        debug=pecan_debug,
        force_canonical=getattr(pecan_config.app, 'force_canonical', True),
        hooks=app_hooks,
        wrap_app=None,
        guess_content_type_from_ext=False
    )
    return app

def load_app():
    # Build the WSGI app
    cfg_file = None
    cfg_path = cfg.CONF.api_paste_config
    if not os.path.isabs(cfg_path):
        cfg_file = CONF.find_file(cfg_path)
    elif os.path.exists(cfg_path):
        cfg_file = cfg_path

    if not cfg_file:
        raise cfg.ConfigFilesNotFoundError([cfg.CONF.api_paste_config])
    LOG.info("Full WSGI config used: %s" % cfg_file)    
    return deploy.loadapp("config:" + cfg_file)

def build_server():
    app = load_app()
    # Create the WSGI server and start it
    host, port = cfg.CONF.api.host, cfg.CONF.api.port

    LOG.info(_('Starting server in PID %s') % os.getpid())
    LOG.info(_("Configuration:"))
    cfg.CONF.log_opt_values(LOG, logging.INFO)

    if host == '0.0.0.0':
        LOG.info(_(
            'serving on 0.0.0.0:%(sport)s, view at http://127.0.0.1:%(vport)s')
            % ({'sport': port, 'vport': port}))
    else:
        LOG.info(_("serving on http://%(host)s:%(port)s") % (
                 {'host': host, 'port': port}))

    serving.run_simple(cfg.CONF.api.host, cfg.CONF.api.port,
                       app, processes=CONF.api.workers)

class VersionSelectorApplication(object):
    def __init__(self):
        pc = get_pecan_config()

        def not_found(environ, start_response):
            start_response('404 Not Found', [])
            return []

        self.v1 = not_found
        self.v2 = setup_app(pecan_config=pc)

    def __call__(self, environ, start_response):
        if environ['PATH_INFO'].startswith('/v1/'):
            return self.v1(environ, start_response)
        return self.v2(environ, start_response)


def app_factory(global_config, **local_conf):
    return VersionSelectorApplication()

