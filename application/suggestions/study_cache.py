import redis
import uuid


class StudyCache():
    '''A Redis Cache to store FindingFiveStudyStoreStudy Objects.'''

    def __init__(self):  # 6378
        self.r = redis.Redis(host='localhost', port=6378, db=0)

    def add_study_to_cache(self, study):
        pipe = self.r.pipeline()
        exitsence = pipe.exists(study['id'])
        if exitsence == 0:
            pipe.hset(study['id'], study)
        # means the id,
        else:
            new_id = str(uuid.uuid5(uuid.NAMESPACE_OID, study['id']))
            second_res = pipe.hset(new_id, study)
            pipe.expire(new_id, 700)

    def get_study_from_cache(self, title):
        result = self.r.exists(title)
        if result == 1:
            return True, self.r.hgetall(title)
        return False, None


if __name__ == "__main__":
    s = StudyCache()
    s.get_study_from_cache("example")
