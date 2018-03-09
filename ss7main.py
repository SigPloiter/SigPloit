#!/usr/bin/env python
# encoding: utf-8
"""
SS7 main

@author:     Loay Abdelrazek

@copyright:  2018. All rights reserved.

@license:    MIT license
"""

import os
import time
import ss7.tracking
import ss7.fraud
import ss7.interception
import ss7.dos
import sigploit


def LocationTracking():
    os.system('clear')

    print " \033[31mLocation Tracking\033[0m ".center(105, "#")
    print " \033[34mSelect a Message from the below\033[0m ".center(105, "#")
    print
    print "   Message".rjust(10) + "\t\t\tDescription"
    print "   --------                    ------------"
    print "0) SendRoutingInfo".rjust(21) + "\t\tLocation Tracking, used to route calls could be blocked"
    print "1) ProvideSubsriberInfo".rjust(26) + "\tReliable Location Tracking"
    print "2) SendRoutingInfoForSM".rjust(26) + "\tReliable Location Tracking, if SMS home routing is not applied,should be run twice to check consistent replies"
    print "3) AnyTimeInterrogation".rjust(26) + "\tLocation Tracking, blocked by most of operators"
    print "4) SendRoutingInfoForGPRS".rjust(28) + "\tLocation tracking, used to route data, it will retrieve SGSN GT"

    print
    print "or type back to go back to Attacks Menu".rjust(42)

    choice = raw_input(
        "\033[37m(\033[0m\033[2;31mLocationTracking\033[0m\033[37m)>\033[0m ")

    if choice == "0":
        ss7.tracking.sri()
    elif choice == "1":
        ss7.tracking.psi()
    elif choice == "2":
        ss7.tracking.srism()
    elif choice == "3":
        ss7.tracking.ati()
    elif choice == "4":
        ss7.tracking.srigprs()
    elif choice == "back":
        attacksMenu()
    else:
        print '\n\033[31m[-]Error:\033[0m Please Enter a Valid Choice (0 - 4)'
        time.sleep(1.5)
        LocationTracking()


def Interception():
    os.system('clear')

    print " \033[31mInterception\033[0m ".center(105, "#")
    print " \033[34mSelect a Message from the below\033[0m ".center(105, "#")
    print
    print "   Message".rjust(10) + "\t\t\t\tDescription"
    print "   --------                             -----------"
    print "0) UpdateLocation".rjust(20) + "\t\t\tStealthy SMS Interception"

    print
    print "or type back to go back to Attacks Menu".rjust(42)

    choice = raw_input(
        "\033[37m(\033[0m\033[2;31mInterception\033[0m\033[37m)>\033[0m ")

    if choice == "0":
        ss7.interception.ul()

    elif choice == "back":
        attacksMenu()
    else:
        print '\n\033[31m[-]Error:\033[0m Please Enter a Valid Choice (0)'
        time.sleep(1.5)
        Interception()


def Fraud():
    os.system('clear')

    print " \033[31mFraud\033[0m ".center(105, "#")
    print " \033[34mSelect a Message from the below\033[0m ".center(105, "#")
    print
    print "   Message".rjust(10) + "\t\t\t\tDescription"
    print "   --------                            ------------"
    print "0) SendIMSI".rjust(14) + "\t\t\t\tRetrieving IMSI of a subscriber"
    print "1) MTForwardSMS".rjust(18) + "\t\t\tSMS Phishing and Spoofing"

    print
    print "or type back to go back to Attacks Menu".rjust(42)

    choice = raw_input(
        "\033[37m(\033[0m\033[2;31mFraud\033[0m\033[37m)>\033[0m ")

    if choice == "0":
        ss7.fraud.simsi()
    elif choice == "1":
        ss7.fraud.mtsms()
    elif choice == "back":
        attacksMenu()
    else:
        print '\n\033[31m[-]Error:\033[0m Please Enter a Valid Choice (0-1)'
        time.sleep(1.5)
        Fraud()


def DoS():
    os.system('clear')

    print " \033[31mDenial of Service\033[0m ".center(105, "#")
    print " \033[34mSelect a Message from the below\033[0m ".center(105, "#")
    print
    print "   Message".rjust(10) + "\t\t\t\tDescription"
    print "   --------                            ------------"
    print "0) PurgeMS-Subscriber DoS".rjust(28) + "\t\t Mass DoS attack on Subscribers to take them off network"

    print
    print "or type back to go back to Attacks Menu".rjust(42)

    choice = raw_input(
        "\033[37m(\033[0m\033[2;31mDoS\033[0m\033[37m)>\033[0m ")

    if choice == "0":
        ss7.dos.purge()
    elif choice == "back":
        attacksMenu()
    else:
        print '\n\033[31m[-]Error:\033[0m Please Enter a Valid Choice (0)'
        time.sleep(1.5)
        DoS()


def attacksMenu():
    os.system('clear')

    print " \033[34mChoose From the Below Attack Categories\033[0m ".center(105, "#")
    print
    print "0) Location Tracking".rjust(23)
    print "1) Call and SMS Interception".rjust(31)
    print "2) Fraud & Info Gathering".rjust(28)
    print "3) DoS".rjust(9)
    print
    print "or type back to return to the main menu".rjust(42)
    print

    choice = raw_input(
        "\033[37m(\033[0m\033[2;31mAttacks\033[0m\033[37m)>\033[0m ")

    if choice == "0":
        LocationTracking()

    elif choice == "1":
        Interception()

    elif choice == "2":
        Fraud()

    elif choice == "3":
        DoS()

    elif choice == "back":
        sigploit.mainMenu()
    else:
        print '\n\033[31m[-]Error:\033[0m Please Enter a Valid Choice (0 - 3)'
        time.sleep(1.5)
        attacksMenu()
