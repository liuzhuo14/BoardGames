# Skull card is a card game that players find good cards (i.e., flower cards) and avoid bad cards (i.e., skull cards)
import numpy as np

class Player:
    def __init__(self, drop_strategy='default', turn_strategy='default',
                 card_strategy='random', challenge_strategy='random'):
        self.cards = [0,0,0,1] # 0 is flower, 1 is skull
        self.card_stack = []
        self.revealed = []
        self.n_success = 0
        self.drop_strategy = drop_strategy
        self.turn_strategy = turn_strategy
        self.card_strategy = card_strategy
        self.challenge_strategy = challenge_strategy
    
    def play_card(self, card=None):
        if card==None:
            if self.card_strategy=='random':
                card = np.random.choice(self.cards)
        self.cards.remove(card)
        self.card_stack.append(card)
    
    def take_back(self):
        self.cards.extend(self.card_stack)
        self.cards.extend(self.revealed)
        self.card_stack = []
        self.revealed = []
    
    def drop_card(self, card=None):
        if card==None:
            if self.drop_strategy=='default':
                card = 1 if len(self.cards)==2 else 0
        self.cards.remove(card)
        if len(self.cards)<=0:
            return True
        return False
    
    def reveal_card(self):
        card = self.card_stack.pop()
        self.revealed.append(card)
        return card
    
    def play_turn(self, price, n_table_cards):
        assert price >= 0
        
        if self.turn_strategy=='default':
            discount = 0.2 if 1 in self.card_stack else 1
            # default probs
            probs = np.arange(0.0,n_table_cards+1.0)
            if price==0 and len(self.cards)<=0: # can only bid
                probs[0] = 0.0
            else:
                probs[0] = 1.0
            
            probs[1:len(self.card_stack)+1] = 1.0
            reduce = 1.0/(n_table_cards+1-len(self.card_stack))
            for i in range(len(self.card_stack)+1, n_table_cards+1):
                probs[i] = probs[i-1]-reduce
            probs[1:] = probs[1:] * discount
            # bid less than price, will be 0
            probs[1:price+1] = 0
            # normalized
            probs = probs / probs.sum()
        
        action = np.random.choice(np.arange(0,n_table_cards+1), p=probs)
        
        return action


class Game:
    def __init__(self, n_player):
        self.n_player = n_player
    
    @property
    def n_player(self):
        return self._n_player
    
    @n_player.setter
    def n_player(self, n):
        assert type(n)==int, 'Please set an integer player number.'
        assert n <= 8, '%d players, too many.' % (n)
        assert n >= 3, '%d players, too few.' % (n)
        self._n_player = n
    
    def restart(self):
        self.players = {}
        for i in range(self.n_player):
            self.players[i] = Player()
        self.winner = -1
    
    def auto_run(self):
        self.restart()
        print('New Game start!')
        
        start_player = np.random.choice(self.n_player)
        Round = 1
        while self.winner == -1:
            print('Round %d. Remaining player and their cards:' % (Round))
            print('\t\t'+', '.join(['P'+str(pl)+': '+str(len(self.players[pl].cards)) for pl in self.players.keys()]))
            print('\tBidding start from P%d.' % start_player)
            n_table_cards = 0
            
            # each player play 1 card
            for i in self.players.keys():
                self.players[i].play_card()
                n_table_cards += 1
            
            # From start player, bidding, until the challenge begins
            current_player = start_player
            add_card = True
            price = 0
            challenge_player = -1
            n_pass = 0
            while True:
                action = self.players[current_player].play_turn(price, n_table_cards)
                if action == 0:
                    if add_card:
                        self.players[current_player].play_card()
                        n_table_cards += 1
                        print('\t\tP%d add card, current cards: %d.' % (current_player, n_table_cards))
                    else:
                        n_pass += 1
                        print('\t\tP%d pass.' % (current_player))
                else:
                    price = action
                    add_card = False
                    challenge_player = current_player
                    n_pass = 0
                    print('\t\tP%d bid %d cards.' % (current_player, action))
                # whether stop bidding
                if n_pass >= len(self.players)-1:
                    break
                # continue bidding
                while True:
                    current_player = (current_player+1) % self.n_player
                    if current_player in self.players.keys():
                        break
            
            # The challenge begins
            print('\tAll passed. P%d challenge begins!' % (challenge_player))
            print('\t\tNumber of cards for each player on table:')
            print('\t\t\t'+', '.join(['P'+str(pl)+': '+str(len(self.players[pl].card_stack)) for pl in self.players.keys()]))
            ch_st = self.players[challenge_player].challenge_strategy
            players_with_card_stack = list(self.players.keys())
            success = True
            while price > 0:
                if challenge_player in players_with_card_stack:
                    chosen_player = challenge_player
                else:
                    if ch_st == 'random':
                        chosen_player = np.random.choice(players_with_card_stack)
                
                reveal = self.players[chosen_player].reveal_card()
                print('\t\tReveal P%d card: %s' % (chosen_player, 'Skull!' if reveal==1 else 'Flower.'))
                if len(self.players[chosen_player].card_stack) == 0:
                    players_with_card_stack.remove(chosen_player)
                if reveal==1: # challenge fail
                    success = False
                    break
                price -= 1
            
            # take all card back
            for i in self.players:
                self.players[i].take_back()
            
            print('\tP%d, challenge %s' % (challenge_player, 'success!' if success else 'fail.'))
            # check challenge result
            if success:
                self.players[challenge_player].n_success += 1
                if self.players[challenge_player].n_success >= 2:
                    self.winner = challenge_player
            else:
                if self.players[challenge_player].drop_card():
                    del self.players[challenge_player]
                    print('\tP%d leave the game.' % (challenge_player))            
                if len(self.players)==1:
                    self.winner = self.players.keys[0]
            
            # next round
            if challenge_player in self.players:
                start_player = challenge_player
            else:
                start_player = np.random.choice(list(self.players.keys()))
            Round += 1
        
        print('Winner: P%d!' % (self.winner))
        return self.winner
    
    def is_exit(self, number):
        if number==-1 or number=='-1':
            print('Exit now.')
            result = True
        else:
            result = False
        return result
    
    def one_player(self):
        self.restart()
        print('New Game start!')
        # choose player number
        print('Choose your player ID: from 0 to %d' % (self.n_player-1))
        while True:
            real_player = input()
            try:
                real_player = int(real_player)
            except ValueError:
                print('Wrong, choose player ID in [0,%d]:' % (self.n_player-1))
            else:
                if self.is_exit(real_player):
                    return -1
                if real_player<0 or real_player>=self.n_player:
                    print('Wrong, choose player ID in [0,%d]:' % (self.n_player-1))
                else:
                    break

        assert real_player<self.n_player and real_player>=0, 'Error: Player ID should be in 0 to %d' % (self.n_player-1)
        print('You are P%d' % (real_player))
        
        start_player = np.random.choice(self.n_player)
        Round = 1
        while self.winner == -1:
            print('Round %d. Remaining player and their cards:' % (Round))
            print('\t\t'+', '.join(['P'+str(pl)+': '+str(len(self.players[pl].cards)) for pl in self.players.keys()]))
            skull_num = sum(self.players[real_player].cards)
            flower_num = len(self.players[real_player].cards) - skull_num
            print('\tYour cards: 0:%d, 1:%d, Your success: %d' % (flower_num, skull_num, self.players[real_player].n_success))
            n_table_cards = 0
            print('\tBidding will start from P%d.' % start_player)
            
            # each player play 1 card
            for i in self.players.keys():
                if real_player==i:
                    print('\tPlay one card to start (0:flower, 1:skull):')
                    while True:
                        your_card = input()
                        try:
                            your_card = int(your_card)
                        except ValueError:
                            print('\tWrong, play one card to start (0:flower, 1:skull):')
                        else:
                            if self.is_exit(your_card):
                                return -1
                            if your_card not in self.players[i].cards:
                                print('\tWrong, play an existing card:')
                            else:
                                break
                    self.players[i].play_card(your_card)
                else:
                    self.players[i].play_card()
                n_table_cards += 1
            
            # From start player, bidding, until the challenge begins
            current_player = start_player
            add_card = True
            price = 0
            challenge_player = -1
            n_pass = 0
            while True:
                if current_player==real_player:
                    available_actions = (['add','bid'] if len(self.players[current_player].cards)>0 else ['bid']) if add_card else (['pass','bid'] if price<n_table_cards else ['pass'])
                    print('\t\tChoose your action (%s):' % (', '.join(available_actions)))
                    while True:
                        action_text = input()
                        if self.is_exit(action_text):
                            return -1
                        if action_text not in available_actions:
                            print('\t\tWrong, choose available actions (%s):' % (', '.join(available_actions)))
                        else:
                            break
                        
                    if action_text=='add':
                        action = 0
                        skull_num = sum(self.players[real_player].cards)
                        flower_num = len(self.players[real_player].cards) - skull_num
                        print('\t\tAdd one card (0:flower, 1:skull) (your cards: 0:%d, 1:%d):' % (flower_num, skull_num))
                        while True:
                            your_card = input()
                            try:
                                your_card = int(your_card)
                            except ValueError:
                                print('\t\tWrong, add one card (0:flower, 1:skull):')
                            else:
                                if self.is_exit(your_card):
                                    return -1
                                if your_card not in self.players[i].cards:
                                    print('\t\tWrong, add existing card:')
                                else:
                                    break
                    elif action_text=='pass':
                        action = 0
                    elif action_text=='bid':
                        print('\t\tYour bid number (%d ~ %d):' % (price+1, n_table_cards))
                        while True:
                            action = input()
                            try:
                                action = int(action)
                            except ValueError:
                                print('\t\tWrong, choose your bid number (%d ~ %d)' % (price+1, n_table_cards))
                            else:
                                if self.is_exit(action):
                                    return -1
                                if action<=price or action>n_table_cards:
                                    print('\t\tWrong, should be in [%d,%d]:' % (price+1, n_table_cards))
                                else:
                                    break
                    else:
                        print()
                else:
                    action = self.players[current_player].play_turn(price, n_table_cards)
                
                if action == 0:
                    if add_card:
                        if current_player==real_player:
                            self.players[current_player].play_card(your_card)
                        else:
                            self.players[current_player].play_card()
                        n_table_cards += 1
                        print('\t\tP%d add card, current cards: %d.' % (current_player, n_table_cards))
                    else:
                        n_pass += 1
                        print('\t\tP%d pass.' % (current_player))
                else:
                    price = action
                    add_card = False
                    challenge_player = current_player
                    n_pass = 0
                    print('\t\tP%d bid %d cards.' % (current_player, action))
                # whether stop bidding
                if n_pass >= len(self.players)-1:
                    break
                # continue bidding
                while True:
                    current_player = (current_player+1) % self.n_player
                    if current_player in self.players.keys():
                        break
            
            # The challenge begins
            print('\tAll passed. P%d challenge begins!' % (challenge_player))
            print('\t\tNumber of cards for each player on table:')
            print('\t\t\t'+', '.join(['P'+str(pl)+': '+str(len(self.players[pl].card_stack)) for pl in self.players.keys()]))
            ch_st = self.players[challenge_player].challenge_strategy
            players_with_card_stack = list(self.players.keys())
            success = True
            while price > 0:
                if challenge_player in players_with_card_stack:
                    chosen_player = challenge_player
                else:
                    if challenge_player==real_player:
                        print('\t\tChoose one other player to reveal from', players_with_card_stack)
                        while True:
                            chosen_player = input()
                            try:
                                chosen_player = int(chosen_player)
                            except ValueError:
                                print('\t\tWrong, Choose from', players_with_card_stack)
                            else:
                                if self.is_exit(chosen_player):
                                    return -1
                                if chosen_player not in players_with_card_stack:
                                    print('\t\tWrong, not available player card stack')
                                else:
                                    break
                    else:
                        if ch_st == 'random':
                            chosen_player = np.random.choice(players_with_card_stack)
                
                reveal = self.players[chosen_player].reveal_card()
                print('\t\tReveal P%d card: %s' % (chosen_player, 'Skull!' if reveal==1 else 'Flower.'))
                if len(self.players[chosen_player].card_stack) == 0:
                    players_with_card_stack.remove(chosen_player)
                if reveal==1: # challenge fail
                    success = False
                    break
                price -= 1
            
            # take all card back
            for i in self.players:
                self.players[i].take_back()
            
            print('\tP%d, challenge %s' % (challenge_player, 'success!' if success else 'fail.'))
            # check challenge result
            if success:
                self.players[challenge_player].n_success += 1
                if self.players[challenge_player].n_success >= 2:
                    self.winner = challenge_player
            else:
                if challenge_player==real_player:
                    skull_num = sum(self.players[real_player].cards)
                    flower_num = len(self.players[real_player].cards) - skull_num
                    print('\t\tDrop one card (0:flower, 1:skull) (your cards: 0:%d, 1:%d):' % (flower_num, skull_num))
                    while True:
                        your_card = input()
                        try:
                            your_card = int(your_card)
                        except ValueError:
                            print('\t\tWrong, drop one card (0:flower, 1:skull):')
                        else:
                            if self.is_exit(your_card):
                                return -1
                            if your_card not in self.players[i].cards:
                                print('\t\tWrong, drop existing card:')
                            else:
                                break
                    leave = self.players[challenge_player].drop_card(your_card)
                else:
                    leave = self.players[challenge_player].drop_card()
                
                if leave:
                    del self.players[challenge_player]
                    print('\tP%d leave the game.' % (challenge_player))           
                if len(self.players)==1:
                    self.winner = list(self.players.keys())[0]
            
            # next round
            if challenge_player in self.players:
                start_player = challenge_player
            else:
                start_player = np.random.choice(list(self.players.keys()))
            Round += 1
        
        print('Winner: P%d!' % (self.winner))
        if self.winner==real_player:
            print('You win!')
        else:
            print('You lose!')
        return self.winner