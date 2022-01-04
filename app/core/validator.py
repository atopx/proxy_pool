from re import findall

import requests
from requests import head
from util.metaclass import with_metaclass
from util.singleton import Singleton
from handler.config import Config

conf = Config()

HEADER = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:34.0) Gecko/20100101 Firefox/34.0',
          'Accept': '*/*',
          'Connection': 'keep-alive',
          'Accept-Language': 'zh-CN,zh;q=0.8'}


class ProxyValidator(with_metaclass(Singleton)):
    pre_validator = []
    http_validator = []
    https_validator = []

    @classmethod
    def add_pre_validator(cls, func):
        cls.pre_validator.append(func)
        return func

    @classmethod
    def add_http_validator(cls, func):
        cls.http_validator.append(func)
        return func

    @classmethod
    def add_https_validator(cls, func):
        cls.https_validator.append(func)
        return func


@ProxyValidator.add_pre_validator
def format_validator(proxy):
    """检查代理格式"""
    verify_regex = r"\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}:\d{1,5}"
    _proxy = findall(verify_regex, proxy)
    return True if len(_proxy) == 1 and _proxy[0] == proxy else False


@ProxyValidator.add_http_validator
def http_time_out_validator(proxy):
    """ http检测超时 """

    proxies = {"http": "http://{proxy}".format(proxy=proxy), "https": "https://{proxy}".format(proxy=proxy)}

    try:
        r = head(conf.http_url, headers=HEADER, proxies=proxies, timeout=conf.verify_timeout)
        return True if r.status_code == 200 else False
    except requests.RequestException:
        return False


@ProxyValidator.add_https_validator
def https_time_out_validator(proxy):
    """https检测超时"""

    proxies = {"http": "http://{proxy}".format(proxy=proxy), "https": "https://{proxy}".format(proxy=proxy)}
    try:
        r = head(conf.https_url, headers=HEADER, proxies=proxies, timeout=conf.verify_timeout, verify=False)
        return True if r.status_code == 200 else False
    except requests.RequestException:
        return False


@ProxyValidator.add_http_validator
def custom_validator_example(proxy):
    """自定义validator函数，校验代理是否可用, 返回True/False"""
    print(f"custom validator: {proxy}")
    return True
