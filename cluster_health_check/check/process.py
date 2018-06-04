#!/usr/bin/env python
# -*- coding: utf-8 -*-
# __author__ = 'wangyc'
# __time__ = 2018/4/13 10:18
# Copyright (c) 2018 WangSu Corp.
# All Rights Reserved.

import os
from cluster_health_check import utils
from oslo_log import log as logging
from oslo_config import cfg

LOG = logging.getLogger(__name__)
CONF = cfg.CONF
LAST_PROCESSES_INFO = {}


def check_process(process, now=None, repeat_alarm_interval=None):
    global LAST_PROCESSES_INFO
    LOG.debug('start %s monitor' % process)
    cmd = 'ps -ef|grep %s|grep -v "grep"|wc -l' % process
    result = os.popen(cmd).read().strip()
    LOG.debug('check {%s:%s}' % (process, result))
    result = int(result)
    data = {}
    if result >= 1:
        if LAST_PROCESSES_INFO.get(process):
            data = {process: 'active'}
            del LAST_PROCESSES_INFO[process]
    else:
        if LAST_PROCESSES_INFO.get(process):
            if round(now - LAST_PROCESSES_INFO.get(process)['check_time'], 3) >= repeat_alarm_interval:
                data = {process: 'unknown'}
                LAST_PROCESSES_INFO[process]['check_time'] = now
        else:
            data = {process: 'unknown'}
            LAST_PROCESSES_INFO.update({process: {'check_time': now}})

    return data


def monitor_processes(processes, now, repeat_alarm_interval):
    """

    :param processes:
    :param now:
    :param repeat_alarm_interval:
    :return:
    """

    global LAST_PROCESSES_INFO
    if not processes:
        LOG.debug('Please pass in monitor argument')
        return {}

    check_queue = []
    process_report = {}

    try:
        for s in processes:
            if s:
                check_exec = utils.MyThread(check_process, args=(s, now, repeat_alarm_interval))
                check_queue.append(check_exec)
                check_exec.start()
                check_exec.join()
        for q in check_queue:
            if q.result:
                # LOG.debug("-------process------q.result: %r" % q.result)
                process_report.update(q.result)
    except Exception as e:
        LOG.error(str(e))
    LOG.debug('check all process %s' % process_report)
    LOG.debug('check  LAST_PROCESSES_INFO %s' % LAST_PROCESSES_INFO)

    return process_report
