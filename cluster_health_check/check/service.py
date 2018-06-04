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

LAST_SERVICES_INFO = {}


def check_service(service, now=None, repeat_alarm_interval=None):
    global LAST_SERVICES_INFO
    data = {}

    try:
        LOG.debug('start %s monitor' % service)
        cmd = '/usr/bin/systemctl is-active %s' % service
        result = os.popen(cmd).read().strip()
        LOG.debug('check {%s:%s}' % (service, result))
        if result == 'active':
            if LAST_SERVICES_INFO.get(service):
                data = {service: 'active'}
                del LAST_SERVICES_INFO[service]

        else:
            if LAST_SERVICES_INFO.get(service):
                LOG.debug("----temp interval------:%r" % round(now - LAST_SERVICES_INFO.get(service)['check_time'], 1))
                LOG.debug("----temp repeat_alarm_interval------:%r" % repeat_alarm_interval)
                if round(now - LAST_SERVICES_INFO.get(service)['check_time'], 3) >= repeat_alarm_interval:
                    LAST_SERVICES_INFO[service]['check_time'] = now
                    data = {service: 'unknown'}

            else:
                data = {service: 'unknown'}
                LAST_SERVICES_INFO.update({service: {'check_time': now}})
            LOG.debug("----temp LAST_SERVICES_INFO------:%r" % LAST_SERVICES_INFO)

    except Exception as e:
        LOG.error(str(e))

    return data


def monitor_services(services=None, now=None, repeat_alarm_interval=None):
    """
    To view the service if the service is normal
    :param repeat_alarm_interval:
    :param now:
    :param services:
    :return: Boolean
    """

    global LAST_SERVICES_INFO
    if not services:
        LOG.debug('Please pass in monitor argument')
        return {}

    check_queue = []
    services_report = {}
    try:
        for s in services:
            if s:
                check_exec = utils.MyThread(check_service, args=(s, now, repeat_alarm_interval))
                check_queue.append(check_exec)
                check_exec.start()
                check_exec.join()
        for q in check_queue:
            if q.result:
                # LOG.debug("-------service------q.result: %r" % q.result)
                services_report.update(q.result)

        LOG.debug('check all service %s' % services_report)
        LOG.debug('check  LAST_SERVICES_INFO %s' % LAST_SERVICES_INFO)

    except Exception as e:
        LOG.error(str(e))

    return services_report
