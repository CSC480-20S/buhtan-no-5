import redis
import uuid
from gui_endpoints.preview_study import x


class SearchCache():
    def __init__(self):
        self.r = redis.Redis(host='localhost', port=6379, db=0)
        self.max_set_size=400

    def check_existence(self, title):
        result = self.r.exists(title)
        if result is 1:
            return True
        return False

    def add_serach_query(self, response, query):
        key = "seach:" + str(query)
        cache_resp = self.r.hmset(key, response)
        if cache_resp > 0:
            return True
        return False

    def add_new_word(self, word):
        id = uuid.uuid5(uuid.NAMESPACE_OID, word)
        pipe = self.r.pipeline()
        pipe.hset(str(id), 'title', word)
        # this can store multiple fields about the given title
        pipe.hset(str(id), "data", "woobie")
        # now iterate over all of the partial strings and use the partial string to map to a sorted set.
        # each sorted set will continain the id:score so it can sort the entries.

        try:
            for partial in self.generate_prefix(word):
                print("tmp:" + str(uuid.uuid5(uuid.NAMESPACE_OID, partial)))
                pipe.zadd("tmp:" + str(uuid.uuid5(uuid.NAMESPACE_OID, partial)), {str(id): 1.0})
        except redis.exceptions.ResponseError as e:
            print(e.args)
        pipe.execute()

    def generate_prefix(self, word):
        for index, char in enumerate(word):
            index = index + 1
            if index == len(word):
                yield word[0:index] + '*'
            yield word[0:index]

    def search_one_word(self, input):
        sorted_set_id = "tmp:" + str(uuid.uuid5(uuid.NAMESPACE_OID, input))
        print(sorted_set_id)
        for id in self.r.zrange(sorted_set_id, 0, 5):
                print(id)
                yield self.r.hget(id, 'title')

    def update_score(self,selected_word,prefix):
        sorted_set_id=self.get_search_id(prefix)
        set_size=self.r.scard(sorted_set_id)
        if not self.check_existence(sorted_set_id):
            if set_size<self.max_set_size:
                self.r.zadd(sorted_set_id,{selected_word:1})
            else:
                last_ele,score=self.r.zrange(sorted_set_id,-1,-1,withscores=True)
                self.r.srem(sorted_set_id,last_ele)
                self.r.zadd(sorted_set_id,{selected_word:score+1})
        self.r.zincrby(sorted_set_id,1,selected_word)


    def get_search_id(self, word):
        return "tmp:" + str(uuid.uuid5(uuid.NAMESPACE_OID, word))

    def search_multiple_word(self, input):
        ''' Does not work as of 04012020'''
        words = input.split(" ")
        print(self.get_search_id(input))
        print(list(map(self.get_search_id, words)))
        self.r.zinterstore(self.get_search_id(input), list(map(self.get_search_id, words)))
        for id in self.r.zrange(self.get_search_id(input), 0, -1):
            yield self.r.hget(id, 'title')

    def read_basic_word_file(self, cap=20):
        with open("/usr/share/dict/words", "r") as f:
            for line in f:
                word = line.strip()
                if len(word) > cap:
                    pass
                yield line.strip()

    def create_basic_prefix(self):
        for word in self.read_basic_word_file(20):
            self.add_new_word(word)


# schema a hash entry where its string:"" and id:""
# First create prefixes before launching redis
# Accept some string from the user and create an associated score and the id
# If string is more than one word, split into individual and then take the intersection of
# all the sorted sets.
# Then iterate over the zrange return and hget with the associated key to get the string recomendation


s = SearchCache()
s.add_new_word("austin")
print(str(uuid.uuid5(uuid.NAMESPACE_OID, '')))
# s.create_basic_prefix()
for word in s.search_one_word("za"):
    print(word)
# res=s.add_serach_query(x.build_dict(),"hell0 world")
# status,study = s.check_existence("hell0 world")
# print(status,study)
#
