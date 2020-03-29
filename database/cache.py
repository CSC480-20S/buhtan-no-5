import redis
from gui_endpoints.preview_study import x
from studystore.FindingFiveStudyStoreStudy import FindingFiveStudyStoreStudy

class SearchCache():
    def __init__(self):
        self.r = redis.Redis(db=1)

    def check_existence(self, title):
        result = self.r.exists("seach:"+title)
        if result is 1:
            return True, self.r.hgetall("seach:"+title)
        return False, None

    def add_serach_query(self, response, query):
        key = "seach:" + str(query)
        cache_resp = self.r.hmset(key, response)
        if cache_resp > 0:
            return True
        return False


s = SearchCache()
res=s.add_serach_query(x.build_dict(),"hell0 world")
status,study = s.check_existence("hell0 world")
print(status,study)

