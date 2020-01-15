#!/usr/bin/env python3
# -*- coding:utf-8 -*-
"""
status蓝图
定义蓝图pg_status，实现status相关页面蓝图
"""
from urllib import parse

from flask import Blueprint, redirect, render_template, request, abort

import funcs
import global_var as gv
from api_loginout import loggeduser, verify_auto

# 定义蓝图-------------------------------------------------
pg_status = Blueprint(
    'pg_status',
    __name__,
    template_folder='templates'
)

# views------------------------------------------------

@pg_status.route('/statuslist', methods=['GET'])
def statuslist_get():
    _un, _role = loggeduser(request)
    if _un is None:
        return redirect('/login')
    if _role == 'parent':
        return '<h1>No authority!</h1><p>Login as admin or staff please.</p>'
    return render_template('statuslist.html', loggeduser=_un)

@pg_status.route('/addstatus', methods=['GET'])
def addstatus_get():
    _un, _role = loggeduser(request)
    if _un is None:
        return redirect('/login')
    if _role == 'parent':
        return '<h1>No authority!</h1><p>Login as admin or staff please.</p>'
    _type = request.args.get('type')
    if _type is None:
        abort(404)
    return render_template('addstatus.html',type=_type,loggeduser=_un)