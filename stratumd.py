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

ALGOS = ['neo']
LOGFILE = '/var/stratum/stratumd.log'

STRATUM_DIR = '/var/stratum'



def doCommand(cmd):
	try:
		ret = subprocess.check_output(cmd.split(), stderr=subprocess.STDOUT)
		logger.info(ret)
	except subprocess.CalledProcessError as e:
		logger.error(e.output)

def stratum_kicker(algo):
	cmds = [STRATUM_DIR+'/stratum', 'config/'+algo]
	while True:
		try:
			ret = subprocess.check_output(cmds, cwd=STRATUM_DIR, stderr=subprocess.STDOUT) 
			logger.info(ret)
		except subprocess.CalledProcessError as e:
			logger.error(e.output)
		time.sleep(15)

def main(): 
	for algo in ALGOS:
		tha = threading.Thread(target=stratum_kicker, args=[algo])
		tha.start()


if __name__ == "__main__":

	logger = getLogger(__name__)
	logger.addHandler(FileHandler(LOGFILE))
	main()


