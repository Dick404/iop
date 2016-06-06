#!/usr/bin/python

import sys
import os
import time
import re


class tester():

    __Excute = os.system
    __Argument=sys.argv
    __ips = []

    def __init__(self):
        print len(self.__Argument)
        for i in range(1,len(self.__Argument)):
            self.__ips.append(self.__Argument[i])

    def test(self):
        for ip in self.__ips:
            if not re.match(r"\d+\.\d+\.\d+\.\d+",ip):
                print ip,"yes"
                return False
        return True if len(self.__ips)>0 else False

    def get_ips(self):
        return self.__ips
