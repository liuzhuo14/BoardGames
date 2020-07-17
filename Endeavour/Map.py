# -*- coding: utf-8 -*-
import random
import math

class font:
    END = '\033[0m'
    ITA = '\x1B[3m'
    UNL = '\033[4m'

class Action:
    SAIL = 0
    OCCUPY = 1
    OBTAIN = 2
    ATTACK = 3
    PAY = 4
    def __init__(self, actions, actionNum):
        self.actionNum = actionNum
        self.actions = actions

class Resource:
    PRODUCT = 0
    CIVIL = 1
    MONEY = 2
    INFLU = 3
    GLORY = 4
    @staticmethod
    def resourceClass(x, types):
        if types==Resource.PRODUCT:
            result = 1
        elif types==Resource.CIVIL:
            result = 2
        elif types==Resource.MONEY:
            result = 1
        elif types==Resource.INFLU:
            result = 1
        
        if x>=2:
            result += 1
        if x>=4:
            result += 1
        if x>=7:
            result += 1
        if x>=10:
            result += 1
        return result

class Token:
    ACTION = 0
    RESOURCE = 1
    def __init__(self, types, values):
        self.types = types
        self.values = values

class TokenStore:
    def __init__(self):
        self.tokenList = []
        self.tokenList.extend([Token(Token.ACTION, [Action.ATTACK]) for i in range(2)])
        self.tokenList.extend([Token(Token.ACTION, [Action.PAY]) for i in range(2)])
        self.tokenList.extend([Token(Token.ACTION, [Action.SAIL,Action.OBTAIN]) for i in range(6)])
        self.tokenList.extend([Token(Token.ACTION, [Action.OCCUPY,Action.OBTAIN]) for i in range(6)])
        self.tokenList.extend([Token(Token.RESOURCE, [Resource.PRODUCT]) for i in range(17)])
        self.tokenList.extend([Token(Token.RESOURCE, [Resource.CIVIL]) for i in range(20)])
        self.tokenList.extend([Token(Token.RESOURCE, [Resource.MONEY]) for i in range(17)])
        self.tokenList.extend([Token(Token.RESOURCE, [Resource.INFLU]) for i in range(25)])
    
    def draw(self):
        if len(self.tokenList) <= 0:
            return None
        random.shuffle(self.tokenList)
        token = random.choice(self.tokenList)
        self.tokenList.remove(token)
        return token

class Position:
    VACANCY = 0
    HASTOKEN = 1
    OCCUPY = 2

class Card:
    def __init__(self, resource, governor, minion, presence, area):
        self.area = area
        self.resource = resource
        self.governor = governor
        self.minion = minion
        self.presence = presence

class Pool:
    def __init__(self, name):
        self.name = name
        self.area = Area.EUROPE if self.name==Area.SLAVE else self.name
        self.top = 0 if self.name==Area.EUROPE or self.name==Area.SLAVE else 1
        self.slot = []
        # Card(product,civil,money,influ,glory,governor,minion,presence)
        if self.name==Area.EUROPE:
            self.slot.append(Card([0,1,1,0,0],False,0,0,Area.EUROPE))
            self.slot.append(Card([0,2,0,1,0],False,0,1,Area.EUROPE))
            self.slot.append(Card([0,1,0,2,0],False,0,2,Area.EUROPE))
            self.slot.append(Card([1,1,1,1,0],False,0,3,Area.EUROPE))
            self.slot.append(Card([0,0,0,0,5],False,0,4,Area.EUROPE))
            self.slot.append(Card([0,3,0,0,3],False,0,5,Area.EUROPE))
        elif self.name==Area.SLAVE:
            self.slot.append(Card([2,0,1,0,0],False,0,0,Area.SLAVE))
            self.slot.append(Card([1,0,2,0,0],False,0,1,Area.SLAVE))
            self.slot.append(Card([3,0,0,0,0],False,0,2,Area.SLAVE))
            self.slot.append(Card([2,0,2,0,0],False,0,3,Area.SLAVE))
            self.slot.append(Card([2,0,2,0,0],False,0,4,Area.SLAVE))
            self.slot.append(Card([2,0,3,0,0],False,0,5,Area.SLAVE))
        elif self.name==Area.FAREAST:
            self.slot.append(Card([2,1,0,0,1],True,0,0,Area.FAREAST))
            self.slot.append(Card([1,0,1,0,0],False,1,1,Area.FAREAST))
            self.slot.append(Card([2,0,1,0,0],False,0,2,Area.FAREAST))
            self.slot.append(Card([2,0,2,0,0],False,0,3,Area.FAREAST))
            self.slot.append(Card([1,1,1,1,1],False,0,4,Area.FAREAST))
            self.slot.append(Card([0,0,0,3,3],False,0,5,Area.FAREAST))
        elif self.name==Area.INDIA:
            self.slot.append(Card([0,1,1,1,1],True,0,0,Area.INDIA))
            self.slot.append(Card([0,1,0,1,0],False,1,1,Area.INDIA))
            self.slot.append(Card([0,1,1,1,0],False,0,2,Area.INDIA))
            self.slot.append(Card([0,1,2,1,0],False,0,3,Area.INDIA))
            self.slot.append(Card([0,0,2,1,2],False,0,4,Area.INDIA))
            self.slot.append(Card([0,0,2,2,2],False,0,5,Area.INDIA))
        elif self.name==Area.NORTHAM:
            self.slot.append(Card([0,0,1,2,1],True,0,0,Area.NORTHAM))
            self.slot.append(Card([2,0,0,0,0],False,1,1,Area.NORTHAM))
            self.slot.append(Card([0,0,3,0,0],False,0,2,Area.NORTHAM))
            self.slot.append(Card([2,2,0,0,0],False,0,3,Area.NORTHAM))
            self.slot.append(Card([0,2,0,2,1],False,0,4,Area.NORTHAM))
            self.slot.append(Card([0,0,0,0,6],False,0,5,Area.NORTHAM))
        elif self.name==Area.CARIBBEAN:
            self.slot.append(Card([0,2,0,1,1],True,0,0,Area.CARIBBEAN))
            self.slot.append(Card([0,0,2,0,0],False,1,1,Area.CARIBBEAN))
            self.slot.append(Card([0,0,1,0,2],False,0,2,Area.CARIBBEAN))
            self.slot.append(Card([0,0,4,0,0],False,0,3,Area.CARIBBEAN))
            self.slot.append(Card([0,0,0,3,2],False,0,4,Area.CARIBBEAN))
            self.slot.append(Card([3,0,0,0,3],False,0,5,Area.CARIBBEAN))
        elif self.name==Area.SOUTHAM:
            self.slot.append(Card([0,0,0,3,1],True,0,0,Area.SOUTHAM))
            self.slot.append(Card([0,2,0,0,0],False,1,1,Area.SOUTHAM))
            self.slot.append(Card([0,3,0,0,0],False,0,2,Area.SOUTHAM))
            self.slot.append(Card([0,4,0,0,0],False,0,3,Area.SOUTHAM))
            self.slot.append(Card([0,0,3,0,2],False,0,4,Area.SOUTHAM))
            self.slot.append(Card([0,0,3,0,3],False,0,5,Area.SOUTHAM))
        elif self.name==Area.AFRICA:
            self.slot.append(Card([0,0,2,1,1],True,0,0,Area.AFRICA))
            self.slot.append(Card([1,0,0,1,0],False,1,1,Area.AFRICA))
            self.slot.append(Card([1,0,1,1,0],False,0,2,Area.AFRICA))
            self.slot.append(Card([0,0,2,2,0],False,0,3,Area.AFRICA))
            self.slot.append(Card([2,0,1,1,1],False,0,4,Area.AFRICA))
            self.slot.append(Card([2,0,2,0,2],False,0,5,Area.AFRICA))
    
    def draw(self):
        if self.top>=6:
            return None
        card = self.slot[self.top]
        self.top += 1
        return card
    
    def govern(self):
        if self.area==Area.EUROPE:
            return None
        return self.slot[0]

class DiscardPool(Pool):
    def __init__(self):
        self.area = Area.EUROPE
        self.slot = []
    
    def showAll(self):
        return self.slot
    
    def draw(self, select):
        if select >= len(self.slot):
            return None
        card = self.slot[select]
        self.slot.remove(card)
        return card
        

class Area:
    EUROPE = 0
    FAREAST = 1
    INDIA = 2
    NORTHAM = 3
    CARIBBEAN = 4
    SOUTHAM = 5
    AFRICA = 6
    SLAVE = 7
    def __init__(self, name, holds, tokenStore, channelSize):
        self.name = name
        self.open = True if self.name==Area.EUROPE else False
        self.channel = Channel(tokenStore, channelSize)
        self.openSea = {} # dicts
        self.pool = Pool(self.name)
        self.holds = holds # dicts

class Join:
    def __init__(self, hold1, hold2, tokenStore, isToken):
        self.hold1 = hold1
        self.hold2 = hold2
        self.glory = 1
        if isToken==True:
            self.token = tokenStore.draw()
        else:
            self.token = None

class Hold:
    CITY = 0
    FLEET = 1
    def __init__(self, name, tokenStore, types, glory):
        self.name = name
        self.owner = None
        self.state = Position.HASTOKEN
        self.glory = glory
        self.token = tokenStore.draw()
    
    def changeOwner(self, playerName):
        returnThing = (self.owner, self.token)
        self.owner = playerName
        self.state = Position.OCCUPY
        self.token = None
        return returnThing

class Channel:
    def __init__(self, tokenStore, size):
        self.positionList = []
        self.tokenList = [tokenStore.draw() for i in range(size)]
        self.size = size
    
    def put(self, playerName):
        position = len(self.positionList)
        if position >= self.size:
            return None
        token = self.tokenList[position]
        self.positionList.append(playerName)
        return token
    
    def govern(self):
        if len(self.positionList) < self.size:
            return None
        counter = {i:self.positionList.count(i) for i in set(self.positionList)}
        maxp = 0
        for i in self.positionList:
            if counter[i] >= maxp: # the last max player
                maxp = counter[i]
                governor = i
        return governor

class BuildingRule:
    CannotPayAtActionPhase = 0
    WarDeadBecomesResource = 1
    ActionObtainToGlory = 2

class Building:
    COLONIALHOUSE = 0
    MERCHANTDOCK = 1
    # level 1
    MARKET = 2
    SHIPYARD = 3
    WORKSHOP = 4
    # level 2
    BANK = 5
    BARRACKS = 6
    GUILDHALL = 7
    # level 3
    FORTRESS = 8
    DOCKS = 9
    THEATRE = 10
    # level 4
    CARTOGRAPHER = 11
    UNIVERSITY = 12
    TRADEOFFICE = 13
    # level 5
    TREASURY = 14
    EXCHANGE = 15
    MEMROIAL = 16
    MUSEUM = 17
    CITYHALL = 18
    PALACE = 19
    PARLIAMENT = 20
    
    def setup(self, resource, action, classes, buildingRule):
        self.resource = resource
        self.action = action
        self.classes = classes
        self.buildingRule = buildingRule
        
    def __init__(self, name):
        self.name = name
        # different buildings
        if self.name==Building.COLONIALHOUSE:
            self.setup([0,0,0,0,0],Action([Action.OCCUPY],1),0,None)
        elif self.name==Building.MERCHANTDOCK:
            self.setup([0,0,1,0,0],Action([Action.SAIL],1),0,None)
        elif self.name==Building.MARKET:
            self.setup([0,0,0,0,0],Action([Action.OBTAIN],1),1,None)
        elif self.name==Building.SHIPYARD:
            self.setup([0,1,0,0,0],Action([Action.SAIL],1),1,None)
        elif self.name==Building.WORKSHOP:
            self.setup([2,0,0,0,0],None,1,None)
        elif self.name==Building.BANK:
            self.setup([0,0,2,0,0],None,2,None)
        elif self.name==Building.BARRACKS:
            self.setup([0,0,0,0,0],Action([Action.ATTACK],1),2,None)
        elif self.name==Building.GUILDHALL:
            self.setup([0,0,0,0,0],Action([Action.OBTAIN,Action.SAIL],1),2,None)
        elif self.name==Building.FORTRESS:
            self.setup([0,0,0,1,0],Action([Action.OCCUPY,Action.ATTACK],1),3,None)
        elif self.name==Building.DOCKS:
            self.setup([0,0,0,0,0],Action([Action.SAIL,Action.OCCUPY],2),3,None)
        elif self.name==Building.THEATRE:
            self.setup([0,2,0,0,0],None,3,None)
        elif self.name==Building.CARTOGRAPHER:
            self.setup([0,0,0,0,0],Action([Action.SAIL,Action.SAIL],2),4,None)
        elif self.name==Building.UNIVERSITY:
            self.setup([0,0,0,0,3],None,4,None)
        elif self.name==Building.TRADEOFFICE:
            self.setup([0,0,0,0,0],Action([Action.OBTAIN,Action.OBTAIN],2),4,None)
        elif self.name==Building.TREASURY:
            self.setup([0,0,0,0,2],Action([Action.PAY,Action.PAY],2),5,BuildingRule.CannotPayAtActionPhase)
        elif self.name==Building.EXCHANGE:
            self.setup([0,0,2,0,0],Action([Action.PAY],1),5,BuildingRule.CannotPayAtActionPhase)
        elif self.name==Building.MEMORIAL:
            self.setup([0,0,0,0,0],Action([Action.SAIL,Action.ATTACK],1),5,BuildingRule.WarDeadBecomesResource)
        elif self.name==Building.MUSEUM:
            self.setup([0,2,0,0,0],Action([Action.PAY],1),5,BuildingRule.CannotPayAtActionPhase)
        elif self.name==Building.CITYHALL:
            self.setup([0,0,0,0,0],Action([Action.OCCUPY,Action.OBTAIN],1),5,BuildingRule.ActionObtainToGlory)
        elif self.name==Building.PALACE:
            self.setup([1,1,1,1,0],None,5,None)
        elif self.name==Building.PARLIAMENT:
            self.setup([0,0,0,2,0],Action(1,),5,BuildingRule.CannotPayAtActionPhase)
        
        # start building station is filled
        self._station = 1 if self.classes==0 else 0 # 0 empty, 1 fill
        
        @property
        def station(self):
            return self._station
        
        @station.setter
        def station(self, value):
            if not isinstance(value, int):
                raise ValueError('station must be an integer 0/1')
            if value != 0 and value != 1:
                raise ValueError('station must be 0/1')
            self._station = value

class Player:
    RED = 0
    BLUE = 1
    YELLOW= 2
    WHITE = 3
    PURPLE = 4
    def __init__(self, name):
        self.name = name
        self.manpower = 35
        self.resource = [0,0,0,0,0] # product, civil, money, influ, glory
        self.resourceToken = []
        self.buildings = []
        self.cards = []
        self.actionToken = []
        self.minions = 0
        self.availableAction = []
    
    def startSetting(self, startBuilding):
        building = Building(startBuilding) # choose start building
        self.buildings.append(building) # add the building
        self.resource = [i+j for i,j in zip(self.resource, building.resource)] # add resource of building
        self.manpower -= 1 # start building has a minion on it
    
    def prepare(self, newBuilding, payBuildingIndex):
        # build
        building = Building(newBuilding) # choose start building
        self.buildings.append(building) # add the building
        self.resource = [i+j for i,j in zip(self.resource, building.resource)] # add resource of building
        # payment
        for b in payBuildingIndex:
            if self.buildings[b].station == 1:
                self.buildings[b].station = 0
                self.minions += 1
        # add minions
        addNum = Resource.resourceClass(self.resource[Resource.CIVIL], Resource.CIVIL)
        self.minions += addNum
        self.manpower -= addNum
     
    def place(self, tokens):
        if self.minions < 1:
            return False
        self.minions -= 1
        if tokens != None:
            for token in tokens:
                if token.types == Token.RESOURCE:
                    self.resource[token.values[0]] += 1
                    self.resourceToken.append(token)
                else:
                    self.availableAction.append(Action(token.values,1))
                    self.actionToken.append(token)
        return True
    
    def work(self, buildingIndex):
        if self.buildings[buildingIndex].station==1 \
        or self.minions<1 \
        or self.buildings[buildingIndex].action==None:
            return None
        self.buildings[buildingIndex].station = 1
        self.minions -= 1
        return self.buildings[buildingIndex].action
    
    def kill(self):
        if self.minions < 1:
            return False
        self.minions -= 1
        self.manpower += 1
        return True
    
    def obtain(self, card):
        self.cards.append(card)
        self.resource = [i+j for i,j in zip(self.resource, card.resource)]
        
    def pay(self, buildingIndex):
        if self.buildings[buildingIndex].buildingRule==BuildingRule.CannotPayAtActionPhase \
        or self.buildings[buildingIndex].station==0:
            return False
        self.buildings[buildingIndex].station = 0
        self.minions += 1
        return True
        
    def chooseDiscard(self):
        cardLimit = Resource.resourceClass(self.resource[Resource.INFLU], Resource.INFLU)
        slaveLimit = 0 if self.resource[Resource.INFLU]>=10 else 1
        if len(self.cards) <= cardLimit:
            return None
        slaveNum = 0
        for card in self.cards:
            if card.area==Area.SLAVE:
                slaveNum += 1
        if slaveNum>=slaveLimit and len(self.cards)<cardLimit+slaveLimit:
            return None
        return (cardLimit, slaveLimit)

class Map:
    def __init__(self, side):
        self.side = side
        tokenStore = TokenStore()
        if self.side=='A':
            self.areas = []
        elif self.side=='B':
            # Areas
            self.areas = []
            # Europe
            holds = {}
            holds['Norwegian'] = Hold('Norwegian', tokenStore, Hold.FLEET, 0)
            holds['Atlantic'] = Hold('Atlantic', tokenStore, Hold.FLEET, 0)
            holds['Biscay'] = Hold('Biscay', tokenStore, Hold.FLEET, 0)
            holds['Gibraltar'] = Hold('Gibraltar', tokenStore, Hold.FLEET, 0)
            holds['London'] = Hold('London', tokenStore, Hold.CITY, 1)
            holds['Bilbao'] = Hold('Bilbao', tokenStore, Hold.CITY, 1)
            holds['Barcelona'] = Hold('Barcelona', tokenStore, Hold.CITY, 1)
            holds['Hamburg'] = Hold('Hamburg', tokenStore, Hold.CITY, 1)
            holds['Dunkirk'] = Hold('Dunkirk', tokenStore, Hold.CITY, 1)
            holds['Rome'] = Hold('Rome', tokenStore, Hold.CITY, 1)
            holds['Gdansk'] = Hold('Gdansk', tokenStore, Hold.CITY, 1)
            holds['Thessaloniki'] = Hold('Thessaloniki', tokenStore, Hold.CITY, 1)
            self.areas.append(Area(Area.EUROPE, holds, tokenStore, 0))
            # Far East
            holds = {}
            holds['Indonesia'] = Hold('Indonesia', tokenStore, Hold.CITY, 1)
            holds['Thailand'] = Hold('Thailand', tokenStore, Hold.CITY, 1)
            holds['Japan'] = Hold('Japan', tokenStore, Hold.CITY, 2)
            holds['Philippines'] = Hold('Philippines', tokenStore, Hold.CITY, 1)
            self.areas.append(Area(Area.FAREAST, holds, tokenStore, 7))
            # India
            holds = {}
            holds['Bengal'] = Hold('Bengal', tokenStore, Hold.CITY, 1)
            holds['Delhi'] = Hold('Delhi', tokenStore, Hold.CITY, 2)
            holds['Mumbai'] = Hold('Mumbai', tokenStore, Hold.CITY, 1)
            holds['Srilanka'] = Hold('Srilanka', tokenStore, Hold.CITY, 1)
            self.areas.append(Area(Area.INDIA, holds, tokenStore, 7))
            # North America
            holds = {}
            holds['Boston'] = Hold('Boston', tokenStore, Hold.CITY, 1)
            holds['Newyork'] = Hold('Newyork', tokenStore, Hold.CITY, 1)
            holds['Houston'] = Hold('Houston', tokenStore, Hold.CITY, 1)
            holds['Mexico'] = Hold('Mexico', tokenStore, Hold.CITY, 2)
            self.areas.append(Area(Area.NORTHAM, holds, tokenStore, 7)) 
            # Caribbean
            holds = {}
            holds['Bahamas'] = Hold('Bahamas', tokenStore, Hold.CITY, 1)
            holds['Cuba'] = Hold('Cuba', tokenStore, Hold.CITY, 1)
            holds['Haiti'] = Hold('Haiti', tokenStore, Hold.CITY, 1)
            holds['Puertorico'] = Hold('Puertorico', tokenStore, Hold.CITY, 1)
            self.areas.append(Area(Area.CARIBBEAN, holds, tokenStore, 6))
            # South America
            holds = {}
            holds['Peru'] = Hold('Peru', tokenStore, Hold.CITY, 2)
            holds['Guyana'] = Hold('Guyana', tokenStore, Hold.CITY, 1)
            holds['Brazil'] = Hold('Brazil', tokenStore, Hold.CITY, 1)
            holds['Uruguay'] = Hold('Uruguay', tokenStore, Hold.CITY, 1)
            self.areas.append(Area(Area.SOUTHAM, holds, tokenStore, 6))
            # Africa
            holds = {}
            holds['Kenya'] = Hold('Kenya', tokenStore, Hold.CITY, 1)
            holds['Mozambique'] = Hold('Mozambique', tokenStore, Hold.CITY, 1)
            holds['Namibia'] = Hold('Namibia', tokenStore, Hold.CITY, 1)
            holds['Ghana'] = Hold('Ghana', tokenStore, Hold.CITY, 1)
            self.areas.append(Area(Area.AFRICA, holds, tokenStore, 6))
            
            # Joins
            self.joins = []
            # Europe
            self.joins.append(Join('Norwegian','Hamburg',tokenStore,False))
            self.joins.append(Join('Atlantic','London',tokenStore,False))
            self.joins.append(Join('London','Hamburg',tokenStore,False))
            self.joins.append(Join('Hamburg','Dunkirk',tokenStore,False))
            self.joins.append(Join('Bilbao','Dunkirk',tokenStore,False))
            self.joins.append(Join('Dunkirk','Rome',tokenStore,False))
            self.joins.append(Join('Rome','Gdansk',tokenStore,False))
            self.joins.append(Join('Biscay','Bilbao',tokenStore,False))
            self.joins.append(Join('Dunkirk','Barcelona',tokenStore,False))
            self.joins.append(Join('Barcelona','Rome',tokenStore,False))
            self.joins.append(Join('Gibraltar','Barcelona',tokenStore,False))
            # Europe to others
            self.joins.append(Join('Gdansk','Philippines',tokenStore,True))
            self.joins.append(Join('Norwegian','Indonesia',tokenStore,True))
            self.joins.append(Join('Norwegian','Srilanka',tokenStore,True))
            self.joins.append(Join('Atlantic','Newyork',tokenStore,True))
            self.joins.append(Join('Atlantic','Bahamas',tokenStore,True))
            self.joins.append(Join('Biscay','Haiti',tokenStore,True))
            self.joins.append(Join('Biscay','Guyana',tokenStore,True))
            self.joins.append(Join('Gibraltar','Brazil',tokenStore,True))
            self.joins.append(Join('Gibraltar','Ghana',tokenStore,True))
            self.joins.append(Join('Barcelona','Namibia',tokenStore,True))
            self.joins.append(Join('Thessaloniki','Kenya',tokenStore,True))
            # Far East
            self.joins.append(Join('Thailand','Philippines',tokenStore,True))
            # India
            self.joins.append(Join('Bengal','Mumbai',tokenStore,True))
            self.joins.append(Join('Bengal','Srilanka',tokenStore,True))
            # North America
            self.joins.append(Join('Boston','Houston',tokenStore,True))
            # Caribbean
            self.joins.append(Join('Bahamas','Cuba',tokenStore,True))
            self.joins.append(Join('Haiti','Puertorico',tokenStore,True))
            # North America and Caribbean
            self.joins.append(Join('Houston','Cuba',tokenStore,True))
            # South America
            self.joins.append(Join('Guyana','Uruguay',tokenStore,True))
            # Africa
            self.joins.append(Join('Kenya','Mozambique',tokenStore,True))
            
            # other 2 pools
            self.slavePool = Pool(Area.SLAVE)
            self.discardPool = DiscardPool()
            
            # Buildings
            self.buildingPool = {}
            for building in range(2,14):
                self.buildingPool[building] = 5-math.floor((building-2)/3)
            for building in random.sample(range(14,21), 3):
                self.buildingPool[building] = 1
    
class Game: 
    def __init__(self):
        self.turn = 0
        
        print('Please input the number of players [2-5]:')
        self.playerNum = int(input())
        if self.playerNum < 4:
            mapSide = 'A'
        elif self.playerNum > 4:
            mapSide = 'B'
        else:
            print('Please choose your game map side [A, B]:')
            mapSide = input()
        self.maps = Map(mapSide)
        print('%d players join the game! Your map is on side %s.' % (self.playerNum, mapSide))
        
        self.players = {}
        for i in range(self.playerNum):
            self.players[i] = Player(i)
            print('Player %d: Choose your start building [Colonial House: 0, Merchant Dock: 1]:' % (i))
            self.players[i].startSetting(int(input()))
        self.startPlayer = random.choice(range(self.playerNum))
        print('The game is ready to start from Player %d' % (self.startPlayer))
        print('run '+font.ITA+'[your game object].start()'+font.END+' to start')
    
    def start(self):
        if self.turn > 7:
            print('Game end.')
            scoring()
        else:
        
    def save(self, path):
    def load(self, path):
    def isFinish(self):
    def scoring(self):