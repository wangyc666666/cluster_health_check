#!/usr/bin/env python
# -*- coding: utf-8 -*-
# __author__ = 'wangyc'
# __time__ = 2018/4/13 11:18
# Copyright (c) 2018 WangSu Corp.
# All Rights Reserved.

from oslo_log import log as logging
from oslo_config import cfg


def load_file(file_dir):
    CONF = cfg.CONF
    logging.register_options(CONF)
    cfg.CONF(default_config_files=[file_dir])
    logging.setup(CONF, __name__)

# def init_log(self):
#     logging.register_options(self.CONF)
#     logging.setup(self.CONF, __name__)


def loadLog():
    '''
    载入日志配置文件
    :return:
    '''
    load_file('/etc/cluster_health_check/health_check.conf')
    #load_health.load_file('/etc/cluster_health_check/health_check.conf')


