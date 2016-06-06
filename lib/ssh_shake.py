#!/usr/bin/python

import sys
import os
import re
import time

import paramiko

class ssh_shake():
    def __init__(self):
        global Excute
        Excute = os.system
        return

    def ssh_config(self,ip,port=22,user="root",passwd="123456a?"):
        ssh = paramiko.SSHClient()
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        ssh.connect(ip, port, user, passwd)
        sftp = paramiko.SFTPClient.from_transport(ssh.get_transport())
        sftp = ssh.open_sftp()
        sftp.put("./config/ssh_config","/etc/ssh/ssh_config")
        ssh.exec_command("systemctl restart sshd")
        ssh.close()
        return


    def ssh_shake_config(self,ip,role,port=22,user="root",passwd="123456a?"):
        ssh = paramiko.SSHClient()
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        ssh.connect(ip, port, user, passwd)
        sftp = paramiko.SFTPClient.from_transport(ssh.get_transport())
        sftp = ssh.open_sftp()
        if role == "proxy" or role == "monitor":
            stdin,stdout,stderr=ssh.exec_command("ssh-keygen -t rsa -f /root/.ssh/id_rsa -P '' -y")
        else:
            stdin,stdout,stderr=ssh.exec_command("ssh-keygen -t rsa -f /root/.ssh/id_rsa -P ''")
        stdin,stdout,stderr=ssh.exec_command("mkdir /tmp/iop")
        stdin,stdout,stderr=ssh.exec_command("ls -l /root/.ssh/id_rsa.pub")
	time.sleep(1)
        sftp.get("/root/.ssh/id_rsa.pub","/tmp/iop/id_rsa.pub")
        sftp.put("/root/.ssh/id_rsa.pub","/tmp/iop/id_rsa")
        Excute("cat /tmp/iop/id_rsa.pub >> /root/.ssh/authorized_keys")
        stdin,stdout,stderr=ssh.exec_command("cat /tmp/iop/id_rsa >> /root/.ssh/authorized_keys")
        return
    

'''
def main():
    ssh = paramiko.SSHClient()
    print "1"
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    print "2"
    ssh.connect("10.110.17.25",22,"root", "123456a?")
    print "3"
    if 0:
        stdin, stdout, stderr = ssh.exec_command("ssh-keygen -t rsa  -f ~/.ssh/id_rsa -P \'10980\'")
#    print "4"
#    print stdout.readlines()
#    print "5"
#    print stderr.readlines()
#    stdin,stdout,stderr = ssh.exec_command("scp  ~/.ssh/id_rsa.pub root@10.110.17.136:/root/.ssh/136.pub")
#    print stdout.readlines()
#    print stderr.readlines()
    stdin, stdout, stderr = ssh.exec_command("ls .ssh/")
    print stdout.readlines()
    sftp = paramiko.SFTPClient.from_transport(ssh.get_transport())
    sftp = ssh.open_sftp()
    sftp.get(".ssh/id_rsa.pub","/root/.ssh/id_rsa.pub")
    ssh.close()
    reader = open("/root/.ssh/id_rsa.pub","r")
    data = reader.readlines()
    reader.close()
    writer = open("/root/.ssh/authorized_keys","a+")
    writer.writelines(data)
    writer.close()

if __name__ == "__main__":
    main()
 '''

