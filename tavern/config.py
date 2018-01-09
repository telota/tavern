""" This module resolves tavern's invocation configuration. """

import argparse
import os

import yaml


CLI_DESCRIPTION = """
Parse yaml + make requests against an API
""".strip()  # FIXME elaborate
ENVVAR_PREFIX = 'TAVERN_VAR_'


def parse_command_line_args():
    parser = argparse.ArgumentParser(
        description=CLI_DESCRIPTION,
        formatter_class=argparse.RawDescriptionHelpFormatter
    )

    parser.add_argument(
        "--tavern-global-cfg",
        required=False,
        help="Global configuration file to include in every test",
    )

    parser.add_argument(
        '--var',
        help='Sets a global variable, can be provided multiple times.',
        metavar='name=value',
        action='append',
        nargs=1
    )

    parser.add_argument(
        '--vars-file',
        help='Loads global variables from that file, '
             'can be provided multiple times.',
        metavar='PATH',
        action='append',
        nargs=1
    )

    parser.add_argument(
        "--log-to-file",
        help="Log output to a file (tavern.log if no argument is given)",
        nargs="?",
        const="tavern.log",
    )

    parser.add_argument(
        "--stdout",
        help="Logs output to stdout",
        action="store_true",
        default=False,
    )

    parser.add_argument(
        "--debug",
        help="Sets logging level to DEBUG.",
        action="store_true",
        default=False,
    )

    parser.add_argument(
        "in_file",
        help="Input file with tests in",
    )

    return vars(parser.parse_args())


def get_vars_from_environment():
    return {k[len(ENVVAR_PREFIX):].lower(): v for k, v in os.environ.items()
            if k.startswith(ENVVAR_PREFIX)}


def get_vars_from_files(files):
    # TODO support glob patterns
    result = {}
    for file in files:
        with open(os.path.expanduser(file), 'rt') as f:
            result.update(yaml.load(f))
    return result


def get_vars_from_cli(cli_args):
    result = {}
    for name, value in (x.split('=', 1) for x in cli_args.pop('var')):
        result[name] = value
    return result


def resolve_vars(cli_args):
    result = get_vars_from_environment()
    vars_files = cli_args.pop('vars_file', [])
    if 'tavern_global_cfg' in cli_args:
        vars_files.append(cli_args.pop('tavern_global_cfg'))
    result.update(get_vars_from_files(vars_files))
    result.update(get_vars_from_cli(cli_args))
    return result


def get_config():
    cli_args = parse_command_line_args()
    cli_args['global_vars'] = resolve_vars(cli_args)
    return cli_args


# TODO deprecate --tavern-global-cfg
