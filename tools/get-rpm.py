#!/usr/bin/env python
import os
import sys
import re

def get_data():
#   global packages_list
    packages_list = []
    if len(sys.argv) > 1:
        directory = sys.argv[1]
    else: 
	directory = os.getcwd()
    data_list = os.listdir(directory)
    for data in data_list:
	if os.path.isfile(data):
	    packages = open(data,"r")
	    packages = packages.readlines()
            for package in packages:
#               print package
                temp = package.split(' ')
#		print temp

		if temp[0] == '' and len(temp)>1:
#                   print "1111111111111111111"
		    packages_list.append(temp[1])
		else :
#                   print temp
		    continue

    return packages_list

def download_package(packages_list):
#    print packages_list
    flag = 1
    packages = ''
    for package in packages_list:
            if flag == 1:
                flag = 0
                continue
	    packages += package + ' '

    return packages


def run(packages):
    if os.path.exists("/var/www/html/IOPa"):
        print "standard directory exists now download files to there------"
        print "-----------------------------------------------------------"
        os.system("yumdownloader --destdir /var/www/html/IOP "+packages)
    else :
        print "standard directory not exists now download files to here------"
        print "--------------------------------------------------------------"
        os.system("yumdownloader "+packages)


if __name__ == "__main__":
    p_list = get_data()
    p = download_package(p_list)
#   print p
    run(p)
