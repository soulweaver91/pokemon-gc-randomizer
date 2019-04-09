#!/usr/bin/env python
# -*- coding: utf-8 -*-

import logging
import os

from contrib.gciso import gciso
from . import util, config
from .handlers import XDHandler
from .constants import IsoGame


class Randomizer:
    handler = None

    def __init__(self, rom_path):
        logging.debug('Trying to load ISO: %s', rom_path)
        try:
            iso = gciso.IsoFile(rom_path)
            logging.debug('ISO loaded.')
            logging.debug('Game code: %s', iso.gameCode.decode('ascii'))
            logging.debug('Internal game name: %s', iso.gameName.decode('ascii'))

            game, region = util.interpret_game_code(iso.gameCode)

            if game is None:
                raise NotImplementedError(
                    'This game cannot be used with this randomizer (detected code: {})!'.format(iso.gameCode)
                )

            logging.info('Detected game: %s (%s)', game.value, region.value)

            if game == IsoGame.COLOSSEUM:
                raise NotImplementedError('Colosseum is not supported yet.')
            elif game == IsoGame.XD:
                self.handler = XDHandler(iso, region)

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
        self.handler.load_pokemon_data()

        if config.patch_impossible_evolutions:
            self.handler.patch_impossible_evolutions()

        if config.rng_pkstats:
            self.handler.randomize_pokemon_stats()
        if config.rng_pktypes:
            self.handler.randomize_pokemon_types()
        if config.rng_pkabi:
            self.handler.randomize_pokemon_abilities()

        self.handler.write_pokemon_data()
        self.handler.write_archives()
