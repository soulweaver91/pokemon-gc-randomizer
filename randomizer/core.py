#!/usr/bin/env python
# -*- coding: utf-8 -*-

import logging
import os
import random
import shutil

from contrib.gciso import gciso
from . import util, config
from .handlers import XDHandler, ColosseumHandler
from .constants import IsoGame, IsoRegion


class Randomizer:
    handler = None

    def __init__(self, rom_path, output_path, in_place=False):
        if not in_place:
            logging.info('Please wait while a copy of the original ISO is being created.')
            logging.debug('Copying from %s to %s', rom_path, output_path)
            try:
                shutil.copyfile(rom_path, output_path)
                rom_path = output_path
            except Exception as e:
                logging.error('Creating a file copy failed, aborting.')
                raise e

        logging.debug('Trying to load ISO: %s', rom_path)
        try:
            iso = gciso.IsoFile(rom_path)
            game, region = util.interpret_game_code(iso.gameCode)
            encoding = 'shift-jis' if region == IsoRegion.JPN else 'ascii'

            logging.debug('ISO loaded.')
            logging.debug('Game code: %s', iso.gameCode.decode(encoding))
            logging.debug('Internal game name: %s', iso.gameName.decode(encoding))

            if game is None:
                raise NotImplementedError(
                    'This game cannot be used with this randomizer (detected code: {})!'.format(iso.gameCode)
                )

            logging.info('Detected game: %s (%s)', game.value, region.value)

            if game == IsoGame.COLOSSEUM:
                self.handler = ColosseumHandler(iso, region)
            elif game == IsoGame.XD:
                self.handler = XDHandler(iso, region)

            seed = config.seed if config.seed else int.from_bytes(os.urandom(8), "big")
            logging.info('Randomizer seed: %d (%s)' % (seed, 'automatic' if config.seed is None else 'user provided'))
            random.seed(seed)

        except IOError as e:
            logging.error('Reading from the ISO file failed.')
            raise e

    def prepare_dump_folder(self):
        dump_dir = os.path.join(config.working_dir, 'dump')
        if not os.path.exists(dump_dir):
            try:
                os.mkdir(dump_dir)
            except OSError:
                logging.warning('Could not create dump folder, disabling dumping capability.')
                config.configure(dump_files=False)
        else:
            if not os.path.isdir(dump_dir):
                logging.warning('Dump folder is obstructed by a file, disabling dumping capability.')
                config.configure(dump_files=False)

    def randomize(self):
        if config.dump_files:
            self.prepare_dump_folder()

        self.handler.open_archives()

        self.handler.load_move_data()
        self.handler.load_tm_data()
        self.handler.load_pokemon_data()
        self.handler.load_trainer_data()
        self.handler.load_item_box_data()

        self.handler.load_game_specific_data()

        if config.rng_move_types or config.rng_move_pp or config.rng_move_power or config.rng_move_accuracy:
            self.handler.randomize_moves()
        if config.rng_tm_moves:
            self.handler.randomize_tms()

        if config.patch_impossible_evolutions:
            self.handler.patch_impossible_evolutions()

        if config.rng_pkevo:
            self.handler.randomize_pokemon_evolution()
        if config.rng_pkstats:
            self.handler.randomize_pokemon_stats()
        if config.rng_pktypes:
            self.handler.randomize_pokemon_types()
        if config.rng_pkabi:
            self.handler.randomize_pokemon_abilities()
        if config.rng_pkmoves:
            self.handler.randomize_pokemon_movesets()
        if config.rng_pktm:
            self.handler.randomize_pokemon_tms()
        if config.rng_pkitem:
            self.handler.randomize_pokemon_items()

        if config.rng_trainers:
            self.handler.randomize_trainers()
        if config.rng_items:
            self.handler.randomize_item_boxes()

        if config.improve_catch_rate:
            self.handler.improve_catch_rates()

        if config.fix_name_casing and self.handler.region in [IsoRegion.USA, IsoRegion.EUR]:
            self.handler.fix_name_casing()

        if config.rng_trade_wants or config.rng_trade_offers or config.rng_gifts:
            self.handler.randomize_and_write_trades_and_gifts()

        self.handler.randomize_game_specific_features()

        if config.rng_starters:
            self.handler.randomize_and_write_starter_data()

        self.handler.write_pokemon_data()
        self.handler.write_move_data()
        self.handler.write_tm_data()
        self.handler.write_trainer_data()
        self.handler.write_item_box_data()

        self.handler.write_game_specific_data()

        self.handler.write_archives()
        self.handler.update_banner()
