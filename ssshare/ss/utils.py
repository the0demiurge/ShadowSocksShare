import requests
from urllib.parse import urlparse
from urllib.robotparser import RobotFileParser
import time


def robots_get(url, *args, **kwargs):
    u = urlparse(url)
    robot_url = '{scm}://{loc}/robots.txt'.format(scm=u.scheme, loc=u.netloc)
    robot = RobotFileParser(robot_url)
    robot.read()
    ua = kwargs.get('headers', dict()).get('User-Agent', '*')
    if not robot.can_fetch(ua, url):
        return 'Not Allowed By robots.txt'
    delay = robot.crawl_delay(ua)
    if delay:
        time.sleep(delay)
    return requests.get(url, *args, **kwargs)
