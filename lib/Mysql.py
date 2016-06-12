#!/usr/bin/python

import sys
import os
import re
import logging as log
from testUnit import tester as T

class mysql_installer():

    def __init__(self):
        pass

    def install_mysql(self,ips):
        for ip in ips:
            os.system('ssh '+ip+' "yum install -y MariaDB-Galera-server MariaDB-client galera rsync"')
            #os.system("ssh "+ip+" systemctl enable mysql")
            os.system("scp ./config/my.cnf root@"+ip+":/etc/")
        return
# ip arguments can't include proxy-ip and monitor-ip 
    def set_mysql(self,num,typeof,ip,lenth=None):
        os.system("ssh node"+str(num+2)+" mysql_install_db")
        os.system("ssh node"+str(num+2)+" systemctl stop firewalld.service;systemctl disable firewalld.service")
        os.system("ssh node"+str(num+2)+" /etc/init.d/mysql start")
        os.system("ssh node"+str(num+2)+" mysql -u root << EOF 2>/dev/null \ngrant all privileges on *.* to 'sst'@'localhost' identified by '123456a?';\ngrant all privileges on *.* to 'sst'@'%' identified by '123456a?';\ngrant all privileges on *.* to 'root'@'localhost' identified by '123456a?';\ngrant all privileges on *.* to 'root'@'%' identified by '123456a?';\nflush privileges;\nEOF")
        os.system("ssh node"+str(num+2)+" /etc/init.d/mysql stop")

        if not os.path.exists("/tmp/iop/wsrep.cnf"):
            reader = open("./config/wsrep.cnf","r")
            configs = reader.readlines()
            reader.close()
        else :
	    reader = open("/tmp/iop/wsrep.cnf","r")
	    configs = reader.readlines()
	    reader.close()
        writer = open("/tmp/iop/wsrep.cnf","w")
        for config in configs:
            temps = config.split("=")
            if num == 0 and re.match(r"wsrep_cluster_address=.*$",config):
	        print "find the option!!!!!!"
                flag = re.search(r"\"(.*)\"",temps[1])
                if flag and not temps[1]=="\"gcomm://\"":
		    temps[1] = "\""+flag.group(1)+"node2"
		    for i in range(1,lenth):
		        temps[1] += ",node"+str(i+2)
		    temps[1]+="\""
	        writer.write(temps[0]+"="+temps[1]+"\n")
         #    elif re.match(r"wsrep_node_name=.*$",config):
         #        temps[1] = "node"+str(num+2)
	        # writer.write(temps[0]+"="+temps[1]+"\n")
         #    elif re.match(r"wsrep_node_address=.*$",config):
         #        temps[1] = ip
	        # writer.write(temps[0]+"="+temps[1]+"\n")
            else :
	        data = temps[0]
	        for i in range(1,len(temps)):
	    	    data += "="+temps[i]
	        writer.write(data)
        writer.close()
        os.system("scp /tmp/iop/wsrep.cnf node"+str(num+2)+":/etc/my.cnf.d/")
        os.system("ssh node"+str(num+2)+" chown -R mysql:mysql /var/lib/mysql/performance_schema/")
	if typeof == "master":
            print "master is starting================================"
	    #os.system("ssh node"+str(num+2)+" mysql_install_db")
	    #os.system("ssh node"+str(num+2)+" systemctl stop firewalld.service;systemctl disable firewalld.service")
            #os.system("ssh node"+str(num+2)+" \"/usr/libexec/mysqld --wsrep-new-cluster --user=root \"&")
            os.system("ssh node"+str(num+2)+" /etc/init.d/mysql bootstrap")
        else :
	    print "slaver is starting================================"
	    #os.system("ssh node"+str(num+2)+" mysql_install_db")
	    #os.system("ssh node"+str(num+2)+" systemctl stop firewalld.service;systemctl disable firewalld.service")
            os.system("ssh node"+str(num+2)+" /etc/init.d/mysql start")
        return

    def config_mysql_ms(self):
        if typeof == "master":
            os.system("mysql -u root << EOF 2>/dev/null \ncreate database keystone; \ncreate database iop_dev; \ngrant all privileges on *.* to 'keystone'@'localhost' identified by '123456a?';\ngrant all privileges on *.* to 'keystone'@'%' identified by '123456a?'\nEOF")
            os.system("mysql -u root << EOF 2>/dev/null \ngrant all privileges on *.* to 'iop_dev'@'localhost' identified by '123456a?;\ngrant all privileges on *.* to 'iop_dev'@'%' identified by '123456a?'\nEOF")
            os.system("mysql -e source \"./config/swift/sql/cloud_storage_swift.sql\"")
            os.system("cp -f ./config/my.cnf /etc/my.cnf")
            os.system("systemctl restart mariadb")
            temp = os.popen("mysql -u root << EOF 2>/dev/null \nshow master status \nEOF")
            mysql_master_info=temp.readlines()
            mysql_master_info=mysql_master_info[1].split('\t')
            return mysql_master_info

        elif typeof == "slaver":
            os.system("ssh node"+str(num)+" 'mysql -u root << EOF  \ncreate database keystone; \ncreate database iop_dev; \ncreate database cloud_storage_swift \nEOF'")
            os.system("scp ./config/my_slave.cnf node2:/etc/my.cnf")
            os.system("systemctl restart mariadb")
            os.system('ssh node2 "systemctl restart mariadb"')
            order = "mysql -u root << EOF  \nslave stop; \nchange master to master_host='"+ip.split(' ')[0]+"',master_user='keystone',master_password='123456a?',master_log_file=\'"+mysql_master_info[0]+"\',master_log_pos="+mysql_master_info[1]+"; \nslave start; \nEOF"
            print order
            os.system('ssh node'+str(num)+' \"'+ order+'\"')

        else:
            print "there is a error that can't image!!!"
            return "error"

    def init_mysql(self):
	os.system("ssh node2 mysql -u root -p123456a? << EOF 2>/dev/null \ncreate database keystone; \ncreate database iop_dev; \ncreate database iop_dev_monitor;\ngrant all privileges on keystone.* to 'keystone'@'localhost' identified by '123456a?';\ngrant all privileges on keystone.* to 'keystone'@'%' identified by '123456a?'\nEOF")
        os.system("ssh node2 mysql -u root -p123456a? << EOF 2>/dev/null \ngrant all privileges on iop_dev.* to 'dev'@'localhost' identified by '123456a?';\ngrant all privileges on iop_dev.* to 'dev'@'%' identified by '123456a?';\ngrant all privileges on iop_dev_monitor.* to 'dev'@'localhost' identified by '123456a?';\ngrant all privileges on iop_dev_monitor.* to 'dev'@'%' identified by '123456a?';\nEOF")
        os.system("scp config/swift/sql/cloud_storage_swift.sql root@node2:/tmp;ssh node2 \"mysql -p123456a? -e 'source /tmp/cloud_storage_swift.sql'\"")   #command need "" and ''
        return

    def operator(self,ips):
        for i in range(len(ips)):
            self.set_mysql(i,"master" if i == 0 else "slaver",ips[i],len(ips) if i == 0 else None)
        os.system("rm -rf /tmp/iop/wsrep.cnf")                  # if not repeate excutation will produce error
        self.init_mysql()
        return 


if __name__ == "__main__":
    examer = T()
    my = mysql_installer()
    if not examer.test():
        raise Exception("less ips or your argument is illegal!")
    ips = examer.get_ips()
    my.install_mysql(ips)
    for i in range(len(ips)):
        my.set_mysql(i,"master" if i == 0 else "slaver",ips[i],len(ips) if i == 0 else None)
    os.system("rm -rf /tmp/iop/wsrep.cnf")                  # if not repeate excutation will produce error
    my.init_mysql()
