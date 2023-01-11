# Copyright (c) 2023.
# !/usr/bin/python
# -*- coding: UTF-8 -*-
# @Project: MIDEP
# @FileName: Database/Mysql.py
# @Author：Ryan Zhang    (https://github.com/hz157)
# @DateTime: 10/1/2023 下午11:45
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from Config import config
from Utils.logutils import LogUtils

logutils = LogUtils()


class Mysql:
    """
    Mysql Module
    """
    def __new__(cls, *args, **kwargs):
        session = None
        """
        Initialize
        :param args:
        :param kwargs:
        """
        try:
            logutils.info("Mysql engine")
            engine = create_engine(
                    f'{config.Mysql_dialect}+{config.Mysql_driver}://{config.Mysql_username}:{config.Mysql_password}@{config.Mysql_host}:{config.Mysql_port}/{config.Mysql_database}',
                    pool_size=config.Mysql_pool_size,
                    pool_recycle=config.Mysql_pool_recycle,
                    echo=config.Mysql_echo)
            MysqlSession = sessionmaker(bind=engine)
            session = MysqlSession()
            logutils.info("Mysql complete")
        except Exception as e:
            logutils.error(e)
        return session
