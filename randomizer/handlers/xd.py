#!/usr/bin/env python
# -*- coding: utf-8 -*-
import random
from io import BytesIO
from struct import unpack, pack
import logging

from randomizer import config
from randomizer.constants import IsoRegion
from randomizer.handlers.base import BasePokemon, BaseMoveEntry, BaseItemBox, get_bst_range_for_level
from randomizer.iso.constants import Move, ExpClass, Ability, Type, PokemonSpecies, Item
from randomizer.util import chunked
from . import BaseHandler


class XDPokemon(BasePokemon):
    SIGNATURE = '>BBBBHHHHHHHHH4sHHH6sHHHHHBBBB50s8s12sHH16sHHHHHHHHHHHH30s80s16s'

    def __init__(self, data, idx):
        super().__init__()

        (
            exp_class,
            self.catch_rate,
            self.gender_ratio,
            self.unknown_0x03,
            self.exp_gain,
            self.base_happiness,
            self.height,
            self.weight,
            self.unknown_running_no_1,
            self.natdex_no,
            self.unknown_0x10_0x11,
            self.unknown_natdex_no_2,
            self.unknown_running_no_2,
            self.unknown_0x16_0x19,
            self.unknown_running_no_3,
            self.unknown_0x1c_0x1d,
            self.species_str_pointer,
            self.unknown_0x20_0x25,
            self.unknown_running_no_4,
            self.unknown_0x28_0x29,
            self.unknown_running_no_5,
            self.unknown_0x2c_0x2d,
            self.internal_idx_no,
            type1,
            type2,
            ability1,
            ability2,
            tm_compatibility,
            hm_compatibility,
            tutor_compatibility,
            item1,
            item2,
            egg_moves,
            base_hp,
            base_atk,
            base_def,
            base_spatk,
            base_spdef,
            base_speed,
            evgain_hp,
            evgain_atk,
            evgain_def,
            evgain_spatk,
            evgain_spdef,
            evgain_speed,
            evolution_data,
            move_data,
            self.unknown_0x115_0x124
        ) = unpack(self.SIGNATURE, data)

        self.exp_class = ExpClass(exp_class)
        self.ability1 = Ability(ability1)
        self.ability2 = Ability(ability2)
        self.type1 = Type(type1)
        self.type2 = Type(type2)
        self.item1 = Item(item1)
        self.item2 = Item(item2)

        self.set_base_stats(base_hp, base_atk, base_def, base_spatk, base_spdef, base_speed)
        self.set_ev_gain(evgain_hp, evgain_atk, evgain_def, evgain_spatk, evgain_spdef, evgain_speed)
        self.set_learn_flags(tm_compatibility, hm_compatibility, tutor_compatibility)
        self.set_egg_moves(egg_moves)
        self.set_evolution(evolution_data)
        self.set_level_up_moves(move_data)

        self.species = PokemonSpecies(idx)

    def encode(self):
        tm_compatibility, hm_compatibility, tutor_compatibility = self.encode_learn_flags()

        return pack(
            self.SIGNATURE,
            self.exp_class.value,
            self.catch_rate,
            self.gender_ratio,
            self.unknown_0x03,
            self.exp_gain,
            self.base_happiness,
            self.height,
            self.weight,
            self.unknown_running_no_1,
            self.natdex_no,
            self.unknown_0x10_0x11,
            self.unknown_natdex_no_2,
            self.unknown_running_no_2,
            self.unknown_0x16_0x19,
            self.unknown_running_no_3,
            self.unknown_0x1c_0x1d,
            self.species_str_pointer,
            self.unknown_0x20_0x25,
            self.unknown_running_no_4,
            self.unknown_0x28_0x29,
            self.unknown_running_no_5,
            self.unknown_0x2c_0x2d,
            self.internal_idx_no,
            self.type1.value,
            self.type2.value,
            self.ability1.value,
            self.ability2.value,
            tm_compatibility,
            hm_compatibility,
            tutor_compatibility,
            self.item1.value,
            self.item2.value,
            self.encode_egg_moves(),
            self.base_stats.hp,
            self.base_stats.attack,
            self.base_stats.defense,
            self.base_stats.sp_attack,
            self.base_stats.sp_defense,
            self.base_stats.speed,
            self.ev_gain.hp,
            self.ev_gain.attack,
            self.ev_gain.defense,
            self.ev_gain.sp_attack,
            self.ev_gain.sp_defense,
            self.ev_gain.speed,
            self.encode_evolution(),
            self.encode_level_up_moves(),
            self.unknown_0x115_0x124)

    def randomize_tutors(self, tutor_data, previous_stage_tutors=None):
        compatibility = self.randomize_compatibility(tutor_data, previous_stage_tutors, "tutor_compatibility",
                                                     config.rng_pktutor_min_status_ratio,
                                                     config.rng_pktutor_min_own_type_ratio,
                                                     config.rng_pktutor_min_normal_type_ratio,
                                                     config.rng_pktutor_min_other_type_ratio)

        logging.debug('%s now learns the following tutor moves: %s', self.species.name,
                      ', '.join([tutor_data[i].move.name for i, l in enumerate(self.tutor_compatibility) if l is True]))
        return compatibility


class XDMoveEntry(BaseMoveEntry):
    SIGNATURE = '>bBBBBBBBBBBB4sBBBBB4sB3sB4sH10sH2sH4s'

    def __init__(self, data, idx):
        super().__init__()

        (
            self.priority,
            self.pp,
            m_type,
            self.targets,
            self.accuracy,
            self.effect_proc,
            self.contact,
            self.protectable,
            self.magic_coat,
            self.snatchable,
            self.mirror_movable,
            self.kings_rock_proc,
            self.unknown_0x0c_0x0f,
            self.sound_move,
            self.unknown_0x11,
            self.hm,
            self.category,
            self.recoil,
            self.unknown_0x15_0x18,
            self.power,
            self.unknown_0x1a_0x1c,
            self.effect_type,
            self.unknown_0x1e_0x21,
            self.name_id,
            self.unknown_0x24_0x2d,
            self.desc_id,
            self.unknown_0x30_0x31,
            self.anim_id,
            self.unknown_0x34_0x37,
        ) = unpack(self.SIGNATURE, data)

        self.type = Type(m_type)
        self.move = Move(idx)
    pass

    def encode(self):
        return pack(
            self.SIGNATURE,
            self.priority,
            self.pp,
            self.type.value,
            self.targets,
            self.accuracy,
            self.effect_proc,
            self.contact,
            self.protectable,
            self.magic_coat,
            self.snatchable,
            self.mirror_movable,
            self.kings_rock_proc,
            self.unknown_0x0c_0x0f,
            self.sound_move,
            self.unknown_0x11,
            self.hm,
            self.category,
            self.recoil,
            self.unknown_0x15_0x18,
            self.power,
            self.unknown_0x1a_0x1c,
            self.effect_type,
            self.unknown_0x1e_0x21,
            self.name_id,
            self.unknown_0x24_0x2d,
            self.desc_id,
            self.unknown_0x30_0x31,
            self.anim_id,
            self.unknown_0x34_0x37
        )


class XDTrainerDeck:
    def __init__(self, data):
        self.sections = []
        self.size = 0
        self.unknown_0x08_0x0B = None
        self.unknown_0x0C_0x0F = None

        data.seek(0)
        values = unpack('>4sIII', data.read(16))

        if values[0] != b'DECK':
            raise TypeError('Not a valid deck header')

        self.size = values[1]
        self.unknown_0x08_0x0B = values[2]
        self.unknown_0x0C_0x0F = values[3]

        while data.tell() < self.size:
            section_type = data.read(4)
            section_size = unpack('>I', data.read(4))[0] - 8
            section_data = data.read(section_size)

            if len(section_data) < section_size:
                raise IndexError('Couldn\'t read %d bytes for deck section' % section_size)

            if section_type == b'DPKM':
                section = XDTrainerDeckDPKM(section_data)
            elif section_type == b'DDPK':
                section = XDTrainerDeckDDPK(section_data)
            elif section_type == b'DTNR':
                section = XDTrainerDeckDTNR(section_data)
            elif section_type == b'DTAI':
                section = XDTrainerDeckDTAI(section_data)
            elif section_type == b'DSTR':
                section = XDTrainerDeckDSTR(section_data)
            else:
                raise TypeError('Unknown deck section type %s' % section_type.decode('ascii', errors='replace'))

            self.sections.append(section)

    def encode(self):
        encoded_deck = b''
        for section in self.sections:
            encoded_deck += section.encode()

        size = len(encoded_deck) + 16
        return b'DECK' + pack('>III', size, self.unknown_0x08_0x0B, self.unknown_0x0C_0x0F) + encoded_deck

    def randomize(self, pokemon_data, shadow_indexes, shadow_candidates):
        for section in self.sections:
            if type(section) is XDTrainerDeckDPKM:
                shadow_candidates = section.randomize(pokemon_data, shadow_indexes, shadow_candidates)
            elif type(section) is XDTrainerDeckDDPK:
                section.randomize()

        return shadow_candidates


class XDTrainerSection:
    def __init__(self, data):
        self.raw_data = data
        self.entries = []
        self.init(data)

    def init(self, data):
        pass

    def encode(self):
        data_encoded = self.encode_data()
        return self.section_type + pack('>I', len(data_encoded) + 8) + data_encoded

    def encode_data(self):
        return self.raw_data

    @property
    def section_type(self):
        return b'????'

    @property
    def section_name(self):
        return 'Unknown section'


class XDTrainerDeckDPKM(XDTrainerSection):
    class Pokemon:
        SIGNATURE = '>HBBHHBBBBBBBBBBBBHHHHHBB'

        def __init__(self, data):
            values = unpack(self.SIGNATURE, data)

            (
                species_no,
                self.level,
                self.happiness,
                item,
                self.unknown_0x06_0x07,
                self.iv_hp,
                self.iv_atk,
                self.iv_def,
                self.iv_spatk,
                self.iv_spdef,
                self.iv_speed,
                self.ev_hp,
                self.ev_atk,
                self.ev_def,
                self.ev_spatk,
                self.ev_spdef,
                self.ev_speed,
                move1,
                move2,
                move3,
                move4,
                self.unknown_0x1c_0x1d,
                self.pid,
                self.unknown_0x1f
            ) = values

            self.species = PokemonSpecies(species_no)
            self.item = Item(item)
            self.moves = [
                Move(move1),
                Move(move2),
                Move(move3),
                Move(move4)
            ]

        def encode(self):
            return pack(
                self.SIGNATURE,
                self.species.value,
                self.level,
                self.happiness,
                self.item.value,
                self.unknown_0x06_0x07,
                self.iv_hp,
                self.iv_atk,
                self.iv_def,
                self.iv_spatk,
                self.iv_spdef,
                self.iv_speed,
                self.ev_hp,
                self.ev_atk,
                self.ev_def,
                self.ev_spatk,
                self.ev_spdef,
                self.ev_speed,
                self.moves[0].value,
                self.moves[1].value,
                self.moves[2].value,
                self.moves[3].value,
                self.unknown_0x1c_0x1d,
                self.pid,
                self.unknown_0x1f
            )

    def init(self, data):
        buf = BytesIO(data)
        buf.seek(0)

        entry_count = unpack('>II', buf.read(8))[0]
        for i in range(entry_count):
            self.entries.append(XDTrainerDeckDPKM.Pokemon(buf.read(32)))

    def encode_data(self):
        data = pack('>II', len(self.entries), 0)
        for pokemon in self.entries:
            data += pokemon.encode()

        return data

    def randomize(self, pokemon_data, shadow_indexes, shadow_candidates):
        bsts = [p.base_stats.total for p in pokemon_data.values()]
        bst_min = min(bsts)
        bst_max = max(bsts)

        for i, pokemon in enumerate(self.entries):
            if pokemon.species == PokemonSpecies.NONE:
                continue

            level_bst_min = 0
            level_bst_max = 5000
            if config.rng_trainers_power_progression:
                level_bst_min, level_bst_max = get_bst_range_for_level(pokemon.level, bst_min, bst_max)

            if i in shadow_indexes and config.rng_trainers_unique_shadow:
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
                if len(level_up_moves) + len(tm_moves) < 4:
                    pokemon.moves = level_up_moves + list(tm_moves)
                else:
                    moves = set()
                    while len(moves) < 4:
                        moves = moves.union(set(random.sample(list(tm_moves) + level_up_moves * 4, 4)))

                    pokemon.moves = list(moves)[0:4]

            pokemon.moves = pokemon.moves + [Move.NONE] * max(0, 4 - len(pokemon.moves))

        return shadow_candidates

    @property
    def section_type(self):
        return b'DPKM'

    @property
    def section_name(self):
        return 'Regular Pokémon data'


class XDTrainerDeckDDPK(XDTrainerSection):
    SHADOW_MOVES = [Move(m) for m in range(Move.SHADOW_BLITZ.value, Move.SHADOW_HALF.value)]
    DAMAGING_SHADOW_MOVES = [Move(m) for m in range(Move.SHADOW_BLITZ.value, Move.SHADOW_BLAST.value)]

    class Pokemon:
        SIGNATURE = '>BBBBHHHHHHHHI'

        def __init__(self, data):
            values = unpack(self.SIGNATURE, data)

            (
                self.unknown_0x00,
                self.catch_rate,
                self.level,
                self.unknown_0x03,
                self.unknown_0x04_0x05,
                self.dpkm_index,
                self.purification_cost,
                self.unknown_0x0A_0x0B,
                move1_override,
                move2_override,
                move3_override,
                move4_override,
                self.unknown_0x14_0x17
            ) = values

            self.move_overrides = [
                Move(move1_override),
                Move(move2_override),
                Move(move3_override),
                Move(move4_override)
            ]

        def encode(self):
            return pack(
                self.SIGNATURE,
                self.unknown_0x00,
                self.catch_rate,
                self.level,
                self.unknown_0x03,
                self.unknown_0x04_0x05,
                self.dpkm_index,
                self.purification_cost,
                self.unknown_0x0A_0x0B,
                self.move_overrides[0].value,
                self.move_overrides[1].value,
                self.move_overrides[2].value,
                self.move_overrides[3].value,
                self.unknown_0x14_0x17
            )

    def init(self, data):
        buf = BytesIO(data)
        buf.seek(0)

        entry_count = unpack('>II', buf.read(8))[0]
        for i in range(entry_count):
            self.entries.append(XDTrainerDeckDDPK.Pokemon(buf.read(24)))

    def encode_data(self):
        data = pack('>II', len(self.entries), 0)
        for pokemon in self.entries:
            data += pokemon.encode()

        return data

    def randomize(self):
        for pokemon in self.entries:
            if pokemon.dpkm_index == 0:
                continue

            first_move = random.choice(self.DAMAGING_SHADOW_MOVES)
            extra_shadow_move_count = random.randint(0, 3)
            moves = [first_move] + random.sample([m for m in self.SHADOW_MOVES if m != first_move],
                                                 extra_shadow_move_count) + [Move.NONE] * (3 - extra_shadow_move_count)
            pokemon.move_overrides = moves

    @property
    def section_type(self):
        return b'DDPK'

    @property
    def section_name(self):
        return 'Shadow Pokémon data'


class XDTrainerDeckDTNR(XDTrainerSection):
    @property
    def section_type(self):
        return b'DTNR'

    @property
    def section_name(self):
        return 'Trainer parameters'


class XDTrainerDeckDTAI(XDTrainerSection):
    @property
    def section_type(self):
        return b'DTAI'

    @property
    def section_name(self):
        return 'Trainer AI data'


class XDTrainerDeckDSTR(XDTrainerSection):
    @property
    def section_type(self):
        return b'DSTR'

    @property
    def section_name(self):
        return 'Trainer string data'


class XDItemBox(BaseItemBox):

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


class XDBattleBingoCard:
    class PokemonData:
        SIGNATURE = '>BBBBHHH'

        def __init__(self, data):
            (
                self.useSecondType,
                self.useSecondAbility,
                self.nature,
                self.gender,
                species,
                move,
                self.unknown_0x08_0x09
            ) = unpack(self.SIGNATURE, data)

            self.species = PokemonSpecies(species)
            self.move = Move(move)

        def encode(self):
            return pack(
                self.SIGNATURE,
                self.useSecondType,
                self.useSecondAbility,
                self.nature,
                self.gender,
                self.species.value,
                self.move.value,
                self.unknown_0x08_0x09)

    SIGNATURE = '>BBBBBBBBIIB20s140s6sB'

    def __init__(self, data, idx):
        (
            self.index,
            self.difficulty,
            self.subindex,
            self.unknown_0x03,
            self.level,
            self.unknown_0x05,
            self.pokemon_count,
            self.mystery_count,
            self.name_pointer,
            self.details_pointer,
            self.unknown_0x10,
            rewards,
            pokemon_data,
            mystery_panels,
            self.unknown_0xb7
        ) = unpack(self.SIGNATURE, data)

        self.rewards = [unpack('>H', s)[0] for s in chunked(2, rewards)]
        self.pokemon_data = [XDBattleBingoCard.PokemonData(s) for s in chunked(10, pokemon_data)]
        self.mystery_panels = [unpack('>BB', s) for s in chunked(2, mystery_panels)]

    def encode(self):
        return pack(
            self.SIGNATURE,
            self.index,
            self.difficulty,
            self.subindex,
            self.unknown_0x03,
            self.level,
            self.unknown_0x05,
            self.pokemon_count,
            self.mystery_count,
            self.name_pointer,
            self.details_pointer,
            self.unknown_0x10,
            b''.join([pack('>H', s) for s in self.rewards]),
            b''.join(p.encode() for p in self.pokemon_data),
            b''.join([pack('>BB', *s) for s in self.mystery_panels]),
            self.unknown_0xb7)

    def randomize(self, pokemon_data, move_data):
        bsts = [p.base_stats.total for p in pokemon_data.values()]
        bst_min = min(bsts)
        bst_max = max(bsts)

        level_bst_min = 0
        level_bst_max = 5000
        if config.rng_trainers_power_progression:
            level_bst_min, level_bst_max = get_bst_range_for_level(self.level, bst_min, bst_max)

        candidates = [p for p in pokemon_data.values() if level_bst_min <= p.base_stats.total <= level_bst_max]
        if len(candidates) == 0:
            candidates = pokemon_data.values()

        for pokemon in self.pokemon_data:
            candidate = random.choice(candidates)

            pokemon.species = candidate.species

            level_up_moves, tm_moves = candidate.get_legal_moves_at_level(self.level)
            pokemon.move = random.choice([m for m in level_up_moves * 4 + list(tm_moves)
                                          if move_data[m.value].power > 0])


class XDHandler(BaseHandler):
    POKEMON_DATA_LIST_LENGTH = 414
    MOVE_DATA_LIST_LENGTH = 373
    ITEM_BOX_LIST_LENGTH = 114
    BINGO_CARD_LIST_LENGTH = 11
    TUTOR_LIST_LENGTH = 12

    # actually 11, but the last two are Bonsly and Munchlax and overwriting their species causes weird things to happen
    POKESPOT_COUNT = 9

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.trainer_decks = {}
        self.bingo_cards = []
        self.shadow_pokemon_indexes = []

    def load_deck(self, deck_name):
        logging.debug('Loading trainer deck %s...' % deck_name.decode('ascii', errors='replace'))
        deck = XDTrainerDeck(self.archives[b'deck_archive.fsys'].get_file(deck_name).data)

        for section in deck.sections:
            logging.debug('  Section: %s (%s), %s bytes%s' % (
                section.section_type.decode('ascii', errors='replace'),
                section.section_name,
                len(section.raw_data),
                '' if len(section.entries) == 0 else (
                        ', %d entr%s' % (len(section.entries), 'ies' if len(section.entries) != 1 else 'y')
                )
            ))

            if len(section.entries) == 0 and len(section.raw_data) > 0:
                continue

            story_dpkm = None
            try:
                story_deck = self.trainer_decks[b'DeckData_Story.bin']
                for story_deck_section in story_deck.sections:
                    if story_deck_section.section_type == b'DPKM':
                        story_dpkm = story_deck_section
                        break
            except KeyError:
                # not yet loaded most probably
                pass

            for i, pokemon in enumerate(section.entries):
                if type(pokemon) is XDTrainerDeckDPKM.Pokemon:
                    if pokemon.species != PokemonSpecies.NONE:
                        logging.debug('    #%d: Lv%d %s with %s' % (
                            i, pokemon.level, pokemon.species.name,
                            '/'.join([m.name for m in pokemon.moves if m != Move.NONE])))
                    else:
                        logging.debug('    #%d: Blank entry' % i)
                elif type(pokemon) is XDTrainerDeckDDPK.Pokemon:
                    if pokemon.dpkm_index != 0:
                        self.shadow_pokemon_indexes.append(pokemon.dpkm_index)

                        species_name = ('???' if story_dpkm is None
                                        else story_dpkm.entries[pokemon.dpkm_index].species.name)

                        logging.debug('    #%d: Lv%d Shadow %s (story deck #%d) with %s' % (
                            i, pokemon.level, species_name, pokemon.dpkm_index,
                            '/'.join([m.name for m in pokemon.move_overrides if m != Move.NONE])))
                    else:
                        logging.debug('    #%d: Blank entry' % i)

        self.trainer_decks[deck_name] = deck

    def load_trainer_data(self):
        self.load_deck(b'DeckData_Story.bin')
        self.load_deck(b'DeckData_Bingo.bin')
        self.load_deck(b'DeckData_Colosseum.bin')
        self.load_deck(b'DeckData_DarkPokemon.bin')
        self.load_deck(b'DeckData_Hundred.bin')
        self.load_deck(b'DeckData_Imasugu.bin')
        self.load_deck(b'DeckData_Virtual.bin')

        # Also load bingo data
        common_rel = self.archives[b'common.fsys'].get_file(b'common_rel').data
        common_rel.seek(self.bingo_data_offset)
        logging.debug('Loading Battle Bingo data...')
        for i in range(self.BINGO_CARD_LIST_LENGTH):
            card = XDBattleBingoCard(common_rel.read(0xB8), i)
            self.bingo_cards.append(card)
            logging.debug('  Card #%d: Lv%d %s' % (i, card.level, ', '.join(
                ['%s (%s)' % (p.species.name, p.move.name) for p in card.pokemon_data])))

    def write_trainer_data(self):
        logging.debug('Encoding trainer data in preparation to be written to the ISO.')

        for deck_name, deck in self.trainer_decks.items():
            logging.debug('Encoding deck %s...', deck_name.decode('ascii', errors='replace'))
            new_data = BytesIO(deck.encode())

            self.archives[b'deck_archive.fsys'].get_file(deck_name).data = new_data

            if self.region == IsoRegion.EUR:
                self.archives[b'deck_archive.fsys'].get_file(deck_name.replace(b'.bin', b'_EU.bin')).data = new_data

            if deck_name == b'DeckData_DarkPokemon.bin':
                # Also overwrite Shadow Pokémon deck copies in common_rel.fsys
                self.archives[b'common.fsys'].get_file(deck_name).data = new_data

                if self.region == IsoRegion.EUR:
                    self.archives[b'common.fsys'].get_file(deck_name.replace(b'.bin', b'_EU.bin')).data = new_data

        # Also write bingo data
        common_rel = self.archives[b'common.fsys'].get_file(b'common_rel').data
        common_rel.seek(self.bingo_data_offset)
        for card in self.bingo_cards:
            common_rel.write(card.encode())

    def make_pokemon_data(self, io_in, idx):
        return XDPokemon(io_in.read(0x124), idx)

    def make_move_data(self, io_in, idx):
        return XDMoveEntry(io_in.read(0x38), idx)

    def make_item_box_data(self, io_in, idx):
        return XDItemBox(io_in.read(0x1C), idx)

    def get_game_specific_randomizable_items(self):
        return [Item.JOY_SCENT_XD, Item.VIVID_SCENT_XD, Item.EXCITE_SCENT_XD, Item.SUN_SHARD, Item.MOON_SHARD]

    def randomize_and_write_starter_data(self):
        exp_values = {
            ExpClass.ERRATIC: 1800,
            ExpClass.FAST: 800,
            ExpClass.MEDIUM_FAST: 1000,
            ExpClass.MEDIUM_SLOW: 560,
            ExpClass.SLOW: 1250,
            ExpClass.FLUCTUATING: 540,
        }

        eevee = self.get_random_starter(0)
        logging.info('Starter Eevee is now replaced with %s' % eevee.species.name)
        moves = [m.move for m in eevee.level_up_moves if m.level <= 10][-4:]
        while len(moves) < 4:
            moves.append(Move.NONE)

        self.dol_file.seek(self.starter_data_offsets[0])
        self.dol_file.write(pack(">H", eevee.species.value))
        self.dol_file.seek(14, 1)
        for i in range(4):
            self.dol_file.write(pack(">H", moves[i].value))
            self.dol_file.seek(2, 1)
        self.dol_file.seek(0x44, 1)
        self.dol_file.write(pack(">H", exp_values[eevee.exp_class]))

    def randomize_trainers(self):
        logging.info('Randomizing trainer data.')
        allowed_shadow_pokemon = [p.species for p in self.normal_pokemon]
        random.shuffle(allowed_shadow_pokemon)

        decks_to_randomize = {
            b'DeckData_Story.bin': config.rng_trainers_cat_story,
            b'DeckData_Bingo.bin': config.rng_trainers_cat_bingo,
            b'DeckData_Colosseum.bin': config.rng_trainers_cat_story,
            b'DeckData_DarkPokemon.bin': config.rng_trainers_cat_story,
            b'DeckData_Hundred.bin': config.rng_trainers_cat_mt_battle,
            b'DeckData_Imasugu.bin': config.rng_trainers_cat_quick_battle,
            b'DeckData_Virtual.bin': config.rng_trainers_cat_battle_sim
        }

        story_dpkm = None
        try:
            story_deck = self.trainer_decks[b'DeckData_Story.bin']
            for story_deck_section in story_deck.sections:
                if story_deck_section.section_type == b'DPKM':
                    story_dpkm = story_deck_section
                    break
        except KeyError:
            # Well, this is awkward. Though this is only used for displaying the Pokémon name for shadow Pokémon.
            # If we go here, there is probably a bug somewhere already or the ISO is broken.
            pass

        shadow_pokemon_dex_nos = []
        for deck_name, deck in self.trainer_decks.items():
            if decks_to_randomize[deck_name]:
                logging.debug('Randomizing deck %s.' % deck_name.decode('ascii', errors='replace'))
                deck.randomize(self.pokemon_data, self.shadow_pokemon_indexes, allowed_shadow_pokemon)

                for section in deck.sections:
                    if section.section_type == b'DPKM':
                        for i, pokemon in enumerate(section.entries):
                            if pokemon.species != PokemonSpecies.NONE:
                                logging.debug('    #%d: Lv%d %s with %s' % (
                                    i, pokemon.level, pokemon.species.name,
                                    '/'.join([m.name for m in pokemon.moves if m != Move.NONE])))
                            else:
                                logging.debug('    #%d: Blank entry' % i)

                    elif section.section_type == b'DDPK':
                        for i, pokemon in enumerate(section.entries):
                            if pokemon.dpkm_index != 0:
                                self.shadow_pokemon_indexes.append(pokemon.dpkm_index)

                                species_name = ('???' if story_dpkm is None
                                                else story_dpkm.entries[pokemon.dpkm_index].species.name)

                                logging.debug('    #%d: Lv%d Shadow %s (story deck #%d) with %s' % (
                                    i, pokemon.level, species_name, pokemon.dpkm_index,
                                    '/'.join([m.name for m in pokemon.move_overrides if m != Move.NONE])))
                            else:
                                logging.debug('    #%d: Blank entry' % i)

                        shadow_pokemon_dex_nos = [story_dpkm.entries[p.dpkm_index].species.value
                                                  for p in section.entries]

        # Randomize the Battle Bingo cards.
        # Although there is a deck called Bingo, the actual bingo data is stored elsewhere.
        if config.rng_trainers_cat_bingo:
            logging.debug('Randomizing Battle Bingo data...')
            for i, card in enumerate(self.bingo_cards):
                card.randomize(self.pokemon_data, self.move_data)
                logging.debug('  Card #%d: Lv%d %s' % (i, card.level, ', '.join(
                    ['%s (%s)' % (p.species.name, p.move.name) for p in card.pokemon_data])))

        # Write the Shadow Pokémon list into the DOL file.
        # In this address, there is obviously a list of all the Shadow Pokémon available.
        # It's not exactly clear at this point whether it's this list or the Shadow Pokémon deck copy in common.fsys
        # that is used to initialize the Shadow Monitor data into the save file, but it shouldn't hurt to write them
        # here in either case.
        self.dol_file.seek(self.shadow_monitor_data_offset)
        self.dol_file.write(b''.join([pack('>H', i) for i in shadow_pokemon_dex_nos]))

    def randomize_pokespot_data(self):
        if not config.rng_pokespot and not config.rng_pokespot_improve_levels:
            return

        logging.debug('Updating Poké Spot data.')

        bsts = [p.base_stats.total for p in self.pokemon_data.values()]
        bst_min = min(bsts)
        bst_max = max(bsts)

        common_rel = self.archives[b'common.fsys'].get_file(b'common_rel').data
        common_rel.seek(self.pokespot_data_offset)

        used_species = []

        for i in range(self.POKESPOT_COUNT):
            if config.rng_pokespot_improve_levels:
                lower_level = random.randint(25, 35)
                upper_level = lower_level + random.randint(0, 10)
                common_rel.write(pack('>BB', lower_level, upper_level))
            else:
                [lower_level, upper_level] = unpack('>BB', common_rel.read(2))

            if config.rng_pokespot:
                if config.rng_pokespot_bst_based:
                    level_bst_min, level_bst_max = get_bst_range_for_level(lower_level, bst_min, bst_max)

                    candidates = [p for p in self.pokemon_data.values()
                                  if level_bst_min <= p.base_stats.total <= level_bst_max
                                  and p.species not in used_species]
                else:
                    candidates = [p for p in self.normal_pokemon if p.species not in used_species]

                if len(candidates) == 0:
                    candidates = self.normal_pokemon

                # Write in order: species, constant zero, encounter rate (set to 33% for two slots and 34% for one slot
                # for each Spot respectively), another constant zero, and steps to meet that Pokémon.
                species = random.choice(candidates).species
                common_rel.write(pack('>HHHHH', species.value, 0, 34 if i % 3 == 0 else 33, 0,
                                      random.randint(80, 160)))
            else:
                species = PokemonSpecies(unpack('>H', common_rel.read(2))[0])
                common_rel.seek(8, 1)

            logging.debug('  Poké Spot slot #%d now has a wild %s encounter at Lv%d–%d' % (
                i + 1, species.name, lower_level, upper_level
            ))

    def load_tutor_data(self):
        logging.debug('Reading tutor data.')
        common_rel = self.archives[b'common.fsys'].get_file(b'common_rel').data
        common_rel.seek(self.tutor_data_common_rel_offset)
        for i in range(self.TUTOR_LIST_LENGTH):
            move = self.move_data[unpack(">H", common_rel.read(2))[0]]
            self.tutor_data.append(move)
            logging.debug('  Tutor move #%d is %s', i + 1, move.move.name)
            common_rel.seek(10, 1)

    def write_tutor_data(self):
        logging.debug('Writing tutor data.')
        common_rel = self.archives[b'common.fsys'].get_file(b'common_rel').data
        common_rel.seek(self.tutor_data_common_rel_offset)
        for move in self.tutor_data:
            common_rel.write(pack(">H", move.move.value))
            common_rel.seek(10, 1)

        # And we also need to patch the move-to-tutor-learnset-offset lookup table in the executable.
        self.dol_file.seek(self.tutor_data_start_dol_offset)
        for i, move in enumerate(self.get_reordered_tutor_data_for_dol_patch()):
            self.dol_file.seek(2, 1)
            self.dol_file.write(pack('>H', move.move.value))
            self.dol_file.seek(4, 1)
            # Write a noop here. The lookup table has some funky not-greater-or-equal branch optimization magic
            # going on, and when our new entries can really be in any order, these make us skip over some equality
            # checks completely. It isn't a problem to lose a few cycles and just go through the list one by one,
            # though, so we'll do that instead and ignore even trying to rebuild a similar structure.
            # The fallback branch instruction after the last entry should not be overwritten, though.
            if i < len(self.tutor_data) - 1:
                self.dol_file.write(b'\x60\x00\x00\x00')

    def get_reordered_tutor_data_for_randomization(self):
        # For some reason, the Pokémon tutor learnset flags are in a different order than the tutor data list.
        return [
            self.tutor_data[7],   # Body Slam
            self.tutor_data[10],  # Double-Edge
            self.tutor_data[2],   # Seismic Toss
            self.tutor_data[0],   # Mimic
            self.tutor_data[5],   # Dream Eater
            self.tutor_data[4],   # Substitute
            self.tutor_data[1],   # Thunder Wave
            self.tutor_data[3],   # Icy Wind
            self.tutor_data[6],   # Swagger
            self.tutor_data[9],   # Sky Attack
            self.tutor_data[11],  # Self-Destruct
            self.tutor_data[8],   # Nightmare
        ]

    def get_reordered_tutor_data_for_dol_patch(self):
        # ...and pointers to bit indices to figure out the above are hard-coded in start.dol and are also in a yet
        # another order. Fun!
        return [
            self.tutor_data[5],   # Dream Eater
            self.tutor_data[1],   # Thunder Wave
            self.tutor_data[10],  # Double-Edge
            self.tutor_data[7],   # Body Slam
            self.tutor_data[2],   # Seismic Toss
            self.tutor_data[11],  # Self-Destruct
            self.tutor_data[0],   # Mimic
            self.tutor_data[8],   # Nightmare
            self.tutor_data[4],   # Substitute
            self.tutor_data[9],   # Sky Attack
            self.tutor_data[6],   # Swagger
            self.tutor_data[3],   # Icy Wind
        ]

    def randomize_tutor_moves(self):
        logging.info('Randomizing tutor moves.')
        self.tutor_data = random.sample(self.get_available_regular_moves(), self.TUTOR_LIST_LENGTH)
        for i, move in enumerate(self.tutor_data):
            logging.debug('  Tutor move #%d is now %s', i + 1, move.move.name)

    def randomize_pokemon_tutor_data(self):
        logging.info('Randomizing Pokémon tutor learnsets.')
        self.randomize_pokemon_aspect_recur('tutors', 'previous_stage_tutors',
                                            self.randomize_pokemon_get_root_level_list(config.rng_pktutor_family),
                                            recurse=config.rng_pktutor_family,
                                            tutor_data=self.get_reordered_tutor_data_for_randomization())

    def load_game_specific_data(self):
        self.load_tutor_data()

    def write_game_specific_data(self):
        self.write_tutor_data()

    def randomize_game_specific_features(self):
        self.randomize_pokespot_data()

        if config.rng_tutor_moves:
            self.randomize_tutor_moves()
        if config.rng_pktutor:
            self.randomize_pokemon_tutor_data()

    def update_banner(self):
        name = 'XDランダマイザー'.encode('shift-jis') if self.region == IsoRegion.JPN else b'XD Randomizer'

        self.write_rom_header_name(name)
        self.write_banner_name(name)

    @property
    def archive_list(self):
        return [
            b'common.fsys',
            b'deck_archive.fsys'
        ]

    @property
    def pokemon_data_offset(self):
        if self.region == IsoRegion.USA:
            return 0x00029ECC
        elif self.region == IsoRegion.EUR:
            return 0x0002BE8C
        elif self.region == IsoRegion.JPN:
            return 0x00028C80
        else:
            raise NotImplementedError

    @property
    def move_data_offset(self):
        if self.region == IsoRegion.USA:
            return 0x000A2748
        elif self.region == IsoRegion.EUR:
            return 0x000A75C4
        elif self.region == IsoRegion.JPN:
            return 0x0005BAB4
        else:
            raise NotImplementedError

    @property
    def tm_data_offset(self):
        if self.region == IsoRegion.USA:
            return 0x004023A0
        elif self.region == IsoRegion.EUR:
            return 0x0043CC80
        elif self.region == IsoRegion.JPN:
            return 0x003DFA60
        else:
            raise NotImplementedError

    @property
    def item_data_offset(self):
        if self.region == IsoRegion.USA:
            return 0x0001EDAC
        elif self.region == IsoRegion.EUR:
            return 0x00020D6C
        elif self.region == IsoRegion.JPN:
            return 0x0001DB60
        else:
            raise NotImplementedError

    @property
    def starter_data_offsets(self):
        if self.region == IsoRegion.USA:
            return [
                0x001CBC52,
                None
            ]
        elif self.region == IsoRegion.EUR:
            return [
                0x001CD726,
                None
            ]
        elif self.region == IsoRegion.JPN:
            return [
                0x001C6AF6,
                None
            ]
        else:
            raise NotImplementedError

    # in start.dol
    @property
    def shadow_monitor_data_offset(self):
        if self.region == IsoRegion.USA:
            return 0x004014E8
        elif self.region == IsoRegion.EUR:
            return 0x0043BDC8
        elif self.region == IsoRegion.JPN:
            return 0x003DEBA8
        else:
            raise NotImplementedError

    # in common.fsys/common_rel
    @property
    def tutor_data_common_rel_offset(self):
        if self.region == IsoRegion.USA:
            return 0x000A7918
        elif self.region == IsoRegion.EUR:
            return 0x000AC794
        elif self.region == IsoRegion.JPN:
            return 0x00060C84
        else:
            raise NotImplementedError

    # in start.dol
    @property
    def tutor_data_start_dol_offset(self):
        if self.region == IsoRegion.USA:
            return 0x001C2EA4
        elif self.region == IsoRegion.EUR:
            return 0x001C47A0
        elif self.region == IsoRegion.JPN:
            return 0x001BE3B4
        else:
            raise NotImplementedError

    # in common.fsys/common_rel
    @property
    def bingo_data_offset(self):
        # The same for all regions
        return 0x00001CAF

    # in common.fsys/common_rel
    @property
    def pokespot_data_offset(self):
        # The same for all regions
        return 0x00002FAC


