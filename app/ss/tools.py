#!/usr/bin/env python
# -*- coding: utf-8 -*-
import cfscrape


def cf_request(url, *args, **kwargs):
    # request from cloud flare ddos protected sites
    scraper = cfscrape.create_scraper()
    response = scraper.get(url)
    return response
