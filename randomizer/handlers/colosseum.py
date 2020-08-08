#!/usr/bin/env python
# -*- coding: utf-8 -*-
from enum import IntEnum
import random
from struct import unpack, pack
import logging

from randomizer import config
from randomizer.constants import IsoRegion
from randomizer.handlers.base import BasePokemon, BaseMoveEntry, randomize_pokemon
from randomizer.iso.constants import Move, ExpClass, Ability, Type, PokemonSpecies, Item, EvolutionType, Nature
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
            self.name_index,
            self.unknown_0x1c_0x1d,
            self.species_str_pointer,
            self.unknown_0x20_0x25,
            self.unknown_running_no_3,
            self.unknown_0x28_0x29,
            self.unknown_running_no_4,
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
            self.name_index,
            self.unknown_0x1c_0x1d,
            self.species_str_pointer,
            self.unknown_0x20_0x25,
            self.unknown_running_no_3,
            self.unknown_0x28_0x29,
            self.unknown_running_no_4,
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


class ColosseumTrainerPokemon:
    SIGNATURE = '>BBBBB5sH2s4sH2sH4sBBBBBBHHHHHH8sH6sH6sH6sH'

    def __init__(self, data):
        (
            self.ability_slot,
            self.gender,
            nature,
            self.shadow_id,
            self.level,
            self.unknown_0x05_0x09,
            species,
            self.unknown_0x0c_0x0d,
            self.unknown_0x0e_0x11,
            item,
            self.unknown_0x14_0x15,
            self.nickname_id,
            self.unknown_0x18_0x1b,
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
            self.unknown_0x2e_0x35,
            move1,
            self.unknown_0x38_0x3d,
            move2,
            self.unknown_0x40_0x45,
            move3,
            self.unknown_0x48_0x4d,
            move4,
        ) = unpack(self.SIGNATURE, data)

        self.species = PokemonSpecies(species)
        self.item = Item(item)
        self.moves = [
            Move(move1),
            Move(move2),
            Move(move3),
            Move(move4)
        ]
        self.nature = Nature(nature)

    def encode(self):
        return pack(
            self.SIGNATURE,
            self.ability_slot,
            self.gender,
            self.nature.value,
            self.shadow_id,
            self.level,
            self.unknown_0x05_0x09,
            self.species.value,
            self.unknown_0x0c_0x0d,
            self.unknown_0x0e_0x11,
            self.item.value,
            self.unknown_0x14_0x15,
            self.nickname_id,
            self.unknown_0x18_0x1b,
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
            self.unknown_0x2e_0x35,
            self.moves[0].value,
            self.unknown_0x38_0x3d,
            self.moves[1].value,
            self.unknown_0x40_0x45,
            self.moves[2].value,
            self.unknown_0x48_0x4d,
            self.moves[3].value,
        )


class ColosseumTrainerEntry:
    SIGNATURE = '>3sBH4sH7sBHHHHHHHHIII4s'

    def __init__(self, data):
        (
            self.unknown_0x00_0x02,
            trainer_class,
            self.party_offset,
            self.unknown_0x06_0x09,
            self.name_id,
            self.unknown_0x0c_0x12,
            self.model_id,
            item1,
            item2,
            item3,
            item4,
            item5,
            item6,
            item7,
            item8,
            self.string_id_post_battle,
            self.string_id_win,
            self.string_id_lose,
            self.unknown_0x30_0x33,
        ) = unpack(self.SIGNATURE, data)

        self.inventory = [
            Item(item1),
            Item(item2),
            Item(item3),
            Item(item4),
            Item(item5),
            Item(item6),
            Item(item7),
            Item(item8),
        ]
        self.trainer_class = ColosseumTrainerClass(trainer_class)


class ColosseumTrainerClass(IntEnum):
    NONE = 0x00
    CIPHER_ADMIN = 0x04
    CIPHER = 0x05
    CIPHER_HEAD = 0x06
    MYTH_TRAINER = 0x07
    MT_BTL_MASTER = 0x08
    RICH_BOY = 0x09
    LADY = 0x0A
    GLASSES_MAN = 0x0B
    LADY_IN_SUIT = 0x0C
    GUY = 0x0D
    TEACHER = 0x0E
    FUN_OLD_MAN = 0x0F
    FUN_OLD_LADY = 0x10
    ATHLETE = 0x11
    COOL_TRAINER = 0x12
    PRE_GYM_LEADER = 0x13
    AREA_LEADER = 0x14
    SUPER_TRAINER = 0x15
    WORKER = 0x16
    SNAGEM_HEAD = 0x17
    MIROR_B_PEON = 0x18
    HUNTER = 0x19
    RIDER = 0x1A
    ROLLER_BOY = 0x1B
    ST_PERFORMER = 0x1C
    BANDANA_GUY = 0x1D
    CHASER = 0x1E
    RESEARCHER = 0x1F
    BODYBUILDER = 0x20
    DEEP_KING = 0x21
    NEWSCASTER = 0x22
    TEAM_SNAGEM = 0x23
    CIPHER_PEON = 0x24
    MYSTERY_TROOP = 0x25
    VR_TRAINER = 0x26
    SHADY_GUY = 0x27
    ROGUE = 0x28


    @classmethod
    def _missing_(cls, value):
        return ColosseumTrainerClass.NONE


class ColosseumHandler(BaseHandler):
    POKEMON_DATA_LIST_LENGTH = 412
    MOVE_DATA_LIST_LENGTH = 357
    ITEM_BOX_LIST_LENGTH = 61
    TRAINER_DATA_LIST_LENGTH = 818
    TRAINER_POKEMON_LIST_LENGTH = 5510

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.trainer_pokemon_data = []
        self.trainer_data = []

    def load_trainer_data(self):
        logging.info('Reading trainer data from the archive file.')
        try:
            common_rel = self.archives[b'common.fsys'].get_file(b'common_rel').data

            logging.debug('Reading trainer Pokémon data...')
            common_rel.seek(self.trainer_pokemon_offset)
            for i in range(1, self.TRAINER_POKEMON_LIST_LENGTH + 1):
                pokemon = ColosseumTrainerPokemon(common_rel.read(0x50))
                self.trainer_pokemon_data.append(pokemon)

                if pokemon.species == PokemonSpecies.NONE:
                    logging.debug('  #%d (Empty entry)', i)
                else:
                    logging.debug(
                        '  #%d Lv%d %s%s%s with %s, %s nature, IVs %s, EVs %s',
                        i,
                        pokemon.level,
                        'Shadow ' if pokemon.shadow_id > 0 else '',
                        PokemonSpecies(pokemon.species).name,
                        ' (Shadow ID: %d)' % pokemon.shadow_id if pokemon.shadow_id > 0 else '',
                        '/'.join([m.name for m in pokemon.moves if m != Move.NONE]),
                        pokemon.nature.name,
                        '/'.join(['?' if v == 255 else str(v) for v in [pokemon.iv_hp, pokemon.iv_atk, pokemon.iv_def,
                                  pokemon.iv_spatk, pokemon.iv_spdef, pokemon.iv_speed]]),
                        '/'.join(['?' if v == 65535 else str(v) for v in [pokemon.ev_hp, pokemon.ev_atk, pokemon.ev_def,
                                  pokemon.ev_spatk, pokemon.ev_spdef, pokemon.ev_speed]]),
                    )

            logging.debug('Reading trainer data...')
            common_rel.seek(self.trainer_data_offset)
            for i in range(1, self.TRAINER_DATA_LIST_LENGTH + 1):
                trainer = ColosseumTrainerEntry(common_rel.read(0x34))
                self.trainer_data.append(trainer)

                party = self.trainer_pokemon_data[trainer.party_offset:trainer.party_offset + 6]

                logging.debug(
                    '  #%d %s, party offset %d (%s)',
                    i,
                    trainer.trainer_class.name,
                    trainer.party_offset,
                    ', '.join(['Lv%d %s%s' % (pokemon.level,
                                              'Shadow ' if pokemon.shadow_id > 0 else '',
                                              PokemonSpecies(pokemon.species).name) for pokemon in party
                               if pokemon.species != PokemonSpecies.NONE])
                )

        except KeyError as e:
            logging.error('Couldn\'t read move data since the required data file was not loaded.')
            raise e
        pass

    def write_trainer_data(self):
        logging.debug('Writing trainer data to the ISO.')

        common_rel = self.archives[b'common.fsys'].get_file(b'common_rel').data
        common_rel.seek(self.trainer_pokemon_offset)
        for i, pkmn in enumerate(self.trainer_pokemon_data):
            logging.debug('Encoding index %d of %d...', i, self.TRAINER_POKEMON_LIST_LENGTH)
            common_rel.write(pkmn.encode())

    def make_pokemon_data(self, io_in, idx):
        return ColosseumPokemon(io_in.read(0x11C), idx)

    def make_move_data(self, io_in, idx):
        return ColosseumMoveEntry(io_in.read(0x38), idx)

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
        if not config.rng_gifts:
            # There are no trades in Colosseum, all randomizable static Pokémon are gifts
            return

        logging.info('Randomizing gift Pokémon data.')

        species = random.sample(self.normal_pokemon, len(self.trade_and_gift_data_offsets))

        for i, offset in enumerate(self.trade_and_gift_data_offsets):
            self.dol_file.seek(offset)
            self.dol_file.seek(2, 1)
            self.dol_file.write(pack('>H', species[i].species.value))

        logging.info('  Agate Celebi is now %s' % species[0].species.name)
        logging.info('  Agate Pikachu is now %s' % species[1].species.name)
        logging.info('  Mt. Battle Ho-Oh is now %s' % species[2].species.name)
        logging.info('  Duking\'s Plusle is now %s' % species[3].species.name)

    def randomize_trainers(self):
        logging.debug('Randomizing trainer data.')
        allowed_shadow_pokemon = [p.species for p in self.normal_pokemon]
        random.shuffle(allowed_shadow_pokemon)

        bsts = [p.base_stats.total for p in self.pokemon_data.values()]
        bst_min = min(bsts)
        bst_max = max(bsts)

        shadow_pokemon_dex_nos = dict()
        for i, pokemon in enumerate(self.trainer_pokemon_data):
            if pokemon.species == PokemonSpecies.NONE:
                continue

            # 245..832: Colosseum Battle rosters
            # 833..839: Seemingly unused Colosseum Battle trainer
            # 840..895: Colosseum Battle rosters
            # 896..1595: Mt. Battle Doubles
            # 1596..2295: Mt. Battle Singles
            # 3774..3801: Colosseum Battle rosters
            if 896 <= i <= 2295 and not config.rng_trainers_cat_mt_battle:
                continue

            if (245 <= i <= 895 or 3774 <= i <= 3801) and not config.rng_trainers_cat_colo_battle:
                continue

            is_shadow = pokemon.shadow_id != 0

            fixed_species = shadow_pokemon_dex_nos.get(pokemon.shadow_id, None)
            randomize_pokemon(pokemon=pokemon, pokemon_data=self.pokemon_data, move_data=self.move_data,
                              is_shadow=is_shadow, bst_min=bst_min, bst_max=bst_max,
                              shadow_candidates=allowed_shadow_pokemon, fixed_species=fixed_species)

            # The Pokémon nickname needs to be fixed as well since for some reason all trainer Pokémon have such
            # a pointer in their data.
            pokemon.nickname_id = self.pokemon_data[pokemon.species.value].name_index

            if is_shadow:
                shadow_pokemon_dex_nos[pokemon.shadow_id] = pokemon.species

        for i, trainer in enumerate(self.trainer_data):
            party = self.trainer_pokemon_data[trainer.party_offset:trainer.party_offset + 6]

            logging.debug(
                '  #%d %s, party offset %d (%s)',
                i,
                trainer.trainer_class.name,
                trainer.party_offset,
                ', '.join(['Lv%d %s%s' % (pokemon.level,
                                          'Shadow ' if pokemon.shadow_id > 0 else '',
                                          PokemonSpecies(pokemon.species).name) for pokemon in party
                           if pokemon.species != PokemonSpecies.NONE])
            )

        # write the Shadow Pokémon list
        common_rel = self.archives[b'common.fsys'].get_file(b'common_rel').data
        for i, species in shadow_pokemon_dex_nos.items():
            common_rel.seek(self.pda_shadow_data_offset + 0x38 * i)
            common_rel.write(pack('>H', species.value))

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
            return 0x0011D814
        elif self.region == IsoRegion.EUR:
            return 0x001EAB90
        elif self.region == IsoRegion.JPN:
            return 0x000A04F0
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
        # Celebi, Pikachu, Ho-Oh, Plusle
        if self.region == IsoRegion.USA:
            return [
                0x0012D6B4,
                0x0012D7C4,
                0x0012D8E4,
                0x0012D9C8
            ]
        elif self.region == IsoRegion.EUR:
            return [
                0x001318E0,
                0x001319F0,
                0x00131B10,
                0x00131BF4
            ]
        elif self.region == IsoRegion.JPN:
            return [
                0x0012ADD0,
                0x0012AEBC,
                0x0012AFB8,
                0x0012B098
            ]
        else:
            raise NotImplementedError

    # in common.fsys/common_rel
    @property
    def trainer_pokemon_offset(self):
        if self.region == IsoRegion.USA:
            return 0x0009FE28
        elif self.region == IsoRegion.EUR:
            return 0x0016AE44
        elif self.region == IsoRegion.JPN:
            return 0x00022B04
        else:
            raise NotImplementedError

    # in common.fsys/common_rel
    @property
    def trainer_data_offset(self):
        if self.region == IsoRegion.USA:
            return 0x00092F04
        elif self.region == IsoRegion.EUR:
            return 0
        elif self.region == IsoRegion.JPN:
            return 0
        else:
            raise NotImplementedError

    # in common.fsys/common_rel
    @property
    def pda_shadow_data_offset(self):
        if self.region == IsoRegion.USA:
            return 0x00145226
        elif self.region == IsoRegion.EUR:
            return 0x002125A2
        elif self.region == IsoRegion.JPN:
            return 0x000C7F02
        else:
            raise NotImplementedError
