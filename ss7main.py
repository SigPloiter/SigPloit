#!/usr/bin/env python
# encoding: utf-8
'''
SS7 main 

@author:     Loay Abdelrazek

@copyright:  2018. All rights reserved.

@license:    MIT license
'''

import os
import time
import ss7.tracking
import ss7.fraud
import ss7.interception
import ss7.dos
import sigploit



def cleaner():

    os.system("rm -f *.xml")

def ss7tracking():
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
        "\033[37m(\033[0m\033[2;31mtracking\033[0m\033[37m)>\033[0m ")

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
        ss7tracking()


def ss7interception():
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
        "\033[37m(\033[0m\033[2;31minterception\033[0m\033[37m)>\033[0m ")

    if choice == "0":
        ss7.interception.ul()

    elif choice == "back":
        attacksMenu()
    else:
        print '\n\033[31m[-]Error:\033[0m Please Enter a Valid Choice (0)'
        time.sleep(1.5)
        ss7interception()


def ss7fraud():
    os.system('clear')

    print " \033[31mFraud & Info\033[0m ".center(105, "#")
    print " \033[34mSelect a Message from the below\033[0m ".center(105, "#")
    print
    print "   Message".rjust(10) + "\t\t\t\tDescription"
    print "   --------                            ------------"
    print "0) SendIMSI".rjust(14) + "\t\t\t\tRetrieving IMSI of a subscriber"
    print "1) MTForwardSMS".rjust(18) + "\t\t\tSMS Phishing and Spoofing"
    print "2) InsertSubscriberData".rjust(26) + "\t\tSubscriber Profile Maniuplation"
    print "3) SendAuthenticationInfo".rjust(28) + "\t\tSubscriber Authentication Vectors retrieval"

    print
    print "or type back to go back to Attacks Menu".rjust(42)

    choice = raw_input(
        "\033[37m(\033[0m\033[2;31mfraud\033[0m\033[37m)>\033[0m ")

    if choice == "0":
        ss7.fraud.simsi()
    elif choice == "1":
        ss7.fraud.mtsms()
    elif choice == "2":
        ss7.fraud.isd()
    elif choice == "3":
        ss7.fraud.sai()
    elif choice == "back":
        attacksMenu()
    else:
        print '\n\033[31m[-]Error:\033[0m Please Enter a Valid Choice (0-3)'
        time.sleep(1.5)
        ss7fraud()


def ss7dos():
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
        "\033[37m(\033[0m\033[2;31mdos\033[0m\033[37m)>\033[0m ")

    if choice == "0":
        ss7.dos.purge()
    elif choice == "back":
        attacksMenu()
    else:
        print '\n\033[31m[-]Error:\033[0m Please Enter a Valid Choice (0)'
        time.sleep(1.5)
        ss7dos()


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
        "\033[37m(\033[0m\033[2;31mattacks\033[0m\033[37m)>\033[0m ")

    if choice == "0":
        ss7tracking()

    elif choice == "1":
        ss7interception()

    elif choice == "2":
        ss7fraud()

    elif choice == "3":
        ss7dos()

    elif choice == "back":
        sigploit.mainMenu()
    else:
        print '\n\033[31m[-]Error:\033[0m Please Enter a Valid Choice (0 - 3)'
        time.sleep(1.5)
        attacksMenu()
