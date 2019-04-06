#!/usr/bin/env python
# -*- coding: utf-8 -*-

from .constants import IsoRegion, IsoGame


def interpret_game_kind(code):
    if code == b'C6':
        return IsoGame.COLOSSEUM
    elif code == b'XX':
        return IsoGame.XD
    else:
        return None


def interpret_game_region(region):
    if region == b'J':
        return IsoRegion.JPN
    elif region == b'E':
        return IsoRegion.USA
    elif region == b'P':
        return IsoRegion.EUR
    else:
        return None


def interpret_game_code(code):
    if len(code) != 4:
        return None, None

    console = code[0:1]
    game = code[1:3]
    region = code[3:4]

    if console != b'G':
        return None, None

    game = interpret_game_kind(game)
    region = interpret_game_region(region)

    if game is None or region is None:
        return None, None

    return game, region


def chunked(size, source):
    for i in range(0, len(source), size):
        yield source[i:i + size]
