#!/usr/bin/python

import os
import sys
import re
from testUnit import tester as test

class nfs_server():

    __Excute = None

    def __init__(self):
        self.__Excute = os.system

    def install(self):
        self.__Excute("yum install -y nfs-utils")

    def run(self):
        self.__Excute("systemctl start rpcbind.service;systemctl start nfs-server.service")
        return True

    def config(self,ips,dev):
        if not os.path.exists("/storage"):
            self.__Excute("mkdir /storage")
            self.mount_disk(dev)
        writer = open("/etc/exports","w")
        configs = "/storage"
        for ip in ips:
            configs += " "+ip+"(rw,sync,no_root_squash,no_wdelay)"
        writer.write(configs+"\n")
        writer.close()

        return

    def mount_disk(self,dev):
        reader = os.popen("parted -s "+dev+" print")
        size = None
        data = reader.readlines()
        readr.close()
        for d in data:
            if re.match(r"Disk /dev/.*",d):
                x = re.search(r"Disk /dev/\w+: (\d+\.\d+)GB",d)
                size = x.group(1)
        self.__Excute("parted -s "+dev+" parted -s /dev/sdc mklabel msdos")
        self.__Excute("parted -s "+dev+" mkpart primary 1 "+size)
        self.__Excute("mkfs.ext4 "+dev+"1")
        self.__Excute("mount "+dev+" /storage")
        writer = open("/etc/fstab","a+")
        writer.write(dev+" /storage ext4 rw 0 0\n")
        return

    def init(self,ips,dev):
        self.config(ips,dev)
        self.mount_disk(dev)
        self.__Excute("ystemctl enable nfs-server.service")
        self.__Excute("systemctl enable rpcbind.service")
        return

class nfs_client():

    __Excute = None

    def __init__(self):
        self.__Excute = os.system
    
    def install(self,ips):
        for ip in ips:
            self.__Excute("ssh "+ip" yum install -y nfs-utils")
        return

    def run(self,ips):
        for ip in ips:
            self.__Excute("ssh "+ip+" systemctl start rpcbind.service")

        return

    def config(self,ips):
        local_ip = []
        reader = os.popen("ip addr")
        data = reader.readlines()
        reader.close()
        for d in data:
            if re.match(r"    inet (\d+\.\d+\.\d+\.\d+)/.*$",d):
                x=re.search(r"    inet (\d+\.\d+\.\d+\.\d+)/.*$",d)
                local_ip.append(x.group(1))
        for ip in ips:
            self.__Excute("ssh "+ip+" mount -t nfs4 "+local_ip[1] if local_ip[0]=="127.0.0.1" else local_ip[0]+":/ /storage")
            self.__Excute("ssh "+ip+" echo "+local_ip[1] if local_ip[0]=="127.0.0.1" else local_ip[0]+":/ /storage nfs4 rw,hard,intr,proto=tcp,port=2049,noauto 0 0 >> /etc/fstab")     #fstab arguments need check

   def init(self,ips):
       for ip in ips:
           self.__Excute("ssh "+ip+" if [ ! -x /storage ];then\n mkdir /storage \n fi")
       self.config(ips)
       
if __name__ == "__main__":
    T = test()
    ips = T.get_ips()
    server = nfs_server()
    client = nfs_client()
    server.install()
    client.install(ips)
    server.init(ips,dev)
    server.run()
    client.run(ips)
    client.init(ips)


