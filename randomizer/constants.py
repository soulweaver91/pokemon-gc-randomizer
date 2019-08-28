#!/usr/bin/env python
# -*- coding: utf-8 -*-

from enum import Enum


class IsoGame(Enum):
    COLOSSEUM = 'Pokémon Colosseum'
    XD = 'Pokémon XD'


class IsoRegion(Enum):
    JPN = 'Japan'
    USA = 'USA'
    EUR = 'Europe'


BANNER_META_SIZE = 0x140
BANNER_META_FIRST_OFFSET = 0x1820
