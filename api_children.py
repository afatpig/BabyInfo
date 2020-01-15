#!/usr/bin/env python3
# -*- coding:utf-8 -*-
"""
孩子API蓝图
定义蓝图api_children，实现孩子相关操作蓝图
视图含义见对应api文档
"""
import traceback

from flask import Blueprint, request
import time
import datetime

import funcs
import global_var as gv
from global_var import enum_error as ee
from db_params import status_tables as sttb
from db_params import status_type_tbn as tptbn
from db_params import get_index
from api_loginout import verify_auto
from api_user import get_id_by_username
from copy import deepcopy

# 定义蓝图-------------------------------------------------
api_children = Blueprint(
    'api_children',
    __name__,
    template_folder='templates'
)


# functions--------------------------------------------
    

def get_cid_by_alias(alias):
    '''
    get cid from db
    '''
    try:
        sqlstr = "select id from child where `alias`='{un}';".format(
            un=funcs.b64encode(alias))
        conn = gv.dbpool.connection()
        cur = conn.cursor()
        cur.execute("SET NAMES UTF8mb4;")
        cur.execute(sqlstr.encode("utf-8", "ignore"))
        pwres = cur.fetchall()
        cur.close()
        conn.close()
        if pwres is None or len(pwres) == 0:
            return ee.NORMAL()
        resu = ee.NORMAL()
        resu['count'] = len(pwres)
        resu['data'].append({
            'id': str(pwres[0][0])})
        return resu
    except:
        gv.logger.error(traceback.format_exc())
        res = ee.DBERR()
        return res



def insert_child():
    """
    insert child info into database
    """
    uid = funcs.get_random_int64()
    tbn = 'child'
    alias = request.form.get('alias')
    flist = [
        {'fn': 'id', 'type': 'int', 'val': uid},
        {'fn': 'name', 'type': 'b64str', 'val': request.form.get('name')},
        {'fn': 'name_chs', 'type': 'b64str',
            'val': request.form.get('name_chs')},
        {'fn': 'alias', 'type': 'b64str', 'val': alias},
        {'fn': 'gender', 'type': 'str', 'val': request.form.get('gender')},
        {'fn': 'religion', 'type': 'b64str',
            'val': request.form.get('religion')},
        {'fn': 'born_day', 'type': 'str', 'val': request.form.get('born_day')},
        {'fn': 'birth_cert_no', 'type': 'str',
            'val': request.form.get('birth_cert_no')},
        {'fn': 'place_birth', 'type': 'b64str',
            'val': request.form.get('place_birth')},
        {'fn': 'address', 'type': 'b64str',
            'val': request.form.get('address')},
        {'fn': 'date_in', 'type': 'str', 'val': request.form.get('date_in')},
        {'fn': 'tel', 'type': 'str', 'val': request.form.get('tel')},
        {'fn': 'email', 'type': 'b64str', 'val': request.form.get('email')},
        {'fn': 'caregiver', 'type': 'int',
            'val': request.form.get('caregiver')},
        {'fn': 'lang', 'type': 'b64str', 'val': request.form.get('lang')},
        {'fn': 'group_id', 'type': 'int', 'val': request.form.get('group_id')}
    ]
    # check parameters
    # gender
    gi = get_index(flist, 'gender')
    if type(flist[gi]['val']) == type(''):
        if flist[gi]['val'].lower() == 'female':
            flist[gi]['val'] = 'f'
        elif flist[gi]['val'].lower() == 'male':
            flist[gi]['val'] = 'm'
        elif flist[gi]['val'].lower() == 'boy':
            flist[gi]['val'] = 'm'
        elif flist[gi]['val'].lower() == 'girl':
            flist[gi]['val'] = 'f'
        elif flist[gi]['val'].lower() == 'man':
            flist[gi]['val'] = 'm'
    # alias
    if alias is None:
        return ee.PARAMERR(app=': alias is needed')
    _cidfa = get_cid_by_alias(alias)
    if _cidfa['code']!=0:
        return _cidfa
    if len(_cidfa['data'])>0:
        return ee.UN_EXISTS(app=': alias already exists')
    # born_day
    bdi = get_index(flist, 'born_day')
    if type(flist[bdi]['val']) == type(''):
        try:
            # check
            bd = datetime.datetime.strptime(flist[bdi]['val'], '%Y-%m-%d').date()
            # get group id
            today = datetime.date.today()
            tdd = (today - bd).days
            tdm = tdd//30
            if tdd % 30 != 0:
                tdm += 1
            for g in gv.groups:
                if tdm >= g['smon'] and tdm <= g['emon']:
                    flist[-1]['val'] = g['id']
        except:
            return ee.PARAMERR(app=': born_day')
    # date_in
    di = get_index(flist, 'date_in')
    if flist[di]['val'] is None or flist[di]['val'] == '':
        flist[di]['val'] = time.strftime(
            '%Y-%m-%d', time.localtime(time.time()))
    else:
        try:
            time.strptime(flist[di]['val'], '%Y-%m-%d')
        except:
            return ee.PARAMERR(app='date_in')
    # parent
    cid = None
    if flist[-3]['val'] is not None:
        _pun = flist[-3]['val']
        pid = get_id_by_username(_pun)
        if pid['code'] != 0:
            return pid
        if pid['count'] == 0 or len(pid['data']) == 0:
            return ee.IDERR(msg='username of caregiver not exists')
        cid = int(pid['data'][0]['id'])
    flist[-3]['val'] = cid
    try:
        conn = gv.dbpool.connection()
        cur = conn.cursor()
        cur.execute("SET NAMES UTF8mb4;")
        res = funcs.insert_if_not_exists(
            cur, tbn, flist, chkfn=None, logger=gv.logger)
        if res['code'] != 0:
            cur.close()
            conn.close()
            return res
        # add to parent
        if cid is not None:
            s1 = 'select child_ids from parent where id={0};'.format(
                str(cid))
            cur.execute(s1.encode("utf-8", "ignore"))
            cidsres = cur.fetchall()
            cids = []
            if cidsres is not None and len(cidsres) > 0:
                if cidsres[0][0] is not None and len(cidsres[0][0]) > 0:
                    _tmp = cidsres[0][0].split(',')
                    for _t in _tmp:
                        if len(_t) > 0:
                            cids.append(str(_t))
            cids.append(str(uid))
            newcids = ','.join(cids)
            s2 = "update parent set child_ids='{0}' where id={1};".format(
                newcids, str(cid))
            cur.execute(s2.encode("utf-8", "ignore"))
        conn.commit()
        cur.close()
        conn.close()
        return ee.NORMAL()
    except:
        estr = traceback.format_exc()
        gv.logger.error('database error!\n'+estr)
        return ee.DBERR()
    return ee.UNKNOWN()


def update_child():
    """
    update child info in database
    """
    uid = request.form.get('id')
    alias = request.form.get('alias')
    if uid is None and alias is None:
        return ee.PARAMERR(app=": id or alias is needed")
    if type(uid) == type('') and not str.isdigit(uid):
        return ee.PARAMERR(app=': id')
    uidfa = None
    if alias is not None:
        uidfa = get_cid_by_alias(alias)
    if uid is not None and alias is not None:
        # 检查唯一性
        if uidfa['code']!=0:
            return uidfa
        if len(uidfa['data'])>0 and \
            str(uidfa['data'][0]['id'])!=str(uid):
            return ee.UN_EXISTS(app=': alias already exists')
    if uid is None:
        if uidfa['code']!=0:
            return uidfa
        if len(uidfa['data'])==0:
            return ee.IDERR(app=': alias not exists')
        uid = uidfa['data'][0]['id']
    tbn = 'child'
    flist = [
        {'fn': 'name', 'type': 'b64str', 'val': request.form.get('name')},
        {'fn': 'name_chs', 'type': 'b64str',
            'val': request.form.get('name_chs')},
        {'fn': 'alias', 'type': 'b64str', 'val': alias},
        {'fn': 'gender', 'type': 'str', 'val': request.form.get('gender')},
        {'fn': 'religion', 'type': 'b64str',
            'val': request.form.get('religion')},
        {'fn': 'born_day', 'type': 'str', 'val': request.form.get('born_day')},
        {'fn': 'birth_cert_no', 'type': 'str',
            'val': request.form.get('birth_cert_no')},
        {'fn': 'place_birth', 'type': 'b64str',
            'val': request.form.get('place_birth')},
        {'fn': 'address', 'type': 'b64str',
            'val': request.form.get('address')},
        {'fn': 'date_in', 'type': 'str', 'val': request.form.get('date_in')},
        {'fn': 'tel', 'type': 'str', 'val': request.form.get('tel')},
        {'fn': 'email', 'type': 'b64str', 'val': request.form.get('email')},
        {'fn': 'caregiver', 'type': 'int',
            'val': request.form.get('caregiver')},
        {'fn': 'lang', 'type': 'b64str', 'val': request.form.get('lang')},
        {'fn': 'group_id', 'type': 'int', 'val': request.form.get('group_id')}
    ]
    # check parameters
    # gender
    gi = get_index(flist, 'gender')
    if type(flist[gi]['val']) == type(''):
        if flist[gi]['val'].lower() == 'female':
            flist[gi]['val'] = 'f'
        elif flist[gi]['val'].lower() == 'male':
            flist[gi]['val'] = 'm'
        elif flist[gi]['val'].lower() == 'boy':
            flist[gi]['val'] = 'm'
        elif flist[gi]['val'].lower() == 'girl':
            flist[gi]['val'] = 'f'
        elif flist[gi]['val'].lower() == 'man':
            flist[gi]['val'] = 'm'
    # born_day
    bdi = get_index(flist, 'born_day')
    if type(flist[bdi]['val']) == type(''):
        try:
            # check
            bd = datetime.datetime.strptime(flist[bdi]['val'], '%Y-%m-%d').date()
            # get group id
            today = datetime.date.today()
            tdd = (today - bd).days
            tdm = tdd//30
            if tdd % 30 != 0:
                tdm += 1
            for g in gv.groups:
                if tdm >= g['smon'] and tdm <= g['emon']:
                    flist[-1]['val'] = g['id']
        except:
            return ee.PARAMERR(app='born_day')
    # date_in
    di = get_index(flist, 'date_in')
    if flist[di]['val'] is None or flist[di]['val'] == '':
        flist[di]['val'] = time.strftime(
            '%Y-%m-%d', time.localtime(time.time()))
    else:
        try:
            time.strptime(flist[di]['val'], '%Y-%m-%d')
        except:
            return ee.PARAMERR(app='date_in')
    # parent
    cid = None
    if flist[-3]['val'] is not None:
        _pun = flist[-3]['val']
        pid = get_id_by_username(_pun)
        if pid['code'] != 0:
            return pid
        if pid['count'] == 0 or len(pid['data']) == 0:
            return ee.IDERR(msg='username of caregiver not exists')
        cid = int(pid['data'][0]['id'])
    flist[-3]['val'] = cid
    try:
        conn = gv.dbpool.connection()
        cur = conn.cursor()
        cur.execute("SET NAMES UTF8mb4;")
        # get origin cid
        cidorg = None
        if cid is not None:
            sqlstr = 'select caregiver from child where id={0};'.format(
                str(uid))
            cur.execute(sqlstr.encode("utf-8", "ignore"))
            cidorg = cur.fetchall()
            if cidorg is None or len(cidorg) == 0:
                cur.close()
                conn.close()
                return ee.IDERR(msg='child id is incorrect')
            cidorg = cidorg[0][0]
        vstr = funcs.build_set_str(flist)
        if vstr is None:
            cur.close()
            conn.close()
            return ee.PARAMERR()
        sqlstr = 'update `{tbn}` set {sstr} where id={cid};'.format(
            tbn=tbn, sstr=vstr, cid=uid)
        cur.execute(sqlstr.encode("utf-8", "ignore"))
        # add to parent
        if cid is not None and str(cidorg) != str(cid):
            # 抹除旧的
            s1 = 'select child_ids from parent where id={0};'.format(
                str(cidorg))
            cur.execute(s1.encode("utf-8", "ignore"))
            cidsres = cur.fetchall()
            if cidsres is not None and len(cidsres) > 0:
                if cidsres[0][0] is not None and len(cidsres[0][0]) > 0:
                    newcids = cidsres[0][0].replace(
                        str(uid), '').replace(',,', ',')
                    s2 = "update parent set child_ids='{0}' where id={1};".format(
                        newcids, str(cidorg))
                    cur.execute(s2.encode("utf-8", "ignore"))
            # 设置新的
            s1 = 'select child_ids from parent where id={0};'.format(
                str(cid))
            cur.execute(s1.encode("utf-8", "ignore"))
            cidsres = cur.fetchall()
            cids = []
            if cidsres is not None and len(cidsres) > 0:
                if cidsres[0][0] is not None and len(cidsres[0][0]) > 0:
                    _tmp = cidsres[0][0].split(',')
                    for _t in _tmp:
                        if len(_t) > 0:
                            cids.append(str(_t))
            cids.append(str(uid))
            newcids = ','.join(cids)
            s2 = "update parent set child_ids='{0}' where id={1};".format(
                newcids, str(cid))
            cur.execute(s2.encode("utf-8", "ignore"))
        conn.commit()
        cur.close()
        conn.close()
        return ee.NORMAL()
    except:
        estr = traceback.format_exc()
        gv.logger.error('database error!\n'+estr)
        return ee.DBERR()
    return ee.UNKNOWN()


def _chk_param_n_gsbc():
    '''
    check param and do get_status_by_cid
    '''
    # get and check params
    startt = request.args.get('startt')
    endt = request.args.get('endt')
    cid = request.args.get('id')
    alias = request.args.get('alias')
    if cid is None and alias is None:
        return ee.PARAMERR(app=': id or alias is needed')
    if type(cid)==type('') and not str.isdigit(cid):
        return ee.PARAMERR(app=': id')
    if cid is None:
        uidfa = get_cid_by_alias(alias)
        if uidfa['code']!=0:
            return uidfa
        if len(uidfa['data'])==0:
            return ee.IDERR(app=': alias not exists')
        cid = uidfa['data'][0]['id']
    _sk = request.args.get('secret_key')
    if _sk is None or _sk not in gv.logged:
        return ee.NOT_LOGGED()
    return get_status_by_cid(cid, startt, endt, _sk)


def get_status_by_cid(cid, startt, endt, sk):
    """
    获取指定child id 对应的status信息
    :param cid: child id
    :param startt:  start time
    :param endt:    end time
    :param sk:      secret key
    """
    if type(startt) == type(''):
        try:
            # check
            datetime.datetime.strptime(startt, '%Y-%m-%d')
        except:
            return ee.PARAMERR(app=': startt')
    elif startt is not None:
        return ee.PARAMERR(app=': startt')
    if type(endt) == type(''):
        try:
            # check
            datetime.datetime.strptime(endt, '%Y-%m-%d')
        except:
            return ee.PARAMERR(app=': endt')
    elif endt is not None:
        return ee.PARAMERR(app=': endt')
    wstr = 'where child_id={0}'.format(str(cid))
    if startt is not None:
        wstr = wstr + " and `time`>='{0}'".format(startt)
    if endt is not None:
        wstr = wstr + " and `time`<='{0} 23:59:59.999'".format(endt)
    try:
        conn = gv.dbpool.connection()
        cur = conn.cursor()
        cur.execute("SET NAMES UTF8mb4;")
        # 判断，如果是家长，只可以看自己的孩子
        role = gv.logged[sk]['role']
        allow = True
        if role == 'parent':
            pid = gv.logged[sk]['id']
            allow = False
            s1 = 'select child_ids from parent where id={0};'.format(
                str(pid))
            cur.execute(s1.encode("utf-8", "ignore"))
            cidsres = cur.fetchall()
            if cidsres is not None and len(cidsres) > 0:
                if cidsres[0][0] is not None and len(cidsres[0][0]) > 0:
                    _tmp = cidsres[0][0].split(',')
                    if str(cid) in _tmp:
                        allow = True
        if not allow:
            cur.close()
            conn.close()
            return ee.NOAUTHORITY(msg='Parents can only view the '
                                  'information of their own children')
        res = ee.NORMAL()
        _sttb = deepcopy(sttb)
        for tbn,fl in _sttb.items():
            cidi = get_index(fl['flist'],'child_id')
            if cidi is not None:
                fl['flist'][cidi]['type']='str'
            datas = funcs.get_datas(cur, tbn, fl['flist'], wstr=wstr, logger=gv.logger)
            for line in datas['data']:
                if tbn!='temperature':
                    line['status'] = gv.enum_selector[tptbn[tbn]][int(line['status'])]
                line['type'] = tbn
            res['data'] = res['data'] + datas['data']
        # 按时间排序
        res['data'] = sorted(res['data'], key=lambda x:x['time'], reverse=True)
        res['count'] = len(res['data'])
        cur.close()
        conn.close()
        return res
    except:
        estr = traceback.format_exc()
        gv.logger.error('database error!\n'+estr)
        return ee.DBERR()
    return ee.UNKNOWN()


def get_status(tp, page=0, limit=0, cid=None):
    '''
    从数据库分页获得status信息
    :param tp:      status type, 指定需要哪种状态信息
    :param page:    页码,0 based
    :param limit:   每页数量，设为0时，不限，直接返回所有数据
    :param cid:      child id，不设置时，返回所有孩子的
    :return :       unity formated json
    '''
    startt = request.args.get('startt')
    endt = request.args.get('endt')
    if type(startt) == type(''):
        try:
            # check
            datetime.datetime.strptime(startt, '%Y-%m-%d')
        except:
            return ee.PARAMERR(app=': startt')
    elif startt is not None:
        return ee.PARAMERR(app=': startt')
    if type(endt) == type(''):
        try:
            # check
            datetime.datetime.strptime(endt, '%Y-%m-%d')
        except:
            return ee.PARAMERR(app=': endt')
    elif endt is not None:
        return ee.PARAMERR(app=': endt')
    
    tdef = deepcopy(sttb[tp])
    cidi = get_index(tdef['flist'],'child_id')
    if cidi is not None:
        tdef['flist'][cidi]['type']='str'
    wstr = ''
    if cid is not None:
        wstr += ' child_id={0}'.format(str(cid))
    if startt is not None:
        if cid is not None:
            wstr = wstr + ' and'
        wstr = wstr + " `time`>='{0}'".format(startt)
    if endt is not None:
        if startt is not None:
            wstr = wstr + ' and'
        wstr = wstr + " `time`<='{0} 23:59:59.999'".format(endt)
    if wstr!='':
        wstr = 'where' + wstr
    try:
        conn = gv.dbpool.connection()
        cur = conn.cursor()
        cur.execute("SET NAMES UTF8mb4;")
        datas = funcs.get_datas(cur, tdef['tbn'], tdef['flist'], page=page,
                              limit=limit, wstr=wstr, logger=gv.logger)
        if tp!='temperature':
            for line in datas['data']:
                line['status'] = gv.enum_selector[tptbn[tp]][int(line['status'])]
        cur.close()
        conn.close()
        return datas
    except:
        estr = traceback.format_exc()
        gv.logger.error('database error!\n'+estr)
        return ee.DBERR()
    return ee.UNKNOWN()


def get_children_infos(page=0, limit=0, simple=False):
    """
    从数据库分页获取孩子信息
    :param page:    页码,0 based
    :param limit:   每页数量，设为0时，不限，直接返回所有数据
    :param simple:  simple模式
    :return :       unity formated json
    """
    tbn = 'child'
    flist = [
        {'fn': 'id', 'type': 'str'},
        {'fn': 'name', 'type': 'b64str'},
        {'fn': 'name_chs', 'type': 'b64str'},
        {'fn': 'alias', 'type': 'b64str'},
        {'fn': 'gender', 'type': 'str'},
        {'fn': 'born_day', 'type': 'str'},
        {'fn': 'place_birth', 'type': 'b64str'},
        {'fn': 'date_in', 'type': 'str', 'sorted': 1},
        {'fn': 'tel', 'type': 'str'},
        {'fn': 'caregiver_id', 'type': 'str'},
        {'fn': 'caregiver_name', 'type': 'b64str'},
        {'fn': 'caregiver_name_chs', 'type': 'b64str'},
        {'fn': 'lang', 'type': 'b64str'},
        {'fn': 'group_id', 'type': 'int'}
    ]
    flist_p = [
        {'fn': 'id` as `caregiver_id', 'type': 'str'},
        {'fn': 'name` as `caregiver_name', 'type': 'b64str'},
        {'fn': 'name_chs` as `caregiver_name_chs', 'type': 'b64str'}
    ]
    if simple:
        flist = flist[:4]
    try:
        conn = gv.dbpool.connection()
        cur = conn.cursor()
        cur.execute("SET NAMES UTF8mb4;")
        wstr = ''
        if not simple:
            kstr_p = funcs.build_field_str(flist_p)
            wstr = 'left join (select {kstr} from parent) as t1'\
                ' on `child`.caregiver=caregiver_id'.format(kstr=kstr_p)
        res = funcs.get_datas(cur, tbn, flist, page=page,
                              limit=limit, wstr=wstr, logger=gv.logger)
        cur.close()
        conn.close()
        return res
    except:
        estr = traceback.format_exc()
        gv.logger.error('database error!\n'+estr)
        return ee.DBERR()
    return ee.UNKNOWN()


def get_children_info(cid, sk):
    """
    从数据库分页获取孩子信息
    :param cid:     child id
    :param sk:      secret key
    :return :       unity formated json
    """
    _id = cid
    pid = gv.logged[sk]['id']
    role = gv.logged[sk]['role']
    flist_c = [
        {'fn': 't1`.`id', 'type': 'str', 'as': 'id'},
        {'fn': 't1`.`name', 'type': 'b64str', 'as': 'name'},
        {'fn': 't1`.`name_chs', 'type': 'b64str', 'as': 'name_chs'},
        {'fn': 'alias', 'type': 'b64str'},
        {'fn': 'gender', 'type': 'str'},
        {'fn': 'religion', 'type': 'b64str'},
        {'fn': 'born_day', 'type': 'str'},
        {'fn': 'birth_cert_no', 'type': 'str'},
        {'fn': 'place_birth', 'type': 'b64str'},
        {'fn': 'address', 'type': 'b64str'},
        {'fn': 'date_in', 'type': 'str', 'sorted': 1},
        {'fn': 't1`.`tel', 'type': 'str', 'as': 'tel'},
        {'fn': 'email', 'type': 'b64str'},
        {'fn': 'caregiver', 'type': 'str', 'as': 'caregiver_id'},
        {'fn': 'parent`.`name', 'type': 'b64str', 'as': 'caregiver_name'},
        {'fn': 'parent`.`name_chs', 'type': 'b64str', 'as': 'caregiver_name_chs'},
        {'fn': 'lang', 'type': 'b64str'},
        {'fn': 'group_id', 'type': 'int'}
    ]
    try:
        conn = gv.dbpool.connection()
        cur = conn.cursor()
        cur.execute("SET NAMES UTF8mb4;")
        # 判断，如果是家长，只可以看自己的孩子
        allow = True
        if role == 'parent':
            allow = False
            s1 = 'select child_ids from parent where id={0};'.format(
                str(pid))
            cur.execute(s1.encode("utf-8", "ignore"))
            cidsres = cur.fetchall()
            if cidsres is not None and len(cidsres) > 0:
                if cidsres[0][0] is not None and len(cidsres[0][0]) > 0:
                    _tmp = cidsres[0][0].split(',')
                    if str(_id) in _tmp:
                        allow = True
        if not allow:
            cur.close()
            conn.close()
            return ee.NOAUTHORITY(msg='Parents can only view the '
                                  'information of their own children')
        wstr = 'right join (select * from child where id={cid}) as t1'\
            ' on `parent`.id=t1.caregiver'.format(cid=_id)
        res = funcs.get_datas(cur, 'parent', flist_c,
                              wstr=wstr, logger=gv.logger)
        res['count'] = len(res['data'])
        cur.close()
        conn.close()
        return res
    except:
        estr = traceback.format_exc()
        gv.logger.error('database error!\n'+estr)
        return ee.DBERR()
    return ee.UNKNOWN()

def get_child_status_by_pid(pid, sk):
    '''
    get child status today by parent id
    '''
    _cids = get_child_ids(pid)
    if _cids['code']==0 and len(_cids['data'])>0:
        if _cids['data'][0]['child_ids'] is None:
            return ee.NORMAL()
        _cids = _cids['data'][0]['child_ids'].split(',')
        startt = endt = time.strftime('%Y-%m-%d', time.localtime())
        datas = ee.NORMAL()
        for _cid in _cids:
            _cn = _get_simple_child_info_by_cid(_cid)
            if _cn['code']!=0:
                return _cn
            _cn = _cn['data'][0]
            _data = get_status_by_cid(_cid, startt, endt, sk)
            if _data['code']!=0:
                return _data
            datas['data'].append({
                'id':str(_cid), 
                'name':_cn['name'], 
                'name_chs':_cn['name_chs'],
                'alias':_cn['alias'],
                'data':_data})
        datas['count'] = len(datas['data'])
        return datas
    return _cids

def _get_simple_child_info_by_cid(cid):
    '''
    get simple child info by id,
    info:   name,name_chs,alias
    '''
    flist = [
        {'fn':'name','type':'b64str'},
        {'fn':'name_chs','type':'b64str'},
        {'fn':'alias','type':'b64str'}
        ]
    try:
        conn = gv.dbpool.connection()
        cur = conn.cursor()
        cur.execute("SET NAMES UTF8mb4;")
        wstr = 'where id={cid}'.format(cid=str(cid))
        res = funcs.get_datas(cur, 'child', flist, wstr=wstr, logger=gv.logger)
        cur.close()
        conn.close()
        return res
    except:
        estr = traceback.format_exc()
        gv.logger.error('database error!\n'+estr)
        return ee.DBERR()
    return ee.UNKNOWN()
    

def get_child_ids(pid):
    '''
    get child ids of parent 
    '''
    fl = [{'fn':'child_ids','type':'str'}]
    try:
        conn = gv.dbpool.connection()
        cur = conn.cursor()
        cur.execute("SET NAMES UTF8mb4;")
        wstr = 'where id={}'.format(str(pid))
        res = funcs.get_datas(cur, 'parent', fl, wstr=wstr, logger=gv.logger)
        cur.close()
        conn.close()
        return res
    except:
        estr = traceback.format_exc()
        gv.logger.error('database error!\n'+estr)
        return ee.DBERR()
    return ee.UNKNOWN()

# views------------------------------------------------

@api_children.route('/api/children/infos', methods=['GET'])
def children_infos_get():
    vres = verify_auto(request, allows=['admin', 'staff'])
    if not vres['code'] == 0:
        # verification failed
        vres['count'] = 0
        vres['data'] = []
        return vres
    page = request.args.get('page')
    limit = request.args.get('limit')
    if page is None or limit is None:
        page = 0
        limit = 0
    else:
        page = int(page)-1
        limit = int(limit)
    # is simple?
    simple = request.args.get('simple')
    if str(simple) == '1':
        simple = True
    else:
        simple = False
    res = get_children_infos(page, limit, simple)
    return res


@api_children.route('/api/children/info', methods=['POST'])
def children_info_post():
    vres = verify_auto(request, allows=['admin', 'staff'])
    if not vres['code'] == 0:
        # verification failed
        vres['count'] = 0
        vres['data'] = []
        return vres
    res = insert_child()
    return res


@api_children.route('/api/children/info', methods=['GET'])
def children_info_get():
    vres = verify_auto(request, allows=['admin', 'staff', 'parent'])
    if not vres['code'] == 0:
        # verification failed
        vres['count'] = 0
        vres['data'] = []
        return vres
    _id = request.args.get('id')
    alias = request.args.get('alias')
    if _id is None and alias is None:
        return ee.PARAMERR(app=": id or alias is needed")
    if type(_id) == type('') and not str.isdigit(_id):
        return ee.PARAMERR(app=': id')
    if _id is None:
        uidfa = get_cid_by_alias(alias)
        if uidfa['code']!=0:
            return uidfa
        if len(uidfa['data'])==0 or \
            uidfa['data'][0]['id'] is None:
            return ee.IDERR(app=': alias not exists')
        _id = uidfa['data'][0]['id']
    _sk = request.args.get('secret_key')
    if _sk is None:
        return ee.NOT_LOGGED()
    res = get_children_info(_id, _sk)
    return res


@api_children.route('/api/children/info', methods=['PUT'])
def children_info_put():
    vres = verify_auto(request, allows=['admin', 'staff'])
    if not vres['code'] == 0:
        # verification failed
        vres['count'] = 0
        vres['data'] = []
        return vres
    res = update_child()
    return res


@api_children.route('/api/children/statuses', methods=['GET'])
def children_statuses_get():
    vres = verify_auto(request, allows=['admin', 'staff'])
    if not vres['code'] == 0:
        # verification failed
        vres['count'] = 0
        vres['data'] = []
        return vres
    page = request.args.get('page')
    limit = request.args.get('limit')
    if page is None or limit is None:
        page = 0
        limit = 0
    else:
        page = int(page)-1
        limit = int(limit)
    tp = request.args.get('type')
    if type(tp) != type(''):
        return ee.PARAMERR(app=': type')
    tp = tp.lower()
    if tp == 'temp':
        tp = 'temperature'
    if tp not in sttb:
        return ee.PARAMERR(app=': type')
    res = get_status(tp, page, limit)
    return res

@api_children.route('/api/children/status', methods=['GET'])
def children_status_get():
    vres = verify_auto(request, allows=['admin', 'staff', 'parent'])
    if not vres['code'] == 0:
        # verification failed
        vres['count'] = 0
        vres['data'] = []
        return vres
    res = _chk_param_n_gsbc()
    return res


