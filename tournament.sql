-- Table definitions for the tournament project.
--
-- Put your SQL 'create table' statements in this file; also 'create view'
-- statements if you choose to use it.
--
-- You can write comments in this file by starting them with two dashes, like
-- these lines here.

--to execute this file use command: \i tournament.sql
--run this command after connection to tournament database is enabled


--drop all old tables
DROP TABLE pairings;
DROP TABLE matches;
DROP TABLE standings;
DROP TABLE players;


-- Create table players
-- id: the player's unique id (assigned by the database)
-- name: the player's full name (as registered)
CREATE TABLE players(
  id_player SERIAL PRIMARY KEY,
  name TEXT);


-- Create a table of standings with columns id, name, wins, matches:
-- id: the player's unique id (assigned by the database)
-- name: the player's full name (as registered)
-- wins: the number of matches the player has won
-- matches: the number of matches the player has played
CREATE TABLE standings ( --as a VIEW ?
  id_player INTEGER REFERENCES players(id_player),
  name TEXT,
  wins INTEGER,
  matches INTEGER);


-- Create a table of matches with winners and losers' with columns:
-- id_match: the match's unique id (assigned by the database)
-- winner: the winner's unique id (references to players(id_player)),
-- loser: the loser's unique id (references to players(id_player)),
CREATE TABLE matches(
  id_match SERIAL PRIMARY KEY,
  winner INTEGER REFERENCES players(id_player),
  loser INTEGER REFERENCES players(id_player));


-- Create a table of pairs of players for the next round of a tournament:
-- id1: the first player's unique id
-- name1: the first player's name
-- id2: the second player's unique id
-- name2: the second player's name
CREATE TABLE pairings ( --as a VIEW ?
  id_match INTEGER PRIMARY KEY,
  player1 INTEGER,
  name_player1 TEXT,
  player2 INTEGER,
  name_player2 TEXT);
o