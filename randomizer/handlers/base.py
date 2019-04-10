#!/usr/bin/env python
# -*- coding: utf-8 -*-
import logging
import random
from struct import unpack, pack

from randomizer import config
from randomizer.iso.constants import Ability, Move, Type, EvolutionType, PokemonSpecies, VALID_POKEMON_TYPES, Item
from randomizer.iso.fsys import FsysArchive
from randomizer.iso.structs import StatSet, EvoEntry, LevelUpMoveEntry
from randomizer.util import chunked


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

    def randomize_base_stats(self, keep_bst, stat_distribution=None):
        if self.base_stats.total == 0:
            return

        new_bst = self.base_stats.total if keep_bst else round(
            min(RANDOM_BST_MAX, max(RANDOM_BST_MIN, random.gauss(
                (RANDOM_BST_MAX + RANDOM_BST_MIN) / 2,
                (RANDOM_BST_MAX - RANDOM_BST_MIN) / 6)))
        )

        if stat_distribution is None:
            stat_distribution = [max(0, random.gauss(1, 0.25)) for _ in range(0, 6)]

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

        return self.type1, self.type2

    def randomize_abilities(self, allowed_abilities, previous_stage_abilities=None):
        if previous_stage_abilities is not None:
            self.ability1, self.ability2 = previous_stage_abilities

            if random.random() < config.rng_pkabi_family_change_ratio / 100:
                return self.randomize_abilities(allowed_abilities)

        else:
            self.ability1 = random.choice(allowed_abilities)

            if random.random() < config.rng_pkabi_monoabi_ratio / 100:
                self.ability2 = self.ability1
            else:
                self.ability2 = random.choice(allowed_abilities)

        # Special case: if Wonder Guard is allowed and a Pokémon with it has 1 HP, then that Pokémon should never
        # get an alternate ability as it would just be unusable.
        if config.rng_pkstats_wg_1hp and (
                self.ability1 == Ability.WONDER_GUARD or self.ability2 == Ability.WONDER_GUARD):
            self.ability1 = Ability.WONDER_GUARD
            self.ability2 = Ability.WONDER_GUARD

        return self.ability1, self.ability2

    def patch_evolution(self, index, evo_type, level_or_item):
        self.evolution[index].type = evo_type
        self.evolution[index].level = level_or_item.value if type(level_or_item) == Item else level_or_item
        self.evolution[index].item = Item(level_or_item)

    def encode(self):
        raise AbstractHandlerMethodError()


class BaseHandler:
    iso = None
    region = None
    archives = dict()
    pokemon_data = dict()

    # these should be filled in in the derived handlers
    POKEMON_DATA_LIST_LENGTH = 0

    def __init__(self, iso, region):
        self.iso = iso
        self.region = region

        # Cacophony is banned because it doesn't have a description and as such crashes the Pokémon status screen and
        # Strategy Memo. It might not work anyways, and its effect is a duplicate one, so it isn't needed in any case.
        self.allowed_abilities = [a for a in list(Ability)
                                  if a not in [Ability.NONE, Ability.CACOPHONY]
                                  and a.name not in map(lambda n: n.upper(), config.rng_pkabi_ban)]
        self.normal_pokemon = []

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
            common_rel = self.archives[b'common.fsys'].get_file(b'common_rel').data
            common_rel.seek(self.get_pokemon_data_offset())

            for i in range(1, self.POKEMON_DATA_LIST_LENGTH + 1):
                logging.debug('Reading index %d of %d...', i, self.POKEMON_DATA_LIST_LENGTH)
                pkmn = self.pokemon_data[i] = self.make_pokemon_data(common_rel, i)

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
                        evo_specifier = 'with item %s ' % evo.item.name

                    logging.debug('  Evolves to %s %s(%s)',
                                  PokemonSpecies(evo.evolves_to).name, evo_specifier, evo.type.name)

            self.normal_pokemon = list(filter(lambda pkmn: pkmn.natdex_no > 0, self.pokemon_data.values()))
        except KeyError as e:
            logging.error('Couldn\'t read Pokémon data since the required data file was not loaded.')
            raise e

    def write_pokemon_data(self):
        logging.debug('Encoding Pokémon data in preparation to be written to the ISO.')

        common_rel = self.archives[b'common.fsys'].get_file(b'common_rel').data
        common_rel.seek(self.get_pokemon_data_offset())

        for i, pkmn in self.pokemon_data.items():
            logging.debug('Encoding index %d of %d...', i, self.POKEMON_DATA_LIST_LENGTH)
            common_rel.write(pkmn.encode())

    def get_available_normal_moves(self):
        return set(range(Move.POUND.value, Move.PSYCHO_BOOST.value)).remove([Move.STRUGGLE.value])

    def get_available_shadow_moves(self):
        raise AbstractHandlerMethodError()

    def randomize_pokemon_get_root_level_list(self, condition):
        return self.get_first_stages() if condition else self.normal_pokemon

    def randomize_pokemon_aspect_recur(self, aspect, result_arg_name, pkmn_list, recurse,
                                       previous_result=None, **kwargs):
        for pkmn in pkmn_list:
            randomization_result = getattr(pkmn, 'randomize_' + aspect)(
                **{result_arg_name: previous_result}, **kwargs)
            if recurse:
                evolution_targets = [self.pokemon_data[evo.evolves_to.value] for evo in pkmn.evolution
                                     if evo.evolves_to is not PokemonSpecies.NONE]

                self.randomize_pokemon_aspect_recur(aspect, result_arg_name, evolution_targets,
                                                    previous_result=randomization_result, recurse=True, **kwargs)

    def randomize_pokemon_stats(self):
        self.randomize_pokemon_aspect_recur('base_stats', 'stat_distribution',
                                            self.randomize_pokemon_get_root_level_list(config.rng_pkstats_family),
                                            recurse=config.rng_pkstats_family, keep_bst=config.rng_pkstats_retain_bst)

    def randomize_pokemon_types(self):
        self.randomize_pokemon_aspect_recur('types', 'previous_stage_types',
                                            self.randomize_pokemon_get_root_level_list(config.rng_pktypes_family),
                                            recurse=config.rng_pktypes_family)

    def randomize_pokemon_abilities(self):
        self.randomize_pokemon_aspect_recur('abilities', 'previous_stage_abilities',
                                            self.randomize_pokemon_get_root_level_list(config.rng_pkabi_family),
                                            recurse=config.rng_pkabi_family, allowed_abilities=self.allowed_abilities)

    def randomize_pokemon_movesets(self):
        pass

    def patch_impossible_evolutions(self):
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

        # TODO: Espeon and Umbreon for Colosseum

    def make_pokemon_data(self, io_in, idx) -> BasePokemon:
        raise AbstractHandlerMethodError()

    def get_first_stages(self):
        pokemon_data = self.normal_pokemon

        first_stage_candidates = [pkmn.species for pkmn in pokemon_data]

        for pkmn in pokemon_data:
            for evo in pkmn.evolution:
                if evo.evolves_to in first_stage_candidates:
                    first_stage_candidates.remove(evo.evolves_to)

        return [self.pokemon_data[p.value] for p in first_stage_candidates]

