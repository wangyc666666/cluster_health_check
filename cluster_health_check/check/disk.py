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

LAST_DISKS_INFO = {}


def check_disk(disk, now=None, repeat_alarm_interval=None, threshold=90):
    """
    check disk usage if > 90, if any, report
    :param disk:
    :param now:
    :param repeat_alarm_interval:
    :param threshold:
    :return:
    """
    global LAST_DISKS_INFO
    try:
        data = {}
        LOG.debug('start %s monitor' % disk)
        grep = "| grep -o -E '[0-9]+%'| grep -o -E '[0-9]+'"
        cmd = "df -h %s" % disk + grep
        result = os.popen(cmd).read().strip()
        LOG.debug('check {%s:%s}' % (disk, result))

        if result:
            if int(result) >= threshold:  # > 90 , report
                if LAST_DISKS_INFO.get(disk):
                    if round(now - LAST_DISKS_INFO.get(disk)['check_time'], 3) >= repeat_alarm_interval:
                        data = {disk: result}
                        LAST_DISKS_INFO[disk] = {'value': result, 'check_time': now}
                        return data
                    # else:
                    #  not report, though > 90, but still in repeat_alarm_interval

                else:
                    data = {disk: result}
                    LAST_DISKS_INFO[disk] = {'value': result, 'check_time': now}
            else:
                if LAST_DISKS_INFO.get(disk):  # not normal once, but normal now, so clear it
                    del LAST_DISKS_INFO[disk]
                    # data = {disk: {'value': result}} # no message is good message, so don't report
                    return data

        else:
            data = {disk: 'unknown'}
            if LAST_DISKS_INFO.get(disk):
                if LAST_DISKS_INFO.get(disk)['value'] == 'unknown':  # still lost
                    if round(now - LAST_DISKS_INFO.get(disk)['check_time'], 3) >= repeat_alarm_interval:
                        LAST_DISKS_INFO[disk] = {'value': 'unknown', 'check_time': now}
                        return data
                LAST_DISKS_INFO[disk] = {'value': 'unknown', 'check_time': now}

            LOG.debug('response {%s:%s}' % (disk, result))
    except Exception as e:
        LOG.error(str(e))
    return data


def monitor_disks(disks, now=None, repeat_alarm_interval=None, threshold=90):
    """

    :param disks:
    :param now:
    :param repeat_alarm_interval:
    :param threshold:
    :return:
    """

    global LAST_DISKS_INFO
    if not disks:
        LOG.debug('Please pass in monitor argument')
        return {}
    check_queue = []
    disk_report = {}
    try:
        for s in disks:
            if s:
                check_exec = utils.MyThread(check_disk, args=(s, now, repeat_alarm_interval, threshold))
                check_queue.append(check_exec)
                check_exec.start()
                check_exec.join()

        for q in check_queue:
            if q.result:
                # LOG.debug("-------disk------q.result: %r" % q.result)
                disk_report.update(q.result)

        LOG.debug('check all disk %s' % disk_report)
        LOG.debug('check  LAST_DISKS_INFO %s' % LAST_DISKS_INFO)

    except Exception as e:
        LOG.error(str(e))

    return disk_report


