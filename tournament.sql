-- Table definitions for the tournament project.
--
-- Put your SQL 'create table' statements in this file; also 'create view'
-- statements if you choose to use it.
--
-- You can write comments in this file by starting them with two dashes, like
-- these lines here.

-- \q: disconnect from database.
-- \i tournament.sql: to run commands in this file.
-- \dt : list table in this database.
-- \d+ table_name: describe table.
DROP DATABASE IF EXISTS tournament;
CREATE DATABASE tournament;
\connect tournament;
CREATE TABLE players (
    id    serial primary key,
    name  text
  );
CREATE TABLE matches (
    winner int references players(id),
    loser int references players(id)
  );

CREATE VIEW win_records (player, win_number) AS
  SELECT id,  COUNT(winner) AS win_number FROM players LEFT JOIN matches
    ON id = winner GROUP BY id ORDER BY win_number;

CREATE VIEW loss_records (player, loss_number) AS
  SELECT id, COUNT(loser) AS loss_number FROM players LEFT JOIN matches 
    ON id = loser GROUP BY id ORDER BY loss_number;

CREATE VIEW records (player, win_number, loss_number) AS
  SELECT win_records.player, win_number, loss_number FROM 
    win_records JOIN loss_records on win_records.player = loss_records.player;

CREATE VIEW standings (player, name, win_number, played_matches) AS
  SELECT player, name, win_number, win_number + loss_number as played_matches
    FROM players JOIN records on players.id = records.player
      ORDER BY win_number DESC,  played_matches;

-- DEBUG USAGE
-- INSERT INTO players (name) VALUES ('A');
-- INSERT INTO players (name) VALUES ('B');
-- INSERT INTO players (name) VALUES ('C');
-- INSERT INTO matches (winner, loser) VALUES (1, 2);
-- select * from win_records;
-- select * from loss_records;
-- select * from records;
-- select * from standings;
