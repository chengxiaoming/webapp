#!/usr/bin
# -*- coding=utf-8 -*-
__author__ = 'Michael'

'''
orm
'''

import asyncio,logging
import aiomysql

async def create_pool(loop,**kw):
    logging.info('create database connection pool')
    global __pool
    __pool = await aiomysql.create_pool(
        host=kw.get('host','localhost'),
        prot=kw.get('port',3306),
        user = kw['user'],
        password =kw['password'],
        db=kw['db'],
        charset=kw.get('charset','utf8'),
        autocommit=kw.get('autocommit',True),
        maxsize=kw.get('maxsize',10),
        minsize=kw.get('minsize',1),
        loop=loop
    )

async def select(sql,args,size=None):
    logging.info(sql,args)
    global __pool
    with (await __pool) as conn:
        cur = await conn.cursor(aiomysql.DictCursor)
        await cur.execute(sql.replace('?','%s'), args or ())
        if size:
            rs=await cur.fetchmany(size)
        else:
            rs=await cur.fetchall()
        await cur.close()
        logging.info('rows returned:%s' % len(rs))
        return rs

async def execute(sql,args):
    logging.info(sql,args)
    global __pool
    with (await __pool) as conn:
        cur = await conn.cursor()
        await cur.execute(sql.replace('?','%s'),args)
        affected = cur.rowcount
        await cur.close()
        return affected


class Model(dict,metaclass=modelMetaclass):
    def __init__(self,**kw):
        super(Model,self).__init__(**kw)
    def __getattr__(self, key):
        try:
            return self[key]
        except KeyError:
            raise AttributeError('')
    def __setattr__(self, key, value):
        self[key] = value
    def getValue(self,key):
        return getattr(self,key,None)
    def getValueOrDefault(self,key):
        value=getattr(self,key,None)
        if value is None:

