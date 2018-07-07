#!/usr/bin/env python

"""
Created on 1 Feb 2018

@author: loay
"""

import os
import sys
import time
from subprocess import *

import sigploit
import ss7main

ul_path = os.path.join(os.getcwd(), 'ss7/attacks/interception/ul')


def ul():
    jar_file = 'UpdateLocation.jar'

    try:
        updateLocation = check_call(['java', '-jar', os.path.join(ul_path, jar_file)])
        if updateLocation == 0:
            it = raw_input('\nWould you like to go back to Interception Menu? (y/n): ')
            if it == 'y' or it == 'yes':
                ss7main.ss7interception()
            elif it == 'n' or it == 'no':
                attack_menu = raw_input('Would you like to choose another attacks category? (y/n): ')
                if attack_menu == 'y' or attack_menu == 'yes':
                    ss7main.attacksMenu()
                elif attack_menu == 'n' or attack_menu == 'no':
                    main_menu = raw_input('Would you like to go back to the main menu? (y/exit): ')
                    if main_menu == 'y' or main_menu == 'yes':
                        sigploit.mainMenu()
                    elif main_menu == 'exit':
                        print 'TCAP End...'
                        time.sleep(1)
                        sys.exit(0)

    except CalledProcessError as e:
        print "\033[31m[-]Error:\033[0m%s Failed to Launch, %s" %(jar_file, e.message)
        time.sleep(2)
        ss7main.ss7interception()
