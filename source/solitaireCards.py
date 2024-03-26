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
        return "cardGraphics/ace/" + cardNumber + ".png"
    
class Spade(SolitaireCard):
    def __init__(self, cardNumber, image):
        super().__init__(self, "Black", cardNumber, Spade.getImageDirectory(cardNumber))

    def getImageDirectory(cardNumber):
        return "cardGraphics/spade/" + cardNumber + ".png"


class Heart(SolitaireCard):
    def __init__(self, cardNumber, image):
        super().__init__(self, "Red", cardNumber, Heart.getImageDirectory(cardNumber))

    def getImageDirectory(cardNumber):
        return "cardGraphics/heart/" + cardNumber + ".png"
    
class Diamond(SolitaireCard):
    def __init__(self, cardNumber, image):
        super().__init__(self, "Red", cardNumber, Spade.getImageDirectory(cardNumber))

    def getImageDirectory(cardNumber):
        return "cardGraphics/diamond/" + cardNumber + ".png"