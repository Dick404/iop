#!/usr/bin/python

import os
import sys
import re

class blobstore():
    global Excute
    Excute = os.system
    def __init__(self):
        return

    def install(self,ip):
#        if not os.path.exists("/opt/cloud-service-factory"):
        Excute("ssh "+ip+" mkdir /opt/cloud-service-factory")
        Excute("ssh "+ip+" tar zxvf ./resource/cache/blobstrore/cloud-service-factory.tar.gz -C /opt/cloud-service-factory")
        return


    def run(self,ip):
        Excute("ssh "+ip+" /opt/cloud-service-factory/block-store-server/gradlew jettyRun &")
        return
