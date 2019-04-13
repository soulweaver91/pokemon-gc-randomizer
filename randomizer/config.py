#!/usr/bin/env python
# -*- coding: utf-8 -*-


class RandomizerConfig:
    def __init__(self):
        self._config = {
            "working_dir": None,
            "dump_files": False,
            "rng_pkstats": True,
            "rng_pkstats_retain_bst": True,
            "rng_pkstats_family": True,
            "rng_pkstats_family_vary_branched_evo": True,
            "rng_pkstats_wg_1hp": True,
            "rng_pkstats_variance": 0.35,
            "rng_pktypes": True,
            "rng_pktypes_family": True,
            "rng_pktypes_family_change_ratio": 33,
            "rng_pktypes_monotype_ratio": 33,
            "rng_pkabi": True,
            "rng_pkabi_family": True,
            "rng_pkabi_family_change_ratio": 33,
            "rng_pkabi_monoabi_ratio": 33,
            "rng_pkabi_ban": ['WONDER_GUARD', 'FORECAST'],
            "rng_pkmoves": True,
            "rng_pkmoves_ban": ['SONICBOOM', 'DRAGON_RAGE', 'GUILLOTINE', 'FISSURE', 'HORN_DRILL', 'SHEER_COLD'],
            "rng_pkmoves_lv1_fullset": True,
            "rng_pkmoves_lv1_ensure_damaging": True,
            "rng_pkmoves_ensure_damaging_interval": True,
            "rng_pkmoves_dmg_progression": True,
            "rng_pkmoves_no_dupes": True,
            "rng_pkmoves_any_type_ratio": 25,
            "rng_pkmoves_min_damaging_ratio": 25,
            "rng_pkmoves_min_own_type_ratio": 15,
            "rng_move_power": False,
            "rng_move_types": False,
            "rng_move_accuracy": False,
            "rng_move_pp": False,
            "rng_tm_moves": True,
            "patch_impossible_evolutions": True
        }

    def configure(self, **kwargs):
        for argn, argv in kwargs.items():
            if argn in self._config and argv is not None:
                self._config[argn] = argv
        pass

    def __getattr__(self, name):
        return self._config[name]


config = RandomizerConfig()
