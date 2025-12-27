#!/usr/bin/env python3
"""
    String Redis
"""
from uuid import uuid4
from typing import Union, Callable
from functools import wraps
import redis


def count_calls(method: Callable = None) -> Callable:
    """ Decorator count calls """
    name = method.__qualname__

    @wraps(method)
    def wrapper(self, *args, **kwargs):
        """ Wrapper method """
        self._redis.incr(name)
        return method(self, *args, **kwargs)

    return wrapper


def call_history(method: Callable) -> Callable:
    @wraps(method)
    def wrapper(self, *args, **kwargs):
        self._redis.rpush(method.__qualname__ + ":inputs", str(args))

        output = method(self, *args, **kwargs)
        self._redis.rpush(method.__qualname__ + ":outputs", str(output))

        return output
    return wrapper


def replay(func: Callable):
    """ Replay function """
    r = redis.Redis()
    func_name = func.__qualname__
    number_calls = r.get(func_name)

    try:
        number_calls = number_calls.decode('utf-8')
    except Exception:
        number_calls = 0

    print(f'{func_name} was called {number_calls} times:')

    ins = r.lrange(func_name + ":inputs", 0, -1)
    outs = r.lrange(func_name + ":outputs", 0, -1)

    for cin, cout in zip(ins, outs):
        try:
            cin = cin.decode('utf-8')
        except Exception:
            cin = ""
        try:
            cout = cout.decode('utf-8')
        except Exception:
            cout = ""

        print(f'{func_name}(*{cin}) -> {cout}')


class Cache:
    """ Functionality Redis """

    def __init__(self):
        """ Constructor """
        self._redis = redis.Redis()
        self._redis.flushdb()

    @call_history
    @count_calls
    def store(self, data: Union[str, bytes, int, float]) -> str:
        """
            Store the cache

            Args:
                data: bring the information to store

            Return:
                Key or number uuid
        """
        key = str(uuid4())
        self._redis.set(key, data)

        return key

    def get(self, key: str, fn: Callable = None):
        data = self._redis.get(key)
        if data is None:
            return None
        return fn(data) if fn else data

    def get_str(self, key: str) -> str:
        return self.get(key, fn=lambda d: d.decode("utf-8"))

    def get_int(self, key: str) -> int:
        return self.get(key, fn=int)
