#!/usr/bin/env python
# -*- coding: utf-8 -*-


class RandomizerConfig:
    def __init__(self):
        self._config = {
            "working_dir": None,
            "dump_files": False,
            "seed": None,
            "rng_pkstats": False,
            "rng_pkstats_retain_bst": True,
            "rng_pkstats_family": True,
            "rng_pkstats_family_vary_branched_evo": True,
            "rng_pkstats_wg_1hp": True,
            "rng_pkstats_variance": 0.35,
            "rng_pktypes": False,
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
            "rng_pktm": True,
            "rng_pktm_min_own_type_ratio": 90,
            "rng_pktm_min_other_type_ratio": 40,
            "rng_pktm_min_status_ratio": 75,
            "rng_pktm_min_normal_type_ratio": 75,
            "rng_pktm_family": True,
            "rng_pktm_full_compat": False,
            "rng_pktutor": True,
            "rng_pktutor_min_own_type_ratio": 90,
            "rng_pktutor_min_other_type_ratio": 40,
            "rng_pktutor_min_status_ratio": 75,
            "rng_pktutor_min_normal_type_ratio": 75,
            "rng_pktutor_family": True,
            "rng_pktutor_full_compat": False,
            "rng_pkevo": False,
            "rng_pkevo_shuffle": True,
            "rng_pkevo_samestage": True,
            "rng_pkitem": True,
            "rng_pkitem_ratio": 33,
            "rng_move_power": False,
            "rng_move_types": False,
            "rng_move_accuracy": False,
            "rng_move_pp": False,
            "rng_tm_moves": True,
            "rng_tutor_moves": True,
            "rng_trainers": True,
            "rng_trainers_cat_story": True,
            "rng_trainers_cat_mt_battle": True,
            "rng_trainers_cat_bingo": True,
            "rng_trainers_cat_battle_sim": True,
            "rng_trainers_cat_quick_battle": True,
            "rng_trainers_cat_colo_battle": True,
            "rng_trainers_unique_shadow": True,
            "rng_trainers_power_progression": True,
            "rng_trainers_level_up_only": False,
            "rng_trainers_item": True,
            "rng_trainers_item_ratio": 33,
            "rng_trade_wants": True,
            "rng_trade_offers": True,
            "rng_gifts": True,
            "rng_items": True,
            "rng_items_shuffle": False,
            "rng_items_berry_reroll": 1,
            "rng_items_random_qty": True,
            "rng_starters": True,
            "rng_starters_fixed": [],
            "rng_starters_max_bst": 500,
            "rng_pokespot": True,
            "rng_pokespot_improve_levels": True,
            "rng_pokespot_bst_based": True,
            "improve_catch_rate": True,
            "improve_catch_rate_minimum": 90,
            "patch_impossible_evolutions": True,
            "patch_early_tutors": True,
            "fix_name_casing": True
        }

    def configure(self, **kwargs):
        for argn, argv in kwargs.items():
            if argn in self._config and argv is not None:
                self._config[argn] = argv

        if self._config["rng_pktm_full_compat"]:
            self._config["rng_pktm_min_own_type_ratio"] = 100
            self._config["rng_pktm_min_other_type_ratio"] = 100
            self._config["rng_pktm_min_status_ratio"] = 100
            self._config["rng_pktm_min_normal_type_ratio"] = 100

        if self._config["rng_pktutor_full_compat"]:
            self._config["rng_pktutor_min_own_type_ratio"] = 100
            self._config["rng_pktutor_min_other_type_ratio"] = 100
            self._config["rng_pktutor_min_status_ratio"] = 100
            self._config["rng_pktutor_min_normal_type_ratio"] = 100

    def __getattr__(self, name):
        return self._config[name]


config = RandomizerConfig()
