#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os
import socket
from oslo_log import log as logging
import sys
import threading
LOG = logging.getLogger(__name__)


def get_hostname():
    hostname = socket.gethostname()
    return hostname


def get_host_ip():
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.connect(("8.8.8.8", 80))
    return s.getsockname()[0]


def is_public_controller():
    """
    check if the controller node can access public net
    :return: bool
    """
    try:
        command = "/usr/sbin/crm status | grep publicVip | awk -F ' ' '{print $4}'|head -n 1"
        public_controller = os.popen(command).read().strip()
        hostname = socket.gethostname()
        if hostname == public_controller:
            return True
        else:
            return False
    except Exception as e:
        LOG.error(e)
        sys.exit()


def get_public_ip():
    try:
        get_public_ip_cmd = "sudo /usr/sbin/crm  configure show|grep -A 1 'publicVip IPaddr'" \
                            "|grep 'ip='|awk -F ' ' '{print $2}'|awk -F '=' '{print $2}'"
        public_ip = os.popen(get_public_ip_cmd).read().strip()
        return public_ip
    except Exception as e:
        LOG.error(e)
        return False


class MyThread(threading.Thread):

    def __init__(self, func, args=()):
        super(MyThread, self).__init__()
        self.func = func
        self.args = args

    def run(self):
        self.result = self.func(*self.args)

    def get_result(self):
        try:
            return self.result  # 如果子线程不使用join方法，此处可能会报没有self.result的错误
        except Exception:
            return None