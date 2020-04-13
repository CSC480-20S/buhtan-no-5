import redis
import os
class StudyCache():
    '''A Redis Cache to store FindingFiveStudyStoreStudy Objects.'''
    def __init__(self): #6378
        self.r = redis.Redis(host='localhost', port=6378, db=0)

    def get_study_from_cache(self, title):
        result = self.r.exists(title)
        if result == 1:
            return self.r.hgetall(title)
        return False

if __name__ == "__main__":
    s=StudyCache()
    s.get_study_from_cache("example")
