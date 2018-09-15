#!/usr/bin/env python
'''
GTPv2 Fraud attacks

Created on 13 Sep 2018

@author: loay
'''

import os
import sys
import time
import sigploit
import gtpmain
import time


from attacks.fraud import tunnel_hijacking




def thijack():
	try:
		while True:
			choice = raw_input("\033[37m(\033[0m\033[2;31mthijack\033[0m\033[37m)>\033[0m ")
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
				tunnel_hijacking.main(gtpmain.config_file, gtpmain.remote_net, gtpmain.listening, gtpmain.verbosity,gtpmain.output_file)
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
		print "\033[31m[-]Error:\033[0m Tunnel Hijacking Failed to Launch, %s" %str(e)
		time.sleep(2)
		gtpmain.gtpattacksv2()
	
