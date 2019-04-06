#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os

__author__ = 'Soulweaver'

import logging
import argparse

from randomizer import PROG_NAME, PROG_VERSION, config, Randomizer

if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Randomizes a Pokémon Colosseum or XD ISO."
    )

    # TODO: copy this file elsewhere so that the original stays untouched
    parser.add_argument(
        'iso_path',
        action='store',
        help='A path to the ISO file to be randomized. Required.',
        metavar='isopath'
    )
    parser.add_argument(
        '-l', '--loglevel',
        action='store',
        help='The desired verbosity level. Any messages with the same or higher '
             'level than the chosen one will be displayed. '
             'Available values: critical, error, warning, info, debug. Default: info.',
        choices=['critical', 'error', 'warning', 'info', 'debug'],
        default='info',
        metavar='level'
    )
    parser.add_argument(
        '--dump-files',
        action='store_true',
        help='Dumps the files extracted from the ISO and the files to be written to the ISO. '
             'This option is only useful to you if you are a developer.'
    )
    parser.add_argument(
        '-v', '--version',
        action='version',
        version="{} version {}".format(PROG_NAME, PROG_VERSION)
    )

    args = parser.parse_args()
    logging.basicConfig(level=getattr(logging, args.loglevel.upper()),
                        format="{asctime} [{levelname}] {message}", style='{')

    config.configure(dump_files=args.dump_files, working_dir=os.path.dirname(__file__))

    randomizer = Randomizer(args.iso_path)
    randomizer.randomize()

