#!/usr/bin/env python
# encoding: utf-8
#       main.py
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

import sys
import os

from optparse import OptionParser
from utilities.configuration_parser import *
from utilities.gtp_v2_server_listener import ServerListener
from utilities.gtpv2_sender_listener import SenderListener
__all__ = []
__version__ = 0.1

GTP_PORT = 2123
DEFAULT_MSG_FREQ = 20
DEFAULT_SLEEPTIME = 1
DEBUG = 0


##
## GTP-C v2 BASE
## 
## @brief      Main file to execute the script.
## 
## This file can be executed to test the gtp-c v2 messages implemented in the gtp_v2_core 
#  package
## 
## Use the -h option to enter the help menu and determine what to do.
## 
## Basic usage examples:
##      * $ python main.py -v -c conf_file.cnf [-c conf2.cnf ...] -r <remote ip> 
#            act as a client connecting to <remote-host-ip>
##      
##      * $ python main.py -sv  -c conf_file.cnf [-c conf2.cnf ...] -r <remote ip> -l <local ip>
##      
##           act as a server listening on <local ip> and accepting replies from <remote-host-ip>
##

def main(argv=None):
    '''Command line options.'''

    program_name = os.path.basename(sys.argv[0])
    program_version = "v0.1"

    program_version_string = '%%prog %s' % (program_version)

    program_license = "Copyright 2018 Rosalia d'Alessandro\
                Licensed under the Apache License 2.0\
                nhttp://www.apache.org/licenses/LICENSE-2.0"

    if argv is None:
        argv = sys.argv[1:]
    try:
        # setup option parser
        parser = OptionParser(version=program_version_string, description=program_license)
        parser.add_option("-v", "--verbose", dest="verbose", action="count", help="set verbosity level [default: %default]")
        parser.add_option("-s", "--server_mode", dest="server_mode", action="store_true", help="the software will act as server [default: %default]")
        parser.add_option("-c", "--config", dest="config_file", help="the configuration file")
        parser.add_option("-l", "--local_ip", dest="local_ip", help="local ip address")
        parser.add_option("-r", "--remote_ip", dest="remote_ip", help="remote ip address")        
        
        # set defaults
        parser.set_defaults(server_mode=False, config_file="", 
                            local_ip = '127.0.0.1',
                            verbose = False)

        # process options
        (opts, args) = parser.parse_args(argv)
        is_verbose = False
        if opts.verbose > 0:
            #print("verbosity level = %d" % opts.verbose)
            is_verbose = True
        server_mode = opts.server_mode

        msg_freq = DEFAULT_SLEEPTIME
        siurc = opts.local_ip
        remote_ip = opts.remote_ip
        sleep_time = DEFAULT_SLEEPTIME
       
        # MAIN BODY #
        if opts.config_file == "" :
            print "Error: missed config file"
            return            
        config = parseConfigs(opts.config_file)
 
        msgs = config.get_unpacked_messages()
       
        if server_mode :
            lstn = ServerListener(remote_ip, msgs, is_verbose, msg_freq, sleep_time)
        else :
            lstn = SenderListener(None, msgs, remote_ip, is_verbose, msg_freq,
                                  sleep_time)  
    except Exception, e:
        indent = len(program_name) * " "
        sys.stderr.write(program_name + ": " + repr(e) + "\n")
        sys.stderr.write(indent + "  for help use --help")
        return 2
    lstn.daemon = True
    lstn.start()
    lstn.join()
    lstn.stop()

if __name__ == "__main__":
    if DEBUG:
        sys.argv.append("-v")
    sys.exit(main())