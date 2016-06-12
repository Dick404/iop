#!/usr/bin/python
#encoding UTF-8

import os
import sys
import re
from  testUnit import tester

class swift():

    __Excute = None

    def __init__(self):
        self.__Excute = os.system
        return

    def install(self,ips):
        for ip in ips:
            self.__Excute("scp -r /opt/iop/resource/web/v1/ root@"+ip+":/opt/tomcat/webapps/")
        return

    def config(self,ips,proxy):
        reader = open("./config/swift/swift.cfg","r")
        data = reader.readlines()
        reader.close()
        for d in data:
            temp = d.split("!!!")
            filename = temp[0]
            temp = temp[1].split("&")
            flag = temp[1]
            temp = temp[0].split("$")
            atributes = temp
            self.configure(ips,proxy,atributes,filename,flag)
            for ip in ips:
                if filename == "storage-service.properties":
                    self.__Excute("scp /tmp/iop/"+filename+" root@"+ip+":/opt/tomcat/webapps/v1/WEB-INF/classes/conf/")
                elif filename == "dataSource.properties":
                    self.__Excute("scp /tmp/iop/"+filename+" root@"+ip+":/opt/tomcat/webapps/v1/WEB-INF/classes/")
        return

    def configure(self,ips,proxy,atributes,filename,flag):
        if os.path.exists("/tmp/iop"):
            writer = open("/tmp/iop/"+filename,"w")
        else:
            self.__Excute("mkdir /tmp/iop")
            writer = open("/tmp/iop/"+filename,"w")
        if os.path.exists("./resource/web/v1/WEB-INF/classes/conf/"+filename):
            reader = open("./resource/web/v1/WEB-INF/classes/conf/"+filename,"r")
        elif os.path.exists("./resource/web/v1/WEB-INF/classes/"+filename):
            reader = open("./resource/web/v1/WEB-INF/classes/"+filename,"r")
        data  = reader.readlines()
        reader.close()
        j = 0
        for atribute in atributes:
            for i in range(j,len(data)):
                temp = atribute.split("=")
                if re.search(temp[0],data[i]):
                    if flag == "proxy\n":
                        writer.write(re.sub("X",proxy,atribute)+"\n")
                        j =i+1
                        break
                    else:
                        print "ERROR:=======================>> BUGS HERE!!!!!"
                else:
                    writer.write(data[i])
        if j != len(data)-1:
            for i in range(j,len(data)):
                writer.write(data[i])
        writer.close()
        return

#    def run(self,ips):
#        self.__Excute("ssh "+ip+" /opt/tomcat/bin/startup.sh")

if __name__ == "__main__":
    T = tester()
    if not T.test():
        raise Exception("less arguments or illegal arguments")
    ips = T.get_ips()
    O = swift()
    O.install(ips)
    O.config(ips,"10.110.17.136")
