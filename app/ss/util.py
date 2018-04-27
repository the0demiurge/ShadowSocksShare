import functools
import logging
from bs4 import BeautifulSoup
from app.config import HEADERS, PROXIES, TIMEOUT, LOG_FILENAME
import array
import regex as re
import requests
from PIL import Image
from io import BytesIO
from pyzbar.pyzbar import decode
from app.config import HEADERS
from app.ss.parse import parse
import time

def get_page_html(url, proxies={}):
    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kw):
            print('requesting', url)
            try:
                response = ''
                response = requests.get(url, headers=HEADERS, timeout=TIMEOUT, proxies=proxies).text
            except requests.exceptions.Timeout:
                logging.error('requests timeout: ' + url)
            except Exception as e:
                logging.error(str(e) + url)
            finally:
                return func(response)
        return wrapper
    return decorator


def scanNetQR(url):
    try:
        if isinstance(url, str):
            ss_data = decode(Image.open(BytesIO(requests.get(url, headers=HEADERS,proxies=PROXIES).content)))
            return str(ss_data[0].data, encoding='utf-8')
    except Exception as e:
        logging.ERROR(str(e) + '请求二维码失败')


if __name__ == '__main__':
    dates = scanNetQR('http://my.freess.org/images/servers/jp01.png')
    print(dates)