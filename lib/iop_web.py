#!/usr/bin/python

import sys
import re
import os
from testUnit import tester

class iopWeb():
    global Excute
    Excute = os.system

    def __init__(self):
        return


    def config(self,ips,proxy):
        print "hello"
        for ip in ips:
            Excute("ssh "+ip+" \"if [ ! -x /opt/tomcat ];then\n mkdir /opt/tomcat /opt/jdk\n fi\"")
            Excute("scp ./resource/cache/jdk/java.tar.gz root@"+ip+":/tmp")
            Excute("scp ./resource/cache/tomcat/tomcat.tar.gz root@"+ip+":/tmp")
            Excute("ssh "+ip+" tar zxvf /tmp/java.tar.gz -C /opt/jdk")
            Excute("ssh "+ip+" tar zxvf /tmp/tomcat.tar.gz -C /opt/tomcat")
            Excute("scp -r ./resource/web/cloud-web/  root@"+ip+":/opt/tomcat/webapps/")
        self.configure(proxy,ips)
        self.sql_import(ips)
        Excute("ssh "+ips[0]+" mysql << EOF\n use iop_dev;\nupdate am_endpoint set url='http://"+proxy+"/v1/AUTH_%(tenant_id)s' where service_id='service_swift'\nEOF")
        return
    
    def configure(self,proxy_ip,ips):
        reader = open("./config/iop_config","r")
        config_data = reader.readlines()
        reader.close()
        for config in config_data:
            temp_data = config.split("!!!")
            filename = temp_data[0]
            temp_data = temp_data[1]
            temp = temp_data.split("&")
            flag = temp[1]
            temp_data = temp[0]
            temp = temp_data.split("$")
            atributes = temp
            self.set_conifg_file(filename,atributes,proxy_ip,ips,flag)
            for ip in ips:
                Excute("scp /tmp/iop/"+filename+" root@"+ip+":/opt/tomcat/webapps/cloud-web/WEB-INF/classes/")
        return 
    
    def set_conifg_file(self,filename,atributes,proxy_ip,ips,flag):
        reader = open("./resource/web/cloud-web/WEB-INF/classes/"+filename,"r")
        data = reader.readlines()
        reader.close()
        if os.path.exists("/tmp/iop"):
            writer = open("/tmp/iop/"+filename,"w")
        else:
            Excute("mkdir /tmp/iop")
            writer = open("/tmp/iop/"+filename,"w")
        j = 0
        for atribute in atributes:
                temp = atribute.split("=")
                for i in range(j,len(data)):
                    print j,i
                    print temp[0],data[i]
                    if re.search(temp[0],data[i]):
                        if flag == "proxy\n":
                            writer.write(re.sub(r"\${proxy}(\n)?",proxy_ip,data[i])+"\n")
                            j = i+1
                            break
                        else:
                            value = ips[0]+":5672"
                            for x in range(1,len(ips)):
                                value += ","+ips[x]+":5672"
                            print data[i]
                            writer.write(re.sub(r"=.*$","="+value,data[i])+"\n")
                            j = i+1
                            print j
                            break
                    else:
                        writer.write(data[i])
        if j != len(data)-1:
            for i in range(j,len(data)):
                 writer.write(data[i])
        return

   
    def sql_import(self,ips):
        for ip in ips:
            Excute("scp ./config/iop-web/iop_dev.sql ./config/iop-web/iop_dev_monitor.sql root@"+ip+":/tmp")
            Excute("ssh "+ip+" \"mysql -p123456a? -e 'source /tmp/iop_dev_monitor.sql'\"")
            Excute("ssh "+ip+" \"mysql -p123456a? -e 'source /tmp/iop_dev.sql'\"")


    def run(self,ips):
        for ip in ips:
            Excute("ssh "+ip+" export PATH=PATH:/opt/jdk/bin;export JAVA_HOME=/opt/jdk;/opt/tomcat/bin/startup.sh")

    def stop(self,ips):
        for ip in ips:
            Excute("ssh "+ip+" export PATH=PATH:/opt/java/bin/opt/tomcat/bin/stop.sh")
        return

if __name__ == "__main__":
    T = tester()
    if not T.test():
        raise Exception("less arguments or illegal arguments")
    ips = T.get_ips()
    O = iopWeb()
    O.config(ips,"10.110.17.136")
    O.sql_import(ips)

