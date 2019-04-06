#!/usr/bin/env python
# -*- coding: utf-8 -*-
import logging
import random
from struct import unpack, pack

from randomizer.iso.constants import Ability, Move, Type, EvolutionType, PokemonSpecies
from randomizer.iso.fsys import FsysArchive
from randomizer.iso.structs import StatSet, EvoEntry, LevelUpMoveEntry
from randomizer.util import chunked


class AbstractHandlerMethodError(NotImplementedError):
    def __init__(self):
        super().__init__('Internal error: Game specific class should implement all abstract game class methods!')


class BasePokemon:
    def __init__(self):
        self.base_stats = None
        self.ev_gain = None
        self.tm_compatibility = [False for _ in range(0, 50)]
        self.hm_compatibility = [False for _ in range(0, 8)]
        self.tutor_compatibility = []
        self.egg_moves = []
        self.evolution = []
        self.level_up_moves = []

    def set_base_stats(self, *args):
        self.base_stats = StatSet(*args)

    def set_ev_gain(self, *args):
        self.ev_gain = StatSet(*args)

    def set_learn_flags(self, tm_compatibility, hm_compatibility, tutor_compatibility=b''):
        self.tm_compatibility = [b == 1 for b in tm_compatibility]
        self.hm_compatibility = [b == 1 for b in hm_compatibility]
        self.tutor_compatibility = [b == 1 for b in tutor_compatibility]

    def set_egg_moves(self, egg_moves_packed):
        self.egg_moves = []
        for move_entry in list(chunked(2, egg_moves_packed)):
            try:
                move = Move.from_idx(unpack('>H', move_entry)[0])
                if move != Move.NONE:
                    self.egg_moves.append(move)
            except KeyError:
                pass

    def set_evolution(self, evolution_data_packed):
        self.evolution = []
        for evo_entry in list(chunked(6, evolution_data_packed)):
            entry = EvoEntry(*unpack('>BBHH', evo_entry))
            if entry.type != 0:
                self.evolution.append(entry)

    def set_level_up_moves(self, level_up_moves_packed):
        self.level_up_moves = []
        for move_entry in list(chunked(4, level_up_moves_packed)):
            entry = LevelUpMoveEntry(*unpack('>BBH', move_entry))
            if entry.move != Move.NONE:
                self.level_up_moves.append(entry)
        pass

    def encode_learn_flags(self):
        return tuple([b''.join([b'\x01' if b is True else b'\x00' for b in flag_list])
                      for flag_list in [self.tm_compatibility, self.hm_compatibility, self.tutor_compatibility]])

    def encode_egg_moves(self):
        egg_moves = b''
        for i in range(0, 8):
            try:
                egg_moves += pack('>H', self.egg_moves[i].idx)
            except IndexError:
                egg_moves += b'\x00\x00'

        return egg_moves

    def encode_evolution(self):
        evolution = b''
        for i in range(0, 5):
            try:
                evolution += pack('>BBHH', self.evolution[i].type.value, self.evolution[i].unknown1,
                                  self.evolution[i].level, self.evolution[i].evolves_to)
            except IndexError:
                evolution += b'\x00\x00\x00\x00\x00\x00'

        return evolution

    def encode_level_up_moves(self):
        level_up_moves = b''
        for i in range(0, 20):
            try:
                level_up_moves += pack('>BBH', self.level_up_moves[i].level, self.level_up_moves[i].unknown1,
                                       self.level_up_moves[i].move.idx)
            except IndexError:
                level_up_moves += b'\x00\x00\x00\x00'

        return level_up_moves

    def encode(self):
        return AbstractHandlerMethodError()


class BaseHandler:
    iso = None
    region = None
    archives = dict()
    pokemon_data = dict()

    # these should be filled in in the derived handlers
    POKEMON_DATA_OFFSET = None
    POKEMON_DATA_LIST_LENGTH = 0

    def __init__(self, iso, region):
        self.iso = iso
        self.region = region

    def open_archives(self):
        raise AbstractHandlerMethodError()

    def open_archive(self, name):
        self.archives[name] = FsysArchive.from_iso(self.iso, bytes(name))

    def write_archives(self):
        raise AbstractHandlerMethodError()

    def write_archive(self, name):
        data = self.archives[name].encode()

        self.iso.resizeFile(name, len(data))
        self.iso.writeFile(name, 0, data)
        logging.debug('Wrote %s (%d bytes) back into the ISO.', name.decode('ascii', errors='ignore'), len(data))

    # noinspection PyUnresolvedReferences
    def load_pokemon_data(self):
        logging.debug('Starting to read Pokémon data into memory.')
        try:
            common_rel = self.archives[b'common.fsys'].files['common_rel'].data
            common_rel.seek(self.POKEMON_DATA_OFFSET)

            for i in range(1, self.POKEMON_DATA_LIST_LENGTH + 1):
                logging.debug('Reading index %d of %d...', i, self.POKEMON_DATA_LIST_LENGTH)
                pkmn = self.pokemon_data[i] = self.make_pokemon_data(common_rel, i)

                logging.debug(
                    '  #%d %s, %s%s%s, %d/%d/%d/%d/%d/%d (BST %d), %s%s%s',
                    pkmn.unknown_natdex_no_1,
                    PokemonSpecies(i).name,
                    pkmn.type1.name,
                    '/' if pkmn.type1 != pkmn.type2 else '',
                    pkmn.type2.name if pkmn.type1 != pkmn.type2 else '',
                    pkmn.base_stats.hp,
                    pkmn.base_stats.attack,
                    pkmn.base_stats.defense,
                    pkmn.base_stats.sp_attack,
                    pkmn.base_stats.sp_defense,
                    pkmn.base_stats.speed,
                    pkmn.base_stats.total,
                    pkmn.ability1.name,
                    '/' if pkmn.ability2 != Ability.NONE else '',
                    pkmn.ability2.name if pkmn.ability2 != Ability.NONE else '',
                )
                logging.debug('  Learnset: %s', ', '.join([
                    '%s (%d)' % (m.move.friendly_name, m.level) for m in pkmn.level_up_moves]))
                logging.debug('  TMs: %s', ', '.join([
                    'TM%02d' % (n + 1) for n, b in enumerate(pkmn.tm_compatibility) if b is True]))
                logging.debug('  HMs: %s', ', '.join([
                    'HM%02d' % (n + 1) for n, b in enumerate(pkmn.hm_compatibility) if b is True]))
                logging.debug('  Egg moves: %s', ', '.join([m.friendly_name for m in pkmn.egg_moves]))
                for evo in pkmn.evolution:
                    if evo.type == EvolutionType.NONE:
                        continue

                    evo_specifier = ''
                    if evo.type.param_is_level:
                        evo_specifier = 'at level %d ' % evo.level
                    if evo.type.param_is_item:
                        evo_specifier = 'with item #%d ' % evo.item

                    logging.debug('  Evolves to %s %s(%s)',
                                  PokemonSpecies(evo.evolves_to).name, evo_specifier, evo.type)
        except KeyError as e:
            logging.error('Couldn\'t read Pokémon data since the required data file was not loaded.')
            raise e

    def write_pokemon_data(self):
        logging.debug('Encoding Pokémon data in preparation to be written to the ISO.')

        common_rel = self.archives[b'common.fsys'].files['common_rel'].data
        common_rel.seek(self.POKEMON_DATA_OFFSET)

        for i, pkmn in self.pokemon_data.items():
            logging.debug('Encoding index %d of %d...', i, self.POKEMON_DATA_LIST_LENGTH)
            common_rel.write(pkmn.encode())

    def get_available_normal_moves(self):
        return set(range(Move.POUND.value, Move.PSYCHO_BOOST.value)).remove([Move.STRUGGLE.value])

    def get_available_shadow_moves(self):
        return AbstractHandlerMethodError()

    def randomize_pokemon_stats(self):
        # TODO temp proof of concept
        types = self.get_normal_types()
        abilities = self.get_safe_abilities()

        for i, pkmn in self.pokemon_data.items():
            if pkmn.unknown_natdex_no_1 == 0:
                continue

            pkmn.type1 = random.choice(types)
            pkmn.type2 = random.choice(types)
            if pkmn.type1 != Type.NORMAL and pkmn.type2 == Type.NORMAL:
                # Normal type as the second type sometimes appears as hidden, so normal/? type should always
                # have the normal type as the first one
                pkmn.type2, pkmn.type1 = pkmn.type1, pkmn.type2

            if pkmn.ability1 in abilities:
                pkmn.ability1 = random.choice(abilities)
                pkmn.ability2 = random.choice(abilities)

    def make_pokemon_data(self, io_in, idx):
        return AbstractHandlerMethodError()

    @staticmethod
    def get_safe_abilities():
        return [a for a in list(Ability) if a not in [
            Ability.NONE,
            Ability.FORECAST,
            Ability.WONDER_GUARD
        ]]

    @staticmethod
    def get_normal_types():
        return [a for a in list(Type) if a not in [
            Type.CURSE,
            Type.SHADOW
        ]]

    def get_first_stages(self):
        first_stage_candidates = [pkmn.species for i, pkmn in self.pokemon_data.items() if pkmn.unknown_natdex_no_1 != 0]

        for i, pkmn in self.pokemon_data.items():
            for evo in pkmn.evolution:
                if evo.evolves_to in first_stage_candidates:
                    first_stage_candidates.remove(evo.evolves_to)

        return first_stage_candidates

