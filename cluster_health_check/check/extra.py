#!/usr/bin/env python
# -*- coding: utf-8 -*-
# __author__ = 'wangyc'
# __time__ = 2018/4/13 10:18
# Copyright (c) 2018 WangSu Corp.
# All Rights Reserved.

import os
from oslo_log import log as logging
from oslo_config import cfg
from cluster_health_check import utils
LOG = logging.getLogger(__name__)
CONF = cfg.CONF

EXECS = {'ping': "ping vod-edge.mirpull.8686c.com -c 4 | grep '0%'| wc -l",
         'crontab': "cat /var/spool/cron/root | grep %s| wc -l",
         'ksm': 'systemctl is-enabled ksm | grep enabled | wc -l',
         'mountstats': ' mountstats | grep %s | wc -l',
         'ntp': 'cat /var/spool/cron/root | grep -o -E "([0-9]{1,3}[\.]){3}[0-9]{1,3}" | xargs  /usr/sbin/ntpdate | grep offset | wc -l',
         }

LAST_EXECS_INFO = {}


def check_item(item, now=None, repeat_alarm_interval=None):
    global LAST_EXECS_INFO
    data = {}

    try:
        if ':' in item:
            ex, params = item.split(':')
            cmd = EXECS[ex] % params
        else:
            cmd = EXECS[item]

        LOG.debug('start %s monitor' % item)

        result = os.popen(cmd).read().strip()
        result = int(result)
        LOG.debug('check {%s:%s}' % (item, result))
        if result == 1:
            if LAST_EXECS_INFO.get(item):
                data = {item: 'active'}
                del LAST_EXECS_INFO[item]

        else:
            if LAST_EXECS_INFO.get(item):
                if round(now - LAST_EXECS_INFO.get(item)['check_time'], 3) >= repeat_alarm_interval:
                    LAST_EXECS_INFO[item]['check_time'] = now
                    data = {item: 'unknown'}

            else:
                data = {item: 'unknown'}
                LAST_EXECS_INFO.update({item: {'check_time': now}})
    except Exception as e:
        LOG.error(str(e))
        return data


def monitor_extra(exec_items=None, time=None, repeat_alarm_interval=None):
    """
    To view the exec_item if the service is normal

    :param exec_items:
    :param time:
    :param repeat_alarm_interval:
    :return:
    """

    global LAST_EXECS_INFO
    extra_report = {}
    if not exec_items:
        LOG.debug('Please pass in monitor argument')
        return {}

    check_queue = []
    try:
        for item in exec_items:
            if item:
                check_exec = utils.MyThread(check_item, args=(item, time, repeat_alarm_interval))
                check_queue.append(check_exec)
                check_exec.start()
                check_exec.join()

        for q in check_queue:
            if q.result:
                # LOG.debug("-------extra------q.result: %r" % q.result)
                extra_report.update(q.result)

        LOG.debug('check all extra %s' % extra_report)
        LOG.debug('check  LAST_EXECS_INFO %s' % LAST_EXECS_INFO)

    except Exception as e:
        LOG.error(str(e))

    return extra_report
