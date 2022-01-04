from abc import ABC

from flask import Flask, request
from gunicorn.app.base import BaseApplication
from six import iteritems

from core.proxy import Proxy
from handler.config import Config
from handler.proxy import ProxyHandler

app = Flask(__name__)
config = Config()
proxy_handler = ProxyHandler()


@app.route("/")
def index():
    return {
        "routers": [
            {"url": "/get", "params": "type: ''https'|''", "desc": "get a proxy"},
            {"url": "/pop", "params": "", "desc": "get and delete a proxy"},
            {"url": "/delete", "params": "proxy: 'e.g. 127.0.0.1:8080'", "desc": "delete an unable proxy"},
            {"url": "/all", "params": "type: ''https'|''", "desc": "get all proxy from proxy pool"},
            {"url": "/count", "params": "", "desc": "return proxy count"}
        ]
    }


@app.route("/get")
def get():
    https = request.args.get("type", "").lower() == 'https'
    proxy = proxy_handler.get(https)
    return proxy.to_dict if proxy else {"code": 0, "src": "no proxy"}


@app.route('/pop')
def pop():
    https = request.args.get("type", "").lower() == 'https'
    proxy = proxy_handler.pop(https)
    return proxy.to_dict if proxy else {"code": 0, "src": "no proxy"}


@app.route('/all')
def get_all():
    https = request.args.get("type", "").lower() == 'https'
    proxies = proxy_handler.get_all(https)
    return {"code": 0, "data": [p.to_dict for p in proxies]}


@app.route('/delete', methods=['GET'])
def delete():
    proxy = request.args.get('proxy')
    return {"code": 0, "src": proxy_handler.delete(Proxy(proxy))}


@app.route('/count')
def get_count():
    return proxy_handler.get_count()


class StandaloneApplication(BaseApplication, ABC):
    def __init__(self, application, options=None):
        self.options = options or dict()
        self.application = application
        super(StandaloneApplication, self).__init__()

    def load_config(self):
        _config = dict([(key, value) for key, value in iteritems(self.options)
                        if key in self.cfg.settings and value is not None])
        for key, value in iteritems(_config):
            self.cfg.set(key.lower(), value)

    def load(self):
        return self.application


def start():
    server = StandaloneApplication(app, {
        'bind': '%s:%s' % (config.server_host, config.server_port),
        'workers': 4,
        'accesslog': '-',
        'access_log_format': '%(h)s %(l)s %(t)s "%(r)s" %(s)s "%(a)s"'
    })
    server.run()


if __name__ == '__main__':
    start()
