#!/usr/bin/env python
'''
SigPloit Main

Created on 1 Feb 2018

@author: loay

@license:    MIT license
'''

import sys
import os
import signal
import time
from ss7.tracking import *
from ss7.interception import *
from ss7.fraud import *
from ss7.dos import *
from ss7main import *
from gtpmain import *
from gtp import *
from colorama import init
from termcolor import cprint
from pyfiglet import figlet_format


def banner(word):
    letterforms = '''\
       |       |       |       |       |       |       | |
  XXX  |  XXX  |  XXX  |   X   |       |  XXX  |  XXX  |!|
  X  X |  X  X |  X  X |       |       |       |       |"|
  X X  |  X X  |XXXXXXX|  X X  |XXXXXXX|  X X  |  X X  |#|
 XXXXX |X  X  X|X  X   | XXXXX |   X  X|X  X  X| XXXXX |$|
XXX   X|X X  X |XXX X  |   X   |  X XXX| X  X X|X   XXX|%|
  XX   | X  X  |  XX   | XXX   |X   X X|X    X | XXX  X|&|
  XXX  |  XXX  |   X   |  X    |       |       |       |'|
   XX  |  X    | X     | X     | X     |  X    |   XX  |(|
  XX   |    X  |     X |     X |     X |    X  |  XX   |)|
       | X   X |  X X  |XXXXXXX|  X X  | X   X |       |*|
       |   X   |   X   | XXXXX |   X   |   X   |       |+|
       |       |       |  XXX  |  XXX  |   X   |  X    |,|
       |       |       | XXXXX |       |       |       |-|
       |       |       |       |  XXX  |  XXX  |  XXX  |.|
      X|     X |    X  |   X   |  X    | X     |X      |/|
  XXX  | X   X |X     X|X     X|X     X| X   X |  XXX  |0|
   X   |  XX   | X X   |   X   |   X   |   X   | XXXXX |1|
 XXXXX |X     X|      X| XXXXX |X      |X      |XXXXXXX|2|
 XXXXX |X     X|      X| XXXXX |      X|X     X| XXXXX |3|
X      |X    X |X    X |X    X |XXXXXXX|     X |     X |4|
XXXXXXX|X      |X      |XXXXXX |      X|X     X| XXXXX |5|
 XXXXX |X     X|X      |XXXXXX |X     X|X     X| XXXXX |6|
XXXXXX |X    X |    X  |   X   |  X    |  X    |  X    |7|
 XXXXX |X     X|X     X| XXXXX |X     X|X     X| XXXXX |8|
 XXXXX |X     X|X     X| XXXXXX|      X|X     X| XXXXX |9|
   X   |  XXX  |   X   |       |   X   |  XXX  |   X   |:|
  XXX  |  XXX  |       |  XXX  |  XXX  |   X   |  X    |;|
    X  |   X   |  X    | X     |  X    |   X   |    X  |<|
       |       |XXXXXXX|       |XXXXXXX|       |       |=|
  X    |   X   |    X  |     X |    X  |   X   |  X    |>|
 XXXXX |X     X|      X|   XXX |   X   |       |   X   |?|
 XXXXX |X     X|X XXX X|X XXX X|X XXXX |X      | XXXXX |@|
   X   |  X X  | X   X |X     X|XXXXXXX|X     X|X     X|A|
XXXXXX |X     X|X     X|XXXXXX |X     X|X     X|XXXXXX |B|
 XXXXX |X     X|X      |X      |X      |X     X| XXXXX |C|
XXXXXX |X     X|X     X|X     X|X     X|X     X|XXXXXX |D|
XXXXXXX|X      |X      |XXXXX  |X      |X      |XXXXXXX|E|
XXXXXXX|X      |X      |XXXXX  |X      |X      |X      |F|
 21.45 |6     8|7      |2   lat|x1    x5|9     4| 31.74 |G|
X     X|X     X|X     X|XXXXXXX|X     X|X     X|X     X|H|
  XXX  |   X   |   X   |   X   |   X   |   X   |  XXX  |I|
      X|      X|      X|      X|X     X|X     X| XXXXX |J|
X    X |X   X  |X  X   |XXX    |X  X   |X   X  |X    X |K|
X      |X      |X      |X      |X      |X      |XXXXXXX|L|
X     X|XX   XX|X X X X|X  X  X|X     X|X     X|X     X|M|
X     X|XX    X|X X   X|X  X  X|X   X X|X    XX|X     X|N|
XXXXXXX|X     X|X     X|X     X|X     X|X     X|XXXXXXX|O|
XXXXXX |X     X|X     X|XXXXXX |X      |X      |X      |P|
 XXXXX |X     X|X     X|X     X|X   X X|X    X | XXXX X|Q|
XXXXXX |X     X|X     X|XXXXXX |X   X  |X    X |X     X|R|
 _IMSI |0x1  GT|PC     | _IMEI |     CI|Kc  421| _HLR_ |S|
XXXXXXX|   X   |   X   |   X   |   X   |   X   |   X   |T|
X     X|X     X|X     X|X     X|X     X|X     X| XXXXX |U|
X     X|X     X|X     X|X     X| X   X |  X X  |   X   |V|
X     X|X  X  X|X  X  X|X  X  X|X  X  X|X  X  X| XX XX |W|
X     X| X   X |  X X  |   X   |  X X  | X   X |X     X|X|
X     X| X   X |  X X  |   X   |   X   |   X   |   X   |Y|
XXXXXXX|     X |    X  |   X   |  X    | X     |XXXXXXX|Z|
 XXXXX | X     | X     | X     | X     | X     | XXXXX |[|
X      | X     |  X    |   X   |    X  |     X |      X|\|
 XXXXX |     X |     X |     X |     X |     X | XXXXX |]|
   X   |  X X  | X   X |       |       |       |       |^|
       |       |       |       |       |       |XXXXXXX|_|
       |  XXX  |  XXX  |   X   |    X  |       |       |`|
       |   XX  |  X  X | X    X| XXXXXX| X    X| X    X|a|
       | XXXXX | X    X| XXXXX | X    X| X    X| XXXXX |b|
       |  XXXX | X    X| X     | X     | X    X|  XXXX |c|
       | XXXXX | X    X| X    X| X    X| X    X| XXXXX |d|
       | XXXXXX| X     | XXXXX | X     | X     | XXXXXX|e|
       | XXXXXX| X     | XXXXX | X     | X     | X     |f|
       |  XXXX | X    X| X     | X  gtp| X    X|  XXXX |g|
       | X    X| X    X| XXXXXX| X    X| X    X| X    X|h|
       |  E    |  n    |  C    |  r    |  P    |  T    |i|
       |      X|      X|      X|      X| X    X|  XXXX |j|
       | X    X| X   X | XXXX  | X  X  | X   X | X    X|k|
       | GT    | PC    | x7    | x6    | x8    | Fraud |l|
       | X    X| XX  XX| X XX X| X    X| X    X| X    X|m|
       | X    X| XX   X| X X  X| X  X X| X   XX| X    X|n|
       |  SGSN | X    X| X    X| X    X| X    X|  gGsN |o|
       | Track | 6    8| s    i|credit | Kc    | G     |p|
       |  XXXX | X    X| X    X| X  X X| X   X |  XXX X|q|
       | XXXXX | X    X| X    X| XXXXX | X   X | X    X|r|
       |  XXXX | X     |  XXXX |      X| X    X|  XXXX |s|
       |--USIM-- |   x0  |   x2  |   x3  |   x8  |   x6  |t|
       | X    X| X    X| X    X| X    X| X    X|  XXXX |u|
       | X    X| X    X| X    X| X    X|  X  X |   XX  |v|
       | X    X| X    X| X    X| X XX X| XX  XX| X    X|w|
       | X    X|  X  X |   XX  |   XX  |  X  X | X    X|x|
       |  X   X|   X X |    X  |    X  |    X  |    X  |y|
       | XXXXXX|     X |    X  |   X   |  X    | XXXXXX|z|
  XXX  | X     | X     |XX     | X     | X     |  XXX  |{|
   X   |   X   |   X   |       |   X   |   X   |   X   |||
  XXX  |     X |     X |     XX|     X |     X |  XXX  |}|
 XX    |X  X  X|    XX |       |       |       |       |~|
'''.splitlines()

    table = {}
    for form in letterforms:
        if '|' in form:
            table[form[-2]] = form[:-3].split('|')

    ROWS = len(table.values()[0])

    for row in range(ROWS):
        for c in word:
            print (table[c][row]),
        print
    print



def mainMenu():
    os.system('clear')

    banner('SigPloit')
    print "\033[33m[-][-]\033[0m\t\tSignaling Exploitation Framework\t\033[33m [-][-]\033[0m"
    print "\033[33m[-][-]\033[0m\t\t\tVersion:\033[31mBETA 1.1\033[0m\t\t\033[33m [-][-]\033[0m"
    print "\033[33m[-][-]\033[0m\t\tAuthor:\033[32mLoay AbdelRazek(@sigploit)\033[0m\t\033[33m [-][-]\033[0m\n"
    print
    print "Contributors:"

    print "\t\033[31mRosalia D'Alessandro\033[0m"
    print "\t\033[31mIlario Dal Grande\033[0m"
    print
    print
    print
    print
    print
    print "   Module".rjust(10) + "\t\t\tDescription"
    print "   --------                --------------------"
    print "0) SS7".rjust(8) + "\t\t2G/3G Voice and SMS attacks"
    print "1) GTP".rjust(8) + "\t\t3G/4G Data attacks"
    print "2) Diameter".rjust(13) + "\t\t4G Data attacks"
    print "3) SIP".rjust(8) + "\t\t4G IMS attacks"

    print
    print "or quit to exit SigPloit\n".rjust(28)

    choice = raw_input("\033[34msig\033[0m\033[37m>\033[0m ")

    if choice == "0":
        os.system('clear')
        ss7main.attacksMenu()

    elif choice == "1":
        os.system('clear')
        prep()
    elif choice == "2":
        print "\n\033[34m[*]\033[0mDiameter will be updated in version 3 release.."
        print "\033[34m[*]\033[0mGoing back to Main Menu"
        time.sleep(2)
        mainMenu()
    elif choice == "3":
        print "\n\033[34m[*]\033[0mSIP will be updated in version 4 release.."
        print "\033[34m[*]\033[0mGoing back to Main Menu"
        time.sleep(2)
        mainMenu()
    elif choice == "quit" or choice == "exit":
        print '\nYou are now exiting SigPloit...'
        time.sleep(1)
        sys.exit(0)
    else:
        print '\n\033[31m[-]Error:\033[0m Please Enter a Valid Choice (0 - 3)'
        time.sleep(2)
        mainMenu()


def signal_handler(signal, frame):
    print
    print '\nYou are now exiting SigPloit...'
    time.sleep(1)
    sys.exit(0)


signal.signal(signal.SIGINT, signal_handler)

if __name__ == '__main__':
    mainMenu()

if __name__ == '__sigploit__':
    ss7tracking()
    ss7interception()
    ss7fraud()
    ss7dos()
    attacksMenu()
    prep()
    gtpattacksv2()
    gtpinfo()
    mainMenu()
