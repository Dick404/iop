#!/usr/bin/python 

import sys
import os
import re
import logging as log
from  haproxy  import haproxy as ha
from nfs import nfs_server as ns
from nfs import nfs_client as nc
from Mycat import Mycat
from ntp import ntp
from keystones import keystone
from report import recorder

def main(ips,dev,monitor="127.0.0.1"):
    E = recorder()
    if E.test("haproxy"):
        ha_operator = ha()
        ns_operator = ns()
        nc_operator = nc()
    if 
    mycat = Mycat()
    ntper = ntp()
    key = keystone()
    if E.test("haproxy"):
        ha_operator.haproxy_install()
        ha_operator.haproxy_config(ips)
        ha_operator.run()
        E.record("haproxy")
    if E.test("nfs_server"):
        ns_operator.install()
        ns_operator.init(ips,dev)
        ns_operator.run()
        E.reader("nfs_server")
    if E.test("nfs_client"):
        nc_operator.install(ips)
        nc_operator.init(ips)
        nc_operator.config(ips)
        nc_operator.run()
        E.record("nfs_client")
    if E.test("ntp"):
        ntper.install(ips)
        ntper.config()
        ntper.run()
        ntper.client(ips)
        E.record("ntp")
    if E.test("keystone"):
        key.main(monitor)
        E.record("keystone")
    return

if __name__ == "__main__":
    main(ips,dev)
