# tournament

To execute this project:
- Clone https://github.com/udacity/fullstack-nanodegree-vm and follow the [instructions](https://www.udacity.com/wiki/ud197/install-vagrant) in Udacity "Intro to Relational Databases" course to install vagrant.
- `vagrant up`
- `vagrant ssh`
- Clone this project and put it under /vagrant
- `vagrant@vagrant-ubuntu-trusty-32:/vagrant/tournament$ psql`
- `vagrant=> \i tournament.sql`
- `python tournament_test.py` and see all tests pass.

All the sorting, aggregation are done in database.

These extra features are implemented:

- Support odd number of players, where a "bye" counts as one win, and player can not get more than one bye.
- Support draw (reportMatch method has a new argument is_draw).
- Rank players by points (win = 3, draw = 1, loss = 0).
- Rank players with the same points by Opponent Match Wins (OMW). Note that if A has played with B twice, the number of wins of B will be counted twice when calculating A's OMW.
 
