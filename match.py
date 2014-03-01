class Match:
        def __init__(self, home, away):
                self.home = home
                self.away = away
                self.home_score = 0
                self.away_score = 0
                self.played = False
                self.drawn = False
                self.winner = None
                self.loser = None

        def __repr__(self):
                if (self.played):
                        return "%s %d - %d %s" % (self.home.name, self.home_score, self.away_score, self.away.name)
                return "%s vs. %s" % (self.home.name, self.away.name)

        def undo(self):
                self.home.rounds -= self.home_score
                self.away.rounds -= self.away_score

                if (self.drawn):
                        self.winner.drawn -= 1
                        self.loser.drawn -= 1
                        self.drawn = False
                else:
                        self.winner.won -= 1
                        self.loser.lost -= 1

        def finish(self, home_score, away_score):
                self.home_score = home_score
                self.home.rounds += home_score
                self.away_score = away_score
                self.away.rounds += away_score

                if (home_score == away_score):
                        self.drawn = True
                if (home_score >= away_score):
                        self.winner = self.home
                        self.loser = self.away
                else:
                        self.loser = self.home
                        self.winner = self.away

                if (self.drawn):
                        self.home.drawn += 1
                        self.away.drawn += 1
                else:
                        self.winner.won += 1
                        self.loser.lost += 1
