import os

from util.lazy_property import LazyProperty
from util.metaclass import with_metaclass
from util.singleton import Singleton


class Config(with_metaclass(Singleton)):

    @LazyProperty
    def db_conn(self):
        return os.getenv("DB_CONN", "redis://@proxy-redis:6379/0")

    @LazyProperty
    def table_name(self):
        return os.getenv("TABLE_NAME", 'proxies')

    @property
    def fetchers(self):
        return [
            "freeProxy01",
            "freeProxy02",
            "freeProxy03",
            "freeProxy04",
            "freeProxy05",
            "freeProxy06",
            "freeProxy07",
            "freeProxy08",
            "freeProxy09",
            "freeProxy10"
        ]

    @LazyProperty
    def http_url(self):
        return os.getenv("HTTP_URL", "http://httpbin.org")

    @LazyProperty
    def https_url(self):
        return os.getenv("HTTPS_URL", "https://www.qq.com")

    @LazyProperty
    def verify_timeout(self):
        return int(os.getenv("VERIFY_TIMEOUT", 10))

    @LazyProperty
    def max_fail_count(self):
        return int(os.getenv("MAX_FAIL_COUNT", 0))

    @LazyProperty
    def pool_size_min(self):
        return int(os.getenv("POOL_SIZE_MIN", 20))

    @LazyProperty
    def timezone(self):
        return os.getenv("TIMEZONE", "Asia/Shanghai")
