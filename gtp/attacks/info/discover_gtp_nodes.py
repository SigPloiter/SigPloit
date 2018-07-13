#!/usr/bin/env python
# encoding: utf-8
#      discover_gtp_nodes.py
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
from commons.message_handler import MessageHandler
from commons.globals import message_queue


DEFAULT_MSG_FREQ = 20
DEFAULT_SLEEPTIME = 1
DEBUG = 0


## 
## @brief      Main file to execute the script.
## 
## This file can discover gtp nodes sending several messages like:
## - echo requests
## - create session request
## - delete session request with random TEIDs or TEID set to zero
## ¯ delete bearer request  
## 
## Example configuration file: EchoRequest.cnf, DeleteSession.cnf, DeleteBearer.cnf

def main(config_file, target, listening=True, verbose = 2, output_file='results.csv'):

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
  
        config = parseConfigs(config_file)
    
 
        msgs = config.get_unpacked_messages()
        port = config.get_gtp_port()
        
        lstn = MessageHandler(messages = msgs, peer = remote_net, 
                              isVerbose = is_verbose, 
                              listening_mode = listening_mode,
                              msgs_freq = msg_freq, wait_time = sleep_time,
                              port = port)  
        
        if lstn : 
            lstn.daemon = True
            lstn.start()
            lstn.join()
            lstn.stop()
        print "\033[34m[*]\033[0m Sent %d GTPV2 messages"%(len(message_queue))
        if not listening_mode :
            return
        gtp_nodes = []

        if output_file != "" :
            fd = open(output_file, 'w')

        for key, value in message_queue.items():
            for k,v in value.items():               
                for i in v :
                    if i['reply'] == 1:
                        gtp_nodes.append(key)
                        print "\033[32m[+]\033[0m %s implements a GTP v2 stack"%key
                        if fd :
                            fd.write("%s implements a GTP v2 stack"%key) 
                        break

        num_gtp_nodes = len(gtp_nodes)
        if num_gtp_nodes > 0 :
            print "\033[32m[+]\033[0m Found in total %d targets implemeting a GTP v2 stack "%num_gtp_nodes
            print "\033[32m[+]\033[0m List of discovered GTPv2 nodes"
            for n in gtp_nodes :
                print n,"\n"
        else :
            print "\033[31m[-]\033[0m Not found targets implemeting a GTP v2 stack"        
    except Exception, e:
        print "\033[31m[-]Error:\033[0m %s"%str(e)

        if lstn : 
            lstn.stop()        
        return 2

