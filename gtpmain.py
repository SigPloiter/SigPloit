#!/usr/bin/env python
'''
GTP Main

Created on 18 June 2018

@author: loay
'''
import os
import time
import sys
import gtp.info
import gtp.fraud
import sigploit


from gtp.gtp_v2_core.utilities.configuration_parser import parseConfigs

config_file= ''
remote_net =''
listening = True
verbosity = 2
output_file ='results.csv'

def gtpinfo():
    os.system('clear')
    print " \033[31mInformation Gathering\033[0m ".center(105, "#")
    print " \033[34mSelect an Attack from the below\033[0m ".center(105, "#")
    print
    print "   Attacks".rjust(10) + "\t\t\t\tDescription"
    print "   --------                             ------------"
    print "0) GTP Nodes Discovery".rjust(25) + "\t\tNE Discovery, using: EchoRequest,CreateSession,DeleteSession or DeleteBearer Messages"
    print "1) TEID Allocation Discovery".rjust(31) + "\t\tTEID Discovery, using: CreateSession,ModifyBearer or CreateBearer Messages"

    print
    print "or type back to go back to Attacks Menu".rjust(42)

    choice = raw_input("\033[37m(\033[0m\033[2;31minfo\033[0m\033[37m)>\033[0m ")

    if choice == "0":
        gtp.info.nediscover()
    elif choice == "1":
        gtp.info.teidiscover()
    elif choice == "back":
  		gtpattacksv2()
    else:
        print '\n\033[31m[-]Error:\033[0m Please Enter a Valid Choice (0-1)'
        time.sleep(1.5)
        gtpinfo()

def gtpfraud():
    os.system('clear')
    print " \033[31mFraud\033[0m ".center(105, "#")
    print " \033[34mSelect an Attack from the below\033[0m ".center(105, "#")
    print
    print "   Attacks".rjust(10) + "\t\t\t\tDescription"
    print "   --------                             ------------"
    print "0) Tunnel Hijack".rjust(19) + "\t\tTEID Hijack, using: ModifyBearerRequest Message, TunnelHijack.cnf"

    print
    print "or type back to go back to Attacks Menu".rjust(42)

    choice = raw_input("\033[37m(\033[0m\033[2;31minfo\033[0m\033[37m)>\033[0m ")

    if choice == "0":
        gtp.fraud.thijack()
    elif choice == "back":
        gtpattacksv2()
    else:
        print '\n\033[31m[-]Error:\033[0m Please Enter a Valid Choice (0)'
        time.sleep(1.5)
        gtpfraud()



def gtpattacksv2():
    os.system('clear')

    print " \033[34mChoose From the Below Attack Categories\033[0m ".center(105, "#")
    print
    print "0) Information Gathering".rjust(27)
    print "1) Fraud".rjust(11)
    print
    print "or type back to return to the main menu".rjust(42)
    print

    choice = raw_input(
        "\033[37m(\033[0m\033[2;31mattacks\033[0m\033[37m)>\033[0m ")

    if choice == "0":
        gtpinfo()
    elif choice == "1":
        gtpfraud()
    elif choice == 'back':
    	sigploit.mainMenu()
    else:
        print '\n\033[31m[-]Error:\033[0m Please Enter a Valid Choice (0-1)'
        time.sleep(1.5)
        gtpattacksv2()

def showOptions(config_file='', remote_net='', listening=True, verbosity=2, output_file='results.csv'):

    print('\n     Option                    \t\t\t\t\tValue')
    print('     --------                                                   ------')
    print('     \033[34mconfig\033[0m     {:<15s} \t\t\t\033[31m%s\033[0m'.format('path to configuration file')) %config_file
    print('     \033[34mtarget\033[0m     {:<15s} \t\033[31m%s\033[0m'.format('example: 10.10.10.1/32 or 10.10.10.0/24')) %remote_net
    print('     \033[34mlistening\033[0m  {:<15s} \t\033[31m%s\033[0m'.format('accepting replies from target, default: True')) %listening
    print('     \033[34mverbosity\033[0m  {:<15s} \t\t\t\033[31m%d\033[0m '.format('versbosity level, default: 2')) %verbosity
    print('     \033[34moutput\033[0m     {:<15s} \t\t\033[31m%s\033[0m\n '.format('output file, default: result.csv')) %output_file
   

def helpmenu():

    print('\n     Command                      Description')
    print('     ---------                   ------------')
    print('     \033[34mshow options\033[0m                display required options to run attack')
    print('     \033[34mset\033[0m                         set a value for an option')
    print("     \033[34mrun\033[0m                         run the exploit")
    print("     \033[34mhelp\033[0m                        display this menu")
    print("     \033[34mback\033[0m                        back to GTP attacks")
    print("     \033[34mexit\033[0m                        exit SigPloit\n")
  

def prep():
    print
    print "   Module".rjust(10) + "\t\tDescription"
    print "   --------             ------------"
    print "0) GTPv1".rjust(8) + "\t\t3G Data attacks"
    print "1) GTPv2".rjust(8) + "\t\t4G Data attacks"
    print
    print "or type back to go back to Main Menu".rjust(39)

    choice = raw_input("\033[34mgtp\033[0m\033[37m>\033[0m ")

    if choice == "0":
        print "\n\033[34m[*]\033[0mGTPv1 will be updated in version 2.1 release.."
        print "\033[34m[*]\033[0mGoing back to GTP Menu"
        time.sleep(2)
        os.system('clear')
        prep()

    elif choice == "1":
        gtpattacksv2()

    elif choice == "back":
        sigploit.mainMenu()

