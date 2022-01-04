from queue import Empty
from threading import Thread
from datetime import datetime

from core.validator import ProxyValidator
from handler.config import Config
from handler.logger import Logger
from handler.proxy import ProxyHandler


class DoValidator(object):
    """ 执行校验 """

    @classmethod
    def validator(cls, proxy):
        """
        校验入口
        Args:
            proxy: Proxy Object
        Returns:
            Proxy Object
        """
        http_r = cls.http_validator(proxy)
        https_r = False if not http_r else cls.https_validator(proxy)

        proxy.check_count += 1
        proxy.last_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        proxy.last_status = True if http_r else False
        if http_r:
            if proxy.fail_count > 0:
                proxy.fail_count -= 1
            proxy.https = True if https_r else False
        else:
            proxy.fail_count += 1
        return proxy

    @classmethod
    def http_validator(cls, proxy):
        for func in ProxyValidator.http_validator:
            if not func(proxy.proxy):
                return False
        return True

    @classmethod
    def https_validator(cls, proxy):
        for func in ProxyValidator.https_validator:
            if not func(proxy.proxy):
                return False
        return True

    @classmethod
    def pre_validator(cls, proxy):
        for func in ProxyValidator.pre_validator:
            if not func(proxy):
                return False
        return True


class _ThreadChecker(Thread):
    """ 多线程检测 """

    def __init__(self, work_type, target_queue, thread_name):
        Thread.__init__(self, name=thread_name)
        self.work_type = work_type
        self.log = Logger("checker")
        self.proxy_handler = ProxyHandler()
        self.target_queue = target_queue
        self.conf = Config()

    def run(self):
        self.log.info("{}ProxyCheck - {}: start".format(self.work_type.title(), self.name))
        while True:
            try:
                proxy = self.target_queue.get(block=False)
            except Empty:
                self.log.info("{}ProxyCheck - {}: complete".format(self.work_type.title(), self.name))
                break
            proxy = DoValidator.validator(proxy)
            if self.work_type == "raw":
                self.raw(proxy)
            else:
                self.use(proxy)
            self.target_queue.task_done()

    def raw(self, proxy):
        if proxy.last_status:
            if self.proxy_handler.exists(proxy):
                self.log.info('RawProxyCheck - {}: {} exist'.format(self.name, proxy.proxy.ljust(23)))
            else:
                self.log.info('RawProxyCheck - {}: {} pass'.format(self.name, proxy.proxy.ljust(23)))
                self.proxy_handler.put(proxy)
        else:
            self.log.info('RawProxyCheck - {}: {} fail'.format(self.name, proxy.proxy.ljust(23)))

    def use(self, proxy):
        if proxy.last_status:
            self.log.info('UseProxyCheck - {}: {} pass'.format(self.name, proxy.proxy.ljust(23)))
            self.proxy_handler.put(proxy)
            return
        if proxy.fail_count > self.conf.max_fail_count:
            self.log.info('UseProxyCheck - {}: {} fail, count {} delete'.format(
                self.name, proxy.proxy.ljust(23), proxy.fail_count))
            self.proxy_handler.delete(proxy)
        else:
            self.log.info('UseProxyCheck - {}: {} fail, count {} keep'.format(
                self.name, proxy.proxy.ljust(23), proxy.fail_count))
            self.proxy_handler.put(proxy)


def checker(tp, queue):
    """
    run Proxy ThreadChecker
    :param tp: raw/use
    :param queue: Proxy Queue
    :return:
    """
    thread_list = list()
    for index in range(20):
        thread_list.append(_ThreadChecker(tp, queue, "thread_%s" % str(index).zfill(2)))

    for thread in thread_list:
        thread.daemon = True
        thread.start()

    for thread in thread_list:
        thread.join()
