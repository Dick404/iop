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

def main(ips,dev,monitor="127.0.0.1"):
    ha_operator = ha()
    ns_operator = ns()
    nc_operator = nc()
    mycat = Mycat()
    ntper = ntp()
    key = keystone()
    ha_operator.haproxy_install()
    ha_operator.haproxy_config(ips)
    ha_operator.run()
    ns_operator.install()
    ns_operator.init(ips,dev)
    ns_operator.run()
    nc_operator.install(ips)
    nc_operator.init(ips)
    nc_operator.config(ips)
    nc_operator.run()
    ntper.install(ips)
    ntper.config()
    ntper.run()
    ntper.client(ips)
    key.main(monitor)
    return

if __name__ == "__main__":
    main(ips,dev)
