
class Skater:
    def __init__(self, name, team, position, games, toiAll):
        self.name = name
        self.team = team
        self.position = position
        self.games = games
        self.toiALL = toiAll

    def __str__(self):
        line1 = self.name + ', ' + self.team + ', ' + '{0:.2f}'.format(self.toiALL) + 'min \n'
        line2 = 'Total ORating: ' + "{0:.4f}".format(self.offensiveRating) + '\n'
        line3 = '5v5 ORating: ' + "{0:.4f}".format(self.evOffensiveRating) + '\n'
        line4 = 'PP ORating: ' + "{0:.4f}".format(self.ppOffensiveRating) + '\n'
        line5 = 'PK ORating: ' + "{0:.4f}".format(self.pkOffensiveRating) + '\n'
        line6 = 'IPP: ' + str(self.iPointPercentage) + '\n'#' : ' +str(self.iPointPercentage * 0.03) + '\n'
        return line1 + line2 + line3 + line4 + line5 + line6

    offensiveRating = 0
    evOffensiveRating = 0
    ppOffensiveRating = 0
    pkOffensiveRating = 0

    toi5v5 = 0
    goals5v5 = 0
    fAssists5v5 = 0
    sAssists5v5 = 0
    iPointPercentage = 0
    iTeamPointPercentage = 0

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
    faceoffsLost = 0

    drawnPenalties = 0
    minorPenalties = 0
    majorPenalties = 0
    misconductPenalties = 0
    badPenalties = 0 # Penalty Taken while already on special teams

    evixG = 0
    eviCF = 0
    eviFF = 0
    eviSF = 0
    eviSCF = 0
    eviHDCF = 0

    ppixG = 0
    ppiCF = 0
    ppiFF = 0
    ppiSF = 0
    ppiSCF = 0
    ppiHDCF = 0

    pkixG = 0
    pkiCF = 0
    pkiFF = 0
    pkiSF = 0
    pkiSCF = 0
    pkiHDCF = 0

    ppGoalTo5v5Weight = 0.7
    pkGoalTo5v5Weight = 1.5
    fAssistToGoalWeight = 0.7
    sAssistToGoalWeight = 0.5

    defenceGoalWeight = 2.2
    defenceFAssistWeight = 1.25
    defenceSAssistWeight = 1.05

    ppForwardShotWeight = 0.65
    pkForwardShotWeight = 2.00

    evDefenceShotWeight = 1.45
    ppDefenceShotWeight = 0.65
    pkDefenceShotWeight = 2.50

    evPointsRating = 0
    ppPointsRating = 0
    pkPointsRating = 0

    evShotsRating = 0
    ppShotsRating = 0
    pkShotsRating = 0

    def calcOffensiveRating(self):
        self.offensiveRating = 0
        self.ppOffensiveRating = 0
        self.pkOffensiveRating = 0

        self.calcOffensivePointsRating()
        self.calcOffensiveShotsRating()

        self.offensiveRating += (self.evOffensiveRating + self.ppOffensiveRating + self.pkOffensiveRating)

        evORatingPer60 = 0
        ppORatingPer60 = 0
        pkORatingPer60 = 0

        ppWeight = self.toiPP / self.toiALL
        pkWeight = self.toiPK / self.toiALL

        if (self.toi5v5 > 0):
            evORatingPer60 = self.offensiveRating / (self.toi5v5 / 60)
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

    #
    #   Offensive Points Rating
    #
    def calcOffensivePointsRating(self):
        toiAllWeight = self.toiALL / self.games * 0.05

        if (self.iTeamPointPercentage != '-'):
            TPP = self.iTeamPointPercentage * 0.05
        else:
            TPP = 1
            #qotFactor

        if (self.iPointPercentage != '-'):
            IPP = self.iPointPercentage  * 0.05
        else:
            IPP = 1

        #print ("TPP  " + str(TPP) + " IPP " + str(IPP))

        evG = self.goals5v5 * 1
        evA1 = self.fAssists5v5 * self.fAssistToGoalWeight
        evA2 = self.sAssists5v5 * self.sAssistToGoalWeight

        ppG = self.ppGoals * self.ppGoalTo5v5Weight
        ppA = self.ppAssists * self.fAssistToGoalWeight * self.ppGoalTo5v5Weight

        pkG = self.pkGoals * self.pkGoalTo5v5Weight
        pkA = self.pkAssists * self.fAssistToGoalWeight * self.pkGoalTo5v5Weight

        if (self.position == "D"):
            self.evPointsRating += evG * self.defenceGoalWeight
            self.evPointsRating += evA1 * self.defenceFAssistWeight
            self.evPointsRating += evA2 * self.defenceSAssistWeight

            self.ppPointsRating += ppG * self.defenceGoalWeight
            self.ppPointsRating += ppA * self.defenceFAssistWeight

            self.pkPointsRating += pkG * self.defenceGoalWeight
            self.pkPointsRating += pkA * self.defenceFAssistWeight
        else:
            self.evPointsRating += evG
            self.evPointsRating += evA1
            self.evPointsRating += evA2

            self.ppPointsRating += ppG
            self.ppPointsRating += ppA

            self.pkPointsRating += pkG
            self.pkPointsRating += pkA


        self.evOffensiveRating += self.evPointsRating * (IPP + TPP)
        self.ppOffensiveRating += self.ppPointsRating * (IPP + TPP)
        self.pkOffensiveRating += self.pkPointsRating * (IPP + TPP)

        self.evOffensiveRating *= toiAllWeight
        self.ppOffensiveRating *= toiAllWeight
        self.pkOffensiveRating *= toiAllWeight


    #
    #   Offensive Shots Rating
    #
    # Each of these stats are including the weighting of of the stats above it in the block
    #   eviCF = even strength individual Corsi For
    #   eviCF = even strength individual Fenwick For
    #   eviSF = even strength individual Shots For
    #   eviSCF = even strength individual Scoring Chances For
    #   eviSCF = even strength individual High-Danger Scoring Chances For
    #
    def calcOffensiveShotsRating(self):
        CFWeight = 0.040
        FFWeight = 0.020
        SFWeight = 0.020
        SCFWeight = 0.020
        HDCFWeight = 0.150

        #
        #   Even Strength (5v5)
        #
        eviCF = self.eviCF * CFWeight
        eviFF = self.eviFF * FFWeight
        eviSF = self.eviSF * SFWeight
        eviSCF = self.eviSCF * SCFWeight
        eviHDCF = self.eviHDCF * HDCFWeight

        evShotsRating = eviCF + eviFF + eviSF + eviSCF + eviHDCF

        if (self.position == "D"):
            self.evOffensiveRating += evShotsRating * self.evDefenceShotWeight
        else:
            self.evOffensiveRating += evShotsRating

        #
        #   Powerplay
        #
        ppiCF = self.ppiCF * CFWeight
        ppiFF = self.ppiFF * FFWeight
        ppiSF = self.ppiSF * SFWeight
        ppiSCF = self.ppiSCF * SCFWeight
        ppiHDCF = self.ppiHDCF * HDCFWeight

        ppShotsRating = ppiCF + ppiFF + ppiSF + ppiSCF + ppiHDCF

        if (self.position == "D"):
            self.ppOffensiveRating += ppShotsRating * self.ppDefenceShotWeight
        else:
            self.ppOffensiveRating += ppShotsRating * self.ppForwardShotWeight

        #
        #   Penalty Kill
        #
        pkiCF = self.pkiCF * CFWeight
        pkiFF = self.pkiFF * FFWeight
        pkiSF = self.pkiSF * SFWeight
        pkiSCF = self.pkiSCF * SCFWeight
        pkiHDCF = self.pkiHDCF * HDCFWeight

        pkShotsRating = pkiCF + pkiFF + pkiSF + pkiSCF + pkiHDCF

        if (self.position == "D"):
            self.pkOffensiveRating += pkShotsRating * self.pkDefenceShotWeight
        else:
            self.pkOffensiveRating += pkShotsRating * self.pkForwardShotWeight