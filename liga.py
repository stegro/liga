#!/usr/bin/env python3

import pickle
import sys
from table import *
from match import *
from team import *

# Functions

def get_int(text):
        v = -1
        while v == -1:
                try:
                        v = int(input(text))
                except ValueError:
                        print("Try entering a number.")
        return v

def cmd_table(table):
        table.print_league_table()

def cmd_match(table):
        current = 0
        accepted = False
        match = None
        while (not accepted):
                match = table.matches_remaining[current]
                print("Match: " + str(match) + " OK?")
                res = input("y/n > ")
                if (res == "y"):
                        accepted = True
                        table.matches_remaining.pop(current)
                        table.matches_played.insert(0, match)
                else:
                        current += 1
        print("Play " + str(match) + "!")

        home_score = get_int("Insert score for " + match.home.name + " > ")
        away_score = get_int("Insert score for " + match.away.name + " > ")
        match.played = True
        match.finish(home_score, away_score)

        if (match.drawn):
                print("A draw!")
        else:
                print(match.winner.name + " wins!")


def cmd_fixtures(table):
        for match in table.matches_remaining[0:5]:
                print(match)

def cmd_results(table):
        for match in table.matches_played[0:5]:
                print(match)

def cmd_adjust(table):
        found_match = False
        idx = 0
        match = None
        while (not found_match):
                print("Which match do you want to adjust? (Type 'n' to get next 5, or 'p' to get previous 5, or 'c' to cancel this.)")
                counter = 0
                for match in table.matches_played[idx:idx+5]:
                        print(str(idx + counter) + ": " + str(match))
                        counter += 1
                res = input("> ")
                if (res == "n"):
                        idx += 5
                        if (idx > len(table.matches_played)):
                                idx -= 5
                elif (res == "p"):
                        idx -= 5
                        if (idx < 0):
                                idx = 0
                elif (res == "c"):
                        return
                else:
                        target = -1
                        try:
                                target = int(res)
                        except ValueError:
                                print("Try entering a number, 'n', 'p', or 'c'.")
                        if (target < 0 or target >= len(table.matches_played)):
                                print("Try entering a valid number, 'n', 'p', or 'c'.")
                        else:
                                found_match = True
                                match = table.matches_played[target]
        match.undo()
        home_score = get_int("Insert NEW score for left player > ")
        away_score = get_int("Insert NEW score for right player > ")
        match.finish(home_score, away_score)
        print("Match updated.")

def cmd_save(table):
        savename = input("Filename? ")
        savename = savename.strip()
        f = open(savename, "wb")
        pickle.dump(table, f, protocol=2)
        f.close()
        print("Saved.")

def cmd_quit(table):
        print("Bye!")
        exit(0)

def cmd_details(table):
        print("Matches played: " + str(len(table.matches_played)))
        print("Matches remaining: " + str(len(table.matches_remaining)))

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

add_cmd("table", "t", "Show current league table standings.", cmd_table)
add_cmd("match", "m", "Request for a match to play.", cmd_match)
add_cmd("fixtures", "f", "Display 5 upcoming fixtures.", cmd_fixtures)
add_cmd("results", "r", "Display 5 previous results.", cmd_results)
add_cmd("details", "d", "Show details about the league.", cmd_details)
add_cmd("adjust", "a", "Adjust a score for a previous match.", cmd_adjust)
add_cmd("save", "s", "Save the league state.", cmd_save)
add_cmd("quit", "q", "Quit.", cmd_quit)
add_cmd("help", "h", "See this help.", help_cmd)

def repl(table):
        global commands
        while len(table.matches_remaining) > 0:
                try:
                        cmd = input("(liga)> ")
                except EOFError:
                        print()
                        commands["quit"](table)
                cmd = cmd.strip()
                if cmd in commands:
                        commands[cmd](table)
                else:
                        print("Unrecognised command. Type 'help' or 'h' to see commands.")

        print()
        print("------- Season finished! Final standings: --------")
        table.print_league_table()
        print("--------------------------------------------------")

def usage():
        print("Usage: liga.py (-n <League Description File>|-l <League Save File>)")
        print()
        print("You want to play Pingpong with your friends? This")
        print("interactive script helps you to manage your liga.")
        print()
        print(" -n    create a new league from a description file ")
        print(" -l    load a league from a save file ")
        exit(1)
		
# Start
	
if (len(sys.argv) < 3):
        usage()

the_table = None
if (sys.argv[1] == "-n"):
        the_table = Table(sys.argv[2])
elif (sys.argv[1] == "-l"):
        f = open(sys.argv[2], "rb")
        the_table = pickle.load(f)
        f.close()
        print("Current standings:-")
        the_table.print_league_table()
else:
        usage()

# go interactive
help_cmd(the_table)
repl(the_table)
