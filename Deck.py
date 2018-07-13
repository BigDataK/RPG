class Deck():
    '''
    Deck contains all information about a deck of cards
    
    '''    
    def __init__(self, name='English', suits=['Diamonds', 'Clubs', 'Hearts', 'Spades'],\
                 value_list=['Ace', '2', '3', '4', '5', '6', '7', '8', '9', '10', 'Jack', 'Queen', 'King'],\
                 arcana=['Joker', 'Joker'], suit_ranking=False, other_data=''):
        '''
        This initialises a deck of cards. In the default, a standard English pattern 52-card deck is generated with two Jokers.
        The arcana are the uncategorised extra cards that do not have suits; in this case, the Jokers. They are enumerated individually
        by name. Value of a card is equal to its position in the values list plus one. 
        If Ace is high, Ace should be identified as a high or trump card.
        Suits may also have relative strength if suit_ranking is set to True, which is why the cards are created value by value rather than suit by suit. 
        In this example, spades would have the highest value suit as per certain variations of the climbing game, President (aka Asshole).
        This means that a card's absolute value relative to other cards is exactly its position in the deck_holder if suit_ranking is True.
        
        name: a name you assign the deck
        
        suits: a list of suits, defaults to ['Diamonds', 'Clubs', 'Hearts', 'Spades'] of the English pattern playing card deck. For Tarot, for example, the suits  
        would be ['Pentacles', 'Cups', 'Swords', 'Wands']. The last suit is considered highest ranked for each card value if suit_ranking is True. When the other_data
        feature is being used, this is a one-element list that contains the column heading of the column of the dataframe to be used as suits.
        
        value_list: the card values in ascending order as a list of strings. When the other_data feature is being used, this is a one-element list that contains
        the column heading of the column of the dataframe to be used as values.
        
        arcana: a list of strings that names, individualy, each card in the deck that is not part of a suit. In a standard deck, there are two Jokers, so each are
        named in the default list as ['Joker', 'Joker']. The Tarot Arcana would be a list of 22 cards by name, starting with 'The Magician' and ending with 'The World'.
        
        suit_ranking: True or False, for certain games, suits are considered as ranked, meaning there are no 'ties' for value. In certain varieties of President, 
        Diamonds are low and Spades high, meaning an Ace of spades beats an Ace of hearts. If this is set to False, an Ace of any suit is tied with an Ace of any other.
        
        sort_by: whether the order of the deck is ordered by suit or by value - only matters if you want to specify an order for something. Can be either "value" or "suit."
        
        other_data: optional. The other_data is given as the file path to a CSV that can be read into a Pandas Dataframe. This dataframe extends the capacity of each card
        to hold data. Two columns in the CSV must be named suits and value_list, and the values given in the dataframe will override the above-passed arguments.
        '''
        self.deck_configuration = {}
        self.suit_ranking = suit_ranking
        
        if other_data != '': 
            import pandas as pd
            self.other_data = other_data
            self.card_values = pd.read_csv(self.other_data)
            self.card_values = self.card_values.to_dict('records')
            self.suits = list(set(self.card_values[suits[0]].tolist()))
            self.values = self.card_values[value_list[0]].tolist()
            self.deck_holder = list(range(len(self.values))) #the deck_holder does not change except to represent absolute values of cards relative to one another
            self.arcana=[]
        else:
            self.suits = suits
            self.values = value_list
            self.arcana = arcana
            self.other_data = False
            self.deck_holder = [] #the deck_holder does not change except to represent absolute values of cards relative to one another            
            for suit in self.suits:
                for value in self.values:
                    self.deck_holder.append({"suit":suit, "value":value})
            #!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
            #append the arcana on to the end of the deck
            #!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
            if len(arcana) > 0:
                for idx, card in enumerate(arcana):
                    self.deck_holder.append({"suit":card, "value":idx})
            self.abs_value()

        self.current_order = list(range(len(self.deck_holder))) #current order is for shuffling, so the whole deck_holder does not have to be used
        for card in self.deck_holder:
            card['trump'] = False #whether this card or a group of cards is considered a trump. This basically adds absolute value to every card in this group
            card['high'] = 0 #from the bottom of the suit, make this card the high/lowest card in the suit by absolute value 1 positive or negative 
            card['wild'] = False #whether the card is considered wild or not, where 'wild' means it can have any value in the deck
            card['absolute_value'] = 0 #the base absolute value of the card, unmodified by any of the above
        
    def __str__(self):

        composition = str(len(self.deck_holder)) + '-card deck created with ' + str(len(self.suits)) + ' suits and ' + str(len(self.arcana)) + ' arcana. \n'
        for card in self.current_order:
            if self.other_data != True:
                my_line = str(self.deck_holder[card])
                composition = composition + my_line + '\n' #breaks here because of the dict being converted to string.
        return composition
    
    def cut(self, wacky=False):
        '''
        Will cut the deck in an error-prone human way.
        If wacky is true, it will allow for cuts all over the deck and not forcibly in or close to the middle of the deck. 
        '''
        from random import randint
        #first split the deck in roughly two groups between the left and right hand, with a 10% margin of error
        left_hand = []
        right_hand = []
        if wacky == False:
            percent_error = int(len(self.deck_holder)/10) #get about a tenth to measure error
            split_error = percent_error*2 #the total split may be positive or negative, so we double total random int and subtract half
            left_split = int(len(self.deck_holder)/2) #initial split of the deck
            left_split = left_split + randint(1, split_error) - percent_error #random digit between 1 and double error minus half error    
        else:
            left_split = randint(0, len(self.deck_holder))
        left_hand = self.current_order[0:left_split]
        right_hand = self.current_order[left_split:len(self.current_order)]
        self.current_order = right_hand + left_hand
        return self.current_order
    
    def shuffle(self, count=1):
        '''
        Will mix the deck in an error-prone human way, and ensure sloppy and randomised errors in shuffle.
        '''
        import random 
        new_order = []
        random.seed()
        percent_error = 2.5 #I made this guess very scientifically
        while count > 0:
            self.cut()
            i=1    
            flip = 1
            while len(self.current_order) > 1: #I find this hilarious.
                flipcheck = random.random() < (i / float(percent_error)) #if the random number between 0.0 and 1.0 is less than iterations over percent_error then TRUE
                i=i+1 #increase iteration count
                if flipcheck is True: #if TRUE, we flip the direction of the shuffle from one end of the deck to the other
                    flip = flip*-1 #by multiplying flipcheck by negative one
                    i=1 #and resetting our count to next flip
                new_order.append(self.current_order.pop(flip)) #whichever direction flip goes, take a card from that end and put it onto the new order
            new_order = new_order + self.current_order
            self.current_order = new_order
            new_order = []
            count = count - 1
        return self.current_order

    def shuffle_suit(self, key, value):
        from random import shuffle
        '''
        This is no longer for just shuffing suits, but for shuffling cards based on any one of their key:value pairs
        key is the card key being searched for
        value is the value within this key to be returned
        the cards are then shuffled and returned to the deck in the same spots they were taken from
        ex.: if the deck has suits ABC, and the key is suit and the value is A
        in a deck that looks like ABBCACBAC, the cards with A will be removed: xBBCxCBxC, shuffled, and replaced into the old gaps in the deck: ABBCACBAC
        '''
        #a = self.suits.index(suit)
        #b = a*len(self.values)
        #c = range(b, b+len(self.values))
        c = []
        for idx, val in enumerate(self.deck_holder):
            if val[key] == value:
                c.append(idx)
        x = []
        y = []
        for idx, val in enumerate(self.current_order):
            if idx in c:
                x.append(idx)
                y.append(val)
        
        shuffle(y)
        
        for idx, val in enumerate(x):
            self.current_order[val] = y[idx]

    def wilds(self, active=False):
        '''
        Used for defining wild cards in the deck. A wild card is not necessarily a high card. A wild card can take any value and/or suit as desired by the player.
        '''
        self.wilds_active = active
        return self.deck_holder
    
    def trumps(self, key, value):
        '''
        Used to mark a card, cards, or suit as trump suit.
        Every card with a key that has the value above will be changed to a trump card.
        Trump card is defined as a card that has a higher value than all other cards with a different value in this key.
        To eliminate the trump setting, simply set any key to a value not contained in that key.
        '''
        for i in self.deck_holder:
            if i[key] == value:
                i['trump'] = True
            else:
                i['trump'] = False
    
    def card_value(self, key, card_number):
        '''
        Determines what value a given card has in the respective key
        '''
        value = self.deck_holder[card_number][key]
        return value 
        
    def abs_value(self):
        '''
        Determines the base absolute value in the deck the card has, relative to other cards, unmodified by any other factors.
        Assigns these values to cards. Used on initialisation of deck. Trump, High, Wild are not counted.
        Can only be used on traditional decks, hence the deck MUST have at least one suit and an ordered list of values from lowest to highest.
        If suit_ranking is true, the suit ranking used in determining absoute value is the order of the suits in the list, from lowest to highest.
        All Arcana is automagically assigned absolute values above the entire deck in ascending order from the start of the Arcana list.
        This is really unruly but can be cleaned up later.
        '''
        highest = 0
        for i in self.deck_holder:
            if self.suit_ranking == True and i['suit'] in self.suits:
                i['absolute_value'] = self.values.index(i['value'])*len(self.suits) + self.suits.index(i['suit'])
            elif self.suit_ranking == False and i['suit'] in self.suits:
                i['absolute_value'] = self.values.index(i['value'])
            else: 
                i['absolute_value'] = -1
            if i['absolute_value'] > highest: 
                highest = i['absolute_value']
        for i in self.deck_holder:
            if i['absolute_value'] == -1:
                i['absolute_value'] = highest + 1 + i['value']             

    def configure_deck(self, pile_class, behaviour):
        '''
        Often in a card game it is necessary to have piles, spreads, decks, hands or tableaux of cards which have a specific behaviour.
        Additionally, it must be possible to select a group of the same type of pile in order to perform a similar action to all members of this class.
        This configuration variable holds the classes and behaviours of different piles so that they can functionaly be instantiated and acted upon by class rather than individually.
        Behaviours
        discard: Face up. Cards enter on top of discard pile, so last card drawn is visible. Cards leave from the top. (face-up, last-in first-out)
        ---Visibility: True, Visibility_card: discard[len(discard)], Visibility_player: all, Enter: discard.append(), Leave: discard.pop()
        draw: Face down. Cards enter from bottom, and if a list is added to the draw deck, it will be shuffled in and lain on the bottom. (face-down, first-in first-out)
        ---Visibility: False, Visibility_card: None, Visibility_player: all, Enter: new_cards + draw, Leave: draw.pop()
        hand: Face up to only one player. Cards enter in any order and may be acted upon by a player. (selective face-down, user-determined in-and-out)
        ---Visibility: True, Visibility_card: All, Visibility_player: (user defined), Enter: new_cards + hand, Leave: hand.pop(specific_cards)
        tableau: Face up, where all cards are visible to all players. Typically empty slots are replaced from a draw deck. (face-up, draw-in user-determined out)
        ---Visibility: True, Visibility_card: All, Visibility_player: All, Enter: tableau[empty_item] = new_item, Leave: river[index] = "Empty" then river[index] = new_card
        river: As tableau, but cards fill in gaps at the end of a round by "flowing" in one direction until all gaps are filled. ABxDxFGxI > xxxABDFGI > LKJABDFGI
        ---Visibility: True, Visibility_card: All, Visibility_player: All, Enter: for each new card: [new_card] + river[], Leave: river.pop(specific_cards)
        trick: A specialised discard pile that allows for clearing at the end of a trick, such that discards are no longer visible. Tricks may be assigned to players.
        ---Visibility: True, Visibility_card: All, Visibility_player: (User defined), Enter: trick=[card_list], Leave: (does not leave), Owner: (user defined)
        fliphand: An inverse hand that is visible to all players but not to the holding player.
        ---Visibility: True, Visibility_card: All, Visibility_player: All except (user defined), Enter: trick=[card_list], Leave: (does not leave), Owner: (user defined)
        secret: A tableau that is face down, and any card may be turned face-up through player actions. Can be accessed in a 2d grid if necessary (e.g. memory)
        meld: sets of same rank that are placed face-up, on the table, and access must be defined as per the game. In Canasta, only the owner may play to a meld. 
        bury: cards that are removed from play and are not to be reshuffled for the rest of the game. As in MTG "exile". (cards enter but do not leave until game over)
        player_deck: In a deckbuilding game, a deck which behaves as a draw but has access limited to one player. (face-down, first-in first-out)
        player_discard: In a deckbuilding game, a discard pile which is limited to being accessed by one player. Cards may enter from player discards or from an external deck.
        '''
        self.deck_configuration[pile_class] = behaviour
