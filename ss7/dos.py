#!/usr/bin/env python

"""
Created on 8 Feb 2018

@author: loay
"""

import os
import sys
import time
from subprocess import *

import sigploit
import ss7main

purge_path = os.path.join(os.getcwd(), 'ss7/attacks/dos/prgms')


def purge():
    jar_file = 'PurgeMS.jar'

    try:
        purgeMS = check_call(['java', '-jar', os.path.join(purge_path, jar_file)])
        if purgeMS == 0:
            ds = raw_input('\nWould you like to go back to Fraud Menu? (y/n): ')
            if ds == 'y' or ds == 'yes':
                ss7main.ss7dos()
            elif ds == 'n' or ds == 'no':
                attack_menu = raw_input('Would you like to choose another attacks category? (y/n): ')
                if attack_menu == 'y' or attack_menu == 'yes':
                    ss7main.attacksMenu()
                elif attack_menu == 'n' or attack_menu == 'no':
                    main_menu = raw_input('Would you like to go back to the main menu? (y/exit): ')
                    if main_menu == 'y' or main_menu == 'yes':
                        sigploit.mainMenu()
                    elif main_menu == 'exit':
                        print 'TCAP End...'
                        sys.exit(0)

    except CalledProcessError as e:
        print "\033[31m[-]Error:\033[0m%s Failed to Launch, %s" %(jar_file, e.message)
        time.sleep(2)
        ss7main.ss7dos()
