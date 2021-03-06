#!/usr/bin/env python
# Test cases for tournament.py

from tournament import *

def testDeleteMatches():
    deleteMatches()
    print "1. Old matches can be deleted."


def testDelete():
    deleteMatches()
    deletePlayers()
    print "2. Player records can be deleted."


def testCount():
    deleteMatches()
    deletePlayers()
    c = countPlayers()
    if c == '0':
        raise TypeError(
            "countPlayers() should return numeric zero, not string '0'.")
    if c != 0:
        raise ValueError("After deleting, countPlayers should return zero.")
    print "3. After deleting, countPlayers() returns zero."


def testRegister():
    deleteMatches()
    deletePlayers()
    registerPlayer("Chandra Nalaar")
    c = countPlayers()
    if c != 1:
        raise ValueError(
            "After one player registers, countPlayers() should be 1.")
    print "4. After registering a player, countPlayers() returns 1."


def testRegisterCountDelete():
    deleteMatches()
    deletePlayers()
    registerPlayer("Markov Chaney")
    registerPlayer("Joe Malik")
    registerPlayer("Mao Tsu-hsi")
    registerPlayer("Atlanta Hope")
    c = countPlayers()
    if c != 4:
        raise ValueError(
            "After registering four players, countPlayers should be 4.")
    deletePlayers()
    c = countPlayers()
    if c != 0:
        raise ValueError("After deleting, countPlayers should return zero.")
    print "5. Players can be registered and deleted."


def testStandingsBeforeMatches():
    deleteMatches()
    deletePlayers()
    registerPlayer("Melpomene Murray")
    registerPlayer("Randy Schwartz")
    standings = playerStandings()
    if len(standings) < 2:
        raise ValueError("Players should appear in playerStandings even before "
                         "they have played any matches.")
    elif len(standings) > 2:
        raise ValueError("Only registered players should appear in standings.")
    if len(standings[0]) != 4:
        raise ValueError("Each playerStandings row should have four columns.")
    [(id1, name1, wins1, matches1), (id2, name2, wins2, matches2)] = standings
    if matches1 != 0 or matches2 != 0 or wins1 != 0 or wins2 != 0:
        raise ValueError(
            "Newly registered players should have no matches or wins.")
    if set([name1, name2]) != set(["Melpomene Murray", "Randy Schwartz"]):
        raise ValueError("Registered players' names should appear in standings, "
                         "even if they have no matches played.")
    print "6. Newly registered players appear in the standings with no matches."


def testReportMatches():
    deleteMatches()
    deletePlayers()
    registerPlayer("Bruno Walton")
    registerPlayer("Boots O'Neal")
    registerPlayer("Cathy Burton")
    registerPlayer("Diane Grant")
    standings = playerStandings()
    [id1, id2, id3, id4] = [row[0] for row in standings]
    reportMatch(id1, id2)
    reportMatch(id3, id4)
    standings = playerStandings()
    for (i, n, w, m) in standings:
        if m != 1:
            raise ValueError("Each player should have one match recorded.")
        if i in (id1, id3) and w != 1:
            raise ValueError("Each match winner should have one win recorded.")
        elif i in (id2, id4) and w != 0:
            raise ValueError("Each match loser should have zero wins recorded.")
    print "7. After a match, players have updated standings."


def testPairings():
    deleteMatches()
    deletePlayers()
    registerPlayer("Twilight Sparkle")
    registerPlayer("Fluttershy")
    registerPlayer("Applejack")
    registerPlayer("Pinkie Pie")
    standings = playerStandings()
    [id1, id2, id3, id4] = [row[0] for row in standings]
    reportMatch(id1, id2)
    reportMatch(id3, id4)
    pairings = swissPairings()
    if len(pairings) != 2:
        raise ValueError(
            "For four players, swissPairings should return two pairs.")
    [(pid1, pname1, pid2, pname2), (pid3, pname3, pid4, pname4)] = pairings
    correct_pairs = set([frozenset([id1, id3]), frozenset([id2, id4])])
    actual_pairs = set([frozenset([pid1, pid2]), frozenset([pid3, pid4])])
    if correct_pairs != actual_pairs:
        raise ValueError(
            "After one match, players with one win should be paired.")
    print "8. After one match, players with one win are paired."


def testPairingsOddPlayers():
    deleteMatches()
    deletePlayers()
    registerPlayer("A")
    registerPlayer("B")
    registerPlayer("C")
    registerPlayer("D")
    registerPlayer("E")
    standings = playerStandings()
    [id1, id2, id3, id4, id5] = [row[0] for row in standings]

    pairings = swissPairings()
    
    if len(pairings) != 2:
        raise ValueError(
            "For five players, swissPairings should return two pairs.")
    [(pid1, pname1, pid2, pname2), (pid3, pname3, pid4, pname4)] = pairings

    bye_id = (set([id1, id2, id3, id4, id5]) - set([pid1, pid2, pid3, pid4])).pop()

    reportMatch(pid1, pid2)
    reportMatch(pid3, pid4)

    one_win_ids = [pid1, pid3, bye_id]
    one_loss_ids = [pid2, pid4]

    pairings = swissPairings()
    
    if len(pairings) != 2:
        raise ValueError(
            "For five players, swissPairings should return two pairs.")

    [(pid1, pname1, pid2, pname2), (pid3, pname3, pid4, pname4)] = pairings

    if bye_id not in [pid1, pid2, pid3, pid4]:
        raise ValueError(
            "Player should not get two byes")

    def _has_different_wins(id_x, id_y):
        return ((id_x in one_win_ids and id_y in one_loss_ids) or
                (id_x in one_loss_ids and id_y in one_win_ids))

    if (_has_different_wins(pid1, pid2) and _has_different_wins(pid3, pid4)):
        raise ValueError("Pairing error. Player with more wins should be paired")

    print "9. swissPairings can handle odd number players."


def testStandingsByPointsBeforeMatches():
    deleteMatches()
    deletePlayers()
    registerPlayer("Melpomene Murray")
    registerPlayer("Randy Schwartz")
    standings = playerStandingsByPoints()
    if len(standings) < 2:
        raise ValueError("Players should appear in playerStandings even before "
                         "they have played any matches.")
    elif len(standings) > 2:
        raise ValueError("Only registered players should appear in standings.")
    if len(standings[0]) != 5:
        raise ValueError("Each playerStandings row should have five columns.")
    [(id1, name1, points1, omw1, matches1), (id2, name2, points2, omw2, matches2)] = standings
    if matches1 != 0 or matches2 != 0 or points1!= 0 or points2!= 0:
        raise ValueError(
            "Newly registered players should have no matches or points.")
    if omw1!= 0 or omw2 != 0 :
        raise ValueError(
            "Newly registered players should have no omw.")
    if set([name1, name2]) != set(["Melpomene Murray", "Randy Schwartz"]):
        raise ValueError("Registered players' names should appear in standings, "
                         "even if they have no matches played.")
    print "10. Newly registered players appear in the standings with no matches."


def testReportMatchesWithDraw():
    deleteMatches()
    deletePlayers()
    registerPlayer("Bruno Walton")
    registerPlayer("Boots O'Neal")
    registerPlayer("Cathy Burton")
    registerPlayer("Diane Grant")
    standings = playerStandings()
    [id1, id2, id3, id4] = [row[0] for row in standings]
    reportMatch(id1, id2, is_draw=False)
    reportMatch(id3, id4, is_draw=False)
    reportMatch(id1, id3, is_draw=True)
    reportMatch(id2, id4, is_draw=True)
    reportMatch(id2, id3, is_draw=False)
    reportMatch(id1, id4, is_draw=True)
    #   id   win    loss   draw   points
    #  id1    1        0      2        5
    #  id2    1        1      1        4
    #  id3    1        1      1        4
    #  id4    0        1      2        2
    standings = playerStandingsByPoints()
    if standings[0][0] != id1 or standings[3][0] != id4:
        raise ValueError("Standing by points has wrong rank.")
    if ((standings[0][2], standings[1][2], standings[2][2], standings[3][2]) !=
        (5, 4, 4, 2)):
        raise ValueError("Standing by points has wrong points.")
    print "11, Standing by points is correct."


def testReportMatchesWithDrawRankByOpponentWins():
    deleteMatches()
    deletePlayers()
    registerPlayer("A")
    registerPlayer("B")
    registerPlayer("C")
    registerPlayer("D")
    registerPlayer("E")
    registerPlayer("F")
    registerPlayer("G")
    standings = playerStandings()
    [id1, id2, id3, id4, id5, id6, id7] = [row[0] for row in standings]
    reportMatch(id1, id2, is_draw=False);
    reportMatch(id3, id4, is_draw=False);
    reportMatch(id1, id3, is_draw=True);
    reportMatch(id2, id5, is_draw=True);
    reportMatch(id2, id3, is_draw=False);
    reportMatch(id1, id4, is_draw=True);
    reportMatch(id5, id6, is_draw=False);

    # records:
    # player | win_number | loss_number | draw_number
    #--------+------------+-------------+------------
    #      1 |          1 |           0 |           2
    #      2 |          1 |           1 |           1
    #      3 |          1 |           1 |           1
    #      4 |          0 |           1 |           1
    #      5 |          1 |           0 |           1
    #      6 |          0 |           1 |           0
    #      7 |          0 |           0 |           0
    #
    # standings ranked by points, omw, and played_matches.
    # player | name | points | omw | played_matches
    #--------+------+--------+-----+----------------
    #      1 | A    |      5 |   2 |              3
    #      2 | B    |      4 |   3 |              3
    #      3 | C    |      4 |   2 |              3
    #      5 | E    |      4 |   1 |              2
    #      4 | D    |      1 |   2 |              2
    #      6 | F    |      0 |   1 |              1
    #      7 | G    |      0 |   0 |              0

    standings = playerStandingsByPoints()
    standings_ids = [x[0] for x in standings]
    
    if standings_ids != [id1, id2, id3, id5, id4, id6, id7]:
        raise ValueError("Standing by points has wrong rank.")
    print ("12, Standing by points can use opponent match wins to rank players"
           " with same points.")

if __name__ == '__main__':
    testDeleteMatches()
    testDelete()
    testCount()
    testRegister()
    testRegisterCountDelete()
    testStandingsBeforeMatches()
    testReportMatches()
    testPairings()
    testPairingsOddPlayers()
    testStandingsByPointsBeforeMatches()
    testReportMatchesWithDraw()
    testReportMatchesWithDrawRankByOpponentWins()
    print "Success!  All tests pass!"
