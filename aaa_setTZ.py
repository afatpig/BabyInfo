#!/usr/bin/env python3
# -*- coding:utf-8 -*-
"""
Set timezone according to config.conf
Must import before all other modules
"""
import configparser
import os
import traceback

__configfn = 'config.conf'
if not os.path.exists(__configfn):
    print('Config file "{0}" not exists'.format(__configfn))

try:
    config = configparser.ConfigParser()
    config.read(__configfn, encoding='utf-8')
    os.environ['TZ'] = config.get('web', 'timezone')
except:
    print("Error when initializing timezone!")
    print(traceback.format_exc)
    exit(-1)
