class FindingFiveStudyStoreUser:
    def __init__(self, userID, numCredits, ownedStudies, viewedStudies):
        self.userID = userID
        self.numCredits = numCredits
        self.ownedStudies = ownedStudies #list of FFSS studies
        self.viewedStudies = viewedStudies #list of FFSS studies

    def get_userId(self):
        return self.userID

    def get_numCredits(self):
        return self.numCredits

    def get_ownedStudies(self):
        return self.ownedStudies

    def get_viewedStudies(self):
        return self.viewedStudies

    def set_userId(self, newUserID):
        self.userID = newUserID

    def set_numCredits(self, newNumCredits):
        self.numCredits = newNumCredits

    def set_ownedStudies(self, newOwnedStudies):
        self.ownedStudies = newOwnedStudies

    def set_viewedStudies(self, newViewedStudies):
        self.viewedStudies = newViewedStudies
