import redis
from redis.connection import Encoder


class RedisHelper:
    """
    RedisHelper
    ~~~~~~~~~~~

    A project based redis helper class
    """

    def __init__(self, host, port, db, **kwargs):
        self.instance = redis.Redis(
            host=host,
            port=port,
            db=db,
            charset="utf-8",
            decode_responses=True,
            **kwargs
        )

    @staticmethod
    def to_byte(value):
        """
        Convert value to byte
        :param value:
        :return:
        """
        accepted_types = (bytes, str, int, float)
        assert isinstance(value, accepted_types), (
            "Given value type cannot be {}, should be one of them {}".format(type(value), accepted_types)
        )

        encoder = Encoder(
            encoding='utf-8',
            encoding_errors='strict',
            decode_responses=True
        )
        return encoder.encode(value)

    def get_value(self, key):
        """
        Get single value given key
        :param key:
        :return:
        """
        key = self.to_byte(key)
        return self.instance.get(key)

    def get_all_keys(self, search_key_expression):
        """
        Get all keys with expression
        :param search_key_expression:
        :return:
        """
        return self.instance.keys(pattern=search_key_expression)

    def set_value(self, key, value, **kwargs):
        """
        Set one value to key, create new one or update exist one
        :param key:
        :param value:
        :return:
        """
        key = self.to_byte(key)
        return self.instance.set(key, value, **kwargs)

    def set_value_expire_time(self, key, value, expire_time):
        """
        Set key with expire time
        :param key:
        :param value:
        :param expire_time:
        :return:
        """

        return self.set_value(key, value, ex=expire_time)

    def is_key_exists(self, key):
        """
        Check if key exist
        :param key:
        :return:
        """
        key = self.to_byte(key)
        return self.instance.exists(key)

    def delete_key(self, key):
        """
        Delete one key
        :param key:
        :return:
        """
        key = self.to_byte(key)
        return self.instance.delete(key)

    def delete_all_keys(self):
        """
        Delete all key, in redis it means flush db
        :return:
        """
        is_deleted = self.instance.flushdb()
        return is_deleted

    def get_hash_value(self, hash):
        hash = self.to_byte(hash)
        return self.instance.hgetall(hash)

    def insert_hash(self, hash, key, value): #Hash
        key = self.to_byte(key)
        value = self.to_byte(value)
        hash = self.to_byte(hash)
        self.instance.hset(hash, key, value)