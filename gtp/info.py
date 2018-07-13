#!/usr/bin/env python
'''
GTPv2 Information gathering attacks

Created on 18 June 2018

@author: loay
'''

import os
import sys
import time
import sigploit
import gtpmain
import time


from attacks.info import discover_gtp_nodes
from attacks.info import discover_teid_allocation



def nediscover():
	try:
		while True:
			choice = raw_input("\033[37m(\033[0m\033[2;31mnediscover\033[0m\033[37m)>\033[0m ")
			if choice == 'help' or choice == '?':
				gtpmain.helpmenu()
			elif choice == 'show options':
				gtpmain.showOptions(gtpmain.config_file,gtpmain.remote_net,gtpmain.listening,gtpmain.verbosity,gtpmain.output_file)
			elif 'set config' in choice:
				gtpmain.config_file = choice.split()[2]
			elif 'set target' in choice:
				gtpmain.remote_net = choice.split()[2]
			elif 'set listening' in choice:
				gtpmain.listening= choice.split()[2]
			elif 'set verbosity' in choice:
				gtpmain.verbosity= int(choice.split()[2])
			elif 'run' in choice:
				discover_gtp_nodes.main(gtpmain.config_file, gtpmain.remote_net, gtpmain.listening, gtpmain.verbosity,gtpmain.output_file)
			elif 'back' in choice:
				gtpmain.gtpattacksv2()
			elif 'exit' in choice:
				print '\nYou are now exiting SigPloit...'
				time.sleep(1)
				sys.exit(0)
			else:
				print '\033[31m[-]Error:\033[0m invalid command, choose one of the below commands\n'
				gtpmain.helpmenu()

	except Exception as e:
		print "\033[31m[-]Error:\033[0mGTP Nodes Discovery Failed to Launch, " + str(e)
		time.sleep(2)
		gtpmain.gtpattacksv2()
	


def teidiscover():
	try:
		while True:
			choice = raw_input("\033[37m(\033[0m\033[2;31mnediscover\033[0m\033[37m)>\033[0m ")
			if choice == 'help' or choice == '?':
				gtpmain.helpmenu()
			elif choice == 'show options':
				gtpmain.showOptions(gtpmain.config_file,gtpmain.remote_net,gtpmain.listening,gtpmain.verbosity,gtpmain.output_file)
			elif 'set config' in choice:
				gtpmain.config_file = choice.split()[2]
			elif 'set target' in choice:
				gtpmain.remote_net = choice.split()[2]
			elif 'set listening' in choice:
				gtpmain.listening= choice.split()[2]
			elif 'set verbosity' in choice:
				gtpmain.verbosity= int(choice.split()[2])
			elif 'run' in choice:
				discover_teid_allocation.main(gtpmain.config_file, gtpmain.remote_net, gtpmain.listening, gtpmain.verbosity,gtpmain.output_file )
			elif 'back' in choice:
				gtpmain.gtpattacksv2()
			elif 'exit' in choice:
				print '\nYou are now exiting SigPloit...'
				time.sleep(1)
				sys.exit(0)
			else:
				print '\033[31m[-]Error:\033[0m invalid command, choose one of the below commands\n'
				gtpmain.helpmenu()

	except Exception as e:
		print "\033[31m[-]Error:\033[0mGTP Nodes Discovery Failed to Launch, " + str(e)
		time.sleep(2)
		gtpmain.gtpattacksv2()

def teidpredict():

	script = "teid_sequence_predictability_index.py"
	print 'teidpredict'
