#!/usr/bin/python
#coding:utf-8

import pytest
import unittest
import os
from os import path
from idb.utils import RandomString
from shutil import rmtree
from idb.helpers import WriteFileValue, ReadFileValue, GetDBValue, IDB_VALUE_NAME

ROOT_DIR = './mytestdb'
FIXTURE_DIR = path.join(path.realpath(__file__), 'fixtures')

def RandomKeyValue(aKeySize = 8, aValueSize = 26):
    key = RandomString(aKeySize)
    value = RandomString(aValueSize)
    return {'key': key, 'value': value}

def RandomPairs(aSize = 99):
    return [RandomKeyValue() for x in range(aSize)]

def create_pairs(aSize = 99, aCached = True):
    pairs = RandomPairs(aSize)
    for item in pairs:
        vDir = path.join(ROOT_DIR, item['key'])
        vStr = item['value']
        WriteFileValue(vDir, vStr, IDB_VALUE_NAME, aCached)
    return pairs

def check_pairs(pairs, wanted_result = True):
    for item in pairs:
        vDir =  path.join(ROOT_DIR, item['key'])
        vWantedStr = item['value']
        vStr = ReadFileValue(vDir)
        assert len(vStr) == 1
        vStr = vStr[0]
        if wanted_result:
            assert vStr == vWantedStr
        else:
            assert vStr != vWantedStr
        vStr = ReadFileValue(vDir + RandomString(6))
        assert vStr == None

class BaseTest(unittest.TestCase):
    def setUp(self):
        rmtree(ROOT_DIR,  True)
    def tearDown(self):
        rmtree(ROOT_DIR, True)

