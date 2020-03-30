# -*- coding: utf-8 -*-
import os

from utilities import logger
from utilities.clean_env import clean_all
from datetime import datetime


class Base(object):

    @classmethod
    def setup_class(cls, logger_name=None):
        log_file = f'./logs/skyTest_{logger_name}_{datetime.now().strftime("%Y%m%d-%H-%M-%S")}.log'
        if not os.path.exists('logs'):
            os.mkdir('logs')
        log_level = "DEBUG"
        logger.setup_logger(log_level, log_file)

    def setup(self):

        # clean_all() # 会删除其它用户的数据，非自动化测试环境勿打开

        logger.log_debug('')
        logger.log_debug('########### New Case Started ###########')


    def teardown(self):
        logger.log_debug('@@@@@@@@@@@@@@ Case Finished @@@@@@@@@@@@@@')
