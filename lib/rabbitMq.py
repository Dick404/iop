#!/usr/bin/python

import sys
import os
import re
import logging as log
from testUnit import tester as T

class rabbitmq_installer():
    def __init__(self):
        pass

    def install_set_rabbitMq(self,ip,typeof,hostname):
        os.system('ssh '+ip+' "yum -y install rabbitmq-server"')
        os.system("scp ./config/.erlang.cookie "+ip+"://var/lib/rabbitmq/")
        os.system("ssh "+ip+" chown rabbitmq:rabbitmq /var/lib/rabbitmq/.erlang.cookie")
        if typeof == "master":
            os.system("ssh "+ip+" rabbitmq-plugins enable rabbitmq_management")
            os.system("ssh "+ip+" rabbitmq-server -detached")
            os.system("ssh "+ip+" rabbitmqctl add_user openstack 123456a?;ssh "+ip+" rabbitmqctl set_user_tags openstack administrator")
            os.system("ssh "+ip+" rabbitmqctl set_policy ha-all \"^\"  '{\"ha-mode\":\"all\"}'")
            os.system("ssh "+ip+" \"rabbitmqctl add_user iop 123456a?;rabbitmqctl set_user_tags iop administrator\"")
            os.system("ssh "+ip+" \"rabbitmqctl set_permissions iop '.*' '.*' '.*'\"")
        else:
            os.system("ssh "+ip+" rabbitmq-plugins enable rabbitmq_management")
            os.system("ssh "+ip+" rabbitmq-server -detached")
            order = "\"rabbitmqctl stop_app;rabbitmqctl join_cluster rabbit@"+hostname+";rabbitmqctl start_app\""
            os.system('ssh '+ip+' '+order)
        return

    def operator(self,ips):
        hostname = os.popen("ssh "+ips[0]+" hostname").readlines()[0].split("\n")[0].split(".")[0]
        print hostname
        for i in range(len(ips)):
            self.install_set_rabbitMq(ips[i],"master" if i == 0 else "slaver",hostname)
        return



if __name__ == "__main__":
    rabbit = rabbitmq_installer()
    examer = T()
    if not examer.test():
        raise Exception("less arguments or wrong arguments")
    ips = examer.get_ips()
    rabbit.operator(ips)
