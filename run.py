# -*- coding: UTF-8 –*-
from proxypool.scheduler import Scheduler
import sys
import io
# apt-get install -y build-essential libzbar-dev
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')


def main():
    try:
        print('开始运行调度器')
        s = Scheduler()
        s.run()
    except:
        main()


if __name__ == '__main__':
    main()