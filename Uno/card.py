class Card():
    def __init__(self,type_,color):
        assert color in set(["blue","green","red","yellow","TBD"]), "INVALID TYPE SET {}".format(type_)
        self.type = type_
        self.color = color
    def __str__(self):
        return "A {} of color {}".format(self.type,self.color)
    def __repr__(self):
        return "A {} of color {}".format(self.type,self.color)

