import random

CARDS_DATA = {
    "Tiger": [(0, -2), (0, 1)],
    "Dragon": [(-2, -1), (2, -1), (-1, 1), (1, 1)],
    "Frog": [(-2, 0), (-1, 1), (1, -1)],
    "Rabbit": [(2, 0), (1, 1), (-1, -1)],
    "Crab": [(-2, 0), (0, 1), (2, 0)],
    "Elephant": [(-1, 0), (-1, 1), (1, 0), (1, 1)],
    "Goose": [(-1, 0), (-1, 1), (1, 0), (1, -1)],
    "Rooster": [(-1, 0), (-1, -1), (1, 0), (1, 1)],
    "Monkey": [(-1, -1), (1, -1), (-1, 1), (1, 1)],
    "Mantis": [(-1, 1), (0, -1), (1, 1)]
}

class Card:
    def __init__(self, name, moves):
        self.name = name
        self.moves = moves

    def __repr__(self): # Añadido para que sea fácil de leer al imprimir
        return f"Card({self.name})"

class CardManager:
    def __init__(self):
        self.deck = self.create_deck()
        self.side_card = None

    def create_deck(self):
        # Ahora está correctamente dentro de la clase
        deck = [Card(name, moves) for name, moves in CARDS_DATA.items()]
        random.shuffle(deck)
        return deck

    def deal_cards(self, players):
        for player in players:
            # Asume que el objeto 'player' tiene un atributo 'cards'
            player.cards = [self.deck.pop(), self.deck.pop()]
        self.side_card = self.deck.pop()

    def swap_card(self, player, used_card):
        # Intercambia la carta usada por la carta lateral
        player.cards.remove(used_card)
        player.cards.append(self.side_card)
        self.side_card = used_card

    def is_valid_move(self, card, move):
        return move in card.moves