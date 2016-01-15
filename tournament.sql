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

CREATE VIEW draw_records (player, draw_number) AS
  SELECT id, COUNT(is_draw) AS draw_number FROM players LEFT JOIN matches 
    ON (id = loser OR id = winner) AND is_draw = TRUE GROUP BY id;

CREATE VIEW records (player, win_number, loss_number, draw_number) AS
  SELECT win_records.player, win_number, loss_number, draw_number FROM 
    win_records JOIN loss_records on win_records.player = loss_records.player
      JOIN draw_records on win_records.player = draw_records.player;

-- Note that win_number and played_matches in this table includes bye.
CREATE VIEW standings (player, name, win_number, played_matches) AS
  SELECT player, name, win_number,
    win_number + loss_number + draw_number as played_matches
    FROM players JOIN records on players.id = records.player
      ORDER BY win_number DESC,  played_matches;

-- A win is 3 points, a draw is 1 point, and a loss is 0 point.
CREATE VIEW points_table (player, points) AS
  SELECT player, win_number * 3 + draw_number * 1 FROM records;

CREATE VIEW standing_by_points (player, name, points, played_matches) AS
  SELECT id as player, name, points,
    win_number + loss_number + draw_number as played_matches
    FROM players JOIN records on players.id = records.player
      JOIN points_table on players.id = points_table.player
        ORDER BY points DESC,  played_matches;

CREATE VIEW matches_with_winner_wins(winner, winner_wins, loser) AS
  SELECT winner, win_number, loser
    FROM matches JOIN records ON winner = records.player;

CREATE VIEW matches_with_winner_wins_loser_wins(
    winner, winner_wins, loser, loser_wins) AS
  SELECT winner, winner_wins, loser, records.win_number
    FROM matches_with_winner_wins JOIN records ON loser = records.player;

-- For example, there are two games, A wins B, A wins C
-- Get this view:
-- player1    player1_wins   player2    player2_wins
----------------------------------------------------
--       A          A_wins         B          B_wins
--       A          A_wins         C          C_wins
--       B          B_wins         A          A_wins
--       C          C_wins         A          A_wins
-- 
-- Row 3 and row 4 are the reverse of row 1 and row2, and is unioned.
-- Then, we can get opponent match wins by a sum(player2_wins) group by player1.

CREATE VIEW matches_with_winner_wins_loser_wins_reverse_union(player1, player1_wins, player2, player2_wins) AS
  SELECT winner AS player1, winner_wins AS player1_wins,
        loser AS player2, loser_wins AS player2_wins FROM
    matches_with_winner_wins_loser_wins
  UNION ALL
  SELECT loser AS player1, loser_wins AS player1_wins,
         winner AS player2, winner_wins AS player2_wins FROM
    matches_with_winner_wins_loser_wins
  ORDER BY player1, player2;

-- Gets opponent wins for players who had played at least one match.
CREATE VIEW opponent_wins_played (player, opp_wins) AS
  SELECT player1 as player, SUM(player2_wins) FROM
    matches_with_winner_wins_loser_wins_reverse_union
      GROUP BY player1 ORDER BY player1;

-- Gets opponent wins for all players.
CREATE VIEW opponent_wins(player, opp_wins) AS
  SELECT id as player, COALESCE(opponent_wins_played.opp_wins, 0) FROM
    players LEFT JOIN opponent_wins_played
      ON players.id = opponent_wins_played.player;

-- Rank players by points DESC, opponent match wins DESC, then played matches.
CREATE VIEW standing_by_points_and_omw (player, name, points, omw, played_matches) AS
  SELECT standing_by_points.player, name, points, opponent_wins.opp_wins AS omw, played_matches
    FROM standing_by_points JOIN opponent_wins
      ON standing_by_points.player = opponent_wins.player
        ORDER BY points DESC,  omw DESC, played_matches;

-- DEBUG USAGE
-- INSERT INTO players (name) VALUES ('A');
-- INSERT INTO players (name) VALUES ('B');
-- INSERT INTO players (name) VALUES ('C');
-- INSERT INTO players (name) VALUES ('D');
-- INSERT INTO players (name) VALUES ('E');
-- INSERT INTO players (name) VALUES ('F');
-- INSERT INTO players (name) VALUES ('G');
-- INSERT INTO matches (winner, loser, is_draw) VALUES (1, 2, false);
-- INSERT INTO matches (winner, loser, is_draw) VALUES (3, 4, false);
-- INSERT INTO matches (winner, loser, is_draw) VALUES (1, 3, true);
-- INSERT INTO matches (winner, loser, is_draw) VALUES (2, 5, true);
-- INSERT INTO matches (winner, loser, is_draw) VALUES (2, 3, false);
-- INSERT INTO matches (winner, loser, is_draw) VALUES (1, 4, true);
-- INSERT INTO matches (winner, loser, is_draw) VALUES (5, 6, false);
-- select * from draw_records;
-- select * from records; 
-- select * from points_table; 
-- select * from standings;
-- select * from standing_by_points; 
-- select * from opponent_wins;
-- select * from standing_by_points_and_omw;
