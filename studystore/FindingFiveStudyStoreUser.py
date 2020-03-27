class FindingFiveStudyStoreUser:
<<<<<<< HEAD
    def __init__(self, userID, numCredits, ownedStudies, viewedStudies):
=======
    def __init__(self, userID, numCredits, ownedStudies, viewedStudies, wishList):
>>>>>>> knock-dev
        self.userID = userID
        self.numCredits = numCredits
        self.ownedStudies = ownedStudies  # list of FFSS studies
        self.viewedStudies = viewedStudies  # list of FFSS studies
<<<<<<< HEAD
=======
        self.wishList = wishList  # wish list of FFSS studies
>>>>>>> knock-dev

    def get_userId(self):
        return self.userID

    def get_numCredits(self):
        return self.numCredits

    def get_ownedStudies(self):
        return self.ownedStudies

    def get_viewedStudies(self):
        return self.viewedStudies

<<<<<<< HEAD
=======
    def get_wishList(self):
        return self.wishList

>>>>>>> knock-dev
    def set_userId(self, newUserID):
        self.userID = newUserID

    def set_numCredits(self, newNumCredits):
        self.numCredits = newNumCredits

    def set_ownedStudies(self, newOwnedStudies):
        self.ownedStudies = newOwnedStudies

<<<<<<< HEAD
=======
    def set_wishList(self, newWishList):
        self.wishList = newWishList

>>>>>>> knock-dev
    def set_viewedStudies(self, newViewedStudies):
        self.viewedStudies = newViewedStudies
