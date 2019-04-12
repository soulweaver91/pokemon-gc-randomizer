#!/usr/bin/env python
# -*- coding: utf-8 -*-

from .constants import Move, EvolutionType, PokemonSpecies, Item


class StatSet:
    def __init__(self, hp, attack, defense, sp_attack, sp_defense, speed):
        self.hp = hp
        self.attack = attack
        self.defense = defense
        self.sp_attack = sp_attack
        self.sp_defense = sp_defense
        self.speed = speed

    def __str__(self):
        return '%d/%d/%d/%d/%d/%d' % (self.hp, self.attack, self.defense,
                                                self.sp_attack, self.sp_defense, self.speed)

    @property
    def total(self):
        return self.hp + self.attack + self.defense + self.sp_attack + self.sp_defense + self.speed


class EvoEntry:
    def __init__(self, type, unknown1, level_or_item, evolves_to):
        self.type = EvolutionType(type)
        self.unknown1 = unknown1
        self.level = level_or_item
        self.item = Item(level_or_item)
        self.evolves_to = PokemonSpecies(evolves_to)

    def __str__(self):
        evo_specifier = ''
        if self.type.param_is_level:
            evo_specifier = 'at level %d ' % self.level
        if self.type.param_is_item:
            evo_specifier = 'with item %s ' % self.item.name

        return 'Evolution to %s %s(%s)' % (PokemonSpecies(self.evolves_to).name, evo_specifier, self.type.name)


class LevelUpMoveEntry:
    def __init__(self, level, unknown1, move):
        self.level = level
        self.unknown1 = unknown1
        self.move = Move(move)

    def __str__(self):
        return '%s at level %d' % (self.move.name, self.level)
