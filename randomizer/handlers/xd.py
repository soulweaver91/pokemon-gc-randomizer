#!/usr/bin/env python
# -*- coding: utf-8 -*-
import random
from io import BytesIO
from struct import unpack, pack
import logging

from randomizer import config
from randomizer.constants import IsoRegion
from randomizer.handlers.base import BasePokemon, BaseMoveEntry, get_bst_range_for_level, randomize_pokemon
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

    def randomize(self, pokemon_data, move_data, shadow_indexes, shadow_candidates):
        for section in self.sections:
            if type(section) is XDTrainerDeckDPKM:
                shadow_candidates = section.randomize(pokemon_data, move_data, shadow_indexes, shadow_candidates)
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

    def randomize(self, pokemon_data, move_data, shadow_indexes, shadow_candidates):
        bsts = [p.base_stats.total for p in pokemon_data.values()]
        bst_min = min(bsts)
        bst_max = max(bsts)

        for i, pokemon in enumerate(self.entries):
            randomize_pokemon(pokemon=pokemon, pokemon_data=pokemon_data, move_data=move_data,
                              is_shadow=i in shadow_indexes, bst_min=bst_min, bst_max=bst_max,
                              shadow_candidates=shadow_candidates)

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
            pokemon.move = random.choice([m for m in level_up_moves * 4 + tm_moves if move_data[m.value].power > 0])


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

    def randomize_and_write_trades_and_gifts(self):
        logging.info('Randomizing gift and trade Pokémon data.')

        # Find what we randomized the Togepi to. We need to put the same species here for coherency.
        # Also, we want to have Hordel accept that Pokémon (only) for his trade.
        togepi = None
        try:
            story_deck = self.trainer_decks[b'DeckData_Story.bin']
            for story_deck_section in story_deck.sections:
                if story_deck_section.section_type == b'DPKM':
                    togepi = self.pokemon_data[story_deck_section.entries[1].species.value]
                    break
        except KeyError:
            # This shouldn't happen.
            logging.warning('Shadow Togepi data was not found, the gifted Pokémon might be incoherent.')
            togepi = random.choice(self.normal_pokemon)

        species = [togepi] + random.sample([p for p in self.normal_pokemon if p != togepi], 7)

        # Depending on the config, the range is either [0], [], [0, 1, 2, 3, 4] or [1, 2, 3, 4]
        for i in range(0 if config.rng_gifts else 1, 1 if config.rng_trade_offers else 5):
            self.dol_file.seek(self.trade_and_gift_data_offsets[i])
            self.dol_file.seek(2, 1)
            self.dol_file.write(pack('>H', species[i].species.value))
            self.dol_file.seek(8, 1)

            level = unpack('>H', self.dol_file.read(2))[0]
            moves = [m.move for m in species[i].level_up_moves if m.level <= level][-4:]
            while len(moves) < 4:
                moves.append(Move.NONE)

            self.dol_file.seek(24, 1)

            for j in range(4):
                self.dol_file.write(pack(">H", moves[j].value))
                self.dol_file.seek(2, 1)

        # Cancel the randomized results if these were ultimately not written. This is really only necessary
        # for the upcoming info console output.
        # If the ROM has been edited beforehand, these are also actually not correct. However, we only support
        # randomizing a clean ROM, so we can allow that slight chance of inconsistency if the user does randomize
        # an already altered ROM.
        if not config.rng_gifts:
            species[0] = self.pokemon_data[PokemonSpecies.TOGEPI]
        if not config.rng_trade_offers:
            species[1:5] = [self.pokemon_data[PokemonSpecies.ELEKID],
                            self.pokemon_data[PokemonSpecies.TRAPINCH],
                            self.pokemon_data[PokemonSpecies.SURSKIT],
                            self.pokemon_data[PokemonSpecies.WOOPER]]

        if config.rng_gifts:
            for i in range(5, 8):
                self.dol_file.seek(self.trade_and_gift_data_offsets[i])
                self.dol_file.seek(2, 1)
                self.dol_file.write(pack('>H', species[i].species.value))
                self.dol_file.seek(2, 1)

                moves = [m.move for m in species[i].level_up_moves if m.level <= 5][-4:]
                while len(moves) < 4:
                    moves.append(Move.NONE)

                for j in range(4):
                    self.dol_file.write(pack(">H", moves[j].value))
                    self.dol_file.seek(2, 1)

        # Then, update what the trainers are asking in the first place.
        if config.rng_trade_wants:
            pyrite_scripts = self.archives[b'M2_guild_1F_2.fsys'].get_file(b'M2_guild_1F_2', 1).data
            pyrite_scripts.seek(self.duking_trade_script_pkmn_offset)
            trade_wants = random.sample(self.normal_pokemon, 3)
            for trade_want in trade_wants:
                pyrite_scripts.write(pack('>H', trade_want.species.value))
                pyrite_scripts.seek(78, 1)
            pyrite_scripts.seek(228, 1)
            for trade_want in trade_wants:
                pyrite_scripts.write(pack('>H', trade_want.species.value))
                pyrite_scripts.seek(66, 1)
        else:
            # Same caveats about already edited ROMs apply to this too.
            trade_wants = [self.pokemon_data[PokemonSpecies.MEDITITE],
                           self.pokemon_data[PokemonSpecies.SHUCKLE],
                           self.pokemon_data[PokemonSpecies.LARVITAR]]

        if config.rng_gifts:
            outskirt_scripts = self.archives[b'S1_shop_1F.fsys'].get_file(b'S1_shop_1F', 1).data
            outskirt_scripts.seek(self.hordel_trade_script_pkmn_offset)
            outskirt_scripts.write(pack('>H', species[0].species.value))
            outskirt_scripts.seek(14, 1)
            outskirt_scripts.write(pack('>H', species[0].species.value))
            outskirt_scripts.seek(1018, 1)
            outskirt_scripts.write(pack('>H', species[0].species.value))
            outskirt_scripts.seek(30, 1)
            outskirt_scripts.write(pack('>H', species[0].species.value))

        logging.info('  Hordel now hands out a Shadow %s and trades a purified %s for his %s'
                     % (species[0].species.name, species[0].species.name, species[1].species.name))
        logging.info('  Duking now trades his %s for your %s, his %s for your %s and his %s for your %s'
                     % (trade_wants[0].species.name, species[2].species.name, trade_wants[1].species.name,
                        species[3].species.name, trade_wants[2].species.name, species[4].species.name))
        logging.info('  Mt. Battle rewards are now %s, %s and %s'
                     % (species[5].species.name, species[6].species.name, species[7].species.name))

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
                deck.randomize(self.pokemon_data, self.move_data, self.shadow_pokemon_indexes, allowed_shadow_pokemon)

                for section in deck.sections:
                    if section.section_type == b'DPKM':
                        for i, pokemon in enumerate(section.entries):
                            if pokemon.species != PokemonSpecies.NONE:
                                logging.debug('    #%d: Lv%d %s with %s%s' % (
                                    i, pokemon.level, pokemon.species.name,
                                    '/'.join([m.name for m in pokemon.moves if m != Move.NONE]),
                                    ('' if pokemon.item == Item.NONE else ' holding %s' % pokemon.item.name)))
                            else:
                                logging.debug('    #%d: Blank entry' % i)

                    elif section.section_type == b'DDPK':
                        for i, pokemon in enumerate(section.entries):
                            if pokemon.dpkm_index != 0:
                                self.shadow_pokemon_indexes.append(pokemon.dpkm_index)

                                species_name = ('???' if story_dpkm is None
                                                else story_dpkm.entries[pokemon.dpkm_index].species.name)

                                logging.debug('    #%d: Lv%d Shadow %s (story deck #%d) with %s, catch rate %d' % (
                                    i, pokemon.level, species_name, pokemon.dpkm_index,
                                    '/'.join([m.name for m in pokemon.move_overrides if m != Move.NONE]),
                                    pokemon.catch_rate))
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
            common_rel.seek(4, 1)
            if config.patch_early_tutors:
                common_rel.write(pack(">H", 1))
            else:
                common_rel.seek(2, 1)
            common_rel.seek(4, 1)

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

    def improve_catch_rates(self):
        logging.info('Updating Pokémon catch rates.')
        for pkmn in self.normal_pokemon:
            pkmn.catch_rate = max(pkmn.catch_rate, config.rng_improve_catch_rate_minimum)
            logging.debug('The catch rate of %s is now %d' % (pkmn.species.name, pkmn.catch_rate))

        # These also need to be updated to the shadow Pokémon deck.
        dark_ddpk = None
        try:
            dark_deck = self.trainer_decks[b'DeckData_DarkPokemon.bin']
            for dark_deck_section in dark_deck.sections:
                if dark_deck_section.section_type == b'DDPK':
                    dark_ddpk = dark_deck_section
                    break
        except KeyError:
            logging.warning('Shadow Pokémon data was not found for some reason, catch rates were not altered.')
            return

        for entry in dark_ddpk.entries:
            if entry.dpkm_index == 0:
                continue

            entry.catch_rate = max(entry.catch_rate, config.rng_improve_catch_rate_minimum)

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
        archives = [
            b'common.fsys',
            b'deck_archive.fsys'
        ]

        if config.rng_trade_wants or config.rng_trade_offers:
            archives += [
                b'M2_guild_1F_2.fsys',  # For Duking trades
            ]
        if config.rng_trade_wants or config.rng_trade_offers or config.rng_gifts:
            archives += [
                b'S1_shop_1F.fsys'      # For Hordel gift/trade
            ]

        return archives

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
    def fixable_name_offsets(self):
        if self.region == IsoRegion.USA:
            return [
                # English
                (0x00051EDC, 0x00052F9E),  # Items pre-TMs
                (0x00053194, 0x000532DE),  # Items post-TMs, pre-Battle CDs
                (0x00055261, 0x00057245),  # Pokémon, types, abilities
                (0x00058083, 0x0005A2FB),  # Natures, locations, moves, trainer classes, stray items
                (0x0005A401, 0x0005BCE9),  # Stray items, trainer names
                (0x0005BE1A, 0x0005BE72),  # Stats
                (0x0006386C, 0x00063942),  # Items again 1
                (0x00063989, 0x00064973),  # Items again 2
                (0x00064B69, 0x00064B79),  # Items again 3
                (0x00065E36, 0x00065ECA),  # Stray stuff
                (0x00065F0A, 0x00065F7C),  # Items again 4
                (0x00066478, 0x0006842C),  # Pokémon, types, abilities again
                (0x0006926A, 0x0006B196),  # Natures, locations, moves, trainer classes, stray items again
                (0x0006B2B6, 0x0006B328),  # Stray items, trainer names again
                (0x0006BA97, 0x0006D6EF),  # Trainer names, trainer classes, stray items, stats again
                # German
                (0x000714DC, 0x000715A4),  # Items 1
                (0x000715EF, 0x00072595),  # Items 2
                (0x000738D8, 0x00073900),  # Stray stuff
                (0x00073994, 0x000739E8),  # Items 3
                (0x00073DCE, 0x00075DAA),  # Pokémon, types, abilities
                (0x00076C74, 0x00078AA4),  # Natures, locations, moves, trainer classes, stray items
                (0x000797E2, 0x00079A1C),  # Stray items, trainer names
                (0x0007A814, 0x0007A81C),  # Stray stuff
                (0x0007A916, 0x0007A976),  # Stats
                # French
                (0x0007E764, 0x0007E840),  # Items 1
                (0x0007E881, 0x0007F897),  # Items 2
                (0x00080D0C, 0x00080D2A),  # Stray stuff
                (0x00080DC6, 0x00080E28),  # Items 3
                (0x0008120E, 0x0008330E),  # Pokémon, types, abilities
                (0x000841AC, 0x00085EE0),  # Natures, locations, moves, trainer classes, stray items
                (0x00086BDA, 0x00086E9C),  # Stray items, trainer names
                (0x00087D9C, 0x00087DF0),  # Stats
                # Italian
                (0x0008BBE8, 0x0008BCB8),  # Items 1
                (0x0008BCF9, 0x0008CD19),  # Items 2
                (0x0008E1AA, 0x0008E236),  # Stray stuff
                (0x0008E276, 0x0008E2D6),  # Items 3
                (0x0008E6BC, 0x000906BC),  # Pokémon, types, abilities
                (0x00091558, 0x0009334A),  # Natures, locations, moves, trainer classes, stray items
                (0x00095050, 0x00095060),  # Stray stuff
                (0x00093F74, 0x00094254),  # Stray items, trainer names
                (0x0009515A, 0x000951B8),  # Stats
                # Spanish
                (0x00098FA4, 0x00099066),  # Items 1
                (0x000990BB, 0x0009A10F),  # Items 2
                (0x0009B4D0, 0x0009B550),  # Stray stuff
                (0x0009B590, 0x0009B5EE),  # Items 3
                (0x0009B9D4, 0x0009D9CC),  # Pokémon, types, abilities
                (0x0009E8A8, 0x000A06A0),  # Natures, locations, moves, trainer classes, stray items
                (0x000A0814, 0x000A0820),  # Stray stuff
                (0x000A12CA, 0x000A1584),  # Stray items, trainer names
                (0x000A2486, 0x000A24E4),  # Stats
            ]
        elif self.region == IsoRegion.EUR:
            return [
                # English
                (0x00053E9C, 0x00054F5E),  # Items pre-TMs
                (0x00055154, 0x0005529E),  # Items post-TMs, pre-Battle CDs
                (0x00057221, 0x00059205),  # Pokémon, types, abilities
                (0x0005A043, 0x0005C2BB),  # Natures, locations, moves, trainer classes, stray items
                (0x0005C3C1, 0x0005DCA9),  # Stray items, trainer names
                (0x0005DDDA, 0x0005DE32),  # Stats
                (0x0006582C, 0x00065902),  # Items again 1
                (0x00065949, 0x00066933),  # Items again 2
                (0x00066B29, 0x00066B39),  # Items again 3
                (0x00067DF2, 0x00067E86),  # Stray stuff
                (0x00067EC6, 0x00067F38),  # Items again 4
                (0x00068434, 0x0006A3E8),  # Pokémon, types, abilities again
                (0x0006B052, 0x0006CF7E),  # Natures, locations, moves, trainer classes, stray items again
                (0x0006D09E, 0x0006D110),  # Stray items, trainer names again
                (0x0006D887, 0x0006F469),  # Trainer names, trainer classes, stray items
                (0x0006F65B, 0x0006F6B3),  # Stats again
                # German
                (0x000734A0, 0x00073568),  # Items 1
                (0x000735C7, 0x00074559),  # Items 2
                (0x0007474F, 0x00074763),  # Stray stuff
                (0x0007589C, 0x00075924),  # Stray stuff
                (0x00075964, 0x000759C6),  # Items 3
                (0x00075E60, 0x00077E3C),  # Pokémon, types, abilities
                (0x00078B52, 0x0007AC46),  # Natures, locations, moves, trainer classes, stray items
                (0x0007AD50, 0x0007ADC8),  # Stray items, trainer names
                (0x0007B62D, 0x0007D179),  # Trainer names and classes
                (0x0007D34B, 0x0007D3AB),  # Stats
                # French
                (0x00081198, 0x00081274),  # Items 1
                (0x000812B5, 0x000822CB),  # Items 2
                (0x000824C1, 0x000824D5),  # Stray stuff
                (0x00083758, 0x0008379E),  # Stray stuff
                (0x000837D4, 0x00085E54),  # Items 3, Pokémon, types, abilities
                (0x00086AFC, 0x00088C6A),  # Natures, locations, moves, trainer classes, trainer names, stray items
                (0x0008951B, 0x0008B227),  # Trainer names and classes
                (0x0008B43B, 0x0008B495),  # Stats
                # Italian
                (0x0008F28C, 0x0008F35C),  # Items 1
                (0x0008F39B, 0x000903BB),  # Items 2
                (0x000905B3, 0x000905D1),  # Stray stuff
                (0x000917E4, 0x00091880),  # Stray stuff
                (0x000918D4, 0x00091920),  # Items 3
                (0x00091DCC, 0x00093DCE),  # Pokémon, types, abilities
                (0x00094A9C, 0x00096B4C),  # Natures, locations, moves, trainer classes, stray items
                (0x00096C56, 0x00096CB0),  # Stray stuff
                (0x000974E9, 0x00099383),  # Stray items, trainer names
                (0x00099573, 0x000995D2),  # Stats
                # Spanish
                (0x0009D3C0, 0x0009D498),  # Items 1
                (0x0009D4D7, 0x0009E52B),  # Items 2
                (0x0009E721, 0x0009E735),  # Stray stuff
                (0x0009F8F0, 0x0009F986),  # Stray stuff
                (0x0009F9C6, 0x000A1EBC),  # Items 3, Pokémon, types, abilities
                (0x000A2BAA, 0x000A4DEC),  # Natures, locations, moves, trainer classes, trainer names, stray items
                (0x000A55C5, 0x000A70F5),  # Stray items, trainer names
                (0x000A7301, 0x000A7361),  # Stats
            ]
        elif self.region == IsoRegion.JPN:
            return []
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
    def trade_and_gift_data_offsets(self):
        # Togepi, Elekid, Meditite, Shuckle, Larvitar, Chikorita, Cyndaquil, Totodile
        if self.region == IsoRegion.USA:
            return [
                0x001C5760,
                0x001C57A4,
                0x001C5888,
                0x001C58D8,
                0x001C5928,
                0x001C5974,
                0x001C59A0,
                0x001C59CC
            ]
        elif self.region == IsoRegion.EUR:
            return [
                0x001C705C,
                0x001C70A0,
                0x001C7184,
                0x001C71D4,
                0x001C7224,
                0x001C7270,
                0x001C729C,
                0x001C72C8
            ]
        elif self.region == IsoRegion.JPN:
            return [
                0x001C0C70,
                0x001C0CB4,
                0x001C0D1C,
                0x001C0D6C,
                0x001C0DBC,
                0x001C0E08,
                0x001C0E34,
                0x001C0E60
            ]
        else:
            raise NotImplementedError

    # in M2_guild_1F_2.fsys/M2_guild_1F_2 (#2)
    @property
    def duking_trade_script_pkmn_offset(self):
        # The same for all regions
        return 0x00000B4A

    # in S1_shop_1F.fsys/S1_shop_1F (#2)
    @property
    def hordel_trade_script_pkmn_offset(self):
        # The same for all regions
        return 0x00000F26

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


