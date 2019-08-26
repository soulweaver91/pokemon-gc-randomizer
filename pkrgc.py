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
        description="Randomizes a Pokémon Colosseum or XD ISO.",
        add_help=False
    )

    parser_behavior_group = parser.add_argument_group('Tool behavior')

    parser_behavior_group.add_argument(
        '-v', '--version',
        action='version',
        help="Display the program version and exit.",
        version="{} version {}".format(PROG_NAME, PROG_VERSION)
    )
    parser_behavior_group.add_argument(
        '-h', '--help',
        action='help',
        help="Display this help message and exit."
    )
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
        'rng-pkstats-family-vary-branched-evo',
        default=config.rng_pkstats_family_vary_branched_evo,
        help_enable='Shuffle the base stat factors for evolutions other than the first when the Pokémon has more '
                    'than one evolution.',
        help_disable='Use the same base stat factors even with branched evolutions, leading to branches having '
                     'very similar stats.'
    )
    parser_pkmn_randomization_group.add_argument(
        '--rng-pkstats-variance',
        action='store',
        default=config.rng_pkstats_variance,
        type=float,
        metavar='VAR',
        help='Decides the variance for the Gauss distribution according to which the base stat factors are generated. '
             'Lower values result in more uniform stats, while higher values result in more extreme stats.'
             '(Default: 0.35)'
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
             '(Default: ' + (', '.join(config.rng_pkabi_ban)) + ')'
    )
    add_enable_disable_argument(
        parser_pkmn_randomization_group,
        'rng-pkmoves',
        default=config.rng_pkmoves,
        help_enable='Enable Pokémon moveset randomization.',
        help_disable='Keep the original Pokémon movesets. Other --rng-pkmoves flags take no effect.'
    )
    add_enable_disable_argument(
        parser_pkmn_randomization_group,
        'rng-pkmoves-dmg-progression',
        default=config.rng_pkmoves_dmg_progression,
        help_enable='Rearrange damaging moves so thaat weaker moves are learned first.',
        help_disable='Don\'t rearrange damaging moves.'
    )
    add_enable_disable_argument(
        parser_pkmn_randomization_group,
        'rng-pkmoves-lv1-fullset',
        default=config.rng_pkmoves_lv1_fullset,
        help_enable='Provide every Pokémon with four moves at level one.',
        help_disable='Do not add additional level one move slots.'
    )
    add_enable_disable_argument(
        parser_pkmn_randomization_group,
        'rng-pkmoves-ensure-damaging-first',
        default=config.rng_pkmoves_lv1_ensure_damaging,
        help_enable='Make sure that the first move the Pokémon learns is a damaging move.',
        help_disable='The first move the Pokémon learns can be a status move.'
    )
    add_enable_disable_argument(
        parser_pkmn_randomization_group,
        'rng-pkmoves-ensure-damaging-interval',
        default=config.rng_pkmoves_ensure_damaging_interval,
        help_enable='Make sure at least every fourth move the Pokémon learns is a damaging move.',
        help_disable='The spacing of damaging moves is not controlled.'
    )
    parser_pkmn_randomization_group.add_argument(
        '--rng-pkmoves-any-type-ratio',
        action='store',
        default=config.rng_pkmoves_any_type_ratio,
        type=int,
        metavar='RATIO',
        help='Control the probability percentage of a movepool of a randomized learned move containing damaging moves '
             'of a type the Pokémon doesn\'t have. All non-damaging moves will still be available for each move slot, '
             'as well as Normal-type moves, unless otherwise enforced by --rng-pkmoves-min-own-type-ratio.'
             '(Default: 25)'
    )
    parser_pkmn_randomization_group.add_argument(
        '--rng-pkmoves-min-damaging-ratio',
        action='store',
        default=config.rng_pkmoves_min_damaging_ratio,
        type=int,
        metavar='RATIO',
        help='Control the probability percentage of a movepool for choosing a randomized learned move only containing '
             'damaging moves.'
             '(Default: 25)'
    )
    parser_pkmn_randomization_group.add_argument(
        '--rng-pkmoves-min-own-type-ratio',
        action='store',
        default=config.rng_pkmoves_min_own_type_ratio,
        type=int,
        metavar='RATIO',
        help='Control the probability percentage of a movepool for choosing a randomized learned move only containing '
             ' moves with a type of that Pokémon itself.'
             '(Default: 15)'
    )
    parser_pkmn_randomization_group.add_argument(
        '--rng-pkmoves-ban',
        nargs='*',
        metavar='MOVE',
        help='Forbid specific moves to be put into the moveset of any Pokémon whose move pool is randomized. '
             'A list of moves in upper case, with spaces converted to underscores, is expected. '
             'You can allow all moves by providing the single move name NONE. '
             '(Default: ' + (', '.join(config.rng_pkmoves_ban)) + ')'
    )
    add_enable_disable_argument(
        parser_pkmn_randomization_group,
        'rng-pkmoves-no-dupes',
        default=config.rng_pkmoves_no_dupes,
        help_enable='Make sure any Pokémon doesn\'t learn the same move twice.',
        help_disable='Pokémon are allowed to learn the same move multiple times.'
    )
    add_enable_disable_argument(
        parser_pkmn_randomization_group,
        'rng-pktm',
        default=config.rng_pktm,
        help_enable='Enable Pokémon TM learnset randomization.',
        help_disable='Keep the original Pokémon TM learnsets. Other --rng-pktm flags take no effect.'
    )
    parser_pkmn_randomization_group.add_argument(
        '--rng-pktm-min-own-type-ratio',
        action='store',
        default=config.rng_pktm_min_own_type_ratio,
        type=int,
        metavar='RATIO',
        help='Control the probability percentage of the Pokémon being able to learn TMs that contain damaging moves '
             'with the same type as the Pokémon itself.'
             '(Default: 90)'
    )
    parser_pkmn_randomization_group.add_argument(
        '--rng-pktm-min-normal-type-ratio',
        action='store',
        default=config.rng_pktm_min_normal_type_ratio,
        type=int,
        metavar='RATIO',
        help='Control the probability percentage of the Pokémon being able to learn TMs that contain Normal-type '
             'damaging moves. This ratio is not used for Normal-type Pokémon themselves.'
             '(Default: 75)'
    )
    parser_pkmn_randomization_group.add_argument(
        '--rng-pktm-min-other-type-ratio',
        action='store',
        default=config.rng_pktm_min_other_type_ratio,
        type=int,
        metavar='RATIO',
        help='Control the probability percentage of the Pokémon being able to learn TMs that contain damaging moves '
             'with a different type as the Pokémon itself, excluding Normal-type moves.'
             '(Default: 40)'
    )
    parser_pkmn_randomization_group.add_argument(
        '--rng-pktm-min-status-ratio',
        action='store',
        default=config.rng_pktm_min_status_ratio,
        type=int,
        metavar='RATIO',
        help='Control the probability percentage of the Pokémon being able to learn TMs that contain non-damaging'
             ' moves. (Default: 75)'
    )
    add_enable_disable_argument(
        parser_pkmn_randomization_group,
        'rng-pktm-family',
        default=config.rng_pktm_family,
        help_enable='Allow evolved Pokémon to always learn all TMs their pre-evolutions can learn.',
        help_disable='Pre-evolution TM learnsets are not considered.'
    )
    parser_pkmn_randomization_group.add_argument(
        '--rng-pktm-full-compat',
        action='store_true',
        help='All Pokémon learn all TMs. This is a shorthand for setting all the other TM ratio variables to 100.'
    )
    add_enable_disable_argument(
        parser_pkmn_randomization_group,
        'rng-pkevo',
        default=config.rng_pkevo,
        help_enable='Randomize the evolutions of Pokémon that originally evolve.',
        help_disable='Keep original Pokémon evolutions.'
    )
    add_enable_disable_argument(
        parser_pkmn_randomization_group,
        'rng-pkevo-shuffle',
        default=config.rng_pkevo_shuffle,
        help_enable='Shuffle existing evolutions rather than fully randomizing each evolution independently.',
        help_disable='Pick every evolution at random.'
    )
    add_enable_disable_argument(
        parser_pkmn_randomization_group,
        'rng-pkevo-samestage',
        default=config.rng_pkevo_samestage,
        help_enable='Limit randomization so that first stages only evolve into second stages and second stages '
                    'into third stages. Note that baby Pokémon are considered first stages for the purposes of the '
                    'randomizer.',
        help_disable='Allow evolutions to randomize to any other Pokémon. This may lead into strong Pokémon evolving '
                     'into weak Pokémon and long or circular evolution chains.'
    )

    parser_move_randomization_group = parser.add_argument_group('Move randomization options')
    add_enable_disable_argument(
        parser_move_randomization_group,
        'rng-tm-moves',
        default=config.rng_tm_moves,
        help_enable='Randomize the moves taught by the 50 Technical Machines.',
        help_disable='Do not change the PP of moves.'
    )
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
                    'will be between 30%% and 100%%, divisible by 5, with a tendency towards 100%% accurate moves.',
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
    add_enable_disable_argument(
        parser_trainer_randomization_group,
        'rng-trainers',
        default=config.rng_trainers,
        help_enable='Enable randomization of trainers\' Pokémon.',
        help_disable='Do not randomize trainer Pokémon.'
    )

    parser_item_randomization_group = parser.add_argument_group('Item randomization options')

    parser_gift_pkmn_randomization_group = parser.add_argument_group('Gift/Starter Pokémon options')
    add_enable_disable_argument(
        parser_gift_pkmn_randomization_group,
        'rng-starters',
        default=config.rng_starters,
        help_enable='Enable editing starter Pokémon.',
        help_disable='The default starter Pokémon are used.'
    )
    parser_gift_pkmn_randomization_group.add_argument(
        '--rng-starters-fixed',
        nargs='*',
        metavar='SPECIES',
        help='Rather than randomizing the starter Pokémon, specify which species the starter(s) should be. '
             'For Colosseum, provide two species, and for XD, provide one. Note the non-standard spellings of the '
             'following Pokémon that must be used: NIDORAN_F, NIDORAN_M, FARFETCH_D, MR_MIME'
    )
    parser_gift_pkmn_randomization_group.add_argument(
        '--rng-starters-max-bst',
        type=int,
        metavar='BST',
        default=config.rng_starters_max_bst,
        help='Limit the base stats total of the starter Pokémon to be smaller or equal to this value. Set to a '
             'high value to allow all Pokémon as starters. (Default: 500)'
    )

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

