class League:
    def __init__(self, year, jornadas):
        self.year = year
        self.jornadas = jornadas

    def __str__(self):
        return "League {}\n{}".format(self.year, "\n".join(
            [str(jornada) for jornada in self.jornadas]))


class Jornada:
    def __init__(self, id, matches):
        self.id = id
        self.matches = matches

    def __str__(self):
        return "Jornada {}\n{}".format(self.id, "\n".join(
            [str(match) for match in self.matches]))


class Match:
    def __init__(self, date, stadium, team_A, team_B, score_team_A,
                 score_team_B):

        self.team_A = team_A
        self.logo_team_A = team_A + '.jpg'
        self.team_B = team_B
        self.logo_team_B = team_B + '.jpg'
        self.score_team_A = score_team_A
        self.score_team_B = score_team_B
        self.date = date
        self.stadium = stadium

    def get_winner(self):
        if self.score_team_A == self.score_team_B:  # Draw
            return 'Draw'
        elif self.score_team_A > self.score_team_B:  # Team A won
            return self.team_A
        else:  # Team B won
            return self.team_B

    def get_winner_as_numeric(self):
        if self.score_team_A == self.score_team_B:  # Draw
            return 0
        elif self.score_team_A > self.score_team_B:  # Team A won
            return 1
        else:  # Team B won
            return 2

    def __str__(self):
        return "{} {} {}({}) vs {} ({}) --- {}-{} ({} {})".format(self.date,
                                                                  self.stadium,
                                                                  self.team_A,
                                                                  self.logo_team_A,
                                                                  self.team_B,
                                                                  self.logo_team_B,
                                                                  self.score_team_A,
                                                                  self.score_team_B,
                                                                  self.get_winner(),
                                                                  self.get_winner_as_numeric())
