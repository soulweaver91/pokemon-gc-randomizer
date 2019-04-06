#!/usr/bin/env python
# -*- coding: utf-8 -*-

from .constants import Move, EvolutionType, PokemonSpecies


class StatSet:
    def __init__(self, hp, attack, defense, sp_attack, sp_defense, speed):
        self.hp = hp
        self.attack = attack
        self.defense = defense
        self.sp_attack = sp_attack
        self.sp_defense = sp_defense
        self.speed = speed

    @property
    def total(self):
        return self.hp + self.attack + self.defense + self.sp_attack + self.sp_defense + self.speed


class EvoEntry:
    def __init__(self, type, unknown1, level_or_item, evolves_to):
        self.type = EvolutionType(type)
        self.unknown1 = unknown1
        self.level = level_or_item
        self.item = level_or_item
        self.evolves_to = PokemonSpecies(evolves_to)


class LevelUpMoveEntry:
    def __init__(self, level, unknown1, move):
        self.level = level
        self.unknown1 = unknown1
        self.move = Move.from_idx(move)
