class FindingFiveStudyStoreStudy:
    def __init__(self, id, title, author, cost, purpose, references, categories, subcategories, keywords, num_stimuli,
                 num_responses, randomize, duration, num_trials, rating, institution, template, images, abstract):
        self.studyID = id
        self.title = title
        self.author = author
        self.costInCredits = cost
        self.purpose = purpose
        self.references = references
        self.categories = categories
        self.subcategories = subcategories
        self.keywords = keywords
        self.num_stimuli = num_stimuli
        self.num_responses = num_responses
        self.num_trials = num_trials
        self.randomize = randomize
        self.duration = duration
        self.rating = rating
        self.institution = institution
        self.template = template
        self.images = images
        self.abstract = abstract

    def build_dict(self):
        returner = dict()
        returner['studyID'] = self.studyID
        returner['title'] = self.title
        returner['author'] = self.author
        returner['costInCredits'] = self.costInCredits
        returner['purpose'] = self.purpose
        returner['references'] = self.references
        returner['categories'] = self.categories
        returner['subcategories'] = self.subcategories
        returner['keywords'] = self.keywords
        returner['num_stimuli'] = self.num_stimuli
        returner['num_responses'] = self.num_responses
        returner['num_trials'] = self.num_trials
        returner['randomize'] = self.randomize
        returner['duration'] = self.duration
        returner['rating'] = self.rating
        returner['institution'] = self.institution
        returner['template'] = self.template
        returner["images"] = self.images
        returner["abstract"] = self.abstract
        return returner

    def get_studyId(self):
        return self.studyID

    def get_costInCredits(self):
        return self.costInCredits

    def get_title(self):
        return self.title

    def get_author(self):
        return self.author

    def get_purpose(self):
        return self.purpose

    def get_references(self):
        return self.references

    def get_categories(self):
        return self.categories

    def get_subcategories(self):
        return self.subcategories

    def get_keywords(self):
        return self.keywords

    def get_num_stimuli(self):
        return self.num_stimuli

    def get_num_responses(self):
        return self.num_responses

    def get_num_trials(self):
        return self.num_trials

    def get_randomize(self):
        return self.randomize

    def get_rating(self):
        return self.rating

    def get_duration(self):
        return self.duration

    def get_institution(self):
        return self.institution

    def get_template(self):
        return self.template

    def get_images(self):
        return self.images

    def get_abstract(self):
        return self.abstract

    def set_studyId(self, newStudyID):
        self.studyID = newStudyID

    def set_costInCredits(self, newCostInCredits):
        self.costInCredits = newCostInCredits

    def set_title(self, newTitle):
        self.title = newTitle

    def set_author(self, newAuthor):
        self.author = newAuthor

    def set_purpose(self, new_purpose):
        self.purpose = new_purpose

    def set_references(self, new_refrences):
        self.references = new_refrences

    def set_categories(self, new_categories):
        self.categories = new_categories

    def set_subcategories(self, new_subcategories):
        self.subcategories = new_subcategories

    def set_keywords(self, new_keywords):
        self.keywords = new_keywords

    def set_num_stimuli(self, new_num_stimuli):
        self.num_stimuli = new_num_stimuli

    def set_num_responses(self, new_num_responses):
        self.num_responses = new_num_responses

    def set_num_trials(self, new_num_trials):
        self.num_trials = new_num_trials

    def set_randomize(self, new_randomize):
        self.randomize = new_randomize

    def set_rating(self, new_rating):
        self.rating = new_rating

    def set_duration(self, new_duration):
        self.duration = new_duration

    def set_institution(self, new_institution):
        self.institution = new_institution

    def set_template(self, new_template):
        self.template = new_template

    def set_images(self, new_images):
        self.images = new_images

    def set_abstract(self, new_abstract):
        self.abstract = new_abstract
