from datetime import datetime, timedelta

import pytest

from tekton_challenge.repositories.cache import CachedObject, LocalCacheRepository
from tekton_challenge.repositories.errors import CacheNotFound, TTLExpired


@pytest.fixture(scope="module")
def local_cache_repository():
    yield LocalCacheRepository()


@pytest.fixture(scope="module")
def cached_object():
    yield CachedObject(key=1, value="Active", end_datetime=datetime.now() - timedelta(minutes=6))


def test_cache_set(local_cache_repository):
    local_cache_repository.set(key=1, value="Active")

    assert local_cache_repository._data[1].value == "Active"


def test_cache_get(local_cache_repository):
    local_cache_repository.set(0, "Inactive")
    cached_value = local_cache_repository.get(0)
    assert cached_value == local_cache_repository._data[0].value


def test_cache_get_not_found(local_cache_repository):
    with pytest.raises(CacheNotFound):
        local_cache_repository.get("test")


def test_cache_get_ttl_expired(local_cache_repository, cached_object):
    with pytest.raises(TTLExpired):
        local_cache_repository.check_ttl(cached_object)
