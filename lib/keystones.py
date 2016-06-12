#!/usr/bin/python
import sys
import os
import re
import keystoneConfig
import ceilometers
from optparse import OptionParser as OP
config = reload(keystoneConfig)
ceilometer = reload(ceilometers)

#sys.path.append("../lib")



class keystone():
    global excute
    excute = os.system
    global token
    temp = os.popen("openssl rand -hex 10")
    token = temp.readlines()[0]
    temp.close()

    def __init__(self):
#	    temp = os.popen("openssl rand -hex 10")
#	    token = temp.readlines()[0]
#	    temp.close()
	    pass

    def install_keystone(self):
	    os.system("yum -y install openstack-keystone httpd mod_wsgi python-openstackclient memcached python-memcached")
            os.system("systemctl enable memcached.service;systemctl start memcached.service")
            # if checkout()  then print infomation
            return


    def set_keystone(self,ip):
        config.set_keystone(ip,token)
        excute("systemctl enable openstack-keystone.service;systemctl restart openstack-keystone.service")
        return

    def create_service_API(self,ip,token):
        excute("systemctl restart openstack-keystone")
#	    os.environ['OS_TOKEN'] = token
#	    os.putenv("OS_TOKEN",token)
#	    os.environ['OS_URL'] = "http://10.110.17.25:35357/v2.0"
#	    writer = open("./config/auth.sh","w")
#	    writer.write("export OS_URL=http://10.110.17.25:35357/v2.0\n")
#	    writer.write("export OS_TOKEN="+token)
#	    writer.close()
#	    excute("ls /root/iop/config")
#	    excute("chmod +x /root/iop/config/auth.sh")
#	    excute("source /root/iop/config/auth.sh")
#	    order = "/bin/bash export OS_TOKEN="+token+";"
        order = "openstack --os-url http://"+ip+":35357/v2.0 --os-token "+token.split("\n")[0]+" service create --name keystone --description 'Openstack Identity' identity"
        print order
        flag = True
#        reader = os.popen("openstack-service list")
#        services = reader.readlines()
 #       reader.close()
#        for service in services:
#            if service == "openstack-keystone\n":
#                flag = False
#        if flag:
        excute("openstack --os-url http://"+ip+":35357/v2.0 --os-token "+token.split("\n")[0]+" service create --name keystone --description 'Openstack Identity' identity")
        excute("openstack  --os-url http://"+ip+":35357/v2.0 --os-token "+token.split("\n")[0]+" endpoint create --publicurl http://"+ip+":5000/v2.0 --internalurl http://"+ip+":5000/v2.0 --adminurl http://"+ip+":35357/v2.0 --region RegionOne identity")
        return


    # create projects users and roles
    def create_PUR(self,ip):
        excute('openstack --os-url http://'+ip+':35357/v2.0 --os-token '+token.split("\n")[0]+' project create --description "Admin Project" admin')
        excute('openstack --os-url http://'+ip+':35357/v2.0 --os-token '+token.split("\n")[0]+' user create --password 123456a? admin')
        excute("openstack --os-url http://"+ip+":35357/v2.0 --os-token "+token.split("\n")[0]+" role create admin")
        excute("openstack --os-url http://"+ip+":35357/v2.0 --os-token "+token.split("\n")[0]+" role add --project admin --user admin admin")
        excute('openstack --os-url http://'+ip+':35357/v2.0 --os-token '+token.split("\n")[0]+' project create --description "Service Project" service')
        excute('openstack --os-url http://'+ip+':35357/v2.0 --os-token '+token.split("\n")[0]+' project create --description "Demo Project" demo')
        excute('openstack --os-url http://'+ip+':35357/v2.0 --os-token '+token.split("\n")[0]+' user create --password 123456a? demo')
        excute('openstack --os-url http://'+ip+':35357/v2.0 --os-token '+token.split("\n")[0]+' role create user')
        excute('openstack --os-url http://'+ip+':35357/v2.0 --os-token '+token.split("\n")[0]+' role add --project demo --user demo user')
        return
 
    def verify():
	    pass


    def create_keystone_script(self,ip):
    	reader = open("./config/admin-openrc.sh","r")
    	writer = open("/root/admin-openrc.sh",'w')
    	text = reader.readlines()
    	reader.close()
    	writer.writelines(text)
    	info = "export OS_AUTH_URL=http://"+ip+":5000/v2.0"
    	writer.write(info)
    	writer.close()
    	os.system("chmod +x /root/admin-openrc.sh")
    	os.system("source /root/admin-openrc.sh")
    	return 
    
    def create_ceilometer_script(self,ip):
        reader = open("./config/ceilometer-openrc.sh","r")
        writer = open("/root/iop/ceilometer-openrc.sh",'w')
        text = reader.readlines()
        reader.close()
        writer.writelines(text)
        info = "export OS_AUTH_URL=http://"+ip+":5000"
        writer.write(info)
        writer.close()
        os.system("chmod +x /root/ceilometer-openrc.sh")
        #os.system("source /root/ceilometer-openrc.sh")
        return 

    def main(self,ip):
        print "begin keystone install"
        self.install_keystone()
        self.set_keystone(ip)
        self.create_service_API(ip,token)
        self.create_PUR(ip)
        self.create_keystone_script(ip)
        self.create_ceilometer_script(ip)
        ceilometerOrder = ceilometer.ceilomter()
        ceilometerOrder.main(ip,token)

class mariaDB():

    __Excute = None

    def __init__(self):
        self.__Excute = os.system

    def install(self,monit="127.0.0.1"):
        self.__Excute("ssh "+monit+" yum install -y mariadb-server")
        return

    def config(self,monit="127.0.0.1"):
        self.__Excute("scp conifg/my.cnf root@"+monit+":/etc/")
        return

    def init(self,monit):
        self.__Excute("ssh "+monit+" \"mysql << EOF \ncreate database keystone;\nGRANT ALL PRIVILEGES ON keystone.* TO 'keystone'@'%' IDENTIFIED BY '123456a?' WITH GRANT OPTION;\nGRANT ALL PRIVILEGES ON keystone.* TO 'keystone'@'localhost' IDENTIFIED BY '123456a?' WITH GRANT OPTION;\nGRANT ALL PRIVILEGES ON keystone.* TO 'keystone'@'"+os.popen("hostname").readlines()[0].split("\n")[0]+"' IDENTIFIED BY '123456a?' WITH GRANT OPTION;\nFLUSH PRIVILEGES;\nEOF\"")
        self.__Excute("ssh "+monit+" systemctl enable mariadb.service")
        return

    def run(self,monit):
        self.__Excute("ssh "+monit+" systemctl start mariadb.service")
        return

    def operator(self,monit="127.0.0.1"):
        self.install(monit)
        self.config(monit)
        self.run(monit)
        self.init(monit)

class RabbitMQ(object):

    """docstring for RabbitMQ"""

    __Excute = None

    def __init__(self):
        self.__Excute = os.system
    
    def install(self,monit):
        self.__Excute("ssh "+monit+" yum -y install rabbitmq-server")
        return

    def init(self,monit):
        self.__Excute("ssh "+monit+" rabbitmq-plugins enable rabbitmq_management;systemctl enable rabbitmq-server;systemctl start rabbitmq-server;")
        self.__Excute("ssh "+monit+" rabbitmqctl add_user openstack 123456a?;rabbitmqctl set_user_tags openstack administrator")
        return

    def run(self,monit):
        self.__Excute("ssh "+monit+" systemctl start rabbitmq-server;")
        return

    def operator(self,monit):
        self.install(monit)
        self.run(monit)
        self.init(monit)

if __name__ == "__main__":
    if len(sys.argv)==1:
        raise Exception("less arguments or illegal arguments!")
    else:
        ip = sys.argv[1]
        mysql = mariaDB()
        rabbitmq = RabbitMQ()
    mysql.operator()
    rabbitmq.operator()
    installer = keystone()
    installer.main(ip)


