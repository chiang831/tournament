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
    loser int references players(id),
    is_draw boolean
  );
CREATE TABLE byes (
    player int references players(id) UNIQUE
  );

CREATE VIEW byes_with_fake_wins (player, wins) AS
  SELECT player, 1 FROM byes;

CREATE VIEW bye_counts (player, bye_number) AS
  SELECT id, COUNT(wins) FROM players LEFT JOIN byes_with_fake_wins
    ON id = byes_with_fake_wins.player GROUP BY id;

CREATE VIEW bye_candidate(player) AS
  SELECT player FROM bye_counts WHERE bye_number = 0 LIMIT 1;

CREATE VIEW win_by_matches (player, wins) AS
  SELECT id, COUNT(winner) AS wins FROM players LEFT JOIN matches
    ON id = winner AND is_draw = FALSE GROUP BY id ORDER BY wins;

-- Union win by matches and win by byes.
CREATE VIEW win_records (player, win_number) AS
  SELECT player, SUM(wins) AS win_number
    FROM (select * from win_by_matches UNION ALL
          select * from byes_with_fake_wins) as subq
      GROUP BY player ORDER BY win_number;

CREATE VIEW loss_records (player, loss_number) AS
  SELECT id, COUNT(loser) AS loss_number FROM players LEFT JOIN matches 
    ON id = loser AND is_draw = FALSE GROUP BY id ORDER BY loss_number;

CREATE VIEW records (player, win_number, loss_number) AS
  SELECT win_records.player, win_number, loss_number FROM 
    win_records JOIN loss_records on win_records.player = loss_records.player;

-- Note that win_number and played_matches in this table includes bye.
CREATE VIEW standings (player, name, win_number, played_matches) AS
  SELECT player, name, win_number, win_number + loss_number as played_matches
    FROM players JOIN records on players.id = records.player
      ORDER BY win_number DESC,  played_matches;

-- DEBUG USAGE
-- INSERT INTO players (name) VALUES ('A');
-- INSERT INTO players (name) VALUES ('B');
-- INSERT INTO players (name) VALUES ('C');
-- INSERT INTO matches (winner, loser, is_draw) VALUES (1, 2, false);
-- INSERT INTO matches (winner, loser, is_draw) VALUES (1, 3, true);
-- select * from win_records;
-- select * from loss_records;
-- select * from records;
-- select * from standings;
