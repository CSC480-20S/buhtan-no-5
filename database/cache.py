import redis
import endpoints.Auxiliary as aux
import time
r = redis.Redis(db=1)


def test_cache():
    studies =aux.getStudies(dict(),4)
    with r.pipeline() as pipe:
        for study in studies:
            map = study.build_dict()
            print(type(map))
            del map['randomize']
            del map['keywords']
            del map['rating']
            r.hmset(map['studyID'],map)
        pipe.execute()
def get_cache():
    start=time.perf_counter()
    resp = r.hgetall('4')
    end=time.perf_counter()
    print(resp)
    print(end-start)
    return -1


def no_cache():
    tart=time.perf_counter()
    studies = aux.getStudies(dict(),4)
    for  study in studies:
            map = study.build_dict()
            print(type(map))
            del map['randomize']
            del map['keywords']
            del map['rating']
    end=time.perf_counter()
    print(end-tart)

test_cache()
get_cache()
no_cache()
