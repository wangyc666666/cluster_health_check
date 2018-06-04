#!/usr/bin/env python
# -*- coding: utf-8 -*-
# __author__ = 'wangyc'
# __time__ = 2018/2/7 23:18
# Copyright (c) 2018 WangSu Corp.
# All Rights Reserved.


from oslo_config import cfg

general_group = cfg.OptGroup("general",
                             title="controller_master Options",
                             help="""monitor items need to be checked on both compute and controller""")
generalOpts = [
    cfg.ListOpt('service',
                default=[],
                help="""service need tobe monitored"""),
    cfg.ListOpt('process',
                default=[],
                help="""process need tobe monitored"""),
    cfg.ListOpt('extra',
                default=[],
                help="""extra need tobe monitored"""),
    cfg.ListOpt('disk',
                default=[],
                help="""disk need tobe monitored"""),
]

controller_group = cfg.OptGroup("controller",
                                title="controller options",
                                help="""monitor items need to be checked on controller""")
controllerOpts = [
    cfg.ListOpt('service',
                default=[],
                help="""service need tobe monitored"""),
    cfg.ListOpt('process',
                default=[],
                help="""process need tobe monitored"""),
    cfg.ListOpt('extra',
                default=[],
                help="""extra need tobe monitored"""),
    cfg.ListOpt('disk',
                default=[],
                help="""disk need tobe monitored"""),
]


compute_group = cfg.OptGroup("compute",
                             title="compute options",
                             help="""monitor items need to be checked on compute""")
computeOpts = [
    cfg.ListOpt('service',
                default=[],
                help="""service need tobe monitored"""),
    cfg.ListOpt('process',
                default=[],
                help="""process need tobe monitored"""),
    cfg.ListOpt('extra',
                default=[],
                help="""extra need tobe monitored"""),
    cfg.ListOpt('disk',
                default=[],
                help="""disk need tobe monitored"""),
]


default_opts = [
    cfg.IntOpt('interval', default=60,
               help="""
               Said how long interval executable program (Unit s)
               """),
    cfg.IntOpt('repeat_alarm_interval', default=300,
               help="""
               Said how long alarm again (Unit s)
               """),
    cfg.IntOpt('disk_usage_threshold', default=90,
               help="""Said if disk usage id greater than this value, then report this alarm item (Unit %)
           """),
]
sys_opts = [
    cfg.BoolOpt('debug',
                default=False,
                help="Whether to open the debug the default False."),

    cfg.StrOpt('log_file',
               default='cluster_health_check.log',
               help="log_config_append is set. (string value)"
               ),

    cfg.StrOpt('log_dir',
               default='/var/log/cluster_health_check',
               help="is ignored if log_config_append is set. (string value)"
               ),

    cfg.BoolOpt('use_stderr',
                default=False,
                help="""
                # Log output to standard error. This option is ignored if log_config_append is
                # set. (boolean value)
                """
                ),
]

opts = sys_opts + default_opts


def opts_register():
    cfg.CONF.register_opts(default_opts)


def register_general():
    cfg.CONF.register_group(general_group)
    cfg.CONF.register_opts(generalOpts, group=general_group)


def register_controller():
    cfg.CONF.register_group(controller_group)
    cfg.CONF.register_opts(controllerOpts, group=controller_group)


# def register_controller_master():
#     cfg.CONF.register_group(controller_master_group)
#     cfg.CONF.register_opts(controllerMasterOpts, group=controller_master_group)


# def register_controller_standby():
#     cfg.CONF.register_group(controller_standby_group)
#     cfg.CONF.register_opts(controllerStandbyOpts, group=controller_standby_group)


def register_compute():
    cfg.CONF.register_group(compute_group)
    cfg.CONF.register_opts(computeOpts, group=compute_group)


def list_opts():
    # Allows the generation of the help text for
    # the baz_group OptGroup object. No help
    # text is generated for the 'blaa' group.
    return [('DEFAULT', opts),
            (general_group, generalOpts),
            (controller_group, controllerOpts),
            (compute_group, computeOpts)
            ]

