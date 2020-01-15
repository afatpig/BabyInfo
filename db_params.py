#!/usr/bin/env python3
# -*- coding:utf-8 -*-
"""
定义数据库结构模板
"""
temperature = {
    'tbn' : 'temperature',
    'flist': [
        {'fn':'id', 'type':'int', 'as':'id'},
        {'fn':'child_id', 'type':'int', 'as':'child_id'},
        {'fn':'time', 'type':'str', 'as':'time'},
        {'fn':'temperature', 'type':'float', 'as':'status'},
        {'fn':'staff_id', 'type':'int', 'as':'staff_id'}
    ]
}

skin = {
    'tbn' : 'skin',
    'flist': [
        {'fn':'id', 'type':'int', 'as':'id'},
        {'fn':'child_id', 'type':'int', 'as':'child_id'},
        {'fn':'time', 'type':'str', 'as':'time'},
        {'fn':'condition_id', 'type':'int', 'as':'status'},
        {'fn':'staff_id', 'type':'int', 'as':'staff_id'},
        {'fn':'count', 'type':'int', 'as':'count'},
        {'fn':'remark', 'type':'b64str', 'as':'remark'}
    ]
}

meal = {
    'tbn' : 'meal',
    'flist': [
        {'fn':'id', 'type':'int', 'as':'id'},
        {'fn':'child_id', 'type':'int', 'as':'child_id'},
        {'fn':'time', 'type':'str', 'as':'time'},
        {'fn':'mealtype', 'type':'int', 'as':'status'},
        {'fn':'staff_id', 'type':'int', 'as':'staff_id'},
        {'fn':'qty', 'type':'int', 'as':'count'},
        {'fn':'remark', 'type':'b64str', 'as':'remark'}
    ]
}

nap = {
    'tbn' : 'nap',
    'flist': [
        {'fn':'id', 'type':'int', 'as':'id'},
        {'fn':'child_id', 'type':'int', 'as':'child_id'},
        {'fn':'time', 'type':'str', 'as':'time'},
        {'fn':'napquality', 'type':'int', 'as':'status'},
        {'fn':'staff_id', 'type':'int', 'as':'staff_id'},
        {'fn':'remark', 'type':'b64str', 'as':'remark'}
    ]
}

diaper = {
    'tbn' : 'diaper',
    'flist': [
        {'fn':'id', 'type':'int', 'as':'id'},
        {'fn':'child_id', 'type':'int', 'as':'child_id'},
        {'fn':'time', 'type':'str', 'as':'time'},
        {'fn':'diaper_id', 'type':'int', 'as':'status'},
        {'fn':'staff_id', 'type':'int', 'as':'staff_id'},
        {'fn':'count', 'type':'int', 'as':'count'},
        {'fn':'remark', 'type':'b64str', 'as':'remark'}
    ]
}


health = {
    'tbn' : 'health',
    'flist': [
        {'fn':'id', 'type':'int', 'as':'id'},
        {'fn':'child_id', 'type':'int', 'as':'child_id'},
        {'fn':'time', 'type':'str', 'as':'time'},
        {'fn':'health_status_id', 'type':'int', 'as':'status'},
        {'fn':'staff_id', 'type':'int', 'as':'staff_id'},
        {'fn':'remark', 'type':'b64str', 'as':'remark'}
    ]
}

perform = {
    'tbn' : 'perform',
    'flist': [
        {'fn':'id', 'type':'int', 'as':'id'},
        {'fn':'child_id', 'type':'int', 'as':'child_id'},
        {'fn':'time', 'type':'str', 'as':'time'},
        {'fn':'perform_id', 'type':'int', 'as':'status'},
        {'fn':'staff_id', 'type':'int', 'as':'staff_id'},
        {'fn':'remark', 'type':'b64str', 'as':'remark'}
    ]
}

status_tables = {
    'temperature': temperature,
    'skin': skin,
    'meal': meal,
    'nap':nap,
    'diaper':diaper,
    'health':health,
    'perform':perform
}

status_type_tbn = {
    'skin':"condition",
    'diaper':"diaper_status",
    'health':"health_status",
    "meal":"meal_type",
    'nap':"nap_status",
    "perform":"perform_detail"
}

def get_index(flist, fn):
    '''
    get index of fn in flist
    '''
    for i, v in enumerate(flist):
        if v['fn'] == fn:
            return i