import requests
from urllib.parse import urlparse
from urllib.robotparser import RobotFileParser


def robots_get(url, *args, **kwargs):
    u = urlparse(url)
    robot_url = '{scm}://{loc}/robots.txt'.format(scm=u.scheme, loc=u.netloc)
    robot = RobotFileParser(robot_url)
    robot.read()
    ua = kwargs.get('headers', dict()).get('User-Agent', '*')
    if not robot.can_fetch(ua, url):
        return 'Not Allowed By robots.txt'
    return requests.get(url, *args, **kwargs)
