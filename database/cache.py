import redis
import uuid
from gui_endpoints.preview_study import x


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

    def add_new_word(self,word):
        self.r.client_list()
        id=uuid.uuid5(uuid.NAMESPACE_OID,word)
        pipe = self.r.pipeline()
        pipe.hset(str(id),'title',word)
        #this can store multiple fields about the given title
        pipe.hset(str(id),"data","woobie")
        #now iterate over all of the partial strings and use the partial string to map to a sorted set.
        #each sorted set will continain the id:score so it can sort the entries.

        try:
            for partial in self.generate_prefix(word):
                print(str(id))
                pipe.zadd("tmp"+str(uuid.uuid5(uuid.NAMESPACE_OID,partial)),{str(id):1.0})
        except redis.exceptions.ResponseError as e:
            print(e.args)
        pipe.execute()

    def generate_prefix(self,word):
        for index,char in enumerate(word):
            index = index+1
            if index == len(word):
                yield word[0:index]+'*'
            yield word[0:index]
#schema a hash entry where its string:"" and id:""






s = SearchCache()
s.add_new_word("hellozz")
# res=s.add_serach_query(x.build_dict(),"hell0 world")
# status,study = s.check_existence("hell0 world")
# print(status,study)
#
