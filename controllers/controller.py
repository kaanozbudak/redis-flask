from settings import REDIS_DB, REDIS_HOST, REDIS_PORT
from core.helpers import RedisHelper

""" 
make redis connection with redis helper
"""
redis = RedisHelper(host=REDIS_HOST, port=REDIS_PORT, db=REDIS_DB)


# Get all keys with expression
def get_keys(search_key_expression):
    all_keys = redis.get_all_keys(search_key_expression)
    return all_keys, "array"


# Get one value by key
def get_value(key):
    value = redis.get_value(key)
    return value, "string"


# Set one value to key, create new one or update exist one
def set_value(key, value):
    is_set = redis.set_value(key, value)
    return is_set, "bool"


# Set key with expire time
def set_value_expire_time(key, value, expire_time):
    is_set = redis.set_value_expire_time(key, value, expire_time)
    return is_set, "bool"


# Check is key exist
def key_exist(key):
    is_key_exist = redis.is_key_exists(key)
    if is_key_exist:
        status_code = 200
    else:
        status_code = 204
    return status_code


# Delete one key
def delete_key(key):
    is_deleted = redis.delete_key(key)
    return is_deleted, "bool"


# Delete all key, in redis means flush db
def delete_all_keys():
    is_deleted = redis.delete_all_keys()
    return is_deleted, "bool"
