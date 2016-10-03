# -*- coding: utf-8 -*-
# ___________________________________________________________________________________
# | File Name: shell.py                                                             |
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
import argparse, getpass, logging, sys
from oslo_utils import encodeutils
from oslo_utils import importutils
from oslo_utils import strutils

logger = logging.getLogger(__name__)

import sidecarclient
from sidecarclient        import client
from sidecarclient.common import cliutils
from sidecarclient        import exception

DEFAULT = {"os_auth_version": 2}

class SidecarClientArgumentParser(argparse.ArgumentParser):
    """
    # | Argument parser class to extend argparse.ArgumentParser
    """
    def __init__(self, *args, **kwargs):
        super(SidecarClientArgumentParser, self).__init__(*args, **kwargs)

    def error(self, message):
        """
        # | error(message: string)
        # |
        # | Prints a usage message incorporating the message to stderr and
        # | exits.
        """
        self.print_usage(sys.stderr)
        choose_from = ' (choose from'
        progparts = self.prog.partition(' ')
        self.exit(2, "error: %(errmsg)s\nTry '%(mainp)s help %(subp)s'"
                       " for more information.\n" %
                  {'errmsg': message.split(choose_from)[0],
                   'mainp': progparts[0],
                   'subp': progparts[2]})

    def _get_option_tuples(self, option_string):
        """
        # | Function to display
        """
        option_tuples = (super(SidecarClientArgumentParser, self)._get_option_tuples(option_string))
        if len(option_tuples) > 1:
            normalizeds = [option.replace('_', '-')
                           for action, option, value in option_tuples]
            if len(set(normalizeds)) == 1:
                return option_tuples[:1]
        return option_tuples


class SidecarHelpFormatter(argparse.HelpFormatter):
    """
    # Formatter class to extend the help
    """
    def __init__(self, prog, indent_increment=2, max_help_position=32, width=None):
        super(SidecarHelpFormatter, self).__init__(prog, indent_increment, max_help_position, width)

    def start_section(self, heading):
        # Title-case the headings
        heading = '%s%s' % (heading[0].upper(), heading[1:])
        super(SidecarHelpFormatter, self).start_section(heading)


class SidecarShell(object):
    def get_base_parser(self):
        parser = SidecarClientArgumentParser(
            prog='sidecar',
            description= "SIDECAR SHELL PROGRAM",
            epilog='See "sidecar help COMMAND" '
                   'for help on a specific command.',
            add_help=False,
            formatter_class=SidecarHelpFormatter,
        )

        # Global arguments
        parser.add_argument(
            '-h', '--help',
            action='store_true',
            help=argparse.SUPPRESS,
        )

        parser.add_argument(
            '--version',
            action='version',
            version=sidecarclient.__version__
        )
        parser.add_argument(
            '--debug',
            default=False,
            action='store_true',
            help="Print debugging output."
        )
        parser.add_argument(
            '--os-auth-token',
            default=cliutils.env('OS_AUTH_TOKEN'),
            help='Defaults to env[OS_AUTH_TOKEN].'
        )
        parser.add_argument(
            '--os-user-id',
            default=cliutils.env('OS_USER_ID'),
            help="keystone admin user id. defaults to OS_USER_ID"
        )
        parser.add_argument(
            '--os-username',
            default=cliutils.env('OS_USERNAME'),
            help="keystone admin username, defaults to  OS_USERNAME"
        )
        parser.add_argument(
            '--os-password',
            default=cliutils.env('OS_PASSWORD'),
            help="Openstack admin password, defaults to OS_PASSWORD"
        )

        parser.add_argument(
            '--os-tenant-name',
            default=cliutils.env('OS_TENANT_NAME', 'OS_PROJECT_NAME'),
            help='Defaults to env[OS_TENANT_NAME].'
        )
        parser.add_argument(
            '--os-tenant-id',
            default=cliutils.env('OS_TENANT_ID', 'OS_PROJECT_ID'),
            help='Defaults to env[OS_TENANT_ID].'
        )
        parser.add_argument(
            '--os-project-name',
            default=cliutils.env('OS_TENANT_NAME', 'OS_PROJECT_NAME'),
            help='Defaults to env[OS_PROJECT_NAME].'
        )
        parser.add_argument(
            '--os-project-id',
            default=cliutils.env('OS_PROJECT_ID'),
            help='Defaults to env[OS_PROJECT_ID].'
        )
        parser.add_argument(
            '--os-auth-url',
            default=cliutils.env('OS_AUTH_URL'),
            help="Keystone auth url. defaults to OS_AUTH_URL"
        )
        parser.add_argument(
            '--os-region-name',
            default=cliutils.env('OS_REGION_NAME', 'SIDECAR_REGION_NAME'),
            help='Defaults to env[OS_REGION_NAME].'
        )
        parser.add_argument(
            '--os-endpoint',
            default=cliutils.env('OS_ENDPOINT', 'SIDECAR_ENDPOINT'),
            help=argparse.SUPPRESS
        )
        parser.add_argument(
            '--os-endpoint-type',
            default=cliutils.env('OS_ENDPOINT_TYPE', 'SIDECAR_ENDPOINT_TYPE'),
            help=argparse.SUPPRESS
        )
        parser.add_argument(
            '--os-auth-version',
            default=cliutils.env('OS_AUTH_VERSION'),
            help="Which os auth version should be used, either 2 or 3. Default OS_AUTH_VERSION"
        )
        parser.add_argument(
            '--os-timeout',
            default=cliutils.env('OS_TIMEOUT'),
            help="Maximum time to wait for result."
        )
        parser.add_argument(
            '--os-insecure',
            default=cliutils.env('OS_INSECURE'),
            help="Wheather https should be verified or not. Defaults to False"
        )
        parser.add_argument(
            '--os-user-domain-id',
            default=cliutils.env('OS_USER_DOMAIN_ID'),
            help="Admin user's domain id, Default OS_USER_DOMAIN_ID"
        )
        parser.add_argument(
            '--os-user-domain-name',
            default=cliutils.env('OS_USER_DOMAIN_NAME'),
            help="Admin user's domain name, Default OS_USER_DOMAIN_NAME"
        )
        parser.add_argument(
            '--os-project-domain-id',
            default=cliutils.env('OS_PROJECT_DOMAIN_ID'),
            help="Admin project's domain id, Default OS_PROJECT_DOMAIN_ID"
        )
        parser.add_argument(
            '--os-project-domain-name',
            default=cliutils.env('OS_PROJECT_DOMAIN_NAME'),
            help="Admin user's domain id, Default OS_USER_DOMAIN_NAME"
        )
        return parser

    
    @cliutils.arg('command', metavar='<subcommand>', nargs='?',  help='Display help for <subcommand>.')
    def do_help(self, args):
        """ Show help for the <command> """
        if args.command:
            # | If command is not empty, and
            # | it is a valid command, registered by us
            # | display its help, other iwse throw error
            if args.command in self.subcommands:
                self.subcommands[args.command].print_help()
            else:
                raise exc.CommandError("'%s' is not a valid subcommand" % (args.command))
        else:
            # If no command given then
            # just print this program help
            self.parser.print_help()


    def do_bash_completion(self, _args):
        """ Prints all the commands to stdout """
        commands = set()
        options = set()
        for sc_str, sc in self.subcommands.items():
            commands.add(sc_str)
            for option in sc._optionals._option_string_actions.keys():
                options.add(option)
        commands.remove('bash-completion')
        commands.remove('bash_completion')
        print(' '.join(commands | options))

    def _add_bash_completion_subparser(self, subparsers):
        """
        # | Fiunnction to excute after the bash completion
        # | 
        # | Arguments: <subparser>: subparser command
        # |
        # | Returns: None
        """
        subparser = subparsers.add_parser('bash_completion', add_help=False, formatter_class=SidecarHelpFormatter)
        self.subcommands['bash_completion'] = subparser
        subparser.set_defaults(func=self.do_bash_completion)


    def get_subcommand_parser(self, version=2, do_help=True):
        """
        # | Getting subcommands
        # |
        # | Arguments:
        # |   <version>: The version to which the subcommand belongs
        # |              As currently we are using verswion 2 so we have 
        # |              Hardcoded it
        # |
        # |  <do_help>: Do we need to display help statement
        # |
        # | This method's main action will be to find the action and
        # | registering it to command parser
        """
        parser = self.get_base_parser()
        self.subcommands = {}
        subparsers = parser.add_subparsers(metavar='<subcommand>')
        actions_module = importutils.import_module("sidecarclient.v%s.shell" % version)        
        self._find_actions(subparsers, actions_module, version, do_help)
        self._find_actions(subparsers, self,  version, do_help)
        self._add_bash_completion_subparser(subparsers)
        return parser


    def _find_actions(self, subparsers, actions_module, version, do_help):
        """
        # | Function to find the subparser in the given list
        # |
        # | Arguments: 
        # |     <subparaser>: instance of a parser
        # |     <action_module>: Module Name
        # |     <version>: Vesrion
        # |     <do_help>: do we need to display the help for the subcommland
        # | 
        # | Returns: None
        """
        for a in dir(actions_module):
            # | Foreach valid name in actions_module scope
            # | if that name starts with do_  (like do_evacuates_events_list in v2/shell.py)
            # | enter into the loop. First strip do_ from it. then replace thos underscores (_)
            # | with dashes (-). Because user will provide command as evacuates-events-list
            # | Then make it a cllback for laster use
            if a.startswith('do_'):
                command = a[3:]
                command = command.replace('_', '-')
                callback = getattr(actions_module, a)
            
                desc = callback.__doc__ or ''
                action_help = desc.strip()
                arguments = getattr(callback, 'arguments', [])

                # | After getting the arguments add the subcommand
                # | to subparser
                subparser = subparsers.add_parser(
                    command,
                    help=action_help,
                    description=desc,
                    add_help=False,
                    formatter_class=SidecarHelpFormatter)
                subparser.add_argument(
                    '-h', '--help',
                    action='help',
                    help=argparse.SUPPRESS,
                )
                self.subcommands[command] = subparser

                # | Okay now we have added the subcommand
                # | Now we need to register the arguments
                # | At this point arguments will look someting
                # | following
                """
                [(('--id',), {'default': None, 'metavar': '<string>', 'help': '==SUPPRESS=='}), (('--name',), {'default': None, 'metavar': '<string>', 'help': '==SUPPRESS=='})]
                """ 
                for (args, kwargs) in arguments:
                    # | If some extra parametrs we need to add
                    # | then we can add in kwarg
                    subparser.add_argument(*args, **kwargs)

                # Okay finally set the call back function
                subparser.set_defaults(func=callback)

    def get_sidecar_client(self):
        """
        # | Function to provide the sidecarclient instance
        # |
        # | Arguments: None
        # |
        # | Returns: None
        """
        return client.Client(
            username            = self.username,
            password            = self.password,
            user_id             = self.user_id,
            auth_url            = self.auth_url,
            auth_token          = self.auth_token,
            tenant_id           = self.tenant_id,
            tenant_name         = self.tenant_name,
            project_name        = self.project_name,
            project_id          = self.project_id,
            endpoint            = self.endpoint,
            endpoint_type       = self.endpoint_type,
            region_name         = self.region_name,
            auth_version        = self.auth_version,
            insecure            = self.insecure,
            timeout             = self.timeout,
            user_domain_id      = self.user_domain_id,
            user_domain_name    = self.user_domain_name,
            project_domain_id   = self.project_domain_id,
            project_domain_name = self.project_domain_name
        )

    def main(self, argv):
        parser = self.get_base_parser()

        # Detect wheather user has asked for help or not
        # For this, argv might be help, --help, -h or argv 
        # empty
        do_help = ('help' in argv) or ('--help' in argv) or ('-h' in argv) or not argv

        # If do_help is true then we do not need to do authentication
        skip_auth = do_help or ('bash-completion' in argv)
        (args, args_list) = parser.parse_known_args(argv)

        subcommand_parser = self.get_subcommand_parser(2, do_help=do_help)
        self.parser = subcommand_parser
        args = subcommand_parser.parse_args(argv)

        # Short-circuit and deal with help right away.
        if args.func == self.do_help:
            self.do_help(args)
            return 0
        elif args.func == self.do_bash_completion:
            self.do_bash_completion(args)
            return 0

        self.auth_version  = args.os_auth_version 
        self.auth_token    = args.os_auth_token
        self.username      = args.os_username
        self.user_id       = args.os_user_id
        self.password      = args.os_password
        self.tenant_name   = args.os_tenant_name
        self.tenant_id     = args.os_tenant_id
        self.project_name  = args.os_project_name
        self.project_id    = args.os_project_id
        self.auth_url      = args.os_auth_url
        self.region_name   = args.os_region_name
        self.endpoint      = args.os_endpoint
        self.endpoint_type = args.os_endpoint_type
        self.timeout       = args.os_timeout
        self.insecure      = args.os_insecure
        self.user_domain_id = args.os_user_domain_id
        self.user_domain_name = args.os_user_domain_name
        self.project_domain_id = args.os_project_domain_id
        self.project_domain_name = args.os_project_domain_name

        self.args = args
        args.func(self, args)

def main():
    """
    # | Shell entry pint
    # |
    # | Arguments: None
    # |
    # | Returns: None
    """
    argv = [encodeutils.safe_decode(a) for a in sys.argv[1:]]
    if ('--debug' in argv):
        SidecarShell().main(argv)
    else:
        try:
            SidecarShell().main(argv)
        except Exception as exc:
            logger.debug(exc, exc_info=1)
            print("ERROR (%s): %s"
               % (exc.__class__.__name__,
                    encodeutils.exception_to_unicode(exc)),
               file=sys.stderr)
            sys.exit(1)
        except KeyboardInterrupt:
            print("... Bye....", file=sys.stderr)
            sys.exit(130)
    

if __name__ == "__main__":
    main()
