# 实现proxy-crawler
from apscheduler.schedulers.blocking import BlockingScheduler
from apscheduler.executors.pool import ProcessPoolExecutor

from queue import Queue

from core.check import checker
from core.fetch import Fetcher
from handler.config import Config
from handler.logger import Logger
from handler.proxy import ProxyHandler


def start_fetch():
    queue = Queue()
    fetcher = Fetcher()
    for proxy in fetcher.run():
        queue.put(proxy)
    checker("raw", queue)


def start_check():
    queue = Queue()
    handler = ProxyHandler()
    if handler.db.get_count().get("total", 0) < handler.conf.pool_size_min:
        start_fetch()
    for proxy in handler.get_all():
        queue.put(proxy)
    checker("use", queue)


def start():
    timezone = Config().timezone
    logger = Logger("scheduler")
    scheduler = BlockingScheduler(logger=logger, timezone=timezone)
    scheduler.add_job(start_fetch, 'interval', minutes=4, id="proxy_fetch", name="proxy采集")
    scheduler.add_job(start_check, 'interval', minutes=2, id="proxy_check", name="proxy检查")
    executors = {
        'default': {'type': 'threadpool', 'max_workers': 20},
        'processpool': ProcessPoolExecutor(max_workers=5)
    }
    job_defaults = {'coalesce': False, 'max_instances': 10}
    scheduler.configure(executors=executors, job_defaults=job_defaults, timezone=timezone)
    scheduler.start()


if __name__ == '__main__':
    start()
