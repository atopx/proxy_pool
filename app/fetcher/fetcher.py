import re
from time import sleep

from util.http import HttpRequest


class ProxyFetcher(object):
    # proxy crawler

    @staticmethod
    def free_proxy01():
        # 米扑代理 https://proxy.mimvp.com/
        url_list = [
            'https://proxy.mimvp.com/freeopen?proxy=in_hp',
            'https://proxy.mimvp.com/freeopen?proxy=out_hp'
        ]
        port_img_map = {'DMxMjg': '3128', 'Dgw': '80', 'DgwODA': '8080',
                        'DgwOA': '808', 'DgwMDA': '8000', 'Dg4ODg': '8888',
                        'DgwODE': '8081', 'Dk5OTk': '9999'}
        for url in url_list:
            html_tree = HttpRequest().get(url).tree
            for tr in html_tree.xpath(".//table[@class='mimvp-tbl free-proxylist-tbl']/tbody/tr"):
                try:
                    ip = ''.join(tr.xpath('./td[2]/text()'))
                    port_img = ''.join(tr.xpath('./td[3]/img/@src')).split("port=")[-1]
                    port = port_img_map.get(port_img[14:].replace('O0O', ''))
                    if port:
                        yield '%s:%s' % (ip, port)
                except Exception as e:
                    print(e)

    @staticmethod
    def free_proxy02():
        # 代理66 http://www.66ip.cn/
        url = "http://www.66ip.cn/mo.php"

        resp = HttpRequest().get(url, timeout=10)
        proxies = re.findall(r'(\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}:\d{1,5})', resp.text)
        for proxy in proxies:
            yield proxy

    @staticmethod
    def free_proxy03():
        # 开心代理
        target_urls = ["http://www.kxdaili.com/dailiip.html", "http://www.kxdaili.com/dailiip/2/1.html"]
        for url in target_urls:
            tree = HttpRequest().get(url).tree
            for tr in tree.xpath("//table[@class='active']//tr")[1:]:
                ip = "".join(tr.xpath('./td[1]/text()')).strip()
                port = "".join(tr.xpath('./td[2]/text()')).strip()
                yield "%s:%s" % (ip, port)

    @staticmethod
    def free_proxy04():
        # 蝶鸟IP
        url = "https://www.dieniao.com/FreeProxy.html"
        tree = HttpRequest().get(url, verify=False).tree
        for li in tree.xpath("//div[@class='free-main col-lg-12 col-md-12 col-sm-12 col-xs-12']/ul/li")[1:]:
            ip = "".join(li.xpath('./span[1]/text()')).strip()
            port = "".join(li.xpath('./span[2]/text()')).strip()
            yield "%s:%s" % (ip, port)

    @staticmethod
    def free_proxy05(page_count=1):
        # 快代理 https://www.kuaidaili.com
        url_pattern = [
            'https://www.kuaidaili.com/free/inha/{}/',
            'https://www.kuaidaili.com/free/intr/{}/'
        ]
        url_list = []
        for page_index in range(1, page_count + 1):
            for pattern in url_pattern:
                url_list.append(pattern.format(page_index))

        for url in url_list:
            tree = HttpRequest().get(url).tree
            proxy_list = tree.xpath('.//table//tr')
            sleep(1)  # 必须sleep 不然第二条请求不到数据
            for tr in proxy_list[1:]:
                yield ':'.join(tr.xpath('./td/text()')[0:2])

    @staticmethod
    def free_proxy06():
        # PROXY11 https://proxy11.com
        url = "https://proxy11.com/api/demoweb/proxy.json?country=hk&speed=2000"
        try:
            resp_json = HttpRequest().get(url).json
            for each in resp_json.get("data", []):
                yield "%s:%s" % (each.get("ip", ""), each.get("port", ""))
        except Exception as e:
            print(e)

    @staticmethod
    def free_proxy07():
        # 云代理
        urls = ['http://www.ip3366.net/free/?stype=1', "http://www.ip3366.net/free/?stype=2"]
        for url in urls:
            r = HttpRequest().get(url, timeout=10)
            proxies = re.findall(r'<td>(\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})</td>[\s\S]*?<td>(\d+)</td>', r.text)
            for proxy in proxies:
                yield ":".join(proxy)

    @staticmethod
    def free_proxy08():
        # 小幻代理
        urls = ['https://ip.ihuan.me/address/5Lit5Zu9.html']
        for url in urls:
            r = HttpRequest().get(url, timeout=10)
            proxies = re.findall(r'>\s*?(\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})\s*?</a></td><td>(\d+)</td>', r.text)
            for proxy in proxies:
                yield ":".join(proxy)

    @staticmethod
    def free_proxy09(page_count=1):
        # 免费代理库
        for i in range(1, page_count + 1):
            url = 'http://ip.jiangxianli.com/?country=中国&page={}'.format(i)
            html_tree = HttpRequest().get(url).tree
            for index, tr in enumerate(html_tree.xpath("//table//tr")):
                if index == 0:
                    continue
                yield ":".join(tr.xpath("./td/text()")[0:2]).strip()

    @staticmethod
    def free_proxy10():
        # 89免费代理
        matcher = re.compile(
            r'<td.*?>[\s\S]*?(\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})[\s\S]*?</td>[\s\S]*?<td.*?>[\s\S]*?(\d+)[\s\S]*?</td>'
        )
        r = HttpRequest().get("https://www.89ip.cn/index_1.html", timeout=10)
        for proxy in matcher.findall(r.text):
            yield ':'.join(proxy)


if __name__ == '__main__':
    p = ProxyFetcher()
    for _ in p.free_proxy10():
        print(_)
