#!/usr/bin/python

import sys
import os
import re
import time
import logging as log

class yum_installer():

    __Excute = None

    def __init__(self):
        self.__Excute = os.system

    def install_yum_source(self):
        os.chdir("./resource/cache/createrepo")
        os.system("rpm -Uvh libxml2-2.9.1-6.el7_2.2.x86_64.rpm")
        os.system("rpm -ivh  deltarpm-3.6-3.el7.x86_64.rpm libxml2-python-2.9.1-6.el7_2.2.x86_64.rpm python-deltarpm-3.6-3.el7.x86_64.rpm createrepo-0.9.9-25.el7_2.noarch.rpm")
        os.chdir("../httpd")
        os.system("rpm -ivh apr-1.4.8-3.el7.x86_64.rpm apr-util-1.5.2-6.el7.x86_64.rpm httpd-tools-2.4.6-40.el7.centos.x86_64.rpm mailcap-2.1.41-2.el7.noarch.rpm")
        os.system("rpm -ivh httpd-2.4.6-40.el7.centos.x86_64.rpm")
        os.system("mkdir -p /var/www/html/IOP")
	os.system("rm -rf /etc/httpd/conf/httpd.conf;cp -f /opt/iop/config/httpd/httpd.conf /etc/httpd/conf/httpd.conf")
        os.system("systemctl enable httpd")
        os.system("systemctl start httpd")
        temp = os.popen("ls "+"../")
        directories = temp.readlines()
        for directory in directories:
	    order = "cp -f ../"+directory.split("\n")[0]+"/* /var/www/html/IOP/"
	    print order
            os.system(order)
        os.system("createrepo /var/www/html/IOP")
        os.chdir("../../../")
        os.system("systemctl disable firewalld;systemctl stop firewalld")
        return

    def set_yum_source(self,ips,proxy):
        self.__Excute("mkdir /etc/yum.repo.d/temp;mv /etc/yum.repos.d/*.repo /etc/yum.repos.d/temp/;")
        file_repo = open("/etc/yum.repos.d/IOP.repo","w")
        file_repo.write("[IOP]\n")
        file_repo.write("name=IOP\n")
        file_repo.write("baseurl=http://"+proxy+":8443/IOP/\n")
        file_repo.write("enable=1\n")
        file_repo.write("gpgcheck=0\n")
        file_repo.close()  
        os.system("yum clean all")
        os.system("yum repolist")
        for ip in ips:
	    print "now check the "+ip+"'s status........"
	    print "scp /etc/yum.repos.d/IOP.repo "+ip+":/etc/yum.repo.d/"
            os.system("ssh "+ip+" mkdir /etc/yum.repos.d/temp")
            os.system("ssh "+ip+" \"mv /etc/yum.repos.d/*.repo /etc/yum.repos.d/temp\";scp /etc/yum.repos.d/IOP.repo "+ip+":/etc/yum.repos.d/")
            os.system("ssh "+ip+" \"yum clean all\"")
            os.system("ssh "+ip+" \"yum repolist\"")
        return 

if __name__ == "__main__":
    ips = []
    for i in range(1,len(sys.argv)):
        ips.append(sys.argv[i])
    if len(ips) == 0:
        raise Exception("less arguments")
    tester = yum_installer()
    tester.install_yum_source()
    tester.set_yum_source(ips,"10.110.17.136")

