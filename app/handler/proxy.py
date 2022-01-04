from core.proxy import Proxy
from handler.redis import RedisClient
from handler.config import Config


class ProxyHandler(object):
    # Proxy CRUD operator

    def __init__(self):
        self.conf = Config()
        self.db = RedisClient.parse_db_conn(self.conf.db_conn)
        self.db.change_table(self.conf.table_name)

    def get(self, https=False):
        # return a proxy, https: True/False
        proxy = self.db.get(https)
        return Proxy.create_from_json(proxy) if proxy else None

    def pop(self, https):
        # return and delete a useful proxy
        proxy = self.db.pop(https)
        if proxy:
            return Proxy.create_from_json(proxy)
        return None

    def put(self, proxy):
        # put proxy into use proxy
        self.db.put(proxy)

    def delete(self, proxy):
        # delete useful proxy
        return self.db.delete(proxy.proxy)

    def get_all(self, https=False):
        # get all proxy from pool as Proxy list
        proxies = self.db.get_all(https)
        return [Proxy.create_from_json(_) for _ in proxies]

    def exists(self, proxy):
        # check proxy exists
        return self.db.exists(proxy.proxy)

    def get_count(self):
        #  return raw_proxy and use_proxy count
        total_use_proxy = self.db.get_count()
        return {'count': total_use_proxy}
