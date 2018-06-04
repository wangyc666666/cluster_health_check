#!/usr/bin/env python
# -*- coding: utf-8 -*-
# __author__ = 'wangyc'
# __time__ = 2018/4/13 10:58
# Copyright (c) 2018 WangSu Corp.
# All Rights Reserved.


from setuptools import setup, find_packages


setup(
    name="cluster_health_check",
    version="1.0.0",
    author="wangyc",
    author_email="wangyc@wangsu.com",
    description="Cluster all service health check",
    packages=find_packages(),
    classifiers=[
        'Programming Language :: Python',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
    ],
    zip_safe=False,
    entry_points={
        'console_scripts': [
            'health_check = cluster_health_check.cmd.main:main',
        ],
        'oslo.config.opts': [
            'cluster_health_check.conf = cluster_health_check.conf.app:list_opts'
        ]

    }
)
