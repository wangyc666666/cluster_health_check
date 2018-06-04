#!/usr/bin/env python
# -*- coding: utf-8 -*-
# __author__ = 'wangyc'
# __time__ = 2018/4/13 10:18
# Copyright (c) 2018 WangSu Corp.
# All Rights Reserved.

import sys
from cluster_health_check.check import disk
from cluster_health_check.check import extra
from cluster_health_check.check import process
from cluster_health_check.check import service
from cluster_health_check.conf import app
from cluster_health_check import utils
from oslo_log import log as logging
from oslo_config import cfg
import time
LOG = logging.getLogger(__name__)
CONF = cfg.CONF


def check_items(items, module, last_items=None, time=None, threshold=90):
    """

    :param items: services, process, disks, or something else in extras
    :param module: specify the module to monitor the items you give
    :param last_items: the alarm items sent last time
    :param time:
    :param threshold: just used for check disk usage for now
    :return:
    """
    if not module:
        LOG.error("please specify the module to monitor the items you give")
        sys.exit()

    if items:
        results = []
        for item in items:
            monitor_run = MyThread(module.monitor_service, args=(item, time, threshold))
            results.append(monitor_run)
            monitor_run.start()
            monitor_run.join()

        # datas = [r.data for r in results]
        # for trans_data in result:
        #     res.update(trans_data.result)


def all_monitor_start():
    hostname = utils.get_hostname()
    app.opts_register()
    app.register_general()
    app.register_compute()
    app.register_controller()
    interval = CONF.interval
    repeat_alarm_interval = CONF.repeat_alarm_interval
    services = []
    disks = []
    processes = []
    extras = []
    host_ip = ''
    if 'controller' in hostname:
        services = CONF.general.service + CONF.controller.service
        disks = CONF.general.disk + CONF.controller.disk
        processes = CONF.general.process + CONF.controller.process
        extras = CONF.general.extra + CONF.controller.extra
        host_ip = utils.get_public_ip()

    elif 'compute' in hostname:
        services = CONF.general.service + CONF.compute.service
        disks = CONF.general.disk + CONF.compute.disk
        processes = CONF.general.process + CONF.compute.process
        extras = CONF.general.extra + CONF.compute.extra
        host_ip = utils.get_host_ip()

    # print 'services', services
    # print 'disks', disks
    # print 'processes', processes
    # print 'extras', extras

    while True:
        # print 'services', services
        report = {}
        start = time.time()
        if not utils.is_public_controller() and 'haproxy' in services:
            services.remove('haproxy')
        elif utils.is_public_controller() and 'haproxy' not in services:
            services.append('haproxy')

        report['service'] = service.monitor_services(services, start, repeat_alarm_interval)
        report['process'] = process.monitor_processes(processes, start, repeat_alarm_interval)
        report['disk'] = disk.monitor_disks(disks, start, repeat_alarm_interval, CONF.disk_usage_threshold)
        report['extra'] = extra.monitor_extra(extras, start, repeat_alarm_interval)

        host_info = {'host_name': hostname,
                     'host_ip': host_ip,
                     }
        report['host_info'] = host_info
        LOG.info("---------report------: %r" % report)

        end = time.time()
        LOG.info('Execute all_monitor_start cost ' + str(round(end - start, 3)) + 's')
        time.sleep(interval)

