import asyncio
import time
import sys
from proxypool.util import validate
try:
    from aiohttp import ClientError
except ImportError:
    from aiohttp import ClientProxyConnectionError as ProxyConnectionError
from proxypool.db import RedisClient
from proxypool.setting import *


class Tester(object):
    def __init__(self):
        self.redis = RedisClient()

    def test_single_proxy(self, proxy):
        """
        测试单个代理
        :param proxy:
        :return:
        """
        try:
            server = eval(proxy)
            if validate(server):
                self.redis.max(proxy)
                print('代理可用', proxy)
            else:
                self.redis.decrease(proxy)
                print('请求响应码不合法 ', 'ss_data', proxy)
        except Exception:
            self.redis.decrease(proxy)
            print('代理测试失败', proxy)

    def run(self):
        """
        测试主函数
        :return:
        """
        print('测试器开始运行')
        try:
            count = self.redis.count()
            print('当前剩余', count, '个代理')
            for i in range(0, count, BATCH_TEST_SIZE):
                start = i
                stop = min(i + BATCH_TEST_SIZE, count)
                print('正在测试第', start + 1, '-', stop, '个代理')
                test_proxies = self.redis.batch(start, stop)
                loop = asyncio.get_event_loop()
                tasks = [self.test_single_proxy(proxy) for proxy in test_proxies]
                loop.run_until_complete(asyncio.wait(tasks))
                sys.stdout.flush()
                time.sleep(5)
        except Exception as e:
            print('测试器发生错误', e.args)
