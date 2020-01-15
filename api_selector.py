#!/usr/bin/env python3
# -*- coding:utf-8 -*-
"""
select API蓝图
定义蓝图api_selector，实现selector相关操作蓝图
用於返回預定義常量
视图含义见对应api文档
"""
import traceback

from flask import Blueprint, request
import time
import datetime

import funcs
import global_var as gv
from global_var import enum_error as ee

# 定义蓝图-------------------------------------------------
api_selector = Blueprint(
    'api_selector',
    __name__,
    template_folder='templates'
)

# functions--------------------------------------------

def get_selectors(name):
    resdata = gv.enum_selector[name].values()
    resdata = sorted(resdata, key=lambda x: x['id'])
    res = ee.NORMAL()
    res['data'] = resdata
    res['count'] = len(resdata)
    return res

# views------------------------------------------------

@api_selector.route('/api/group', methods=['GET'])
def get_group_selector():
    res = ee.NORMAL()
    res['data'] = gv.groups
    res['count'] = len(res['data'])
    return res

@api_selector.route('/api/condition', methods=['GET'])
def get_condition_selector():
    return get_selectors('condition')

@api_selector.route('/api/meal_type', methods=['GET'])
def get_meal_type_selector():
    return get_selectors('meal_type')

@api_selector.route('/api/nap_status', methods=['GET'])
def get_nap_status_selector():
    return get_selectors('nap_status')

@api_selector.route('/api/diaper_status', methods=['GET'])
def get_diaper_status_selector():
    return get_selectors('diaper_status')

@api_selector.route('/api/health_status', methods=['GET'])
def get_health_status_selector():
    return get_selectors('health_status')

@api_selector.route('/api/perform_detail', methods=['GET'])
def get_perform_detail_selector():
    return get_selectors('perform_detail')