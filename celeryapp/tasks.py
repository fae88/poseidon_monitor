# -*- coding: utf-8 -*-
from __future__ import absolute_import

import time
from . import common
from celery import shared_task



@shared_task
def test_task():
    time.sleep(20)
    return 'Completed'

@shared_task
def create_lazada_tasks():

    # 测试 lazada
    common.poseidon_task('fufan@51dojo.com', 'moxie121314', 'lazada', 'PWD', None)


@shared_task
def create_jdid_tasks():
    
    # 测试 jdid
    common.poseidon_task('dongyajun@51dojo.com', 'moxie@121314', 'jdid', 'PWD', None)

@shared_task
def create_gojek_tasks():

    # 测试 gojek
    common.poseidon_task('dongyajun@51dojo.com', 'moxie@121314', 'gojek', 'SMS')


@shared_task
def create_telkomsel_tasks():

    # 测试 telkomsel
    common.poseidon_task('sherrysheldn@gmail.com', 'mx121314', 'telkomsel', 'PWD', None)

@shared_task
def create_mycelcom_tasks():

    # 测试 mycelcom
    common.poseidon_task('jasonzhouxf', 'qaz123987', 'mycelcom', 'PWD', None)

@shared_task
def create_digi_tasks():
    
    # 测试 digi
    common.poseidon_task('+600143182173', 'qaz123987', 'digi', 'PWD', None)

@shared_task
def create_maxis_tasks():

    # 测试 maxis
    common.poseidon_task('jason_zhouxf@163.com', 'Hello1234', 'maxis', 'PWD', None)

@shared_task
def create_instagram_tasks():

    # 测试 instagram
    common.poseidon_task('lirenhao95', 'a411867400', 'instagram', 'PWD', None)

@shared_task
def create_facebook_tasks():

    # 测试 facebook
    common.poseidon_task('', '', 'facebook', 'PWD', None)

@shared_task
def create_googleplay_tasks():
    
    # 测试 googleplay
    common.poseidon_task('lirenhao95@gmail.com', 'a411867400', 'googleplay', 'PWD', None)

@shared_task
def create_tokopedia_tasks():

    # 测试 tokopedia
    common.poseidon_task('fufan@51dojo.com', 'moxie121314', 'tokopedia', 'PWD', None)


@shared_task
def create_bukalapak_tasks():

    # 测试 bukalapak
    common.poseidon_task('ptgofreepassionfintech@gmail.com', 'PP0813', 'bukalapak', 'PWD', None)
