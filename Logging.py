#!/usr/bin/python
# -*- coding=utf-8 -*-
from os import sys
sys.path.append("..")
from imp import reload
reload(sys)
import logging,datetime

class Logging:
     
    def __init__(self,logger_name="logger_name",filename_index=""):
        # piece = str(int(datetime.datetime.now().strftime('%M'))/10)
        # self.path = "./log/test" + datetime.datetime.now().strftime('%m%d%H%M0%s' % piece) + ".log"
        self.path = "./logs/coe" + datetime.datetime.now().strftime('%m%d') + "_%s.log" % filename_index
        self.logger = logging.getLogger("logger_name")
        self.logger.setLevel(logging.INFO)
        self.fmt = logging.Formatter(
        '%(asctime)s %(levelname)s %(message)s', '%Y-%m-%d %H:%M:%S')
        #设置CMD日志
        self.sh = logging.StreamHandler()
        self.sh.setFormatter(self.fmt)
        self.fh = logging.FileHandler(self.path)
        self.fh.setFormatter(self.fmt)
        self.logger.addHandler(self.sh)
        self.logger.addHandler(self.fh)

    def __del__(self):
        self.logger.removeHandler(self.fh)
        self.logger.removeHandler(self.sh)
        self.logger.handler=[]

    def debug(self, message):
        self.logger.debug(message)
    
    def info(self, message):
        self.logger.info(message)

    def war(self, message):
        self.logger.warning(message)

    def error(self, message):
        self.logger.error(message)

    def cri(self, message):
        self.logger.critical(message)
        
if __name__ == '__main__':
    w=Logging()
    w.info('success')
    