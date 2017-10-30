class Deck():
    '''
    Deck contains all information about a deck of cards
    
    '''    
    def __init__(self, name='Classic', suits=['Diamonds', 'Clubs', 'Hearts', 'Spades'],\
                 value_list=['A', '2', '3', '4', '5', '6', '7', '8', '9', '10', 'J', 'Q', 'K'],\
                 arcana=['Joker', 'Joker']):
        '''
        This initialises a deck of cards. In the default, a standard 54-card deck is generated
        with two Jokers. The arcana are the uncategorised extra cards that do not have suits, in this case, the Jokers. They are enumerated individually
        by name. Value of a card is equal to its position in the values list plus one. If Ace is high, Ace should be last in the row.
        '''
        self.deck_holder = []
        self.suits = suits
        self.values = value_list
        self.arcana = arcana        
        
        for suit in suits:
            for value in self.values:
                self.deck_holder.append(value + ' of ' + suit)
        
        for card in arcana:
            self.deck_holder.append(card)
            
        self.current_order = list(range(len(self.deck_holder)))
        
    def __str__(self):
        composition = str(len(self.deck_holder)) + '-card deck created with ' + str(len(self.suits)) + ' suits and ' + str(len(self.arcana)) + ' arcana. \n'
        for card in self.current_order:
            composition = composition + self.deck_holder[card] + '\n'
        return composition
    
    def cut(self):
        '''
        Will cut the deck in an error-prone human way.
        '''
        from random import randint
        #first split the deck in roughly two groups between the left and right hand, with a 10% margin of error
        left_hand = []
        right_hand = []
        percent_error = int(len(self.deck_holder)/10) #get about a tenth to measure error
        split_error = percent_error*2 #the total split may be positive or negative, so we double total random int and subtract half
        left_split = int(len(self.deck_holder)/2) #initial split of the deck
        left_split = left_split + randint(1, split_error) - percent_error #random digit between 1 and double error minus half error    
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
        percent_error = int(len(self.deck_holder)/20) #get about a twentienth to measure error
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
            
x = Deck()
x.shuffle(count=7)
print(x)