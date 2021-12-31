from threading import Thread

from core.check import DoValidator
from core.proxy import Proxy
from fetcher.fetcher import ProxyFetcher
from handler.config import Config
from handler.logger import Logger
from handler.proxy import ProxyHandler


class _ThreadFetcher(Thread):

    def __init__(self, fetch_source, proxy_dict):
        Thread.__init__(self)
        self.fetch_source = fetch_source
        self.proxy_dict = proxy_dict
        self.fetcher = getattr(ProxyFetcher, fetch_source, None)
        self.log = Logger("fetcher")
        self.conf = Config()
        self.proxy_handler = ProxyHandler()

    def run(self):
        self.log.info("ProxyFetch - {func}: start".format(func=self.fetch_source))
        try:
            for proxy in self.fetcher():
                self.log.info('ProxyFetch - %s: %s ok' % (self.fetch_source, proxy.ljust(23)))
                proxy = proxy.strip()
                if proxy in self.proxy_dict:
                    self.proxy_dict[proxy].add_source(self.fetch_source)
                else:
                    self.proxy_dict[proxy] = Proxy(
                        proxy, source=self.fetch_source)
        except Exception as e:
            self.log.error("ProxyFetch - {func}: error".format(func=self.fetch_source))
            self.log.error(str(e))


class Fetcher(object):
    name = "fetcher"

    def __init__(self):
        self.log = Logger(self.name)
        self.conf = Config()

    def run(self):
        proxy_dict = dict()
        thread_list = list()
        self.log.info("ProxyFetch : start")

        for fetch_source in self.conf.fetchers:
            self.log.info("ProxyFetch - {func}: start".format(func=fetch_source))
            fetcher = getattr(ProxyFetcher, fetch_source, None)
            if not fetcher:
                self.log.error("ProxyFetch - {func}: class method not exists!".format(func=fetch_source))
                continue
            if not callable(fetcher):
                self.log.error("ProxyFetch - {func}: must be class method".format(func=fetch_source))
                continue
            thread_list.append(_ThreadFetcher(fetch_source, proxy_dict))

        for thread in thread_list:
            thread.daemon = True
            thread.start()

        for thread in thread_list:
            thread.join()

        self.log.info("ProxyFetch - all complete!")
        for _ in proxy_dict.values():
            if DoValidator.pre_validator(_.proxy):
                yield _
