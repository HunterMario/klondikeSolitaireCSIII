import pygame
import sys
import random
import os

# Initialize Pygame
pygame.init()
current_dir = os.path.dirname(os.path.abspath(__file__))
os.chdir(current_dir)

# Constants
SCREEN_WIDTH = 1280
SCREEN_HEIGHT = 720
CARD_WIDTH = 104
CARD_HEIGHT = 114
FOUNDATION_WIDTH = CARD_WIDTH
FOUNDATION_HEIGHT = CARD_HEIGHT
FPS = 60
WHITE = (255, 255, 255)
GREEN = (0, 128, 0)
RED = (255, 0, 0)

# Function to load images
def load_image(filename):
    return pygame.image.load(filename).convert_alpha()

# Function to draw text on screen
def draw_text(surface, text, font, color, x, y):
    text_surface = font.render(text, True, color)
    surface.blit(text_surface, (x, y))

# Function to create a deck of cards
def create_deck():
    suits = ['H', 'D', 'C', 'S']
    ranks = ['2', '3', '4', '5', '6', '7', '8', '9', '10', 'J', 'Q', 'K', 'A']
    deck = [{'suit': suit, 'rank': rank, 'visible': False} for suit in suits for rank in ranks]
    random.shuffle(deck)
    return deck

# Function to draw a card
def draw_card(surface, card, x, y):
    filename = 'cards/' + card['rank'] + card['suit'] + '.png'
    image = load_image(filename)
    surface.blit(image, (x, y))

# Function to draw the back of a card
def draw_back(surface, x, y):
    back_image = load_image('cards/back.png')
    surface.blit(back_image, (x, y))

# Function to draw a pile of cards
def draw_pile(surface, pile, x, y):
    offset = 0
    for card in pile:
        if card['visible']:
            draw_card(surface, card, x, y + offset)
        else:
            draw_back(surface, x, y + offset)
        offset += 20

# Function to check if a point is inside a rectangle
def point_inside_rect(x, y, rect):
    return (rect.left < x < rect.right) and (rect.top < y < rect.bottom)

# Function to check if two cards can be stacked
def can_stack(card1, card2):
    if card1['suit'] in ['H', 'D'] and card2['suit'] in ['C', 'S']:
        return (card1['rank'] == str(int(card2['rank']) + 1))
    elif card1['suit'] in ['C', 'S'] and card2['suit'] in ['H', 'D']:
        return (card1['rank'] == str(int(card2['rank']) + 1))
    else:
        return False

# Function to main game loop
def main():
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption('Pygame Solitaire')

    clock = pygame.time.Clock()
    font = pygame.font.Font(None, 36)

    # Load background image
    background_image = load_image('bg/title.png')

    # Placeholder images for foundations
    foundation_images = {
        'H': load_image('cards/foundation_heart.png'),
        'D': load_image('cards/foundation_diamond.png'),
        'C': load_image('cards/foundation_club.png'),
        'S': load_image('cards/foundation_spade.png')
    }

    deck = create_deck()
    stock = deck[:]
    random.shuffle(stock)

    waste_stack = []
    foundation_piles = [[] for _ in range(4)]
    tableau_piles = [[] for _ in range(7)]

    # Deal cards to tableau piles
    for i in range(len(tableau_piles)):
        for j in range(i + 1):
            card = stock.pop()
            if j == i:  # Only the top card is visible
                card['visible'] = True
            tableau_piles[i].append(card)

    suits = ['H', 'D', 'C', 'S']  # Define suits here

    # Game loop
    dragging = False
    drag_card = None
    holding_card = False  # Variable to track if a card is being held
    while True:
        screen.fill(WHITE)

        # Draw background image
        screen.blit(background_image, (0, 0))

        # Event handling
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                if not holding_card:
                    # Check if the user clicks on a card in tableau piles
                    for pile_index, pile in enumerate(tableau_piles):
                        if pile:
                            top_card = pile[-1]
                            if point_inside_rect(*event.pos, pygame.Rect(130 + (pile_index * 100), 150, CARD_WIDTH, CARD_HEIGHT)):
                                dragging = True
                                drag_card = pile.pop()
                                holding_card = True
                                break
                else:
                    # Check if the user clicks on the stock
                    if len(stock) > 0 and point_inside_rect(*event.pos, pygame.Rect(20, 20, CARD_WIDTH, CARD_HEIGHT)):
                        # Draw 3 cards from stock to waste
                        for _ in range(min(3, len(stock))):
                            card = stock.pop()
                            card['visible'] = True
                            waste_stack.append(card)
                        holding_card = False  # Release the held card
                    # Check if the user clicks on a tableau pile
                    for pile_index, pile in enumerate(tableau_piles):
                        if point_inside_rect(*event.pos, pygame.Rect(130 + (pile_index * 100), 150, CARD_WIDTH, CARD_HEIGHT)):
                            if pile:
                                top_card = pile[-1]
                                if can_stack(drag_card, top_card):
                                    pile.append(drag_card)
                                    dragging = False
                                    drag_card = None
                                    holding_card = False  # Release the held card
                                    break
                    # Check if the user clicks on the waste stack or the foundation piles
                    if point_inside_rect(*event.pos, pygame.Rect(20, 150, CARD_WIDTH, CARD_HEIGHT)):
                        waste_stack.append(drag_card)
                        dragging = False
                        drag_card = None
                        holding_card = False  # Release the held card
                    for pile_index, pile in enumerate(foundation_piles):
                        if point_inside_rect(*event.pos, pygame.Rect(SCREEN_WIDTH - 150 + (pile_index * 100), 50, CARD_WIDTH, CARD_HEIGHT)):
                            if pile:
                                top_card = pile[-1]
                                if can_stack(drag_card, top_card):
                                    pile.append(drag_card)
                                    dragging = False
                                    drag_card = None
                                    holding_card = False  # Release the held card
                                    break

        if dragging:
            # Update the position of the dragged card
            drag_card['x'], drag_card['y'] = pygame.mouse.get_pos()
            draw_card(screen, drag_card, drag_card['x'], drag_card['y'])

        # Draw foundation piles
        for pile_index, pile in enumerate(foundation_piles):
            pygame.draw.rect(screen, GREEN, (SCREEN_WIDTH - 150 + (pile_index * 100), 50, CARD_WIDTH, CARD_HEIGHT), 2)
            if pile:
                draw_pile(screen, pile, SCREEN_WIDTH - 150 + (pile_index * 100), 50)
            else:
                screen.blit(foundation_images[suits[pile_index]], (SCREEN_WIDTH - 150 + (pile_index * 100), 50))

        # Draw tableau piles
        for pile_index, pile in enumerate(tableau_piles):
            for card_index, card in enumerate(pile):
                if card['visible']:
                    draw_card(screen, card, 130 + (pile_index * 100), 150 + (card_index * 20))
                else:
                    draw_back(screen, 130 + (pile_index * 100), 150 + (card_index * 20))  # Draw back of the card
                pygame.draw.rect(screen, GREEN, (130 + (pile_index * 100), 150 + (card_index * 20), CARD_WIDTH, CARD_HEIGHT), 1)

        # Draw stock and waste stack
        if stock:
            screen.blit(load_image('cards/back.png'), (20, 20))
        else:
            pygame.draw.rect(screen, WHITE, (20, 20, CARD_WIDTH, CARD_HEIGHT))

        if waste_stack:
            draw_card(screen, waste_stack[-1], 20, 150)

        pygame.display.flip()
        clock.tick(FPS)

if __name__ == '__main__':
    main()
