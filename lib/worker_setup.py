#!/usr/bin.python
# code : UTF-8

import os
import sys
import re
import logging as log
from Mysql import mysql_installer as mysql
from rabbitMq import rabbitmq_installer as rabbit
from iop_web import iopWeb as iop
from swifts import swift
from testUnit import tester
from report import recorder
from testUnit import tester 

def main(ips,proxy):
    E = recorder()
    M = mysql()
    R = rabbit()
    I = iop()
    S = swift()
    if E.test("mysql-install"):
        M.install_mysql(ips)
        E.record("mysql-install")
    if E.test("mysql-config"):
        M.operator(ips)
        E.record("mysql-config")
    if E.test("rabbitmq"):
        R.operator(ips)
        E.record("rabbitmq")
    if E.test("iop-web"):
        I.config(ips,proxy)
        E.record("iop-web")
    if E.test("swift-install"):
	S.install(ips)
        E.record("swift-install")
    if E.test("swift-config"):
        S.config(ips,proxy)
        E.record("swift-config")
    return

if __name__ == "__main__":
    T = tester()
    if not T.test():
        raise Exception("less arguments or illegal arguments.")
    ips = T.get_ips()
    main(ips,"10.110.17.136")
