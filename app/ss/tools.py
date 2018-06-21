#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os
import cfscrape
from selenium import webdriver
from selenium.webdriver.firefox.options import Options


def cf_request(url, *args, **kwargs):
    # request from cloud flare ddos protected sites
    scraper = cfscrape.create_scraper()
    response = scraper.get(url)
    return response


def load_headless_webdriver():
    webdriver_path = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'lib', 'geckodriver')
    print('load geckodriver from:', webdriver_path)
    try:
        ops = Options()
        ops.set_headless(headless=True)
        driver = webdriver.Firefox(firefox_options=ops, executable_path=webdriver_path)
        return driver
    except Exception as e:
        return e


if __name__ == '__main__':
    load_headless_webdriver()