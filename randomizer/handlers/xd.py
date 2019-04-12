#!/usr/bin/env python
# -*- coding: utf-8 -*-
from struct import unpack, pack

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
        self.move = Move.from_idx(idx)
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


class XDHandler(BaseHandler):
    POKEMON_DATA_LIST_LENGTH = 414
    MOVE_DATA_LIST_LENGTH = 373

    def get_available_shadow_moves(self):
        return set(range(Move.SHADOW_BLITZ.value, Move.SHADOW_HALF.value))

    def open_archives(self):
        self.open_archive(b'common.fsys')
        # self.open_archive(b'deck_archive.fsys')

    def make_pokemon_data(self, io_in, idx):
        return XDPokemon(io_in.read(0x124), idx)

    def make_move_data(self, io_in, idx):
        return XDMoveEntry(io_in.read(0x38), idx)

    def write_archives(self):
        self.write_archive(b'common.fsys')

    def get_pokemon_data_offset(self):
        if self.region == IsoRegion.USA:
            return 0x00029ECC
        elif self.region == IsoRegion.EUR:
            return 0x0002BE8C
        elif self.region == IsoRegion.JPN:
            raise NotImplementedError
        else:
            raise NotImplementedError

    def get_move_data_offset(self):
        if self.region == IsoRegion.USA:
            return 0x000A2748
        elif self.region == IsoRegion.EUR:
            return 0x000A75C4
        elif self.region == IsoRegion.JPN:
            raise NotImplementedError
        else:
            raise NotImplementedError

    def get_tm_data_offset(self):
        if self.region == IsoRegion.USA:
            return 0x004023A0
        elif self.region == IsoRegion.EUR:
            return 0x0043CC80
        elif self.region == IsoRegion.JPN:
            raise NotImplementedError
        else:
            raise NotImplementedError
