# -*- coding: utf-8 -*-
"""
Created on Wed Oct 20 10:43:55 2021

@author: lzh02
"""

from enum import Enum, unique
from itertools import combinations

@unique
class HumanSpecies(Enum):
    Neanderthal = 0
    CroMagnon = 1
    Archaic = 2

@unique
class BoardSide(Enum):
    vowel = 0
    tribe = 1

@unique
class MorphemeColor(Enum):
    black = 0 # technology
    orange = 1 # social
    white = 2 # nature

@unique
class BoardColor(Enum):
    yellow = 0
    red = 1
    green = 2

@unique
class ElderName(Enum):
     craft = 0
     warrior = 1
     hunter = 2
     fire = 3
     husband = 4

@unique
class ElderState(Enum):
    none = 0
    novice = 1
    skilled = 2

@unique
class MarriageSystem(Enum):
    monogamy = 0
    polygamy = 1
    bipolygamy = 2

@unique
class Event(Enum):
    colder = 0
    hotter = 1
    death = 2
    storm = 3
    hit = 4
    wander = 5
    extend = 6

@unique
class DaughterName(Enum):

@unique
class Skill(Enum):

@unique
class PreyName(Enum):

@unique
class PreyType(Enum):
    
    
class Area:
    def __init__(self, color):
        self.color = color
        self.morphemes = {}
    def fill(self, color):
        self.morphemes.add(color)
    def isActivated(self):
        return len(self.morphemes) >= 3
    
class Portal:
    def __init__(self, colors):
        self.colors = colors
        self.waitingMorphemes = list(colors)
    def fill(self, color):
        if color in self.waitingMorphemes:
            self.waitingMorphemes.remove(color)
            return True
        return False
    def count(self):
        return len(self.colors) - len(self.waitingMorphemes)

class Brain:
    def __init__(self, species):
        self.areas = {color.value:Area(color) for color in MorphemeColor}
        self.portals = {colors[0].value+colors[1].value:Portal(colors) for colors in combinations(MorphemeColor, 2)}
        self.morphemeNumber = 0
        self.insert(species.value+(species.value+1)%3, MorphemeColor(species.value))
    def insert(self, portalId, morpheme):
        if self.portals[portalId].fill(morpheme):
            self.morphemeNumber += 1
            self.areas[portalId//2*2].fill(morpheme)
            self.areas[portalId%2].fill(morpheme)
            return True
        return False

class Elder:
    def __init__(self, name):
        self.name = name
        self.state = ElderState.none
    def occupy(self):
        if self.state == ElderState.none:
            self.state = ElderState.novice
            return True
        return False
    def train(self):
        if self.state == ElderState.novice:
            self.state = ElderState.skilled
            return True
        return False
    def kill(self):
        if self.state != ElderState.none:
            self.state = ElderState.none
            return True
        return False

class Board:
    def __init__(self, species):
        self.side = BoardSide.vowel
        self.species = species
        self.boardColor = BoardColor(species.value)
        self.brain = Brain(species)
        self.elders = {ElderName(i):Elder(ElderName(i)) for i in range(4)}
        self.raiseElder(ElderName.fire)
    def raiseElder(self, name):
        if name.value < 3:
            if self.brain.areas[MorphemeColor(name.value)].isActivated():
                return self.elders[name].occupy()
            return False
        else:
            return self.elders[name].occupy()
    def trainElder(self, name):
        return self.elders[name].train()
    def killElder(self, name):
        return self.elders[name].kill()
    def brainDevelop(self, portalId, morpheme):
        return self.brain.insert(portalId, morpheme)

class Daughter:
    def __init__(self, name):
        self.name = name
        self.events = eventMapping[name]
        self.portalColor = portalColorMapping[name]
        self.skill = skillMapping[name]
        self.availableMorpheme = availabelMorphemeMapping[name]
        self.growDuration = {color:0 for color in self.availableMorpheme}
        self.husband = Elder(ElderName.husband)

class Prey:
    def __init__(self, name):
        self.name = name
        self.preyType = preyTypeMapping[name]
        self.adaptation = name.value
        self.freeze = freezeMapping[name]
        self.condition = conditionMapping[name]

class Player:
    def __init__(self, playerName, species, marriage):
        self.playerName = playerName
        self.species = species
        self.marriage = marriage
        self.board = Board(species)
        self.morphemes = {color:5-marriage.value for color in MorphemeColor} # initial for marriage system
        self.morphemes[MorphemeColor.black] -= 1 # initial for fire elder
        self.morphemes[MorphemeColor(species.value)] -= 1 # initial in brain
        self.members = 6
        self.fighter = 0
        self.elders = 1 # initial for fire
        self.gathering = True if marriage==MarriageSystem.bipolygamy else False
    
