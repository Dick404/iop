#!/usr/bin/python

import os
import sys
import re

def config(ip,token):
    configs_new = []
    reader = open("./config/ceilometer.conf","r")
    writer = open("/etc/ceilometer/ceilometer.conf","w")
    configs = reader.readlines()
    reader.close()
    for config in configs:
	if re.match(r"connection ?= ?mongodb://ceilometer:.*$",config):
	    configs_new.append(re.sub(r"= .*$","= mongodb://ceilometer:123456a?@"+ip+":27017/ceilometer",config))
	elif re.match(r"rabbit_host(.?)=(.?).*",config):
	    configs_new.append(re.sub(r"= ?.*$","= "+ip,config))
	elif re.match(r"auth_uri\ ?=\ ?http://.*",config):
	    configs_new.append(re.sub(r"= .*$","= http://"+ip+":5000/v2.0",config))
	elif re.match(r"os_auth_url\ ?=\ ?http://.*",config):
	    configs_new.append(re.sub(r"= ?.*$","= http://"+ip+":5000/v2.0",config))
	elif re.match(r"telemetry_secret\ ?=\ ?.*",config):
	    configs_new.append(re.sub(r"= ?.*$","= "+"d3188d9532688b941fa7",config))
        elif re.match(r"identity_uri\ ?=\ ?http://.*",config):
            configs_new.append(re.sub(r"= ?.*$","= http://"+ip+":35357",config))
	else :
	    configs_new.append(config)
    writer.writelines(configs_new)
    writer.close()
    return    


if __name__=="__main__":
    config("10.110.17.136","123456a?")
