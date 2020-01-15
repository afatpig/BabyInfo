#!/usr/bin/env python3
# -*- coding:utf-8 -*-
"""
孩子蓝图
定义蓝图pg_child，实现孩子相关页面蓝图
"""
from urllib import parse

from flask import Blueprint, redirect, render_template, request, abort

import funcs
import global_var as gv
from api_loginout import loggeduser, verify_auto

# 定义蓝图-------------------------------------------------
pg_child = Blueprint(
    'pg_child',
    __name__,
    template_folder='templates'
)

# views------------------------------------------------


@pg_child.route('/childinfo', methods=['GET'])
def childinfo_get():
    _cid = request.args.get('id')
    if _cid is None:
        abort(404)
    _un, _role = loggeduser(request)
    return render_template('infopage.html', loggeduser=_un,
                           uid=_cid, role='childinfo')


@pg_child.route('/addchild', methods=['GET'])
def addchild_get():
    _un, _role = loggeduser(request)
    return render_template('addchild.html', loggeduser=_un)

@pg_child.route('/childlist', methods=['GET'])
def childlist_get():
    _un, _role = loggeduser(request)
    return render_template('childlist.html', loggeduser=_un)

@pg_child.route('/alterchild', methods=['GET'])
def alterchild_get():
    _cid = request.args.get('id')
    if _cid is None:
        abort(404)
    _un, _role = loggeduser(request)
    return render_template('alterchild.html', loggeduser=_un, cid=_cid)

@pg_child.route('/filelist', methods=['GET'])
def filelist_get():
    _un, _role = loggeduser(request)
    return render_template('filelist.html', loggeduser=_un)
@pg_child.route('/file', methods=['GET'])
def file_get():
    _fid = request.args.get('id')
    if _fid is None:
        abort(404)
    _un, _role = loggeduser(request)
    return render_template('file.html', loggeduser=_un, fid=_fid)
@pg_child.route('/upfile', methods=['GET', 'POST'])
def upfile():
    _un, _role = loggeduser(request)
    return render_template('upfile.html', loggeduser=_un)
