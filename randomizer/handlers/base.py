#!/usr/bin/env python
# -*- coding: utf-8 -*-

from datetime import datetime
import logging
import math
import os
import random
from struct import unpack, pack

from randomizer import config
from randomizer.constants import BANNER_META_SIZE, BANNER_META_FIRST_OFFSET, IsoRegion
from randomizer.iso.constants import Ability, Move, Type, EvolutionType, PokemonSpecies, VALID_POKEMON_TYPES, Item
from randomizer.iso.fsys import FsysArchive
from randomizer.iso.structs import StatSet, EvoEntry, LevelUpMoveEntry
from randomizer.util import chunked, flatten

RANDOM_BST_MIN = 120
RANDOM_BST_MAX = 800
BASE_STAT_MINIMUM = 15
BASE_STAT_MAXIMUM = 255


class AbstractHandlerMethodError(NotImplementedError):
    def __init__(self):
        super().__init__('Internal error: Game specific class should implement all abstract game class methods!')


class BasePokemon:
    def __init__(self):
        self.exp_class = None
        self.catch_rate = None
        self.gender_ratio = None
        self.exp_gain = None
        self.base_happiness = None
        self.natdex_no = None
        self.base_stats = None
        self.ev_gain = None
        self.type1 = None
        self.type2 = None
        self.ability1 = None
        self.ability2 = None
        self.item1 = None
        self.item2 = None
        self.height = None
        self.weight = None
        self.species = None
        self.tm_compatibility = [False for _ in range(0, 50)]
        self.hm_compatibility = [False for _ in range(0, 8)]
        self.tutor_compatibility = []
        self.egg_moves = []
        self.evolution = []
        self.level_up_moves = []

        self.tm_moves_list = []

    def __str__(self):
        return "#%03d %s, %s/%s" % (self.natdex_no, self.species.name, self.type1.name, self.type2.name)

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
                move = Move(unpack('>H', move_entry)[0])
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
                egg_moves += pack('>H', self.egg_moves[i].value)
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
                                       self.level_up_moves[i].move.value)
            except IndexError:
                level_up_moves += b'\x00\x00\x00\x00'

        return level_up_moves

    def randomize_base_stats(self, keep_bst, stat_distribution=None, list_index=None):
        if self.base_stats.total == 0:
            return

        if list_index is not None and list_index > 0:
            random.shuffle(stat_distribution)

        new_bst = self.base_stats.total if keep_bst else round(
            min(RANDOM_BST_MAX, max(RANDOM_BST_MIN, random.gauss(
                (RANDOM_BST_MAX + RANDOM_BST_MIN) / 2,
                (RANDOM_BST_MAX - RANDOM_BST_MIN) / 6)))
        )

        if stat_distribution is None:
            stat_distribution = [max(0, random.gauss(1, config.rng_pkstats_variance)) for _ in range(0, 6)]

        multiplier = sum(stat_distribution) / 6 * (new_bst / 6)

        new_stats = [min(BASE_STAT_MAXIMUM, max(BASE_STAT_MINIMUM, round(stat * multiplier)))
                     for stat in stat_distribution]

        if config.rng_pkstats_wg_1hp and self.ability1 == Ability.WONDER_GUARD or self.ability2 == Ability.WONDER_GUARD:
            new_stats[0] = 1

        # Fudge random stats until we're at target BST
        while sum(new_stats) > new_bst:
            stat_idx = random.randint(0, 5)
            if new_stats[stat_idx] > BASE_STAT_MINIMUM and new_stats[stat_idx] != 1:
                new_stats[stat_idx] -= 1

        while sum(new_stats) < new_bst:
            stat_idx = random.randint(0, 5)
            if new_stats[stat_idx] < BASE_STAT_MAXIMUM and new_stats[stat_idx] != 1:
                new_stats[stat_idx] += 1

        self.base_stats = StatSet(*new_stats)

        logging.debug('%s\'s base stats are now %s', self.species.name, self.base_stats)

        return stat_distribution

    def randomize_types(self, previous_stage_types=None):
        if previous_stage_types is not None:
            self.type1, self.type2 = previous_stage_types

            if random.random() < config.rng_pktypes_family_change_ratio / 100:
                # Normal type is handled differently:
                # - solo Normal type can evolve into solo or dual other type
                # - Normal/? type needs to have its first type replaced rather than the second one
                # - Non-Normal type cannot be randomized back to Normal
                if self.type1 == Type.NORMAL and self.type2 == Type.NORMAL:
                    return self.randomize_types()
                elif self.type1 == Type.NORMAL:
                    self.type1 = random.choice([t for t in VALID_POKEMON_TYPES if t != Type.NORMAL])
                else:
                    self.type2 = random.choice([t for t in VALID_POKEMON_TYPES if t != self.type2 and t != Type.NORMAL])

        else:
            self.type1 = random.choice(VALID_POKEMON_TYPES)

            if random.random() < config.rng_pktypes_monotype_ratio / 100:
                self.type2 = self.type1
            else:
                # Normal type as the second type sometimes appears as hidden (for example in XD Strategy Memo)
                # even though canonically solo types are encoded as matching type 1 and type 2. To fix this,
                # Normal/? types are never allowed unless the Pokémon is monotype
                self.type2 = random.choice([t for t in VALID_POKEMON_TYPES if t != Type.NORMAL])

        logging.debug('%s is now the %s%s%s type', self.species.name,
                      self.type1.name,
                      '/' if self.type1 != self.type2 else '',
                      self.type2.name if self.type1 != self.type2 else '')

        return self.type1, self.type2

    def randomize_abilities(self, allowed_abilities, previous_stage_abilities=None):
        if previous_stage_abilities is not None:
            self.ability1, self.ability2 = previous_stage_abilities

            if random.random() < config.rng_pkabi_family_change_ratio / 100:
                return self.randomize_abilities(allowed_abilities)

        else:
            self.ability1 = random.choice(allowed_abilities)

            if random.random() < config.rng_pkabi_monoabi_ratio / 100:
                self.ability2 = Ability.NONE
            else:
                self.ability2 = random.choice(allowed_abilities)

        # Special case: if Wonder Guard is allowed and a Pokémon with it has 1 HP, then that Pokémon should never
        # get an alternate ability as it would just be unusable.
        if config.rng_pkstats_wg_1hp and (
                self.ability1 == Ability.WONDER_GUARD or self.ability2 == Ability.WONDER_GUARD):
            self.ability1 = Ability.WONDER_GUARD
            self.ability2 = Ability.NONE

        if self.ability1 == self.ability2:
            self.ability2 = Ability.NONE

        logging.debug('%s has now the abilit%s %s%s%s', self.species.name,
                      'ies' if self.ability2 != Ability.NONE else 'y',
                      self.ability1.name,
                      '/' if self.ability2 != Ability.NONE else '',
                      self.ability2.name if self.ability2 != Ability.NONE else '')

        return self.ability1, self.ability2

    def select_random_move_from_movepool(self, movepool, allow_all_types, force_same_type, force_offensive):
        viable_moves = [
            m for m in movepool
            if (
                not force_offensive or m.power > 0
            ) and (
                allow_all_types
                or m.power == 0
                or m.type in [Type.NORMAL, self.type1, self.type2]
            ) and (
                not force_same_type
                or m.type in [self.type1, self.type2]
            ) and not (
                config.rng_pkmoves_no_dupes
                and m.move in [n.move for n in self.level_up_moves]
            )
        ]

        return random.choice(viable_moves)

    def randomize_moveset(self, movepool):
        if config.rng_pkmoves_lv1_fullset:
            lv1_move_count = len([m for m in self.level_up_moves if m.move != Move.NONE and m.level == 1])
            for i in range(lv1_move_count, 4):
                self.level_up_moves.insert(0, LevelUpMoveEntry(1, 0, Move.NONE))
            if len(self.level_up_moves) > 20:
                self.level_up_moves = self.level_up_moves[0:20]

        # Already assigned moves are possibly filtered out
        for move in self.level_up_moves:
            move.move = Move.NONE

        offensive_moves = []
        offensive_move_drought = 4 if config.rng_pkmoves_lv1_ensure_damaging else 0

        for i, slot in enumerate(self.level_up_moves):
            allow_all_types = random.random() < (config.rng_pkmoves_any_type_ratio / 100)
            force_offensive = random.random() < (config.rng_pkmoves_min_damaging_ratio / 100)
            force_same_type = random.random() < (config.rng_pkmoves_min_own_type_ratio / 100)

            try:
                if config.rng_pkmoves_ensure_damaging_interval and offensive_move_drought > 3:
                    offensive_move_drought = 0
                    move = self.select_random_move_from_movepool(
                        movepool, allow_all_types, force_same_type, True)
                else:
                    move = self.select_random_move_from_movepool(
                        movepool, allow_all_types, force_same_type, force_offensive)
            except IndexError:
                # Restrictions exhausted all available move options, so add one with no restrictions
                move = self.select_random_move_from_movepool(
                    movepool, True, False, False)

            slot.move = move.move
            if move.power == 0:
                offensive_move_drought += 1
            else:
                offensive_move_drought = 0
                # Exclude special damage moves (1 BP) from rearrangement
                if move.power >= 10:
                    offensive_moves.append((i, move))

        if config.rng_pkmoves_dmg_progression:
            indices = [m[0] for m in offensive_moves]
            offensive_moves = sorted(offensive_moves, key=lambda m: m[1].power)

            for i, m in enumerate(offensive_moves):
                self.level_up_moves[indices[i]].move = m[1].move

        logging.debug('%s now learns %s', self.species.name,
                      ', '.join(['%s on level %d' % (m.move.name, m.level) for m in self.level_up_moves]))

    def randomize_compatibility(self, moves_data, previous_stage_compat, target_property,
                                status_ratio, own_type_ratio, normal_type_ratio, other_type_ratio):
        for i, move in enumerate(moves_data):
            if move.power == 0:
                # Status move
                ratio = status_ratio
            elif move.type == self.type1 or move.type == self.type2:
                ratio = own_type_ratio
            elif move.type == Type.NORMAL:
                ratio = normal_type_ratio
            else:
                ratio = other_type_ratio

            getattr(self, target_property)[i] = random.random() < ratio / 100

        # Optionally mark previous stage learnable moves as learnable by this Pokémon too
        if previous_stage_compat is not None:
            for i in range(len(previous_stage_compat)):
                getattr(self, target_property)[i] = getattr(self, target_property)[i] or previous_stage_compat[i]

        return getattr(self, target_property)

    def randomize_tms(self, tm_data, previous_stage_tms=None):
        compatibility = self.randomize_compatibility(tm_data, previous_stage_tms, "tm_compatibility",
                                                     config.rng_pktm_min_status_ratio,
                                                     config.rng_pktm_min_own_type_ratio,
                                                     config.rng_pktm_min_normal_type_ratio,
                                                     config.rng_pktm_min_other_type_ratio)
        self.update_tm_move_set(tm_data)

        logging.debug('%s now learns the following TM moves: %s', self.species.name,
                      ', '.join([tm_data[i].move.name for i, l in enumerate(self.tm_compatibility) if l is True]))
        return compatibility

    def update_tm_move_set(self, tm_data):
        self.tm_moves_list = [tm_data[i].move for i, l in enumerate(self.tm_compatibility) if l is True]

    def randomize_item(self):
        if random.random() < config.rng_pkitem_ratio / 100:
            item = random.choice([i for i in Item if Item.NONE.value < i.value <= Item.TM50.value])
            self.item1 = item
            self.item2 = item
        else:
            self.item1 = Item.NONE
            self.item2 = Item.NONE

    def patch_evolution(self, index, evo_type, level_or_item):
        self.evolution[index].type = evo_type
        self.evolution[index].level = level_or_item.value if type(level_or_item) == Item else level_or_item
        self.evolution[index].item = Item(level_or_item)

    def get_legal_moves_at_level(self, level):
        return [m.move for m in self.level_up_moves if m.level <= level], self.tm_moves_list

    def encode(self):
        raise AbstractHandlerMethodError()


class BaseMoveEntry:
    def __init__(self):
        self.priority = None
        self.pp = None
        self.type = None
        self.targets = None
        self.accuracy = None
        self.effect_proc = None
        self.contact = None
        self.protectable = None
        self.magic_coat = None
        self.snatchable = None
        self.mirror_movable = None
        self.kings_rock_proc = None
        self.sound_move = None
        self.hm = None
        self.recoil = None
        self.power = None
        self.effect_type = None
        self.name_id = None
        self.anim_id = None
        self.desc_id = None
        self.move = None

    def __str__(self):
        return "%s (%s), %dBP, %d%%" % (self.move.name, self.type.name, self.power, self.accuracy)

    def encode(self):
        raise AbstractHandlerMethodError()

    def randomize(self, change_type, change_pp, change_power, change_acc):
        if change_type and self.move not in [Move.CURSE, Move.STRUGGLE]:
            self.type = random.choice(VALID_POKEMON_TYPES)

        if change_power and self.power > 10:
            self.power = random.randint(2, 18) * 5

        if change_acc and self.accuracy > 0:
            rand = random.random()
            # Linear scale from 30% to 280% that is clamped to 30-100%, meaning about 70% chance of
            # normal 100% accuracy and about 30% chance spread evenly among all multiples of 5 between 30% and 100%.
            self.accuracy = min(100, 30 + round(rand * 50) * 5)

        if change_pp and self.pp > 1:
            self.pp = random.randint(1, 8) * 5


class ItemBox:
    SIGNATURE = '>BBhHH6sHfff'

    def __init__(self, data, idx):
        super().__init__()

        (
            self.type,
            self.quantity,
            self.angle,
            self.room_id,
            self.flags,
            self.unknown_0x08_0x0D,
            item_id,
            self.coord_x,
            self.coord_y,
            self.coord_z

        ) = unpack(self.SIGNATURE, data)

        self.item = Item(item_id)

    def encode(self):
        return pack(
            self.SIGNATURE,
            self.type,
            self.quantity,
            self.angle,
            self.room_id,
            self.flags,
            self.unknown_0x08_0x0D,
            self.item.value,
            self.coord_x,
            self.coord_y,
            self.coord_z)

    @property
    def type_text(self):
        if self.type == 0x24:
            return 'box'
        elif self.type == 0x44:
            return 'sparkle'
        elif self.type == 0x6C:
            return 'ring binder'
        else:
            return 'unknown'

    def randomize(self, allowed_items, berry_reroll_count, random_qty, item_pool):
        # Don't ever randomize key items
        if self.item not in allowed_items:
            return

        if item_pool is not None:
            item_entry = item_pool.pop()
            self.item = item_entry[0]
            self.quantity = item_entry[1]
        else:
            for i in range(berry_reroll_count):
                self.item = random.choice(allowed_items)
                if self.item.value < Item.CHERI_BERRY.value or self.item.value > Item.STARF_BERRY.value:
                    break

        if random_qty:
            self.quantity = 16 - round(math.pow(random.randint(1, 65536), 1/4) * 15/16)


class BaseHandler:
    # these should be filled in in the derived handlers
    POKEMON_DATA_LIST_LENGTH = 0
    MOVE_DATA_LIST_LENGTH = 0
    ITEM_BOX_LIST_LENGTH = 0

    def __init__(self, iso, region):
        self.iso = iso
        self.region = region

        self.archives = dict()
        self.pokemon_data = dict()
        self.move_data = dict()
        self.item_box_data = dict()
        self.tm_data = []
        self.tutor_data = []

        # Cacophony is banned because it doesn't have a description and as such crashes the Pokémon status screen and
        # Strategy Memo. It might not work anyways, and its effect is a duplicate one, so it isn't needed in any case.
        self.allowed_abilities = [a for a in list(Ability)
                                  if a not in [Ability.NONE, Ability.CACOPHONY]
                                  and a.name not in [n.upper() for n in config.rng_pkabi_ban]]
        self.banned_learnset_moves = [n.upper() for n in config.rng_pkmoves_ban]
        self.normal_pokemon = []
        self.dol_file = iso.open(b'start.dol')

        if config.dump_files:
            dump_path = os.path.join(config.working_dir, 'dump', 'start.dol')
            try:
                with open(dump_path, 'wb') as f:
                    f.write(self.dol_file.read())
            except IOError:
                logging.warning('Couldn\'t dump the file %s, skipping dumping.', dump_path)

    def open_archives(self):
        for archive in self.archive_list:
            self.open_archive(archive)

    def open_archive(self, name):
        self.archives[name] = FsysArchive.from_iso(self.iso, bytes(name))

    def write_archives(self):
        logging.info('Compressing and writing archive files back into the ISO. Be patient, this may take a while!')
        for archive in self.archive_list:
            self.write_archive(archive)

    def write_archive(self, name):
        logging.info('Writing archive %s into the file.' % name.decode('ascii', errors='ignore'))
        data = self.archives[name].encode()

        self.iso.resizeFile(name, len(data))
        self.iso.writeFile(name, 0, data)
        logging.debug('Wrote %s (%d bytes) back into the ISO.', name.decode('ascii', errors='ignore'), len(data))

    def load_pokemon_data(self):
        logging.info('Reading Pokémon data from the archive file.')
        try:
            common_rel = self.archives[b'common.fsys'].get_file(b'common_rel').data
            common_rel.seek(self.pokemon_data_offset)

            for i in range(1, self.POKEMON_DATA_LIST_LENGTH + 1):
                logging.debug('Reading index %d of %d...', i, self.POKEMON_DATA_LIST_LENGTH)
                pkmn = self.pokemon_data[i] = self.make_pokemon_data(common_rel, i)
                pkmn.update_tm_move_set(self.tm_data)

                logging.debug(
                    '  #%d %s, %s%s%s, %d/%d/%d/%d/%d/%d (BST %d), %s%s%s',
                    pkmn.natdex_no,
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
                    '%s (%d)' % (m.move.name, m.level) for m in pkmn.level_up_moves]))
                logging.debug('  TMs: %s',
                              ', '.join(['TM%02d %s' % (n + 1, self.tm_data[n].move.name)
                                        for n, b in enumerate(pkmn.tm_compatibility) if b is True]))
                logging.debug('  HMs (not available): %s',
                              ', '.join(['HM%02d' % (n + 1)
                                         for n, b in enumerate(pkmn.hm_compatibility) if b is True]))
                logging.debug('  Egg moves: %s', ', '.join([m.name for m in pkmn.egg_moves]))
                for evo in pkmn.evolution:
                    if evo.type == EvolutionType.NONE:
                        continue

                    evo_specifier = ''
                    if evo.type.param_is_level:
                        evo_specifier = 'at level %d ' % evo.level
                    if evo.type.param_is_item:
                        evo_specifier = 'with item %s ' % evo.item.name

                    logging.debug('  Evolves to %s %s(%s)',
                                  PokemonSpecies(evo.evolves_to).name, evo_specifier, evo.type.name)

            self.normal_pokemon = list(filter(lambda pkmn: 0 < pkmn.natdex_no < 388, self.pokemon_data.values()))
        except KeyError as e:
            logging.error('Couldn\'t read Pokémon data since the required data file was not loaded.')
            raise e

    def load_move_data(self):
        logging.info('Reading move data from the archive file.')
        try:
            common_rel = self.archives[b'common.fsys'].get_file(b'common_rel').data
            common_rel.seek(self.move_data_offset)

            for i in range(1, self.MOVE_DATA_LIST_LENGTH + 1):
                logging.debug('Reading index %d of %d...', i, self.MOVE_DATA_LIST_LENGTH)
                move = self.move_data[i] = self.make_move_data(common_rel, i)

                logging.debug(
                    '  #%d %s, %s, %d BP, %d PP, %d%% accuracy',
                    i,
                    self.move_data[i].move.name,
                    move.type.name,
                    move.power,
                    move.pp,
                    move.accuracy
                )

        except KeyError as e:
            logging.error('Couldn\'t read move data since the required data file was not loaded.')
            raise e

    def load_tm_data(self):
        logging.debug('Reading TM data from the executable binary.')
        self.dol_file.seek(self.tm_data_offset)
        for i in range(0, 50):
            self.dol_file.seek(6, 1)
            move = self.move_data[unpack(">H", self.dol_file.read(2))[0]]
            self.tm_data.append(move)
            logging.debug('  TM%02d contains %s', i + 1, move.move.name)

    def write_pokemon_data(self):
        logging.debug('Encoding Pokémon data in preparation to be written to the ISO.')

        common_rel = self.archives[b'common.fsys'].get_file(b'common_rel').data
        common_rel.seek(self.pokemon_data_offset)

        for i, pkmn in self.pokemon_data.items():
            logging.debug('Encoding index %d of %d...', i, self.POKEMON_DATA_LIST_LENGTH)
            common_rel.write(pkmn.encode())

    def write_move_data(self):
        logging.debug('Encoding move data in preparation to be written to the ISO.')

        common_rel = self.archives[b'common.fsys'].get_file(b'common_rel').data
        common_rel.seek(self.move_data_offset)

        for i, move in self.move_data.items():
            logging.debug('Encoding index %d of %d...', i, self.MOVE_DATA_LIST_LENGTH)
            common_rel.write(move.encode())

    def write_tm_data(self):
        logging.info('Writing TM data into the executable binary.')
        self.dol_file.seek(self.tm_data_offset)
        for m in self.tm_data:
            self.dol_file.seek(6, 1)
            self.dol_file.write(pack(">H", m.move.value))

    def load_trainer_data(self):
        raise AbstractHandlerMethodError()

    def write_trainer_data(self):
        raise AbstractHandlerMethodError()

    def load_item_box_data(self):
        logging.info('Reading item box data from the archive file.')
        try:
            common_rel = self.archives[b'common.fsys'].get_file(b'common_rel').data
            common_rel.seek(self.item_data_offset)

            for i in range(1, self.ITEM_BOX_LIST_LENGTH + 1):
                item_box = self.item_box_data[i] = self.make_item_box_data(common_rel, i)

                logging.debug(
                    '  #%d %d x %s (%s)',
                    i,
                    item_box.quantity,
                    item_box.item.name,
                    item_box.type_text
                )

        except KeyError as e:
            logging.error('Couldn\'t read item box data since the required data file was not loaded.')
            raise e

    def write_item_box_data(self):
        logging.debug('Encoding item box data in preparation to be written to the ISO.')

        common_rel = self.archives[b'common.fsys'].get_file(b'common_rel').data
        common_rel.seek(self.item_data_offset)

        for i, item in self.item_box_data.items():
            logging.debug('Encoding index %d of %d...', i, self.ITEM_BOX_LIST_LENGTH)
            common_rel.write(item.encode())

    def get_available_regular_moves(self):
        return [m for _, m in self.move_data.items() if m.move not in [Move.STRUGGLE, Move.NONE]
                and m.move.value < Move.UNUSED_0x163.value]

    def get_game_specific_randomizable_items(self):
        return []

    def randomize_pokemon_get_root_level_list(self, condition):
        return self.get_first_stages() if condition else self.normal_pokemon

    def randomize_pokemon_aspect_recur(self, aspect, result_arg_name, pkmn_list, recurse,
                                       previous_result=None, pass_index=False, already_done=set(), **kwargs):
        for i, pkmn in enumerate(pkmn_list):
            args = {
                result_arg_name:  previous_result
            }
            if pass_index and recurse and previous_result is not None:
                args['list_index'] = i

            randomization_result = getattr(pkmn, 'randomize_' + aspect)(**args, **kwargs)
            if recurse:
                evolution_targets = [self.pokemon_data[evo.evolves_to.value] for evo in pkmn.evolution
                                     if evo.evolves_to is not PokemonSpecies.NONE
                                     and self.pokemon_data[evo.evolves_to.value].species not in already_done]

                self.randomize_pokemon_aspect_recur(
                    aspect, result_arg_name, evolution_targets,
                    previous_result=randomization_result, recurse=True, pass_index=pass_index,
                    already_done=already_done.union(set([p.species for p in pkmn_list])), **kwargs)

    def randomize_pokemon_stats(self):
        logging.info('Randomizing Pokémon stats.')
        self.randomize_pokemon_aspect_recur('base_stats', 'stat_distribution',
                                            self.randomize_pokemon_get_root_level_list(config.rng_pkstats_family),
                                            recurse=config.rng_pkstats_family, pass_index=True,
                                            keep_bst=config.rng_pkstats_retain_bst)

    def randomize_pokemon_types(self):
        logging.info('Randomizing Pokémon types.')
        self.randomize_pokemon_aspect_recur('types', 'previous_stage_types',
                                            self.randomize_pokemon_get_root_level_list(config.rng_pktypes_family),
                                            recurse=config.rng_pktypes_family)

    def randomize_pokemon_abilities(self):
        logging.info('Randomizing Pokémon abilities.')
        self.randomize_pokemon_aspect_recur('abilities', 'previous_stage_abilities',
                                            self.randomize_pokemon_get_root_level_list(config.rng_pkabi_family),
                                            recurse=config.rng_pkabi_family, allowed_abilities=self.allowed_abilities)

    def randomize_pokemon_movesets(self):
        logging.info('Randomizing Pokémon movesets.')
        allowed_moves = [m for m in self.get_available_regular_moves() if m.move.name not in self.banned_learnset_moves]
        for pkmn in self.normal_pokemon:
            pkmn.randomize_moveset(allowed_moves)

    def randomize_pokemon_tms(self):
        logging.info('Randomizing Pokémon TM learnsets.')
        self.randomize_pokemon_aspect_recur('tms', 'previous_stage_tms',
                                            self.randomize_pokemon_get_root_level_list(config.rng_pktm_family),
                                            recurse=config.rng_pktm_family, tm_data=self.tm_data)

    def randomize_pokemon_items(self):
        logging.info('Randomizing Pokémon held items.')
        for pkmn in self.normal_pokemon:
            pkmn.randomize_item()
            if pkmn.item1 == Item.NONE:
                logging.debug('Wild %s is no longer holding any item' % pkmn.species.name)
            else:
                logging.debug('Wild %s is now holding %s' % (pkmn.species.name, pkmn.item1.name))

    def randomize_pokemon_evolutions_pass(self, evolvers, evolutions):
        def debug_message(pkmn):
            new_evos = [e.evolves_to.name for e in pkmn.evolution
                        if e.evolves_to != PokemonSpecies.NONE]
            if len(new_evos) == 0:
                return
            logging.debug('%s now evolves into %s' % (pkmn.species.name, ', '.join(new_evos)))

        if config.rng_pkevo_shuffle:
            evolutions = [e for e in evolutions]
            random.shuffle(evolutions)
            for evolver in evolvers:
                for evo in evolver.evolution:
                    if evo.evolves_to != PokemonSpecies.NONE:
                        # We should always have the right amount of evolutions to pop from the list.
                        evo.evolves_to = evolutions.pop().species
                debug_message(evolver)
        else:
            for evolver in evolvers:
                for evo in evolver.evolution:
                    if evo.evolves_to != PokemonSpecies.NONE:
                        evo.evolves_to = random.choice(evolutions).species
                debug_message(evolver)
        pass

    def randomize_pokemon_evolution(self):
        logging.info('Randomizing Pokémon evolutions.')
        if config.rng_pkevo_samestage:
            current_stage = self.get_first_stages()
            while len(current_stage) > 0:
                next_stage = [
                    self.pokemon_data[e.evolves_to.value] for e in flatten([p.evolution for p in current_stage])
                    if e.evolves_to != PokemonSpecies.NONE
                ]

                self.randomize_pokemon_evolutions_pass(current_stage, next_stage)
                current_stage = next_stage
        else:
            self.randomize_pokemon_evolutions_pass(self.normal_pokemon, self.normal_pokemon)

    def randomize_moves(self):
        logging.info('Randomizing move data.')
        for i, move in self.move_data.items():
            move.randomize(config.rng_move_types, config.rng_move_pp,
                           config.rng_move_power, config.rng_move_accuracy)

    def randomize_tms(self):
        # TODO: TM item descriptions should be updated with the newly selected moves' descriptions as well.
        logging.info('Randomizing TM data.')
        self.tm_data = random.sample(self.get_available_regular_moves(), 50)
        for i, move in enumerate(self.tm_data):
            logging.debug('  TM%02d now contains %s', i + 1, move.move.name)

    def randomize_trainers(self):
        raise AbstractHandlerMethodError()

    def randomize_item_boxes(self):
        logging.info('Randomizing item boxes.')

        allowed_items = [i for i in Item if Item.NONE.value < i.value <= Item.TM50.value] \
                        + self.get_game_specific_randomizable_items()

        original_items = None
        if config.rng_items_shuffle:
            original_items = [(box.item, box.quantity) for i, box in self.item_box_data.items()
                              if box.item in allowed_items]
            random.shuffle(original_items)

        for i, item_box in self.item_box_data.items():
            item_box.randomize(allowed_items, config.rng_items_berry_reroll,
                               config.rng_items_random_qty, original_items)
            logging.debug(
                '  Item %s #%d now contains %d x %s',
                item_box.type_text,
                i,
                item_box.quantity,
                item_box.item.name
            )

    def load_game_specific_data(self):
        pass

    def write_game_specific_data(self):
        pass

    def randomize_game_specific_features(self):
        pass

    def randomize_and_write_starter_data(self):
        raise AbstractHandlerMethodError()

    def randomize_and_write_trades_and_gifts(self):
        raise AbstractHandlerMethodError()

    def improve_catch_rates(self):
        raise AbstractHandlerMethodError()

    def patch_impossible_evolutions(self):
        logging.info('Patching impossible evolutions.')
        # Plain trade evolution after evolving once
        self.pokemon_data[PokemonSpecies.KADABRA].patch_evolution(0, EvolutionType.LEVEL_UP, 32)
        self.pokemon_data[PokemonSpecies.MACHOKE].patch_evolution(0, EvolutionType.LEVEL_UP, 37)
        self.pokemon_data[PokemonSpecies.GRAVELER].patch_evolution(0, EvolutionType.LEVEL_UP, 37)
        self.pokemon_data[PokemonSpecies.HAUNTER].patch_evolution(0, EvolutionType.LEVEL_UP, 37)

        # Trade evolution with item, no branching
        self.pokemon_data[PokemonSpecies.ONIX].patch_evolution(0, EvolutionType.LEVEL_UP, 30)
        self.pokemon_data[PokemonSpecies.SCYTHER].patch_evolution(0, EvolutionType.LEVEL_UP, 30)
        self.pokemon_data[PokemonSpecies.PORYGON].patch_evolution(0, EvolutionType.LEVEL_UP, 30)
        self.pokemon_data[PokemonSpecies.SEADRA].patch_evolution(0, EvolutionType.LEVEL_UP, 42)

        # Trade evolution with item, with branching
        self.pokemon_data[PokemonSpecies.POLIWHIRL].patch_evolution(1, EvolutionType.STONE_EVOLUTION, Item.SUN_STONE)
        self.pokemon_data[PokemonSpecies.SLOWPOKE].patch_evolution(1, EvolutionType.STONE_EVOLUTION, Item.MOON_STONE)
        self.pokemon_data[PokemonSpecies.CLAMPERL].patch_evolution(0, EvolutionType.STONE_EVOLUTION, Item.SUN_STONE)
        self.pokemon_data[PokemonSpecies.CLAMPERL].patch_evolution(1, EvolutionType.STONE_EVOLUTION, Item.MOON_STONE)

        # High beauty evolution; Orre doesn't have PokéBlocks
        self.pokemon_data[PokemonSpecies.FEEBAS].patch_evolution(0, EvolutionType.LEVEL_UP, 30)

        self.patch_impossible_game_specific_evolutions()

    def patch_impossible_game_specific_evolutions(self):
        return

    def make_pokemon_data(self, io_in, idx) -> BasePokemon:
        raise AbstractHandlerMethodError()

    def make_move_data(self, io_in, idx) -> BaseMoveEntry:
        raise AbstractHandlerMethodError()

    def make_item_box_data(self, io_in, idx):
        return ItemBox(io_in.read(0x1C), idx)

    def fix_name_casing(self):
        logging.debug('Fixing name casing.')

        common_rel = self.archives[b'common.fsys'].get_file(b'common_rel').data
        regions = self.fixable_name_offsets
        for region_start, region_end in regions:
            common_rel.seek(region_start)
            should_cap = True
            while common_rel.tell() < region_end:
                char = unpack('>H', common_rel.read(2))[0]

                if 0x0040 < char < 0x005C or 0x00BF < char < 0x00D7 or 0x00D7 < char < 0x00E0:
                    if not should_cap:
                        common_rel.seek(-2, 1)
                        common_rel.write(pack('>H', (char | 0x0020)))
                    should_cap = False
                else:
                    # keep using lowercase after an apostrophe (the Farfetch'd case)
                    # and after already lowercase letters (like in POKéMON which would otherwise become PokéMon)
                    if char in [0x0027] or 0x0060 < char < 0x007C or 0x00DF < char < 0x00F7 or 0x00F7 < char < 0x0100:
                        continue

                    should_cap = True

    @property
    def archive_list(self):
        raise AbstractHandlerMethodError()

    # in common.fsys/common_rel
    @property
    def pokemon_data_offset(self):
        raise AbstractHandlerMethodError()

    # in common.fsys/common_rel
    @property
    def move_data_offset(self):
        raise AbstractHandlerMethodError()

    # in common.fsys/common_rel
    @property
    def item_data_offset(self):
        raise AbstractHandlerMethodError()

    # in start.dol
    @property
    def tm_data_offset(self):
        raise AbstractHandlerMethodError()

    # in start.dol
    @property
    def starter_data_offsets(self):
        raise AbstractHandlerMethodError()

    # in common.fsys/common_rel
    @property
    def fixable_name_offsets(self):
        raise AbstractHandlerMethodError()

    def get_first_stages(self):
        pokemon_data = self.normal_pokemon

        first_stage_candidates = [pkmn.species for pkmn in pokemon_data]

        for pkmn in pokemon_data:
            for evo in pkmn.evolution:
                if evo.evolves_to in first_stage_candidates:
                    first_stage_candidates.remove(evo.evolves_to)

        return [self.pokemon_data[p.value] for p in first_stage_candidates]

    def get_random_starter(self, idx, disallowed=None):
        if disallowed is None:
            disallowed = []

        if len(config.rng_starters_fixed) > idx:
            name = config.rng_starters_fixed[idx].upper()
            try:
                return self.pokemon_data[PokemonSpecies[name].value]
            except KeyError:
                raise ValueError("No such Pokémon: %s" % name)
        else:
            min_bst = min([p.base_stats.total for p in self.normal_pokemon if p.base_stats.total > 0
                           and p not in disallowed])
            max_bst = max(min_bst, config.rng_starters_max_bst)
            return random.choice([p for p in self.normal_pokemon if p.base_stats.total <= max_bst])

    def write_banner_name(self, text):
        from randomizer import PROG_VERSION

        banner = self.iso.open(b'opening.bnr')
        banner_meta_count = int(math.floor((banner.size - BANNER_META_FIRST_OFFSET) / BANNER_META_SIZE))

        banner.seek(BANNER_META_FIRST_OFFSET)
        start_pos = BANNER_META_FIRST_OFFSET

        text = text[0:32]

        template = b'Randomized at %s\x0awith Pok\xe9mon GameCube Randomizer v%s'
        date_str = datetime.now().replace(microsecond=0).isoformat(' ').encode('ascii', errors='ignore')
        template_params = (date_str, PROG_VERSION.encode('ascii', errors='ignore'))

        if self.region == IsoRegion.JPN:
            template = "ポケモンゲームキューブランダマイザーv%sで\x0a%sにランダム化しました".encode('shift-jis')
            template_params = (template_params[1], template_params[0])

        for i in range(banner_meta_count):
            banner.seek(start_pos)
            banner.write(b'\x00' * 0x20)
            banner.seek(start_pos)
            banner.write(text)
            banner.seek(start_pos + 0x40)
            banner.write(b'\x00' * 0x40)
            banner.seek(start_pos + 0x40)
            banner.write(text)
            banner.seek(start_pos + 0xC0)
            banner.write(b'\x00' * 0x80)
            banner.seek(start_pos + 0xC0)
            banner.write(template % template_params)

            start_pos += BANNER_META_SIZE

    def write_rom_header_name(self, text):
        self.iso.file.seek(0x20)
        self.iso.file.write(b'\x00' * 32)
        self.iso.file.seek(0x20)
        self.iso.file.write(text[0:32])

    def update_banner(self):
        pass


def get_bst_range_for_level(level, bst_min, bst_max):
    level_bst_min = min(bst_max - 100, max(bst_min, bst_min + (level - 10) / 65 * (bst_max - bst_min)))
    level_bst_max = min(bst_max, max(bst_min, bst_min + (level + 30) / 80 * (bst_max - bst_min)))

    return level_bst_min, level_bst_max


def randomize_pokemon(pokemon, pokemon_data, move_data, bst_min, bst_max, is_shadow, shadow_candidates,
                      fixed_species=None):
    if pokemon.species == PokemonSpecies.NONE:
        return

    level_bst_min = 0
    level_bst_max = 5000
    if config.rng_trainers_power_progression:
        level_bst_min, level_bst_max = get_bst_range_for_level(pokemon.level, bst_min, bst_max)

    if fixed_species:
        pokemon.species = fixed_species
    elif is_shadow and config.rng_trainers_unique_shadow:
        current_bst = 0
        attempts = 0
        # Go through the whole list once. If there are no suitable BST Pokémon,
        # just pick the first one in the queue.
        while (level_bst_min > current_bst or level_bst_max < current_bst) \
                and attempts < len(shadow_candidates):
            attempts += 1

            pokemon.species = shadow_candidates.pop()
            current_bst = pokemon_data[pokemon.species.value].base_stats.total

            if level_bst_min > current_bst or level_bst_max < current_bst:
                shadow_candidates.insert(0, pokemon.species)
    else:
        available_pokemon = [p.species for p in pokemon_data.values() if 0 < p.natdex_no < 388
                             and level_bst_min <= p.base_stats.total <= level_bst_max]

        if len(available_pokemon) == 0:
            # Only happens if the BSTs have a huge gap somewhere. In that case, just pick randomly.
            available_pokemon = [p.species for p in pokemon_data.values() if 0 < p.natdex_no < 388]

        pokemon.species = random.choice(available_pokemon)

    level_up_moves, tm_moves = pokemon_data[pokemon.species.value].get_legal_moves_at_level(pokemon.level)

    if config.rng_trainers_level_up_only:
        pokemon.moves = level_up_moves[-4:]
    else:
        if len(level_up_moves) + len(tm_moves) <= 4:
            pokemon.moves = level_up_moves + tm_moves
        else:
            moves = []
            pool = tm_moves + level_up_moves * 4

            # Pick a damaging move for the pool if only possible
            damaging_moves = [m for m in pool if move_data[m.value].power > 0]
            if len(damaging_moves) > 0:
                moves.append(random.choice(damaging_moves))

            while len(moves) < 4:
                move = random.choice(pool)
                if move not in moves:
                    moves.append(move)

            pokemon.moves = moves

    pokemon.moves = pokemon.moves + [Move.NONE] * max(0, 4 - len(pokemon.moves))

    if config.rng_trainers_item:
        if random.random() < config.rng_trainers_item_ratio / 100:
            pokemon.item = random.choice([i for i in Item if Item.NONE.value < i.value <= Item.TM50.value])
        else:
            pokemon.item = Item.NONE
