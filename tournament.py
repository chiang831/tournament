#!/usr/bin/env python
# 
# tournament.py -- implementation of a Swiss-system tournament
#

import contextlib
import psycopg2


def connect():
    """Connect to the PostgreSQL database.  Returns a database connection."""
    return psycopg2.connect("dbname=tournament")


@contextlib.contextmanager
def _connect_db():
    """Connect to DB and get cursor. Close cursor and connection on exit.

    Returns:
      A tuple (connection, cursor) connecting to tournament database.
    """
    try:
        conn = connect()
        cur = conn.cursor()        
        yield conn, cur

    finally:
        cur.close()
        conn.close()


def deleteMatches(cur=None, conn=None):
    """Remove all the match records from the database."""
    with _connect_db() as (conn, cur):
        cur.execute("""DELETE FROM matches;""")
        cur.execute("""DELETE FROM byes;""")
        conn.commit()


def deletePlayers():
    """Remove all the player records from the database."""
    with _connect_db() as (conn, cur):
        cur.execute("""DELETE FROM players;""")
        conn.commit()


def countPlayers():
    """Returns the number of players currently registered."""
    with _connect_db() as (conn, cur):
        cur.execute("""SELECT COUNT(*) from players;""")
        ret = int(cur.fetchone()[0])
        return ret


def registerPlayer(name):
    """Adds a player to the tournament database.
  
    The database assigns a unique serial id number for the player.  (This
    should be handled by your SQL database schema, not in your Python code.)
  
    Args:
      name: the player's full name (need not be unique).
    """
    with _connect_db() as (conn, cur):
        cur.execute("""INSERT INTO players (name) VALUES (%s);""", (name,))
        conn.commit()


def playerStandings():
    """Returns a list of the players and their win records, sorted by wins.

    The first entry in the list should be the player in first place, or a player
    tied for first place if there is currently a tie.

    Returns:
      A list of tuples, each of which contains (id, name, wins, matches):
        id: the player's unique id (assigned by the database)
        name: the player's full name (as registered)
        wins: the number of matches the player has won
        matches: the number of matches the player has played
    """
    with _connect_db() as (conn, cur):
        cur.execute("""SELECT * FROM standings;""")
        standings = cur.fetchall()
        return standings


def reportMatch(winner, loser, is_draw=False):
    """Records the outcome of a single match between two players.

    Args:
      winner:  the id number of the player who won
      loser:  the id number of the player who lost
      is_draw:  True if this match is a draw, False otherwise.
    """
    with _connect_db() as (conn, cur):
        cur.execute("""INSERT INTO matches VALUES (%s, %s, %s);""",
                    (winner, loser, is_draw))
        conn.commit()
 
 
def _getAndSetByePlayer():
    """Returns an int for player id that should get bye this round.

    Query the database using by_candidate view for bye candidate id.
    Also, insert byes table to mark that player has got a bye.

    Returns:
      An int for id number of the player who should get bye this round.
    """
    with _connect_db() as (conn, cur):
        cur.execute("""SELECT player FROM bye_candidate;""")
        query_result = cur.fetchall()
        bye_player = query_result[0]
        cur.execute("""INSERT INTO byes VALUES (%s);""", (bye_player,))
        conn.commit()
        return bye_player


def swissPairings():
    """Returns a list of pairs of players for the next round of a match.
  
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
    """
    with _connect_db() as (conn, cur):
        number_of_players = countPlayers()
        pairings = [] 

        if number_of_players & 1:
          # Decides bye player and skip that player in the query of standings.
          bye_id = _getAndSetByePlayer()
          for pair_index in xrange(0, number_of_players - 1, 2):
              cur.execute(
                     """SELECT player, name FROM standings WHERE
                             player != %s OFFSET %s LIMIT 2;""",
                     (bye_id, pair_index,))
              query_result = cur.fetchall()
              id1, name1 = query_result[0]
              id2, name2 = query_result[1]
              pairings.append((id1, name1, id2, name2))
        else:
          for pair_index in xrange(0, number_of_players, 2):
              cur.execute(
                      """SELECT player, name FROM standings
                              OFFSET %s LIMIT 2;""",
                      (pair_index,))
              query_result = cur.fetchall()
              id1, name1 = query_result[0]
              id2, name2 = query_result[1]
              pairings.append((id1, name1, id2, name2))

        return pairings
