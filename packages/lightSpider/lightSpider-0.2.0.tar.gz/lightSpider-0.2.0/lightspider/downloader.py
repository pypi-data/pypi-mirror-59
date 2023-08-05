import requests

from lightspider.utils.proxy import get_proxy


def get_response(url, use_proxy=False):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
                      'Chrome/79.0.3945.88 Safari/537.36'
    }
    if use_proxy:
        proxy = get_proxy()
        if proxy:
            proxy = {
                'http': proxy
            }
    else:
        proxy = None
    r = requests.get(url, headers=headers, proxies=proxy, timeout=3)
    if r.status_code == requests.codes.ok:
        if r.encoding != 'utf-8':
            r.encoding = 'utf-8'
        return r
    return None
