import redis

class StudyCache():
    ''''''
    def __init__(self):
        self.r = redis.Redis(host='localhost', port=6379, db=0)
        self.max_set_size = 400
