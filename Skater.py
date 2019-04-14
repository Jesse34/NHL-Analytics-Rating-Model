class Skater:
    def __init__(self, name, team, position, games):
        self.name = name
        self.team = team
        self.position = position
        self.games = games

    def __str__(self):
        return self.name + ', ' + self.team

    offensiveRating = 0
    ppOffensiveRating = 0
    pkOffensiveRating = 0

    toi5v5 = 0
    goals5v5 = 0
    fAssists5v5 = 0
    sAssists5v5 = 0
    shots5v5 = 0
    iPointPercentage = 0

    # PP Stats
    ppGoals = 0
    ppAssists = 0

    hits = 0
    hitsAgainst = 0
    shotsBlocked = 0
    faceoffsWon = 0
    faceofsLost = 0

    drawnPenalties = 0
    minorPenalties = 0
    majorPenalties = 0
    misconductPenalties = 0
    badPenalties = 0 # Penalty Taken while already on special teams

    ixG = 0
    iCF = 0
    iFF = 0
    iSCF = 0
    iHDCF = 0

    ppGoalTo5v5Weight = 0.36
    pkGoalTo5v5Weight = 2.20
    fAssistToGoalWeight = 0.8
    sAssistToGoalWeight = 0.6

    def calcOffensiveRating(self):
        self.offensiveRating = 0
        self.ppOffensiveRating = 0
        self.pkOffensiveRating = 0

        self.offensiveRating += (self.goals5v5 * 1)
        self.offensiveRating += (self.fAssists5v5 * self.fAssistToGoalWeight)
        self.offensiveRating += (self.sAssists5v5 * self.sAssistToGoalWeight)

        self.pkOffensiveRating += (self.ppGoals * self.ppGoalTo5v5Weight)
        self.pkOffensiveRating += (self.ppAssists * (self.fAssistToGoalWeight * self.ppGoalTo5v5Weight))
        self.offensiveRating += self.pkOffensiveRating

        oRatingPer60 = self.offensiveRating / (self.toi5v5 / 60)
        self.offensiveRating = oRatingPer60

        return oRatingPer60