import logging
from dataclasses import dataclass
from datetime import datetime, timedelta
from typing import Dict, Protocol

from tekton_challenge.repositories.errors import CacheNotFound, TTLExpired

logger = logging.getLogger(__name__)


class CacheProtocol(Protocol):
    """Cache Protocol for future duck typing with others cache systems"""
    _data: Dict

    def get(self, key: str) -> str:
        ...

    def set(self, key: str, value: str, ttl: int = 300) -> None:
        ...


@dataclass
class CachedObject:
    key: str
    value: str
    end_datetime: datetime


class LocalCacheRepository(CacheProtocol):
    _data: Dict[str, CachedObject]

    def __init__(self, data=None):
        if data:
            self._data = data
        else:
            self._data = dict()

    def get(self, key: str) -> str:
        if key in self._data:
            try:
                self.check_ttl(self._data[key])
            except TTLExpired as ttl_error:
                logger.exception(str(ttl_error))
                self._data.pop(key)
            return self._data[key].value
        raise CacheNotFound(key)

    def set(self, key: str, value: str, ttl: int = 300) -> None:
        """
        Save in cache
        :param value: value to store
        :param key: key to store
        :param ttl: time to live in seconds
        :return:
        """
        end_datetime = datetime.now() + timedelta(seconds=ttl)
        self._data[key] = CachedObject(key, value, end_datetime)

    @staticmethod
    def check_ttl(cached_object: CachedObject):
        """ Checks cache ttl in CachedObject
        :param cached_object:
        :return:
        """
        if datetime.now() > cached_object.end_datetime:
            raise TTLExpired(cached_object.key)
