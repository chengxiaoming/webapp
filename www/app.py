#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = 'Michael'
'''
web app
'''

import logging;logging.basicConfig(level=logging.INFO)
import asyncio,os,json,time
from datetime import datetime
from aiohttp import web

def index(req):
    return web.Response(body='b<h1>hello world</h1>')


async def init(loop):
    app = web.Application(loop=loop)
    app.router.add_route('Get','/',index)
    srv = await loop.create_server(app.make_handler(),'127.0.0.1',9000)
    logging.info('server started listening 127.0.0.1:9000')

loop = asyncio.get_event_loop()
loop.run_until_complete(init(loop))
loop.run_forever()
