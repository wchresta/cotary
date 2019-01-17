#!/usr/bin/env python3

# Copyright (C) 2019 Wanja Chresta
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.
#
#    You should have received a copy of the GNU General Public License
#    along with this program.  If not, see <https://www.gnu.org/licenses/>.

import argparse
import sys # for stdin and stderr
import os # for path manipulation

import cotary.config
import cotary.checksum
import cotary.publisher
# Parse arguments


_copyright_notice="""
Copyright (C) 2019 Wanja Chresta
This program comes with ABSOLUTELY NO WARRANTY
This is free software, and you are welcome to redistribute it
under certain conditions. See the LICENCE file for more information.
"""

_default_config=os.path.join(os.path.expanduser("~"),'.config','cotary','config.yaml')

def parse_arguments():
    # Constants
    parser = argparse.ArgumentParser(
            description='Publish the checksum of a file on Twitter.',
            epilog=_copyright_notice)

    # We use sys.stdin.buffer to make sure we read in binary mode
    parser.add_argument('file', type=str, nargs='?', default='--',
            help='File for which to publish checksum. If none is given, read from stdin')
    parser.add_argument('-c','--calc_only', action='store_true',
            help='Only calculate and print the checksum, do not publish it')
    parser.add_argument('--config', nargs='?', default=_default_config,
            help='Use given config instead of ~/.local/cotary/config.yaml')
    parser.add_argument('-q','--quiet', action='store_true',
            help='Do not print any messages')

    return parser.parse_args()


def echo(args, *strs, **kwargs):
    if not args.quiet:
        print(*strs, **kwargs)


def error(args, errno, *strs):
    echo(args, *strs, file=sys.stderr)
    sys.exit(errno)


def get_config(args):
    """Read configuration. If there is no config file, create one"""
    
    # Do we need to create a new config file?
    # Only create one, if the config path was not changed
    if args.config == _default_config:
        # Check if it exists
        if not os.path.exists(_default_config):
            # Create the config file and dump the default config
            try:
                os.makedirs(os.path.dirname(_default_config), exist_ok=True)
                fh = open(_default_config, 'w')
                fh.write(cotary.config.DEFAULT_CONFIG)
                fh.close()
            except (PermissionError):
                pass

    return cotary.config.Config(args.config) # Read config


def get_filehandler(args):
    if args.file == '--': # Read from stdin
        echo(args, "Reading from stdin.")
        return sys.stdin.buffer # .buffer to make sure we read raw
    else: # Is a path
        try:
            return open(args.file,'rb') # Read binary
        except FileNotFoundError as e:
            error(args, 1, e.strerror, file=sys.stderr)


def calc_checksum(args, fh):
    try:
        return cotary.checksum.Checksum(fh)
    except ValueError:
        error(args, 2, "Input is empty. Aborting.")
    except KeyboardInterrupt:
        error(args, 3, "Aborted by the user.")


def publish_checksum(args, config, checksum):
    publisher = cotary.publisher.Publisher(config)
    if not publisher.is_configured():
        error(args, 4, "Config file {} is not set up correctly.".format(args.config))

    try:
        return publisher.publish(cs)
    except publisher.TwitterError as e:
        # Something went wrong; try to give a somewhat good error message
        try:
            errno = e.message[0]["code"]
            errmsg = e.message[0]["message"]
        except (IndexError, ValueError):
            errno = 8
            errmsg = "Unknown Twitter error"

        if errno == 187: # Status is a duplicate.
            errmsg = "This checksum was already published."

        error(args, errno, errmsg)


def main():
    args = parse_arguments()
    config = get_config(args)

    fh = get_filehandler(args)

    # Calculate checksum
    checksum = calc_checksum(args, fh)
    echo(args, "checksum: {}".format(checksum))

    if args.calc_only: # User does not want to publish checksum
        sys.exit(0) # Success

    # Publish checksum and get the published twitter status back
    status = publish_checksum(args, config, checksum)

    if not args.quiet:
        import datetime
        publish_datetime = datetime.datetime.fromtimestamp(status.created_at_in_seconds)
        print("Status published at {}".format(publish_datetime))

    sys.exit(0)

if __name__=="__main__":
    main()
