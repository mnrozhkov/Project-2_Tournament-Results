#!/usr/bin/env python
#
# tournament.py -- implementation of a Swiss-system tournament
#

import psycopg2

def connect():
    '''Connects to the PostgreSQL database.

    Returns:
      a database connection.
    '''

    return psycopg2.connect("dbname=tournament")


def deleteMatches():
    '''Remove all the match records from the database.'''

    DB = psycopg2.connect("dbname=tournament")
    c = DB.cursor()
    c.execute("DELETE FROM matches")
    c.execute("DELETE FROM pairings")
    c.close()
    DB.commit()
    DB.close()


def deletePlayers():
    '''Remove all the player records from the database.'''

    DB = psycopg2.connect("dbname=tournament")
    c = DB.cursor()
    #TABLE standings should be deleted first
    # due to foreign_key (id_player) referencing to the TABLE players
    c.execute("DELETE FROM standings")
    c.execute("DELETE FROM players")
    c.close()
    DB.commit()
    DB.close()


def countPlayers():
    '''Returns the number of players currently registered.

    Returns:
      the number of players currently registered
    '''

    DB = psycopg2.connect("dbname=tournament")
    c = DB.cursor()
    c.execute("SELECT * FROM players")
    players_num = c.fetchall()
    c.close()
    DB.commit()
    DB.close()
    return len(players_num)


def registerPlayer(player_name):
    '''Adds a player to the tournament database.

    The database assigns a unique serial id number for the player.  (This
    should be handled by your SQL database schema, not in your Python code.)

    Args:
      name: the player's full name (need not be unique).
    '''

    DB = psycopg2.connect("dbname=tournament")
    c = DB.cursor()
    c.execute("INSERT INTO players (name) VALUES (%s)", (player_name,))
    c.execute("SELECT MAX(id_player) FROM players")
    id_player = c.fetchone()[0]
    #print(id_player)
    c.execute("INSERT INTO standings (id_player, name, wins, matches) VALUES (%s, %s, %s, %s)",
              (id_player, player_name, 0, 0))
    c.close()
    DB.commit()
    DB.close()


def playerStandings():
    '''Returns a list of the players and their win records, sorted by wins.

    The first entry in the list should be the player in first place, or a player
    tied for first place if there is currently a tie.

    Returns:
      A list of tuples, each of which contains (id, name, wins, matches):
        id: the player's unique id (assigned by the database)
        name: the player's full name (as registered)
        wins: the number of matches the player has won
        matches: the number of matches the player has played
    '''

    DB = psycopg2.connect("dbname=tournament")
    c = DB.cursor()
    c.execute("SELECT * FROM standings ORDER BY wins")

    DB.commit()
    players_standings = c.fetchall()
    #print(players_standings)

    c.close()
    DB.close()
    return players_standings


def reportMatch(winner, loser):
    '''Records the outcome of a single match between two players.

    Args:
      winner:  the id number of the player who won
      loser:  the id number of the player who lost
    '''

    DB = psycopg2.connect("dbname=tournament")
    c = DB.cursor()

    #update matches date
    c.execute("INSERT INTO matches (winner, loser)"
              "VALUES (%s, %s)", (winner, loser))

    #update standings table
    c.execute("UPDATE standings "
              "SET wins = wins + 1 WHERE id_player = (%s)",
              (winner,))
    #DB.commit()
    #print(c.fetchall())
    c.execute("UPDATE standings "
              "SET matches = matches + 1 WHERE id_player = (%s)",
              (winner,))
    c.execute("UPDATE standings "
              "SET matches = matches + 1 WHERE id_player = (%s)",
              (loser,))
    c.close()
    DB.commit()
    DB.close()


def swissPairings():
    '''Returns a list of pairs of players for the next round of a match.

    Assuming that there are an even number of players registered, each player
    appears exactly once in the pairings.  Each player is paired with another
    player with an equal or nearly-equal win record, that is, a player adjacent
    to him or her in the standings.

    Returns:
      A list of tuples, each of which contains (id1, name1, id2, name2)
        id1: the first player's unique id
        name1: the first player's name
        id2: the second player's unique id
        name2: the second player's name
    '''

    DB = psycopg2.connect("dbname=tournament")
    c = DB.cursor()

    #get final version of standings list
    standings = playerStandings()
    i = 0
    match_id = 1
    for record in standings:
        player_id = record[0]
        player_name = record[1]
        i += 1

        if i % 2 != 0:
            c.execute("INSERT INTO pairings (id_match, player1, name_player1) "
                      "VALUES (%s, %s, %s)", (match_id, player_id, player_name))
            DB.commit()
        elif i % 2 == 0:
            c.execute("UPDATE pairings SET player2 = %s, name_player2 = %s"
                      "WHERE id_match = %s", (player_id, player_name, match_id))
            DB.commit()
            match_id += 1

    #fetch and returns a list of pairs of players for the next round of a match
    c.execute("SELECT player1, name_player1, player2, name_player2 "
              "FROM pairings")
    DB.commit()
    match_pairings = c.fetchall()
    #print(match_pairings)
    c.close()
    DB.close()
    return match_pairings