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

import config
import checksum
import publisher

copyright_notice="""
Copyright (C) 2019 Wanja Chresta
This program comes with ABSOLUTELY NO WARRANTY
This is free software, and you are welcome to redistribute it
under certain conditions. See the LICENCE file for more information.
"""

# Constants
default_config = os.path.expanduser("~/.config/cotary/config.yaml")

# Parse arguments
def parse_arguments():
    parser = argparse.ArgumentParser(
            description='Publish the checksum of a file on Twitter.',
            epilog=copyright_notice)

    # We use sys.stdin.buffer to make sure we read in binary mode
    parser.add_argument('file', type=str, nargs='?', default='--',
            help='File for which to publish checksum. If none is given, read from stdin')
    parser.add_argument('-c','--calc_only', action='store_true',
            help='Only calculate and print the checksum, do not publish it')
    parser.add_argument('--config', nargs='?', default=default_config,
            help='Use given config instead of ~/.local/cotary/config.yaml')
    parser.add_argument('-q','--quiet', action='store_true',
            help='Do not print any messages')

    return parser.parse_args()

def main():
    args = parse_arguments()
    conf = config.Config(args.config) # Read config

    def echo(*strs, **kwargs):
        if not args.quiet:
            print(*strs, **kwargs)

    def error(errno, *strs):
        echo(*strs, file=sys.stderr)
        sys.exit(errno)

    if args.file == '--': # Read from stdin
        echo("Reading from stdin.")
        fh = sys.stdin.buffer # .buffer to make sure we read raw
    else: # Is a path
        try:
            fh = open(args.file,'rb') # Read binary
        except FileNotFoundError as e:
            error(1, e.strerror, file=sys.stderr)

    # Calculate checksum
    try:
        cs = checksum.Checksum(fh)
    except ValueError:
        error(2, "Input is empty. Aborting.")
    except KeyboardInterrupt:
        error(3, "Aborted by the user.")

    echo("checksum: {}".format(cs))

    if args.calc_only:
        sys.exit(0) # Success

    publ = publisher.Publisher(conf)
    if not publ.is_configured():
        error(4, "Config file is not set up correctly.")

    try:
        status = publ.publish(cs)
    except publisher.TwitterError as e:
        try:
            errno = e.message[0]["code"]
            errmsg = e.message[0]["message"]
        except (IndexError, ValueError):
            errno = 8
            errmsg = "Unknown Twitter error"

        if errno == 187: # Status is a duplicate.
            errmsg = "This checksum was already published."

        error(errno, errmsg)

    if not args.quiet:
        import datetime
        publish_datetime = datetime.datetime.fromtimestamp(status.created_at_in_seconds)
        print("Status published at {}".format(publish_datetime))

    sys.exit(0)

if __name__=="__main__":
    main()
