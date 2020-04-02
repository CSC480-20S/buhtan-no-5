import redis
import uuid


class SearchCache():
    def __init__(self):
        self.r = redis.Redis(host='localhost', port=6379, db=0)
        self.max_set_size = 400

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
        hash_id = self.get_hash_id(word)
        pipe = self.r.pipeline()
        pipe.hset(hash_id, 'title', word)
        # this can store multiple fields about the given title
        pipe.hset(hash_id, "data", "woobie")
        # now iterate over all of the partial strings and use the partial string to map to a sorted set.
        # each sorted set will continain the id:score so it can sort the entries.
        try:
            for partial in self.generate_prefix(word):
                print("tmp:" + hash_id)
                pipe.zadd("tmp:" + hash_id, {hash_id: 1.0})
        except redis.exceptions.ResponseError as e:
            print(e.args)
        pipe.execute()

    def generate_prefix(self, word):
        for index, char in enumerate(word):
            index = index + 1
            if index == len(word):
                # this may be old.
                yield word[0:index] + '*'
            yield word[0:index]

    def search_one_word(self, input):
        sorted_set_id = self.get_set_id(input)
        print(sorted_set_id)
        for id in self.r.zrevrange(sorted_set_id, 0, 5):
            yield self.r.hget(id, 'title')

    def update_score(self, selected_word, prefix):
        sorted_set_id = self.get_set_id(prefix)
        hash_id = self.get_hash_id(selected_word)
        set_size = self.r.zcard(sorted_set_id)
        if not self.check_existence(sorted_set_id):
            if set_size < self.max_set_size:
                self.r.zadd(sorted_set_id, {hash_id: 1})
                self.r.hset(hash_id, "title", selected_word)
            else:
                last_ele, score = self.r.zrange(sorted_set_id, -1, -1, withscores=True)
                self.r.zrem(sorted_set_id, last_ele)
                self.r.zadd(sorted_set_id, {hash_id: score + 1})
        self.r.zincrby(sorted_set_id, 1, hash_id)

    def get_set_id(self, word):
        return "tmp:" + str(uuid.uuid5(uuid.NAMESPACE_OID, word))

    def get_hash_id(self, word):
        return str(uuid.uuid5(uuid.NAMESPACE_OID, word))

    def search_multiple_word(self, input):
        ''' Does not work as of 04012020'''
        words = input.split(" ")
        print(self.get_set_id(input))
        print(list(map(self.get_set_id, words)))
        self.r.zinterstore(self.get_set_id(input), list(map(self.get_set_id, words)))
        for id in self.r.zrange(self.get_set_id(input), 0, -1):
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
for word in s.search_one_word("moles"):
    print(word)
