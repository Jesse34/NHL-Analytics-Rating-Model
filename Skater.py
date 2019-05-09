class Skater:
    def __init__(self, name, team, position, games, toiAll, shPerc):
        self.name = name
        self.team = team
        self.position = position
        self.games = games
        self.toiALL = toiAll
        self.shPercentage = shPerc

    def __str__(self):
        """
        Displays:
         - Name, Team, Position, Time on Ice
         - Total Offensive Rating
         - Offensive Ratings for each of the 3 situations (even, pp, pk)
         - Offensive Points Ratings
         - Offensive Shots Ratings
        :return: Skater Object data string
        """
        line1 = self.name + ', ' + self.position + ', ' + self.team + ', ' + '{0:.2f}'.format(self.toiALL) + 'min \n'
        line2 = 'Total ORating: ' + "{0:.4f}".format(self.offensiveRating) + '\n'
        line3 = '5v5 ORating: ' + "{0:.4f}".format(self.evOffensiveRating) + '\n'
        line4 = 'PP ORating: ' + "{0:.4f}".format(self.ppOffensiveRating) + '\n'
        line5 = 'PK ORating: ' + "{0:.4f}".format(self.pkOffensiveRating) + '\n'
        line6 = 'Offensive Points Rating: ' + "{0:.4f}".format(self.offensivePointsRating) + '\n'
        line7 = 'Offensive Shots Rating: ' + "{0:.4f}".format(self.offensiveShotsRating) + '\n'
        return line1 + line2 + line3 + line4 + line5 + line6 + line7

    # Declaring variables to store any applicable data
    # Some of this isn't used yet and some of it should be moved into a different "Model" class to cut down on the clutter
    offensiveRating = 0
    offensivePointsRating = 0
    offensiveShotsRating = 0

    evOffensiveRating = 0
    ppOffensiveRating = 0
    pkOffensiveRating = 0

    evShotQualityAdjustment = 0
    ppShotQualityAdjustment = 0
    pkShotQualityAdjustment = 0

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
        """
        Calculate a Rating to combine a Player's total Offensive Output per 60min of play.
        This looks at Even Strength, Penalty Kill, and Powerplay situations
        Goals/Assists & Shooting output data in each situation will have their values weighted and added up.
        :return: Overall Offensive Rating
        """
        toiAllWeight = self.toiALL / self.games * 0.05

        self.offensiveRating = 0
        self.ppOffensiveRating = 0
        self.pkOffensiveRating = 0

        self.calcOffensivePointsRating()
        self.evOffensiveRating += self.evPointsRating
        self.ppOffensiveRating += self.ppPointsRating
        self.pkOffensiveRating += self.pkPointsRating

        self.calcOffensiveShotsRating()
        self.evOffensiveRating += self.evShotsRating
        self.ppOffensiveRating += self.ppShotsRating
        self.pkOffensiveRating += self.pkShotsRating

        self.offensiveRating += (self.evOffensiveRating + self.ppOffensiveRating + self.pkOffensiveRating)

        self.offensiveRating *= toiAllWeight

        evORatingPer60 = 0
        ppORatingPer60 = 0
        pkORatingPer60 = 0

        ppWeight = self.toiPP / self.toiALL
        pkWeight = self.toiPK / self.toiALL

        # Shots are multiplied to keep data scaled similarly to the Points Rating.
        # Temporary fix until the weightings are better adjusted.
        shotMultiplier = 8

        if (self.toi5v5 > 0):
            self.evPointsRating = self.evPointsRating / (self.toi5v5 / 60)
            self.evShotsRating = (self.evShotsRating / (self.toi5v5 / 60)) * shotMultiplier
            evORatingPer60 += self.evPointsRating + self.evShotsRating
        if (self.toiPP > 0):
            self.ppPointsRating = (self.ppPointsRating / (self.toiPP / 60)) * ppWeight
            self.ppShotsRating = ((self.ppShotsRating / (self.toiPP / 60)) * ppWeight) * shotMultiplier
            ppORatingPer60 += self.ppPointsRating + self.ppShotsRating
        if (self.toiPK > 0):
            self.pkPointsRating = (self.pkPointsRating / (self.toiPK / 60)) * pkWeight
            self.pkShotsRating = ((self.pkShotsRating / (self.toiPK / 60)) * pkWeight) * shotMultiplier
            pkORatingPer60 += self.pkPointsRating + self.pkShotsRating

        self.offensivePointsRating = self.evPointsRating + self.ppPointsRating + self.pkPointsRating
        self.offensiveShotsRating = self.evShotsRating + self.ppShotsRating + self.pkShotsRating

        self.evOffensiveRating = evORatingPer60
        self.ppOffensiveRating = ppORatingPer60
        self.pkOffensiveRating = pkORatingPer60

        ORatingPer60 = evORatingPer60 + ppORatingPer60 + pkORatingPer60

        self.offensiveRating = ORatingPer60

        return ORatingPer60

    def calcOffensivePointsRating(self):
        """
        Calculates a player's Points Rating to be used in the Overall Offense Rating
        :return: Offensive Points Rating
        """
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

    def calcOffensiveShotsRating(self):
        """
        Calculates a player's Shots Rating to be used in the Overall Offense Rating.
        :return: Offensive Shots Rating
        """

        CFWeight = 0.040
        FFWeight = 0.020
        SFWeight = 0.020
        SCFWeight = 0.020
        HDCFWeight = 0.150

        # League avg Shooting% for Unblocked Shots (Fenwick)
        evxFSHLeagueAvg = 0.057
        ppxFSHLeagueAvg = 0.092
        pkxFSHLeagueAvg = 0.070

        if (self.shPercentage != '-'):
            self.evShotQualityAdjustment = (evxFSHLeagueAvg * self.shPercentage) * 0.10
            self.ppShotQualityAdjustment = (ppxFSHLeagueAvg * self.shPercentage) * 0.10
            self.pkShotQualityAdjustment = (pkxFSHLeagueAvg * self.shPercentage) * 0.10
        #
        #   Even Strength (5v5)
        #
        #   eviCF = even strength individual Corsi For
        #   eviCF = even strength individual Fenwick For
        #   eviSF = even strength individual Shots For
        #   eviSCF = even strength individual Scoring Chances For
        #   eviHDSCF = even strength individual High-Danger Scoring Chances For
        #
        eviCF = self.eviCF * CFWeight
        eviFF = self.eviFF * FFWeight
        eviSF = self.eviSF * SFWeight
        eviSCF = self.eviSCF * SCFWeight
        eviHDCF = self.eviHDCF * HDCFWeight

        self.evShotsRating = eviCF + eviFF + eviSF + eviSCF + eviHDCF

        if (self.position == "D"):
            self.evShotsRating = (self.evShotsRating * self.evDefenceShotWeight) * self.evShotQualityAdjustment
        else:
            self.evShotsRating = self.evShotsRating * self.evShotQualityAdjustment

        #
        #   Powerplay
        #
        ppiCF = self.ppiCF * CFWeight
        ppiFF = self.ppiFF * FFWeight
        ppiSF = self.ppiSF * SFWeight
        ppiSCF = self.ppiSCF * SCFWeight
        ppiHDCF = self.ppiHDCF * HDCFWeight

        self.ppShotsRating = ppiCF + ppiFF + ppiSF + ppiSCF + ppiHDCF

        if (self.position == "D"):
            self.ppShotsRating = (self.ppShotsRating * self.ppDefenceShotWeight) * self.ppShotQualityAdjustment
        else:
            self.ppShotsRating = (self.ppShotsRating * self.ppForwardShotWeight) * self.ppShotQualityAdjustment

        #
        #   Penalty Kill
        #
        pkiCF = self.pkiCF * CFWeight
        pkiFF = self.pkiFF * FFWeight
        pkiSF = self.pkiSF * SFWeight
        pkiSCF = self.pkiSCF * SCFWeight
        pkiHDCF = self.pkiHDCF * HDCFWeight

        self.pkShotsRating = pkiCF + pkiFF + pkiSF + pkiSCF + pkiHDCF

        if (self.position == "D"):
            self.pkShotsRating = (self.pkShotsRating * self.pkDefenceShotWeight) * self.pkShotQualityAdjustment
        else:
            self.pkShotsRating = (self.pkShotsRating * self.pkForwardShotWeight) * self.pkShotQualityAdjustment