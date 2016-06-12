import sys
import os
import re

class util():

    __Excute = None
    __data = None

    def __init__(self):
        self.__Excute=os.system
        self.__data = {}
        return

    def init(self,index,*arg)->list,->tuple:
        for i in range(len(index)):
            self.__data.setdefault(index[i],arg[i])
        return

    def value(self,info):
        return


