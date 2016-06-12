#!/usr/bin/python

import sys
import os
import re
import logging as log
from testUnit import tester 

class ntp():

    __Excute = None

    def __init__(self):
        self.__Excute=os.system
        return

    def install(self,ips,monitor=None):
	self.__Excute("yum install -y ntp")
        for ip in ips:
            self.__Excute("ssh "+ip+" yum install -y ntp")
	for ip in ips:
	    self.__Excute("ssh "+ip+" systemctl stop ntpd.service")
        return

    def config(self):
        self.__Excute("cp -f ./config/ntp/ntp.conf /etc/")
        return

    def run(self):
        self.__Excute("systemctl restart ntpd.service")
        return

    def client(self,ips):
        local_ip=[]
        reader = os.popen("ip addr | grep inet")
        data = reader.readlines()
        reader.close()
        for d in data:
            temp = re.search("inet (\d+\.\d+\.\d+\.\d+)/.*$",d)
            if temp and temp.group(1) != "127.0.0.1":
                local_ip.append(temp.group(1))
        for ip in ips:
            self.__Excute("ssh "+ip+" 'echo \"0 */1 * * * root ntpdate "+local_ip[0]+"\">> /etc/crontab'")
        return
    
if __name__ == "__main__":
    test = tester()
    if not test.test():
        raise Exception("less arguments or illegal arguments.")
    ips = test.get_ips()
    ntper = ntp()
    ntper.install(ips,"172.22.29.179")
    ntper.config()
    ntper.run()
    ntper.client(ips,"172.22.29.179")
