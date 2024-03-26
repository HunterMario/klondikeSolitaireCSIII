# These classes will consist of the foundation piles in the game
from solitaireCards import Ace, Spade, Heart, Diamond

class FoundationPile:
    def __init__(self, cardType):
        self.type = cardType
        self.__cardStack = []
    
    def addToStack(self, card):
        if ((isinstance(card, self.cardType) and 
        card.cardNumber == self.cardStack[-1].cardNumber) or
        (self.__cardStack.len() == 0 and card.cardNumber == 1)):
            self.__cardStack.append(card)
        else:
            return None


class AceFoundation(FoundationPile):
    def __init__(self):
        super.__init__(Ace())