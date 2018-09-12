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

sri_path = os.path.join(os.getcwd(), 'ss7/attacks/tracking/sri')
srism_path = os.path.join(os.getcwd(), 'ss7/attacks/tracking/srism')
psi_path = os.path.join(os.getcwd(), 'ss7/attacks/tracking/psi')
ati_path = os.path.join(os.getcwd(), 'ss7/attacks/tracking/ati')
srigprs_path = os.path.join(os.getcwd(), 'ss7/attacks/tracking/srigprs')


def sri():
    jar_file = 'SendRoutingInfo.jar'

    try:
        sendRoutingInfo = check_call(['java', '-jar', os.path.join(sri_path, jar_file)])
        if sendRoutingInfo == 0:
            lt = raw_input('\nWould you like to go back to LocationTracking Menu? (y/n): ')
            if lt == 'y' or lt == 'yes':
                ss7main.ss7tracking()
            elif lt == 'n' or lt == 'no':
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
        ss7main.ss7tracking()


def psi():
    jar_file = 'ProvideSubscriberInfo.jar'

    try:
        psi = check_call(['java', '-jar', os.path.join(psi_path, jar_file)])
        if psi == 0:
            lt = raw_input('\nWould you like to go back to LocationTracking Menu? (y/n): ')
            if lt == 'y' or lt == 'yes':
                ss7main.ss7tracking()
            elif lt == 'n' or lt == 'no':
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
       ss7main.ss7tracking()


def srism():
    jar_file = 'SendRoutingInfoforSM.jar'

    try:
        srism = check_call(['java', '-jar', os.path.join(srism_path, jar_file)])
        if srism == 0:
            lt = raw_input('\nWould you like to go back to LocationTracking Menu? (y/n): ')
            if lt == 'y' or lt == 'yes':
                ss7main.ss7tracking()
            elif lt == 'n' or lt == 'no':
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
        ss7main.ss7tracking()


def ati():
    jar_file = 'AnyTimeInterrogation.jar'

    try:
        ati = check_call(['java', '-jar', os.path.join(ati_path, jar_file)])
        if ati == 0:
            lt = raw_input('\nWould you like to go back to LocationTracking Menu? (y/n): ')
            if lt == 'y' or lt == 'yes':
                ss7main.ss7tracking()
            elif lt == 'n' or lt == 'no':
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
        ss7main.ss7tracking()

def srigprs():
    jar_file = 'SendRoutingInfoForGPRS.jar'

    try:
        srigprs = check_call(['java', '-jar', os.path.join(srigprs_path, jar_file)])
        if srigprs == 0:
            lt = raw_input('\nWould you like to go back to LocationTracking Menu? (y/n): ')
            if lt == 'y' or lt == 'yes':
                ss7main.ss7tracking()
            elif lt == 'n' or lt == 'no':
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
        ss7main.ss7tracking()
