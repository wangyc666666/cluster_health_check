#!/usr/bin/env python
# -*- coding: utf-8 -*-
# __author__ = 'wangyc'
# __time__ = 2018/4/13 10:18
# Copyright (c) 2018 WangSu Corp.
# All Rights Reserved.

import commands
import os
import sys

from oslo_config import cfg
from oslo_log import log as logging
from cluster_health_check.cmd import service
from cluster_health_check.log.logme import loadLog

CONF = cfg.CONF
LOG = logging.getLogger(__name__)


def mkdir_dir(path=None):
    if not path:
        return
    existed = os.path.exists(path)
    if not existed:
        os.makedirs(path)


def if_process_already(process=None):
    if not process:
        return
    cmd = 'ps -ef|grep %s|grep -v "grep"|wc -l' % process
    (status, output) = commands.getstatusoutput(cmd)
    if status == 0:
        output = int(output.strip())
        if output > 1:
            LOG.warning('%s already running' % process)
            sys.exit()


def main():
    """
    run cluster health check script
    :return:
    """
    mkdir_dir('/var/log/cluster_health_check')
    mkdir_dir('/etc/cluster_health_check/')
    loadLog()
    if_process_already('/usr/bin/cluster_health_check')
    service.all_monitor_start()

main()






