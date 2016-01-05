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
    id    serial,
    name  text
  );
