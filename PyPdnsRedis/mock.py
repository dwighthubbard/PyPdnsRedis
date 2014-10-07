#!/usr/bin/env python

"""
Class to Mock out the Redis class for testing
"""

__copyright__ = """
pdns-redis.py, Copyright 2011, Bjarni R. Einarsson <http://bre.klaki.net/>
                               and The Beanstalks Project ehf.

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU Lesser General Public License as published
by the Free Software Foundation, either version 3 of the License, or (at
your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU Lesser General Public License for more details.

You should have received a copy of the GNU Lesser General Public License
along with this program.  If not, see <http://www.gnu.org/licenses/>.
"""


class MockRedis(object):
    """A mock-redis object for quick offline tests."""

    def __init__(self, host=None, port=None, password=None):
        self.data = {}
        self.host = host

    def ping(self):
        return True

    def get(self, key):
        if key in self.data:
            return self.data[key]
        return None

    def encode(self, val):
        if isinstance(val, str):
            return val
        if isinstance(val, unicode):
            return val.encode('utf-8')
        return str(val)

    def set(self, key, val):
        self.data[key] = self.encode(val)
        return True

    def setnx(self, key, val):
        if key in self.data:
            return None
        self.data[key] = self.encode(val)
        return val

    def incr(self, key):
        if key not in self.data:
            self.data[key] = 0
        self.data[key] = self.encode(int(self.data[key]) + 1)
        return int(self.data[key])

    def incrby(self, key, val):
        if key not in self.data:
            self.data[key] = 0
        self.data[key] = self.encode(int(self.data[key]) + int(val))
        return int(self.data[key])

    def delete(self, key):
        if key in self.data:
            del (self.data[key])
            return True
        else:
            return False

    def hget(self, key, hkey):
        if key in self.data and hkey in self.data[key]:
            return self.data[key][hkey]
        return None

    def hincrby(self, key, hkey, val):
        if key not in self.data:
            self.data[key] = {}
        if hkey not in self.data[key]:
            self.data[key][hkey] = 0
        self.data[key][hkey] = self.encode(int(self.data[key][hkey]) + int(val))
        return int(self.data[key][hkey])

    def hgetall(self, key):
        if key in self.data:
            return self.data[key]
        return {}

    def hdel(self, key, hkey):
        if key in self.data and hkey in self.data[key]:
            del (self.data[key][hkey])
        return True

    def hset(self, key, hkey, val):
        if key not in self.data:
            self.data[key] = {}
        self.data[key][hkey] = self.encode(val)
        return True

    def sadd(self, key, member):
        if key not in self.data:
            self.data[key] = {}
        self.data[key][member] = 1
        return True

    def srem(self, key, member):
        if key in self.data and member in self.data[key]:
            del self.data[key][member]
            return True
        return False

    def lpush(self, key, value):
        if key not in self.data:
            self.data[key] = []
        self.data[key].append(value)
        return True

    def llen(self, key):
        if key not in self.data:
            return 0
        return len(self.data[key])

    def lpop(self, key):
        return self.data[key].pop(0)
