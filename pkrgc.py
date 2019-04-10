#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os

__author__ = 'Soulweaver'

import logging
import argparse

from randomizer import PROG_NAME, PROG_VERSION, config, Randomizer


def add_enable_disable_argument(p, name, default=False, help_enable=None, help_disable=None,
                                default_passage=' (Default)'):
    dest_name = name.replace('-', '_')

    if help_enable is not None:
        help_enable += default_passage if default else ''
    if help_disable is not None:
        help_enable += default_passage if not default else ''

    group = p.add_mutually_exclusive_group(required=False)
    group.add_argument('--' + name, dest=dest_name, action='store_true', help=help_enable)
    group.add_argument('--no-' + name, dest=dest_name, action='store_false', help=help_disable)

    p.set_defaults(**{dest_name: default})


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Randomizes a Pokémon Colosseum or XD ISO."
    )

    parser_behavior_group = parser.add_argument_group('Tool behavior')

    # TODO: copy this file elsewhere so that the original stays untouched
    parser_behavior_group.add_argument(
        'iso_path',
        action='store',
        help='A path to the ISO file to be randomized. Required.',
        metavar='isopath'
    )
    parser_behavior_group.add_argument(
        '-l', '--loglevel',
        action='store',
        help='The desired verbosity level. Any messages with the same or higher '
             'level than the chosen one will be displayed. '
             'Available values: critical, error, warning, info, debug. Default: info.',
        choices=['critical', 'error', 'warning', 'info', 'debug'],
        default='info',
        metavar='level'
    )
    parser_behavior_group.add_argument(
        '--dump-files',
        action='store_true',
        help='Dumps the files extracted from the ISO and the files to be written to the ISO. '
             'This option is only useful to you if you are a developer.'
    )
    parser_behavior_group.add_argument(
        '-v', '--version',
        action='version',
        version="{} version {}".format(PROG_NAME, PROG_VERSION)
    )

    parser_pkmn_randomization_group = parser.add_argument_group('Pokémon randomization options')
    add_enable_disable_argument(
        parser_pkmn_randomization_group,
        'rng-pkstats',
        default=config.rng_pkstats,
        help_enable='Enable Pokémon base stats randomization.',
        help_disable='Keep the original Pokémon base stats. Other --rng-pkstats flags take no effect.'
    )
    add_enable_disable_argument(
        parser_pkmn_randomization_group,
        'rng-pkstats-retain-bst',
        default=config.rng_pkstats_retain_bst,
        help_enable='Redistribute the Pokémon\'s base stat total rather than '
                    'setting the values to fully random values.',
        help_disable='Ignore the Pokémon\'s original base stat total.'
    )
    add_enable_disable_argument(
        parser_pkmn_randomization_group,
        'rng-pkstats-family',
        default=config.rng_pkstats_family,
        help_enable='Try to make the stat distributions consistent within each evolution family.',
        help_disable='Ignore the stat distribution of other evolution family members.'
    )
    add_enable_disable_argument(
        parser_pkmn_randomization_group,
        'rng-pkstats-wg-1hp',
        default=config.rng_pkstats_wg_1hp,
        help_enable='A Pokémon that has Wonder Guard is also always set to have 1 HP.',
        help_disable='A Pokémon with Wonder Guard is randomized like any other Pokémon.'
    )

    add_enable_disable_argument(
        parser_pkmn_randomization_group,
        'rng-pktypes',
        default=config.rng_pktypes,
        help_enable='Enable Pokémon type randomization.',
        help_disable='Keep the original Pokémon types. Other --rng-pktypes flags take no effect.'
    )
    add_enable_disable_argument(
        parser_pkmn_randomization_group,
        'rng-pktypes-family',
        default=config.rng_pktypes_family,
        help_enable='Try to make typing in evolution families more natural. Evolutions keep the primary type of the '
                    'previous stage Pokémon and may gain or alter the second type.',
        help_disable='Ignore the types of other evolution family members.'
    )
    parser_pkmn_randomization_group.add_argument(
        '--rng-pktypes-family-change-ratio',
        action='store',
        default=config.rng_pktypes_family_change_ratio,
        type=int,
        metavar='RATIO',
        help='Control the percentage probability of an evolved form gaining a new type. '
             'Only used if --rng-pktypes-family is also enabled.'
             '(Default: 33)'
    )
    parser_pkmn_randomization_group.add_argument(
        '--rng-pktypes-monotype-ratio',
        action='store',
        default=config.rng_pktypes_monotype_ratio,
        type=int,
        metavar='RATIO',
        help='Control the percentage probability of the randomizer forcing a Pokémon to only have a single type. '
             'This restriction does not apply to evolved forms if --rng-pktypes-family is enabled. '
             '(Default: 33)'
    )

    add_enable_disable_argument(
        parser_pkmn_randomization_group,
        'rng-pkabi',
        default=config.rng_pkabi,
        help_enable='Enable Pokémon ability randomization.',
        help_disable='Keep the original Pokémon abilities. Other --rng-pkabi flags take no effect.'
    )
    add_enable_disable_argument(
        parser_pkmn_randomization_group,
        'rng-pkabi-family',
        default=config.rng_pkabi_family,
        help_enable='Try to make abilities in evolution families more natural. Evolutions have a chance of keeping '
                    'the abilities of the previous stage Pokémon.',
        help_disable='Ignore the types of other evolution family members.'
    )
    parser_pkmn_randomization_group.add_argument(
        '--rng-pkabi-family-change-ratio',
        action='store',
        default=config.rng_pkabi_family_change_ratio,
        type=int,
        metavar='RATIO',
        help='Control the percentage probability of an evolved form getting its abilities also randomized. '
             'Only used if --rng-pkabi-family is also enabled.'
             '(Default: 33)'
    )
    parser_pkmn_randomization_group.add_argument(
        '--rng-pkabi-monoabi-ratio',
        action='store',
        default=config.rng_pkabi_monoabi_ratio,
        type=int,
        metavar='RATIO',
        help='Control the percentage probability of the randomizer forcing a Pokémon to only have a single ability. '
             'This restriction does not apply to evolved forms if --rng-pkabi-family is enabled. '
             '(Default: 33)'
    )
    parser_pkmn_randomization_group.add_argument(
        '--rng-pkabi-ban',
        nargs='*',
        metavar='ABILITY',
        help='Forbid specific abilities to be given to any Pokémon whose ability is randomized. '
             'A list of abilities in upper case, with spaces converted to underscores, is expected. '
             'You can allow all abilities by providing the single ability name NONE. '
             '(Default: WONDER_GUARD, FORECAST)'
    )

    parser_move_randomization_group = parser.add_argument_group('Move randomization options')
    add_enable_disable_argument(
        parser_move_randomization_group,
        'rng-move-power',
        default=config.rng_move_power,
        help_enable='Randomize the base power of each damaging move to a value between 10 and 180, divisible by 5.',
        help_disable='Do not change the move base powers.'
    )
    add_enable_disable_argument(
        parser_move_randomization_group,
        'rng-move-types',
        default=config.rng_move_types,
        help_enable='Randomize the type of every move except Curse and Struggle. Note that this cannot make normal '
                    'moves shadow moves and vice versa. The resulting types will be used when determining Pokémon '
                    'learn-up movesets if --rng-pkmoves is enabled.',
        help_disable='Do not change the typing of moves.'
    )
    add_enable_disable_argument(
        parser_move_randomization_group,
        'rng-move-accuracy',
        default=config.rng_move_accuracy,
        help_enable='Randomize the accuracy of every move that uses the accuracy check. The accuracy of each move '
                    'will be between 30% and 100%, divisible by 5, with a tendency towards 100% accurate moves.',
        help_disable='Do not change the accuracy of moves.'
    )
    add_enable_disable_argument(
        parser_move_randomization_group,
        'rng-move-pp',
        default=config.rng_move_pp,
        help_enable='Randomize the PP of every move to a value betwen 5 and 40, divisible by 40.',
        help_disable='Do not change the PP of moves.'
    )

    parser_trainer_randomization_group = parser.add_argument_group('Trainer randomization options')
    parser_item_randomization_group = parser.add_argument_group('Item randomization options')
    parser_gift_pkmn_randomization_group = parser.add_argument_group('Gift/Starter Pokémon options')
    parser_wild_randomization_group = parser.add_argument_group('Poké Spot randomization options (XD)')

    parser_patches_group = parser.add_argument_group('Miscellaneous patches')
    # TODO. Name casing change, etc. patches.
    add_enable_disable_argument(
        parser_patches_group,
        'update-evolutions',
        default=config.patch_impossible_evolutions,
        help_enable='Alter evolutions that would otherwise require connecting to another game to happen on a specific '
                    'level or with a specific evolution item instead. Note that evolutions are changed before they are '
                    'randomized, if --rng-pkevo is enabled. Evolutions are changed as follows: '
                    'Kadabra evolves into Alakazam at level 32. '
                    'Machoke, Graveler and Haunter evolve into Machamp, Golem and Gengar at level 37. '
                    'Onix, Porygon, Scyther and Feebas evolve into Steelix, Porygon2, Scizor and Milotic at level 30. '
                    'Seadra evolves into Kingdra at level 42. '
                    'Poliwhirl and Clamperl evolve into Politoed and Gorebyss with a Sun Stone. '
                    'Slowpoke and Clamperl evolve into Politoed and Huntail with a Moon Stone.',
        help_disable='Do not change evolution methods. Some evolutions will be unavailable.'
    )

    args = parser.parse_args()
    logging.basicConfig(level=getattr(logging, args.loglevel.upper()),
                        format="{asctime} [{levelname}] {message}", style='{')

    config.configure(working_dir=os.path.dirname(__file__), **vars(args))

    randomizer = Randomizer(args.iso_path)
    randomizer.randomize()

