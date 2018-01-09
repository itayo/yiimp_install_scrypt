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
import daemon
from logging import getLogger, FileHandler

algos = ['lyra2v2', 'neo']
workdir = '/var/web'
logfile = '/var/stratum/yiimpd.log'

stratum_dir = '/var/stratum'


def log(label, msg):
	logger = getLogger(__name__ + ':' + msg)
	logger.addHandler(FileHandler(logfile))
	logger.info(msg)

def doCommand(cmd, label):
	try:
		ret = subprocess.check_output(cmd.split(), stderr=subprocess.STDOUT)
		log(label, ret)
	except subprocess.CalledProcessError as e:
		log(label, e.output)

def blocks():
	cmd='php -d max_execution_time=60 runconsole.php cronjob/runBlocks'
	while True:
		doCommand(cmd, 'blocks')
		time.sleep(20);	

def loop2():
	cmd='php -d max_execution_time=120 runconsole.php cronjob/runLoop2'
	while True:
		doCommand(cmd, 'loop2')
		time.sleep(60);	

def appmain():
	cmd='php -d max_execution_time=120 runconsole.php cronjob/run'
	while True:
		doCommand(cmd, 'main')
		time.sleep(90);	

def stratum_kicker(algo):
	cmds = [stratum_dir+'/stratum', 'config/'+algo]
	while True:
		try:
			subprocess.check_output(cmds, cwd=stratum_dir, stderr=subprocess.STDOUT) 
		except subprocess.CalledProcessError as e:
			log('stratum:'+algo, e.output)
		time.sleep(15)

def main(): 
	os.chdir(workdir)
	th1 = threading.Thread(target=appmain)
	th2 = threading.Thread(target=loop2)
	th3 = threading.Thread(target=blocks)

	th1.start()
	th2.start()
	th3.start()

	for algo in algos:
		tha = threading.Thread(target=stratum_kicker, args=[algo])
		tha.start()


if __name__ == "__main__":

	main()


