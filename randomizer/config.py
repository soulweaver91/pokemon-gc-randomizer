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
            "rng_pkstats_wg_1hp": True,
            "rng_pktypes": True,
            "rng_pktypes_family": True,
            "rng_pktypes_family_change_ratio": 33,
            "rng_pktypes_monotype_ratio": 33,
            "rng_pkabi": True,
            "rng_pkabi_family": True,
            "rng_pkabi_family_change_ratio": 33,
            "rng_pkabi_monoabi_ratio": 33,
            "rng_pkabi_ban": ['WONDER_GUARD', 'FORECAST'],
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
