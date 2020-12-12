import logging
import hashlib

from django.conf import settings
from django.core.cache import cache, InvalidCacheBackendError


def one_min_cache(key, value):
    return set_cached_value(key, value, 60)


def two_min_cache(key, value):
    return set_cached_value(key, value, 60 * 2)


def five_min_cache(key, value):
    return set_cached_value(key, value, 60 * 5)


def ten_min_cache(key, value):
    return set_cached_value(key, value, 60 * 10)


def half_hour_cache(key, value):
    return set_cached_value(key, value, 60 * 30)


def hour_cache(key, value):
    return set_cached_value(key, value, 60 * 60)


def day_cache(key, value):
    return set_cached_value(key, value, 60 * 60 * 24)


def week_cache(key, value):
    return set_cached_value(key, value, 60 * 60 * 24 * 7)


def month_cache(self, key, value):
    return set_cached_value(key, value, 60 * 60 * 24 * 7 * 4)


def get_cached_value(key):
    try:
        return cache.get(make_key(key))
    except Exception as error:
        logging.warning('Cache {key} not found, issue {error}'.format(key=key, error=error))
        return None


def set_cached_value(key, value, timeout):
    return cache.get_or_set(make_key(key), value, timeout)


def delete_cached_value(key):
    cache.remove(make_key(key))


def make_key(name, **kwargs):
    return '{hash}'.format(
        hash=hashlib.md5(
            '{name}:{version}:{kwargs}'.format(
                name=name,
                version=settings.VERSION,
                kwargs=kwargs
            ).encode()
        ).hexdigest()
    )
