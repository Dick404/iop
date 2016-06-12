#!/usr/bin/python
import sys
import os
import re
import time
import logging as log
from report import recorder
#from keystones import keystone as ks
#import keystones
#ks = reload(keystones).keystone()
import  ssh_shake
ssh = reload(ssh_shake).ssh_shake()
from optparse import OptionParser as op
from setup_yum import yum_installer as yum
import worker_setup as worker
import ha_setup

def dependence():
    os.system("tar zxvf ./tools/pip-8.1.1.tar.gz -C /opt/")
    os.system("cd /opt/pip-8.1.1;python setup.py install")
    os.system("cd /opt/iop/tools/")
    os.system("pip install pycrypto")
    os.system("pip install paramiko")
    os.chdir("/opt/iop")
    return



def ssh_belive_eachother(ips,roles):
    if not os.path.exists("/root/.ssh/id_rsa.pub"):
        os.system("ssh-keygen -t rsa -f /root/.ssh/id_rsa -P ''")
        os.system("cat /root/.ssh/id_rsa.pub >> /root/.ssh/authorized_keys")
    if not os.path.exists("/tmp/iop"):
       	os.system("mkdir /tmp/iop")
    for i in range(len(ips)):
        ssh.ssh_config(ips[i])
	time.sleep(1)
        ssh.ssh_shake_config(ips[i],roles[i])

def get_argv(ips,hosts):
#    os.chdir("../")
    num_host = len(ips)
    result_info = []
    for host in range(num_host):
        IP = ips[host]
        Info = []
        Info.append(IP+" ")
#    print temp
        temp = os.popen("ssh "+IP+" 'uname -n'").readlines()
        print temp
        temp = temp[0].split("\n")[0]
        domain = temp
        Info.append(domain+" ")
#    global name_Master
        name = ""
#    global name_slaver
        tmplist = domain.split(".")
        print tmplist
        for x in range(len(tmplist)-1):
            name = name + tmplist[x]
        print tmplist
        Info.append(name+" ")
        Info.append(hosts[host]+" ")
        Info.append("node"+str(host+1))
        result_info.append(Info)
    return result_info
    


def init_env(ips,hosts):
    info_env = get_argv(ips,hosts)
    print info_env
    print sys.argv[0]
    print os.getcwd()
    file_read_hosts = open("./config/hosts","r")
    file_write_hosts = open("/etc/hosts","w")
    temp = file_read_hosts.readlines()
    file_write_hosts.writelines(temp)
    for index in range(len(info_env)):
    	file_write_hosts.writelines(info_env[index])
    	file_write_hosts.write("\n")
    file_read_hosts.close()
    file_write_hosts.close()
    for index in range(len(info_env)):
        os.system("scp /etc/hosts "+info_env[index][3].split(" ")[0]+":/etc/hosts")
#    os.system("cp ./config/IOP.pth /usr/lib/python2.7/site-packages/")

        



 
def main():
    proxy = None
    monitor = None
    ips_worker = []
    ips = []
    roles = []
    hosts = []
    dev = []
    record = recorder()
    Y = yum()
    usage = "usage: %prog options"
    option = op(usage)
    option.add_option("-f","--file",default=False,action="store",dest="filename",help="point the config file",metavar="FILE")
    option.add_option("-i","--ips",default=False,action="store",dest="ips",help="point the ips except file",metavar="Ips")
    (options,arg) = option.parse_args()
    if not options.filename and not options.ips:
        option.print_help()
        return 
    if options.filename != False:
        if not os.path.exists(options.filename):
            print "ERROR : [ main ] config file is not existed."
            return
        reader = open(options.filename)
        configs = reader.readlines()
        reader.close()
        for config in configs:
            temp = config.split(":")
            if temp[0] == "proxy" or temp[0]=="worker" or temp[0]=="monitor":
                roles.append(temp[0].strip())
                ips.append(temp[1].strip())
            elif temp[0] == "proxyhost" or temp[0] == "workerhost" or temp[0] == "monitorhost":
                hosts.append(temp[1].split("\n")[0])
            elif temp[0]=="device":
                dev.append(temp[1])
            else:
                raise Exception("config file is wrong,please check it.")
    else :
        ips = options.ips.split(",")
        for i in range (len(ips)):
            if i == 0:
                roles.append("proxy")
            else:
                roles.append("worker")
    for i in range(len(ips)):
        if roles[i]=="proxy":
            proxy = ips[i]
        elif roles[i]=="worker":
            ips_worker.append(ips[i])
        elif roles[i] == "monitor":
            monitor = ips[i]
        else:
            raise Exception("Unkown Error!")

    if record.test("ssh_dependence"):
        dependence()
        record.record("ssh_dependence")
    if record.test("ssh_shake"):
        ssh_belive_eachother(ips,roles)
        record.record("ssh_shake")
    if record.test("host"):
        init_env(ips,hosts)
        record.record("host")
    if record.test("yum-install"):
        Y.install_yum_source()
        record.record("yum-install")
    if record.test("yum-source"):
        Y.set_yum_source(ips_worker,proxy)
        record.record("yum-source")
    worker.main(ips_worker,proxy)
    ha_setup.main(ips,dev[0].split("\n")[0],monitor)

#    dependence()
#    ssh_belive_eachother()
#    init_env()
#    install_yum_source()
#    set_yum_source()
#    install_mysql()
#    mysql_master_info = []
#    for num in range(len(result_info)):
#	    if num == 0:
#                 set_mysql(num,"master",result_info[num][0],len(result_info))
#	    else :
#	         set_mysql(num,"slaver",result_info[num][0],len(result_info))
#    os.system("rm -rf /tmp/iop/galera.cnf")
#    init_mysql()
#    f = 1
#    for info in result_info:
#	if f :
#	    flag = "master"
#	    f = 0
#        else :
#	    flag = "slaver"
#    	install_set_rabbitMq(info[0].split(" ")[0],flag)
#    ip = result_info[0][0].split(" ")[0]
#    ks.main(ip)

if __name__ == "__main__":
    main()
    
