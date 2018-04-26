import requests
import functools
import logging
from bs4 import BeautifulSoup
import regex as re

from app.ss.parse import parse, scanNetQR, gen_uri
from app.ss.ssr_check import validate
from app.ss.tools import cf_request


LOG_FILENAME = 'logging_example.out'
TIMEOUT = 5

headers = {'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.108 Safari/537.36'}

logging.basicConfig(
    filename = LOG_FILENAME,
    level = logging.ERROR,
)

proxies = {
	"http": "127.0.0.1:8087",
}

def get_html(url, proxies={}):
    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kw):
            print('requesting',url)
            try:
                response = ''
                response = requests.get(url, headers=headers, timeout=TIMEOUT,proxies=proxies).text
            except requests.exceptions.Timeout:
                logging.error('requests timeout: ' + url)
            except Exception as e:
                logging.error(str(e) + url)
            finally:
                return func(response)
        return wrapper
    return decorator


@get_html('https://my.freess.org/', proxies=proxies)
def request_freess_cx(response):
    qr = list()
    servers = list()
    try:
        soup = BeautifulSoup(response, 'html.parser')
        title = soup.find('title').text
        msg = soup.find('section', attrs={'id': 'banner'}).text.strip()

        info = {'message': msg, 'url': url, 'name': str(title)}
        qr = list(map(lambda x: url.strip('/') + '/' + x.find('a').get('href'), soup.find_all('div', attrs={'class': '4u 12u(mobile)'})))
        for i, img_url in enumerate(qr):
            print('req img', img_url)
            try:
                servers.append(parse(scanNetQR(img_url, headers=headers), ' '.join([title, str(i)])))
            except Exception as e:
                print(img_url)
                logging.exception(e, stack_info=False)
                print('IMG_URL FOR freess.cx:', img_url)
    except Exception as e:
        logging.exception(e, stack_info=True)
        return [], {'message': str(e), 'url': '', 'name': ''}
    return servers, info

if __name__ == '__main__':
	server, info = request_freess_cx()
	print(server,info)

