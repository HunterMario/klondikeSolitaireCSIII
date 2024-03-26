# This file defines the classes for each of the solitaire cards

class SolitaireCard:
    def __init__(self, cardColor, cardNumber, image):
        self.cardColor = cardColor
        self.cardNumber = cardNumber
        self.image = image

class Ace(SolitaireCard):
    def __init__(self, cardNumber, image):
        super().__init__(self, "Black", cardNumber, Ace.getImageDirectory(cardNumber))

    # i'll work on this later
    def getImageDirectory(cardNumber):
        pass