class Skater:
    def __init__(self, name, team, position, games):
        self.name = name
        self.team = team
        self.position = position
        self.games = games

    def __str__(self):
        line1 = self.name + ', ' + self.team + ', ' + '{0:.2f}'.format(self.toiALL) + 'min \n'
        line2 = 'Total ORating: ' + "{0:.4f}".format(self.offensiveRating) + '\n'
        line3 = '5v5 ORating: ' + "{0:.4f}".format(self.evOffensiveRating) + '\n'
        line4 = 'PP ORating: ' + "{0:.4f}".format(self.ppOffensiveRating) + '\n'
        line5 = 'PK ORating: ' + "{0:.4f}".format(self.pkOffensiveRating) + '\n'
        line6 = 'IPP: ' + str(self.iPointPercentage) + ' : ' +str(self.iPointPercentage * 0.03) + '\n'
        return line1 + line2 + line3 + line4 + line5 + line6

    offensiveRating = 0
    evOffensiveRating = 0
    ppOffensiveRating = 0
    pkOffensiveRating = 0

    toiALL = 0

    toi5v5 = 0
    goals5v5 = 0
    fAssists5v5 = 0
    sAssists5v5 = 0
    shots5v5 = 0
    iPointPercentage = 0

    # PP Stats
    toiPP = 0
    ppGoals = 0
    ppAssists = 0

    # PK Stats
    toiPK = 0
    pkGoals = 0
    pkAssists = 0

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

    ppGoalTo5v5Weight = 0.6
    pkGoalTo5v5Weight = 1.5
    fAssistToGoalWeight = 0.8
    sAssistToGoalWeight = 0.6

    defenceGoalWeight = 2.2
    defenceFAssistWeight = 1.25
    defenceSAssistWeight = 1.05

    def calcOffensiveRating(self):
        self.offensiveRating = 0
        self.ppOffensiveRating = 0
        self.pkOffensiveRating = 0

        ppWeight = self.toiPP / self.toiALL
        pkWeight = self.toiPK / self.toiALL

        if (self.iPointPercentage != '-'):
            IPP = self.iPointPercentage  * 0.05
        else:
            IPP = 1

        if (self.position == "D"):
            self.evOffensiveRating += ((self.goals5v5 * 1) * self.defenceGoalWeight) * IPP
            self.evOffensiveRating += ((self.fAssists5v5 * self.fAssistToGoalWeight) * self.defenceFAssistWeight) * IPP
            self.evOffensiveRating += ((self.sAssists5v5 * self.sAssistToGoalWeight) * self.defenceSAssistWeight) * IPP

            self.ppOffensiveRating += ((self.ppGoals * self.ppGoalTo5v5Weight) * self.defenceGoalWeight)
            self.ppOffensiveRating += ((self.ppAssists * (self.fAssistToGoalWeight * self.ppGoalTo5v5Weight)) * self.defenceFAssistWeight)

            self.pkOffensiveRating += ((self.pkGoals * self.pkGoalTo5v5Weight) * self.defenceGoalWeight)
            self.pkOffensiveRating += ((self.pkAssists * (self.fAssistToGoalWeight * self.pkGoalTo5v5Weight)) * self.defenceFAssistWeight)
        else:
            self.offensiveRating += (self.goals5v5 * 1) * IPP
            self.offensiveRating += (self.fAssists5v5 * self.fAssistToGoalWeight) * IPP
            self.offensiveRating += (self.sAssists5v5 * self.sAssistToGoalWeight) * IPP

            self.ppOffensiveRating += (self.ppGoals * self.ppGoalTo5v5Weight)
            self.ppOffensiveRating += (self.ppAssists * self.fAssistToGoalWeight * self.ppGoalTo5v5Weight)

            self.pkOffensiveRating += (self.pkGoals * self.pkGoalTo5v5Weight)
            self.pkOffensiveRating += (self.pkAssists * self.fAssistToGoalWeight * self.pkGoalTo5v5Weight)

        self.offensiveRating += self.evOffensiveRating
        self.offensiveRating += self.ppOffensiveRating
        self.offensiveRating += self.pkOffensiveRating

        evORatingPer60 = self.offensiveRating / (self.toi5v5 / 60)
        ppORatingPer60 = 0
        pkORatingPer60 = 0

        if (self.toiPP > 0):
            ppORatingPer60 = self.ppOffensiveRating / (self.toiPP / 60) * ppWeight
        if (self.toiPK > 0):
            pkORatingPer60 = self.pkOffensiveRating / (self.toiPK / 60) * pkWeight

        self.evOffensiveRating = evORatingPer60
        self.ppOffensiveRating = ppORatingPer60
        self.pkOffensiveRating = pkORatingPer60

        ORatingPer60 = evORatingPer60 + ppORatingPer60 + pkORatingPer60

        self.offensiveRating = ORatingPer60
        return ORatingPer60