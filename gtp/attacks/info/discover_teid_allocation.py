#!/usr/bin/env python
# encoding: utf-8
#      discover_teid_allocation.py
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
from gtp_v2_core.utilities.configuration_parser import parseConfigs
from gtp_v2_core.commons.gtp_v2_commons import GTPmessageTypeStr
from commons.message_handler import MessageHandler

from commons.globals import message_queue




GTP_PORT = 2123
DEFAULT_MSG_FREQ = 20
DEFAULT_SLEEPTIME = 1
DEBUG = 0


## 
## @brief      Main file to execute the script.
## 
## This file can be used to understand how TEID are created by the target nodes.
## Example configuration file: TeidAllocationDiscover.cnf

def main(config_file, target, listening=True, verbose = 2,output_file=""):
    

    lstn = None
    try:

        listening_mode = listening
        is_verbose = verbose
         

        msg_freq = DEFAULT_SLEEPTIME
        remote_net = target
        sleep_time = DEFAULT_SLEEPTIME
      
        if listening_mode and  remote_net == None:
            print "\033[33m[!]\033[0m remote network (e.g. 10.0.0.0/24, 10.0.0.1/32) is required"
            return
        
        # MAIN BODY #
        if sys.argv[0] == "" :
            print "\033[31m[-]Error:\033[0m missed config file"
            return         
# 
#         if opts.num_msg is None or opts.num_msg == "" or int(opts.num_msg) == 0 :
#             print "Error: missed num of messages to send"
#             return 
          
        config = parseConfigs(config_file)
 
        msgs = config.get_unpacked_messages()

       
        lstn = MessageHandler(messages = msgs, peer = remote_net, 
                              isVerbose = is_verbose, listening_mode = listening_mode,
                              msgs_freq = msg_freq, wait_time = sleep_time)  
        if lstn : 
            lstn.daemon = True
            lstn.start()
            lstn.join()
            lstn.stop()
            
        print "\033[34m[*]\033[0m Sent %d GTPV2 messages"%(len(msgs))
        
        fd = None
        if not listening_mode :
            return

        if output_file != "" :
            fd = open(output_file, 'w')
        printed = False              
        for key, value in message_queue.items():
            for k,v in value.items():              
                for i in v :
                    if i['reply'] == 1:
                        if not printed :
                            print "\033[32m[+]\033[0m %s implements a GTP v2 stack"%key
                            printed = True
                        print "\033[32m[+]\033[0m%s : < local teid %s, remote teid %s>"%(
                            GTPmessageTypeStr[k], format(i['local_teid'], '#08X'), 
                            i['remote_teid'])    
                        if fd :
                            fd.write("%s implements a GTP v2 stack"%key)   
                            fd.write("for %d msg type created teid %s"%(k, i['remote_teid']))                        
    except Exception, e:
        print "\033[31m[-]Error:\033[0m %s"%str(e)
        if lstn : 
            lstn.stop()        
        return 2

