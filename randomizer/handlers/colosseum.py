#!/usr/bin/env python
# -*- coding: utf-8 -*-
from struct import unpack, pack
import logging

from randomizer import config
from randomizer.constants import IsoRegion
from randomizer.handlers.base import BasePokemon, BaseMoveEntry
from randomizer.iso.constants import Move, ExpClass, Ability, Type, PokemonSpecies, Item, EvolutionType
from . import BaseHandler


class ColosseumPokemon(BasePokemon):
    SIGNATURE = '>BBBBHHHHHHHHH4sHHH6sHHHHHBBBB50s8sHHH16sHHHHHHHHHHHH30s80s18s'

    def __init__(self, data, idx):
        super().__init__()

        (
            exp_class,
            self.catch_rate,
            self.gender_ratio,
            self.unknown_0x03,
            self.unknown_0x04,
            self.exp_gain,
            self.base_happiness,
            self.height,
            self.weight,
            self.unknown_running_no_1,
            self.natdex_no,
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
            self.unknown_0x6e_0x6f,
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
            self.unknown_0x10A_0x11B
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
        self.set_learn_flags(tm_compatibility, hm_compatibility, [])
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
            self.unknown_0x04,
            self.exp_gain,
            self.base_happiness,
            self.height,
            self.weight,
            self.unknown_running_no_1,
            self.natdex_no,
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
            self.unknown_0x6e_0x6f,
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
            self.unknown_0x10A_0x11B)


class ColosseumMoveEntry(BaseMoveEntry):
    SIGNATURE = '>bBBBBBBBBBBB4sBBBB3sB3sB6sH10sH2sH4s'

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
            self.recoil,
            self.unknown_0x14_0x16,
            self.power,
            self.unknown_0x18_0x1a,
            self.effect_type,
            self.unknown_0x1c_0x21,
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
            self.recoil,
            self.unknown_0x14_0x16,
            self.power,
            self.unknown_0x18_0x1a,
            self.effect_type,
            self.unknown_0x1c_0x21,
            self.name_id,
            self.unknown_0x24_0x2d,
            self.desc_id,
            self.unknown_0x30_0x31,
            self.anim_id,
            self.unknown_0x34_0x37
        )


class ColosseumHandler(BaseHandler):
    POKEMON_DATA_LIST_LENGTH = 412
    MOVE_DATA_LIST_LENGTH = 357
    ITEM_BOX_LIST_LENGTH = 0

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def load_trainer_data(self):
        # TODO
        pass

    def write_trainer_data(self):
        # TODO
        pass

    def make_pokemon_data(self, io_in, idx):
        return ColosseumPokemon(io_in.read(0x11C), idx)

    def make_move_data(self, io_in, idx):
        return ColosseumMoveEntry(io_in.read(0x38), idx)

    def make_item_box_data(self, io_in, idx):
        # TODO
        pass

    def get_game_specific_randomizable_items(self):
        return [Item.JOY_SCENT_COLO, Item.VIVID_SCENT_COLO, Item.EXCITE_SCENT_COLO]

    def randomize_and_write_starter_data(self):
        exp_values = {
            ExpClass.ERRATIC: 23437,
            ExpClass.FAST: 12500,
            ExpClass.MEDIUM_FAST: 15625,
            ExpClass.MEDIUM_SLOW: 11735,
            ExpClass.SLOW: 19531,
            ExpClass.FLUCTUATING: 12187,
        }

        used = []
        for i in range(0, 2):
            starter = self.get_random_starter(1, used)
            moves = [m.move for m in starter.level_up_moves if m.level <= 10][-4:]
            while len(moves) < 4:
                moves.append(Move.NONE)

            self.dol_file.seek(self.starter_data_offsets[i])
            self.dol_file.write(pack(">H", starter.species.value))
            self.dol_file.seek(2, 1)
            self.dol_file.write(pack(">H", 25))
            self.dol_file.seek(14, 1)
            for j in range(4):
                self.dol_file.write(pack(">H", moves[j].value))
                self.dol_file.seek(14, 1)
            self.dol_file.seek(0x3C, 1)
            self.dol_file.write(pack(">H", exp_values[starter.exp_class]))

            used.append(starter)

        logging.info('Starters are now replaced with %s and %s' % (used[0].species.name, used[1].species.name))

    def randomize_and_write_trades_and_gifts(self):
        # TODO
        pass

    def randomize_trainers(self):
        # TODO
        pass

    def improve_catch_rates(self):
        logging.info('Updating Pokémon catch rates.')
        for pkmn in self.normal_pokemon:
            pkmn.catch_rate = max(pkmn.catch_rate, config.rng_improve_catch_rate_minimum)
            logging.debug('The catch rate of %s is now %d' % (pkmn.species.name, pkmn.catch_rate))

    def load_game_specific_data(self):
        pass

    def write_game_specific_data(self):
        pass

    def randomize_game_specific_features(self):
        pass

    def load_item_box_data(self):
        # TODO: not implemented yet, temp. override
        pass

    def write_item_box_data(self):
        # TODO: not implemented yet, temp. override
        pass

    def patch_impossible_game_specific_evolutions(self):
        self.pokemon_data[PokemonSpecies.EEVEE].patch_evolution(3, EvolutionType.STONE_EVOLUTION, Item.SUN_STONE)
        self.pokemon_data[PokemonSpecies.EEVEE].patch_evolution(4, EvolutionType.STONE_EVOLUTION, Item.MOON_STONE)

    def update_banner(self):
        name = 'コロシアムランダマイザー'.encode('shift-jis') if self.region == IsoRegion.JPN else b'Colosseum Randomizer'

        self.write_rom_header_name(name)
        self.write_banner_name(name)

    @property
    def archive_list(self):
        archives = [
            b'common.fsys'
        ]

        return archives

    @property
    def pokemon_data_offset(self):
        if self.region == IsoRegion.USA:
            return 0x0012336C
        elif self.region == IsoRegion.EUR:
            return 0x001F06E8
        elif self.region == IsoRegion.JPN:
            return 0x000A6048
        else:
            raise NotImplementedError

    @property
    def move_data_offset(self):
        if self.region == IsoRegion.USA:
            return 0x0011E048
        elif self.region == IsoRegion.EUR:
            return 0x001EB3C4
        elif self.region == IsoRegion.JPN:
            return 0x000A0D24
        else:
            raise NotImplementedError

    @property
    def tm_data_offset(self):
        if self.region == IsoRegion.USA:
            return 0x00365018
        elif self.region == IsoRegion.EUR:
            return 0x003B20D0
        elif self.region == IsoRegion.JPN:
            return 0x00351758
        else:
            raise NotImplementedError

    @property
    def item_data_offset(self):
        if self.region == IsoRegion.USA:
            raise NotImplementedError
        elif self.region == IsoRegion.EUR:
            raise NotImplementedError
        elif self.region == IsoRegion.JPN:
            raise NotImplementedError
        else:
            raise NotImplementedError

    @property
    def starter_data_offsets(self):
        if self.region == IsoRegion.USA:
            return [
                0x0012DACA,
                0x0012DBF2
            ]
        elif self.region == IsoRegion.EUR:
            return [
                0x00131CF6,
                0x00131E1E
            ]
        elif self.region == IsoRegion.JPN:
            return [
                0x0012B19A,
                0x0012B2C2
            ]
        else:
            raise NotImplementedError

    # in start.dol
    @property
    def trade_and_gift_data_offsets(self):
        if self.region == IsoRegion.USA:
            raise NotImplementedError
        elif self.region == IsoRegion.EUR:
            raise NotImplementedError
        elif self.region == IsoRegion.JPN:
            raise NotImplementedError
        else:
            raise NotImplementedError
