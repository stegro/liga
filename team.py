
class Team:
        def __init__(self, name):
                self.name = name
                self.won = 0
                self.lost = 0
                self.drawn = 0
                self.rounds = 0

        def getPoints(self):
                return (self.won * 3) + self.drawn

        def getPlayed(self):
                return (self.won + self.lost + self.drawn)

        def __repr__(self):
                return "%s %d %d %d %d" % (self.name, self.won, self.lost, self.drawn, self.rounds)
        
        def __lt__(self, other):
                return self
