#!/usr/bin/python

import os
import re
import sys
import xml.etree.ElementTree as ET
from  testUnit import tester

class Mycat():

    __Excute=None

    def __init__(self):
        self.__Excute = os.system
        return

    def install(self):
        self.__Excute("tar -zxvf resource/cache/Mycat/Mycat-server-1.5-RELEASE-linux.tar.gz -C /usr/local/")
        if os.path.exists("/usr/local/java"):
            self.__Excute("tar -zxvf resource/cache/jdk/java.tar.gz -C /usr/local/java/")
        else:
            self.__Excute("mkdir /usr/local/java")
            self.__Excute("tar -zxvf resource/cache/jdk/java.tar.gz -C /usr/local/java/")
        if os.path.exists("/usr/local/mycat/bin/mycat"):
            return True
        else :
            return False
        return

    def config(self,ips):
        tree = ET.parse('config/schema.xml')
        root = tree.getroot()
        data_node = root.getiterator("dataHost")
        data_node = data_node[0]
        for i in range(len(ips)):
            data_node.append("writeHost")
        writeHost_node = data_node.findall("writeHost")
        for i in range(len(writeHost_node)):
            writeHost_node[i].set("host","hostM"+str(i))
            writeHost_node[i].set("url",ips[i]+":3306")
            writeHost_node[i].set("user","root")
            writeHost_node[i].set("password","123456a?")
        print tree
        tree.write("/usr/local/mycat/schema.xml")
        return

    def run(self):
        self.__Excute("export JAVA_HOME=/usr/local/java;export path=\$path\:\$JAVA_HOME/bin;/usr/local/mycat/bin/mycat start")
        if os.path.exists("/usr/local/mycat/logs/mycat.pid"):
            return True
        else :
            return False
        return

    def operator(self,ips):
        self.install()
        self.config(ips)
        self.run()

if __name__ == "__main__":
    T = tester()
    if not T.test():
        raise Exception("less arguments or illegal arguments")
    ips = T.get_ips()
    cat = Mycat()
    cat.operator(ips)

        

