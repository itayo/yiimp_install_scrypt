#!/usr/bin/python
#
#  Please donate authors:
#
#   Origin: coelacanthus: bitcoin:1PGrE58W6921iVNTMFPAQGBsiHTx7WmdY2
#
import time
import threading
import os
import sys
import subprocess
from logging import getLogger, FileHandler

WORKDIR = '/var/web'
LOGFILE = '/var/stratum/yiimpd.log'


def doCommand(cmd):
	try:
		ret = subprocess.check_output(cmd.split(), stderr=subprocess.STDOUT)
		logger.info(ret)
	except subprocess.CalledProcessError as e:
		logger.error(e.output)

def blocks():
	cmd='php -d max_execution_time=60 runconsole.php cronjob/runBlocks'
	while True:
		doCommand(cmd)
		time.sleep(20);	

def loop2():
	cmd='php -d max_execution_time=120 runconsole.php cronjob/runLoop2'
	while True:
		doCommand(cmd)
		time.sleep(60);	

def appmain():
	cmd='php -d max_execution_time=120 runconsole.php cronjob/run'
	while True:
		doCommand(cmd)
		time.sleep(90);	

def main(): 
	os.chdir(WORKDIR)
	th1 = threading.Thread(target=appmain)
	th2 = threading.Thread(target=loop2)
	th3 = threading.Thread(target=blocks)

	th1.start()
	th2.start()
	th3.start()


if __name__ == "__main__":

	logger = getLogger(__name__)
	logger.addHandler(FileHandler(LOGFILE))
	main()


