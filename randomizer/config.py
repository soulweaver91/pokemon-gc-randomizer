#!/usr/bin/env python
# -*- coding: utf-8 -*-


class RandomizerConfig:
    def __init__(self):
        self._config = {
            "working_dir": None,
            "dump_files": False,
            "randomize_types": True,
            "randomize_abilities": True,
        }

    def configure(self, **kwargs):
        for argn, argv in kwargs.items():
            if argn in self._config:
                self._config[argn] = argv
        pass

    def __getattr__(self, name):
        return self._config[name]


config = RandomizerConfig()
