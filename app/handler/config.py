import os

from util.lazy_property import LazyProperty
from util.metaclass import with_metaclass
from util.singleton import Singleton


class Config(with_metaclass(Singleton)):

    @LazyProperty
    def db_conn(self):
        return os.getenv("DB_CONN", "redis://@localhost:6379/0")

    @LazyProperty
    def server_host(self):
        return os.getenv("SERVER_HOST", "0.0.0.0")

    @LazyProperty
    def server_port(self):
        return os.getenv("SERVER_PORT", "5000")

    @LazyProperty
    def table_name(self):
        return os.getenv("TABLE_NAME", 'proxies')

    @property
    def fetchers(self):
        return [
            "free_proxy01",
            "free_proxy02",
            "free_proxy03",
            "free_proxy04",
            "free_proxy05",
            "free_proxy06",
            "free_proxy07",
            "free_proxy08",
            "free_proxy09",
            "free_proxy10"
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
