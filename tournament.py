#!/usr/bin/env python
#
# tournament.py -- implementation of a Swiss-system tournament
#

import psycopg2

def connect():
    '''Connects to the PostgreSQL database.

    Returns:
      DB - a database connection
      cursor - a cursor
    '''

    DB = psycopg2.connect("dbname=tournament")
    cursor = DB.cursor()
    return DB, cursor


def deleteMatches():
    '''Remove all the match records from the database.'''

    DB,cursor = connect()
    cursor.execute("DELETE FROM matches")
    cursor.execute("DELETE FROM pairings")
    cursor.close()
    DB.commit()
    DB.close()


def deletePlayers():
    '''Remove all the player records from the database.'''

    DB,cursor = connect()
    #TABLE standings should be deleted first
    # due to foreign_key (id_player) referencing to the TABLE players
    cursor.execute("DELETE FROM standings")
    cursor.execute("DELETE FROM players")
    cursor.close()
    DB.commit()
    DB.close()


def countPlayers():
    '''Returns the number of players currently registered.

    Returns:
      the number of players currently registered
    '''

    DB,cursor = connect()
    cursor.execute("SELECT * FROM players")
    players_num = cursor.fetchall()
    cursor.close()
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

    DB,cursor = connect()
    SQL = "INSERT INTO players (name) VALUES (%s);"
    data = (player_name,)
    cursor.execute(SQL, data)
    cursor.execute("SELECT MAX(id_player) FROM players")
    id_player = cursor.fetchone()[0]
    SQL = "INSERT INTO standings (id_player, name, wins, matches) VALUES (%s, %s, %s, %s);"
    data = (id_player, player_name, 0, 0)
    cursor.execute(SQL, data)
    cursor.close()
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

    DB,cursor = connect()
    cursor.execute("SELECT * FROM standings ORDER BY wins")
    DB.commit()
    players_standings = cursor.fetchall()
    cursor.close()
    DB.close()
    return players_standings


def reportMatch(winner, loser):
    '''Records the outcome of a single match between two players.

    Args:
      winner:  the id number of the player who won
      loser:  the id number of the player who lost
    '''

    DB,cursor = connect()

    #update matches date
    SQL = "INSERT INTO matches (winner, loser) VALUES (%s, %s);"
    data = (winner, loser)
    cursor.execute(SQL, data)

    #update standings table
    SQL = "UPDATE standings SET wins = wins + 1 WHERE id_player = (%s);"
    data = (winner,)
    cursor.execute(SQL, data)
    SQL = "UPDATE standings SET matches = matches + 1 WHERE id_player = (%s);"
    data = (winner,)
    cursor.execute(SQL, data)

    #cursor.execute("UPDATE standings "
    SQL = "UPDATE standings SET matches = matches + 1 WHERE id_player = (%s);"
    data = (loser,)
    cursor.execute(SQL, data)
    cursor.close()
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

    DB,cursor = connect()

    #get final version of standings list
    standings = playerStandings()
    i = 0
    match_id = 1
    for record in standings:
        player_id = record[0]
        player_name = record[1]
        i += 1

        if i % 2 != 0:
            SQL = "INSERT INTO pairings (id_match, player1, name_player1) VALUES (%s, %s, %s);"
            data = (match_id, player_id, player_name)
            cursor.execute(SQL, data)

            DB.commit()
        elif i % 2 == 0:
            SQL = "UPDATE pairings SET player2 = %s, name_player2 = %s WHERE id_match = %s;"
            data = (player_id, player_name, match_id)
            cursor.execute(SQL, data)
            DB.commit()
            match_id += 1

    #fetch and returns a list of pairs of players for the next round of a match
    cursor.execute("SELECT player1, name_player1, player2, name_player2 "
              "FROM pairings")
    DB.commit()
    match_pairings = cursor.fetchall()
    cursor.close()
    DB.close()
    return match_pairings
