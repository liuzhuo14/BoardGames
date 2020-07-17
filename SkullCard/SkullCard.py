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
    
    def play_card(self):
        if self.card_strategy=='random':
            card = np.random.choice(self.cards)
        self.cards.remove(card)
        self.card_stack.append(card)
    
    def take_back(self):
        self.cards.extend(self.card_stack)
        self.cards.extend(self.revealed)
        self.card_stack = []
        self.revealed = []
    
    def drop_card(self):
        if self.drop_strategy=='default':
            card = 1 if len(self.cards)==2 else 0
        self.cards.remove(card)
        if len(self.cards)<=0:
            return 1
        return 0
    
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
            print('\tBidding start from Player %d.' % start_player)
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
                        print('\t\tPlayer %d add card, current cards: %d.' % (current_player, n_table_cards))
                    else:
                        n_pass += 1
                        print('\t\tPlayer %d pass.' % (current_player))
                else:
                    price = action
                    add_card = False
                    challenge_player = current_player
                    n_pass = 0
                    print('\t\tPlayer %d bid %d cards.' % (current_player, action))
                # whether stop bidding
                if n_pass >= len(self.players)-1:
                    break
                # continue bidding
                while True:
                    current_player = (current_player+1) % self.n_player
                    if current_player in self.players.keys():
                        break
            
            # The challenge begins
            print('\tAll passed. Player %d challenge begins!' % (challenge_player))
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
                print('\t\tReveal player %d card: %s' % (chosen_player, 'Skull!' if reveal==1 else 'Flower.'))
                if len(self.players[chosen_player].card_stack) == 0:
                    players_with_card_stack.remove(chosen_player)
                if reveal==1: # challenge fail
                    success = False
                    break
                price -= 1
            
            # take all card back
            for i in self.players:
                self.players[i].take_back()
            
            print('\tPlayer %d, challenge %s' % (challenge_player, 'success!' if success else 'fail.'))
            # check challenge result
            if success:
                self.players[challenge_player].n_success += 1
                if self.players[challenge_player].n_success >= 2:
                    self.winner = challenge_player
            else:
                if self.players[challenge_player].drop_card():
                    del self.players[challenge_player]
                    print('\tPlayer %d leave the game.' % (challenge_player))            
                if len(self.players)==1:
                    self.winner = self.players.keys[0]
            
            # next round
            if challenge_player in self.players:
                start_player = challenge_player
            else:
                start_player = np.random.choice(list(self.players.keys()))
            Round += 1
        
        print('Winner: Player %d!' % (self.winner))