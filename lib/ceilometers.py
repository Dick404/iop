#!/usr/bin/python

import os
import sys
import re
import mongodbConfig as mongo
import ceilometerConfig as ceilometer

class ceilomter():
    global Excute
    Excute = os.system

    def __init__(self):
	pass

    def install(self,ip,token):
        mongo.install()
	IPs = mongo.getLocalIp()
	print IPs
        mongo.config(IPs)
        mongo.run()
        mongo.create(ip)
        Excute("source admin-openrc.sh")
        Excute("openstack --os-url http://"+ip+":35357/v2.0 --os-token "+token.split('\n')[0]+" user create --password 123456a? ceilometer ")
        Excute("openstack --os-url http://"+ip+":35357/v2.0 --os-token "+token.split('\n')[0]+" role add --project service --user ceilometer admin")
        Excute("openstack --os-url http://"+ip+":35357/v2.0 --os-token "+token.split('\n')[0]+" service create --name ceilometer --description \"Telemetry\" metering")
        Excute('openstack --os-url http://'+ip+':35357/v2.0 --os-token '+token.split('\n')[0]+' endpoint create --publicurl http://'+ip+":8777 --internalurl http://"+ip+":8777 --adminurl http://"+ip+":8777 --region RegionOne metering")
        Excute('yum -y install openstack-ceilometer-api openstack-ceilometer-collector openstack-ceilometer-notification openstack-ceilometer-central openstack-ceilometer-alarm python-ceilometerclient')
        return


    def config(self,ip,token):
        ceilometer.config(ip,token)
        return


    def run(self):
        Excute("systemctl enable openstack-ceilometer-api.service openstack-ceilometer-collector.service openstack-ceilometer-notification.service openstack-ceilometer-alarm-evaluator.service openstack-ceilometer-alarm-notifier.service")
        Excute("systemctl restart openstack-ceilometer-api.service openstack-ceilometer-collector.service openstack-ceilometer-collector.service openstack-ceilometer-notification.service openstack-ceilometer-alarm-evaluator.service openstack-ceilometer-alarm-notifier.service")

    def main(self,ip,token):
        self.install(ip,token)
	self.config(ip,token)
	self.run()
