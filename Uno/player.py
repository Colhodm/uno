class Player():
    def __init__(self,name):
        #for card in cards:
            #type_,value = card.type,card.value
            #self.quick_cards[(type_,value)] = self.quick_cards.get((type_,value)+1,0)
        self.name = name
        self.cards = []
        self.colors = {}
    def add_card(self,card):
        self.colors[card.color] = self.colors.get(card.color,0) + 1
        self.cards.append(card)
        return self
    def play_card(self,card):
        self.colors[card.color] = self.colors.get(card.color,0) - 1
        print("should be removing a card.....")
        print(len(self.cards))
        self.cards.remove(card)
        print(len(self.cards))
