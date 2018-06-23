#!/usr/bin/env python
# encoding: utf-8
#       teid_sequence_predictability_index.py
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
from gtp.gtp_v2_core.utilities.teid_predictability import TeidPredictabilityIndex,\
    TeidFixedPart

__all__ = []
__version__ = 0.1

DEFAULT_NUM_MSG = 6

DEBUG = 0


##
## ATTACKING TOOL 
## 
## @brief      Main file to execute the script.
## 
## This file roughly estimates how difficult it would be to predict the next 
## teid from the known sequence of six probe responses. 
##
## Use the -h option to enter the help menu and determine what to do.
## 
## Basic usage examples:
##      * $ python teid_sequence_predictability_index.py -v -t <teids>




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
    lstn = None
    try:
        # setup option parser
        parser = OptionParser(version=program_version_string, description=program_license)
        parser.add_option("-v", "--verbose", dest="verbose", action="count", 
                          help="set verbosity level [default: %default]")

        parser.add_option("-t", "--teids", dest="teids_file", help="file "
                          "containing list of at least six consecutives tests")
      
        
        # set defaults
        parser.set_defaults(teids_file="teids.cnf", 
                            verbose = False)

        # process options
        (opts, args) = parser.parse_args(argv)
        is_verbose = False
 
        # MAIN BODY #
        if opts.teids_file == "" :
            print "Error: missed file containing at least six consecutive teids"
            return            
        ##read file
        teids = []
        with open(opts.teids_file) as f:
            teids = f.readlines()
        teids = [int(t.strip(),16) for t in teids]
        
        if len(teids) < 6:
            print ("Error: File shall contain least six consecutive teids.",
                   "provided %d")%(len(teids))
            return           
        tpi = TeidPredictabilityIndex()
        index, msg = tpi.teidPredictabilityIndex(teids)
        print ("%d, %s")%(index, msg)
        tcp = TeidFixedPart()
        teids_hex = [hex(t) for t in teids]

        common_prefixes = tcp.teidFixedPart(teids_hex)
        if common_prefixes != [] :
            print "The algorithm seems to use a number of bits less than 32 for",\
                   "TEID generation."
            print common_prefixes
        else :
                print ("The algorithm seems to use a all 32 bits for",
                   "TEID generation.")          
       
    except Exception, e:
        indent = len(program_name) * " "
        sys.stderr.write(program_name + ": " + repr(e) + "\n")
        sys.stderr.write(indent + "  for help use --help")
        print "Exception %s"%str(e)       
        return 2
if __name__ == "__main__":
    if DEBUG:
        sys.argv.append("-v")
    sys.exit(main())
