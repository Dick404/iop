yum remove -y MariaDB-Galera-server
yum remove -y MariaDB-client 
yum remove -y galera 
yum remove -y rsync
rpm -e --nodeps MariaDB-common-10.0.21-1.el7.centos.x86_64
rpm -e --nodeps MariaDB-client-10.0.21-1.el7.centos.x86_64
rpm -e --nodeps MariaDB-shared-10.0.21-1.el7.centos.x86_64
rpm -e --nodeps MariaDB-Galera-server-10.0.21-1.el7.centos.x86_64

rm -rf /var/lib/mysql 
rm -rf /etc/my.cnf.d/wsrep.cnf
rm -rf /etc/my.cnf.d/wsrep.cnf.bak
