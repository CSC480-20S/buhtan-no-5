class FindingFiveStudyStoreUser:
    def __init__(self, userID, numCredits, ownedStudies, viewedStudies, wishList, authorList):
        self.userID = userID
        self.numCredits = numCredits
        self.ownedStudies = ownedStudies  # list of FFSS studies
        self.viewedStudies = viewedStudies  # list of FFSS studies
        self.wishList = wishList  # wish list of FFSS studies
        self.authorList = authorList

    def get_userId(self):
        return self.userID

    def get_numCredits(self):
        return self.numCredits

    def get_ownedStudies(self):
        return self.ownedStudies

    def get_viewedStudies(self):
        return self.viewedStudies

    def get_wishList(self):
        return self.wishList

    def get_authorList(self):
        return self.authorList

    def set_userId(self, newUserID):
        self.userID = newUserID

    def set_numCredits(self, newNumCredits):
        self.numCredits = newNumCredits

    def set_ownedStudies(self, newOwnedStudies):
        self.ownedStudies = newOwnedStudies

    def set_wishList(self, newWishList):
        self.wishList = newWishList

    def set_viewedStudies(self, newViewedStudies):
        self.viewedStudies = newViewedStudies

    def set_authorList(self, newAuthorList):
        self.authorList = newAuthorList
