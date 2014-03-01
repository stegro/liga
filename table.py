import random

class Table:
        def __init__(self, team_file):
                self.teams_lookup = {}
                self.teams = []
                self.matches_remaining = []
                self.matches_played = []
                self.load_teams(team_file)

        def load_teams(self, team_file):
                """The team_file is a text file: The first line is the number of matches,
                followed by the names of all teams, one name in each line."""
                num_matches = 0
                f = open(team_file, "r")
                for line in f.readlines():
                        if num_matches == 0:
                                num_matches = int(line.strip())
                                continue
                        name = line.strip()
                        team = Team(name)
                        # FIXME really necessary?
                        self.teams.append(team)
                        self.teams_lookup[name] = team
                f.close()
                self.generate_matches(num_matches)

        def generate_matches(self, num_matches):
                for i in range(0, len(self.teams)):
                        team1 = self.teams[i]
                        for j in range(i+1, len(self.teams)):
                                team2 = self.teams[j]
                                for k in range(0, num_matches):
                                        self.matches_remaining.append(Match(team1, team2))
                random.shuffle(self.matches_remaining)

        def print_league_table(self):
                rankings = []
                for team in self.teams:
                        rankings.append((team.getPoints(), team.rounds, team))
                rankings = sorted(rankings, reverse=True)
                print("%5s %10s %3s %3s %3s %3s %5s %5s" % ("rank", "name", "M", "W", "D", "L", "R", "P"))

                rank = 1
                for (points, rounds, team) in rankings:
                        print("%5d %10s %3d %3d %3d %3d %5d %5d" % (rank, team.name, team.getPlayed(), team.won, team.drawn, team.lost, rounds, points))
                        rank += 1
