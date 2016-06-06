#!/usr/bin/python

import os
import sys
import re

class haproxy():

    __Excute = None

    def __init__(self):
        self.__Excute = os.system

    def haproxy_install(self):
        self.__Excute("rpm -ivh ../resource/cache/haproxy/haproxy-1.5.4-4.el7_1.x86_64.rpm")     # this block should use popen but don't have time
        return

    def haproxy_config(self,ips):
        reader = open("../config/haproxy/haproxy.cfg"."r")
        configs = reader.readlines()
        reader.close()
        writer = open("/etc/haproxy/haproxy.cfg","w")
        for config in configs:
            if re.match(r"    server  app1 10.110.19.240:8080 check  inter 2000 fall 3 weight 30.*$",conifg):
                for i in range(len(ips)):
                    writer.write("    server  app"+str(i)+" "+ips[i]+":8080 check  inter 2000 fall 3 weight 30\n")
            elif re.match(r"    server mq1 10.110.19.240:5672 check inter 2000 fall 3.*$",config):
                for i in range(len(ips)):
                    writer.write("    server mq"+str(i)+" "+ips[i]+":5672 check inter 2000 fall 3\n")
            elif re.match(r"    server aaaa 10.110.19.241:81  check",config):
                for i in range(len(ips)):
                    writer.write("    server swift"+str(i)+" "+ips[i]+"  check inter 2000 fall 3 weight 30\n")
            else:
                writer.write(config+"\n")
                pass
            pass
        return

    def run(self):
        self.__Excute("haproxy -f /etc/haproxy/haproxy.cfg")              # change the code with os.popen
        if os.path.exists("/run/haproxy.pid"):
            return True
        else:
            return False
