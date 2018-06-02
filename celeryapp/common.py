# -*- coding: utf-8 -*-
import base64
import json
import os

import chardet
import requests
import time
import subprocess

import sys

task_headers = {
    'Content-Type' : 'application/json',
    'Accept' : 'application/json',
    'Authorization' : 'apikey 6149056c09e1498ca9b1bcd534b5ad0c'
}

bill_headers = {
    'Accept' : 'application/json',
    'Authorization' : 'token cb2f48f3c2a74488ad3abb52cfc4c8b6'
}

image_path = os.path.join(os.getcwd(), 'image.jpg')

poseidon_domain = 'https://api.91mxdata.com/gateway'
# poseidon_domain = 'http://localhost:9999/gateway'

def task_param(account, pwd, taskType, loginType=None, country=None):
    data = {
        'account': account,
        'name': 'moxie_test',
        'id_card': '421083199307281216',
        'login_type': 'PWD' if loginType == None else loginType,
        'origin': '0',
        'password': pwd,
        'user_id': 'moxie_client_demo_test',
        'lang': 'CN',
        'country': 'indonesia' if country == None else country,
        'task_type': taskType
    }
    return json.dumps(data)

def task_input_param(value):
    data = {
        'input': '' if value == None else value
    }
    return json.dumps(data)

def create_task(account, pwd, taskType, loginType, country):
    r = requests.post(poseidon_domain + '/v1/tasks', data=task_param(account, pwd, taskType, loginType, country),\
                      headers=task_headers)
    content = r.content
    encode_type = chardet.detect(content)  # 解决返回体编码的问题
    content = content.decode(encode_type['encoding'])
    print("task_type: %s, account: %s, create task, response: code = %s, content = %s" % \
          (taskType, account, r.status_code, content))
    return json.loads(content)

def task_status(taskId):
    r = requests.get(poseidon_domain + '/v1/tasks/{}/status'.format(taskId), headers=task_headers)
    content = r.content
    encode_type = chardet.detect(content)  # 解决返回体编码的问题
    content = content.decode(encode_type['encoding'])
    print("loop task status, task_id: %s, response: code = %s, content = %s" % \
          (taskId, r.status_code, content))
    return json.loads(content)

def task_input(taskId, value):
    r = requests.post(poseidon_domain + '/v1/tasks/{}/input'.format(taskId), headers=task_headers, \
                      data=task_input_param(value))
    content = r.content
    encode_type = chardet.detect(content)  # 解决返回体编码的问题
    content = content.decode(encode_type['encoding'])
    print("task input code, task_id: %s, response: code = %s, content = %s" % \
          (taskId, r.status_code, content))

def query_data(taskId, taskType):
    r = requests.get(poseidon_domain + '/{}/v1/{}/data'.format(taskType, taskId), headers=bill_headers)
    content = r.content
    encode_type = chardet.detect(content)  # 解决返回体编码的问题
    content = content.decode(encode_type['encoding'])
    print("query data, response: code = %s, content = %s" % (r.status_code, content))
    return json.loads(content)

def show_image(content):
    f = open(image_path, 'wb')
    f.write(base64.b64decode(content))
    f.close()
    time.sleep(1)

    if sys.platform.find('darwin') >= 0:
        subprocess.call(['open', image_path])
    elif sys.platform.find('linux') >= 0:
        subprocess.call(['xdg-open', image_path])
    else:
        os.startfile(image_path)


def poseidon_task(account, pwd, taskType, loginType, country):
    # step-1 create task
    task_response = create_task(account, pwd, taskType, loginType, country)
    task_id = task_response['task_id']
    print('task_id : {}'.format(task_id))


    # step-2 poll for task status, maximum time is 5 minute
    poll_end_time = int(time.time() + 5 * 60)
    is_task_done = False
    while True:
        status = task_status(task_id)
        desc = status['description']
        phase = status['phase']
        phase_status = status['phase_status']
        print("phase:%s - phase_status:%s - description:%s" % (phase, phase_status, desc))

        if phase_status == "DOING":
            print("task is processing")

        elif phase_status == "DONE_SUCC" and phase == 'DONE':
            print("task done")
            is_task_done = True
            break

        elif phase_status == "DONE_FAIL" or phase_status == "DONE_TIMEOUT":
            print("task fail")
            return

        elif phase_status == "WAIT_CODE":
            type = status['input']['type']
            value = ''
            if type == 'sms':
                value = input('please input sms code:')
            elif type == 'img':
                base64Img = status['input']['value']
                show_image(base64Img)
                # python2需要区分raw_input和input的区；python3没有区别
                value = input('please input img code:')
            task_input(task_id, value)
            os.remove(image_path)


        # 轮询时间间隔2s
        time.sleep(2)

        if int(time.time()) > poll_end_time:
            print("task timeout")
            break

    # step-3 query data
    if is_task_done:
        print("awesome! now make calls the data api")
        return query_data(task_id, taskType)
