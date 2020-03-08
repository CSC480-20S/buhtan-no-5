class FindingFiveStudyStoreStudy:
    def __init__(self, id, title, author, cost):
        self.studyID = id
        self.title = title
        self.author = author
        self.costInCredits = cost

    def get_studyId(self):
        return self.studyID

    def get_costInCredits(self):
        return self.costInCredits

    def get_title(self):
        return self.title

    def get_author(self):
        return self.author

    def set_studyId(self, newStudyID):
        self.studyID = newStudyID

    def set_costInCredits(self, newCostInCredits):
        self.costInCredits = newCostInCredits

    def set_title(self, newTitle):
        self.title = newTitle

    def set_Author(self, newAuthor):
        self.author = newAuthor