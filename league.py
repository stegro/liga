#!/usr/bin/env python

import random, sys, pickle

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

class Table:
	def __init__(self, team_file):
		self.teams_lookup = {}
		self.teams = []
		self.matches_remaining = []
		self.matches_played = []
		self.load_teams(team_file)

	def load_teams(self, team_file):
		num_matches = 0
		f = open(team_file, "r")
		for line in f.readlines():
			if num_matches == 0:
				num_matches = int(line.strip())
				continue
			name = line.strip()
			team = Team(name)
			self.teams.append(team)
			self.teams_lookup[name] = team
		f.close()
		self.generate_matches(num_matches)

	def generate_matches(self, num_matches):
		for i in xrange(0, len(self.teams)):
			team1 = self.teams[i]
			for j in xrange(i+1, len(self.teams)):
				team2 = self.teams[j]
				for k in xrange(0, num_matches):
					self.matches_remaining.append(Match(team1, team2))
		random.shuffle(self.matches_remaining)

# Functions

def cmd_match(table):
	current = 0
	accepted = False
	match = None
	while (not accepted):
		match = table.matches_remaining[current]
		print("Match: " + str(match) + " OK?")
		input = raw_input("y/n > ")
		if (input == "y"):
			accepted = True
			table.matches_remaining.pop(current)
			table.matches_played.append(match)
		else:
			current += 1
	
	print("Play " + str(match) + "!")
	home_score = int(raw_input("Insert score for left player > "))
	away_score = int(raw_input("Insert score for right player > "))

	match.home_score = home_score
	match.home.rounds += home_score
	match.away_score = away_score
	match.away.rounds += away_score

	if (home_score == away_score):
		match.drawn = True

	if (home_score >= away_score):
		match.winner = match.home
		match.loser = match.away
	else:
		match.loser = match.home
		match.winner = match.away

	if (match.drawn):
		match.home.drawn += 1
		match.away.drawn += 1
		print("A draw!")
	else:
		match.winner.won += 1
		match.loser.lost += 1
		print(match.winner.name + " wins!")

def cmd_save(table):
	savename = raw_input("Filename? ")
	savename = savename.strip()
	f = open(savename, "w")
	pickle.dump(table, f)
	f.close()
	print("Saved.")

def cmd_quit(table):
	print("Bye..")
	exit(0)

commands = {}
commands_help = []
def add_cmd(longstr, shortstr, helpstr, cmd):
	global commands
	global commands_help
	commands[longstr] = cmd	
	commands[shortstr] = cmd
	commands_help.append("%s / %s - %s" % (longstr, shortstr, helpstr)) 

def help_cmd(table):
	global commands_help
	for cmdhelp in commands_help:
		print(cmdhelp)

add_cmd("match", "m", "Request for a match to play.", cmd_match)
add_cmd("save", "s", "Save the league state.", cmd_save)
add_cmd("quit", "q", "Quit.", cmd_quit)
add_cmd("help", "h", "See this help...", help_cmd)

def repl(table):
	global commands
	while len(table.matches_remaining) > 0:
		input = raw_input("(%d)> " % len(table.matches_remaining))
		input = input.strip()
		if input in commands:
			commands[input](table)
		else:
			print("Unrecognised command. Type 'help' or 'h' to see commands.")
		
# Start
	
if (len(sys.argv) < 3):
	usage()

the_table = None
if (sys.argv[1] == "-n"):
	the_table = Table(sys.argv[2])
elif (sys.argv[1] == "-r"):
	f = open(sys.argv[2])
	the_table = pickle.load(f)	
	f.close()
else:
	usage()

repl(the_table)
