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

simsi_path = os.path.join(os.getcwd(), 'ss7/attacks/fraud/simsi')
mtsms_path = os.path.join(os.getcwd(), 'ss7/attacks/fraud/mtsms')
cl_path = os.path.join(os.getcwd(), 'ss7/attacks/fraud/cl')


def simsi():
    jar_file = 'SendIMSI.jar'

    try:
        sendIMSI = check_call(['java', '-jar', os.path.join(simsi_path, jar_file)])
        if sendIMSI == 0:
            fr = raw_input('\nWould you like to go back to Fraud Menu? (y/n): ')
            if fr == 'y' or fr == 'yes':
                ss7main.Fraud()
            elif fr == 'n' or fr == 'no':
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
        print "\033[31m[-]Error:\033[0mSendIMSI Failed to Launch, " + str(e)
        time.sleep(2)
        ss7main.Fraud()


def mtsms():
    jar_file = 'MTForwardSMS.jar'

    try:
        mtForwardSMS = check_call(['java', '-jar', os.path.join(mtsms_path, jar_file)])
        if mtForwardSMS == 0:
            fr = raw_input('\nWould you like to go back to Fraud Menu? (y/n): ')
            if fr == 'y' or fr == 'yes':
                ss7main.Fraud()
            elif fr == 'n' or fr == 'no':
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
        print "\033[31m[-]Error:\033[0mMTForwardSMS Failed to Launch, " + str(e)
        time.sleep(2)
        ss7main.Fraud()


def cl():
    jar_file = 'CancelLocation.jar'

    try:
        cancelLocation = check_call(['java', '-jar', os.path.join(cl_path, jar_file)])
        if cancelLocation == 0:
            fr = raw_input('\nWould you like to go back to Fraud Menu? (y/n): ')
            if fr == 'y' or fr == 'yes':
                ss7main.Fraud()
            elif fr == 'n' or fr == 'no':
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
        print "\033[31m[-]Error:\033[0mCancelLocation Failed to Launch, " + str(e)
        time.sleep(2)
        ss7main.Fraud()
