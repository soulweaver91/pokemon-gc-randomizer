#!/usr/bin/env python
# -*- coding: utf-8 -*-
import random
from io import BytesIO
from struct import unpack, pack
import logging

from randomizer import config
from randomizer.constants import IsoRegion
from randomizer.handlers.base import BasePokemon, BaseMoveEntry
from randomizer.iso.constants import Move, ExpClass, Ability, Type, PokemonSpecies, Item
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
        for i, pokemon in enumerate(self.entries):
            if pokemon.species == PokemonSpecies.NONE:
                continue

            if i in shadow_indexes and config.rng_trainers_unique_shadow:
                pokemon.species = shadow_candidates.pop()
            else:
                pokemon.species = random.choice([p.species for p in pokemon_data.values() if 0 < p.natdex_no < 388])

            # todo: moves, restrictions, etc.

        return shadow_candidates

    @property
    def section_type(self):
        return b'DPKM'

    @property
    def section_name(self):
        return 'Regular Pokémon data'


class XDTrainerDeckDDPK(XDTrainerSection):
    SHADOW_MOVES = [Move(m) for m in range(Move.SHADOW_BLITZ.value, Move.SHADOW_HALF.value)]

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

            shadow_move_count = random.randint(1, 4)
            moves = random.sample(self.SHADOW_MOVES, shadow_move_count) + [Move.NONE] * (4 - shadow_move_count)
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


class XDHandler(BaseHandler):
    POKEMON_DATA_LIST_LENGTH = 414
    MOVE_DATA_LIST_LENGTH = 373

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.trainer_decks = {}
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

    def write_trainer_data(self):
        logging.debug('Encoding trainer data in preparation to be written to the ISO.')

        for deck_name, deck in self.trainer_decks.items():
            logging.debug('Encoding deck %s...', deck_name.decode('ascii', errors='replace'))
            new_data = BytesIO(deck.encode())

            self.archives[b'deck_archive.fsys'].get_file(deck_name).data = new_data

            if self.region == IsoRegion.EUR:
                self.archives[b'deck_archive.fsys'].get_file(deck_name.replace(b'.bin', b'_EU.bin')).data = new_data

    def make_pokemon_data(self, io_in, idx):
        return XDPokemon(io_in.read(0x124), idx)

    def make_move_data(self, io_in, idx):
        return XDMoveEntry(io_in.read(0x38), idx)

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
            raise NotImplementedError
        else:
            raise NotImplementedError

    @property
    def move_data_offset(self):
        if self.region == IsoRegion.USA:
            return 0x000A2748
        elif self.region == IsoRegion.EUR:
            return 0x000A75C4
        elif self.region == IsoRegion.JPN:
            raise NotImplementedError
        else:
            raise NotImplementedError

    @property
    def tm_data_offset(self):
        if self.region == IsoRegion.USA:
            return 0x004023A0
        elif self.region == IsoRegion.EUR:
            return 0x0043CC80
        elif self.region == IsoRegion.JPN:
            raise NotImplementedError
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
            raise NotImplementedError
        else:
            raise NotImplementedError
