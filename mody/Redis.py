from redis import StrictRedis

db = StrictRedis(decode_responses=True)
