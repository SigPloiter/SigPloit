#       delete_bearer.py
#       
#       Copyright 2018 Rosalia d'Alessandro
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

#!/usr/bin/env  python
# -*- coding: utf-8 -*-
from gtp_v2_core.commons.gtp_v2_msg_base import GTPV2MessageBase

from gtp_v2_core.commons.gtp_v2_commons import GTPmessageTypeDigit
from gtp_v2_core.commons.gtp_v2_information_element_base import *


##
## @brief  Class implementing a Delete Bearer Request message
##
class DeleteBearerRequest(GTPV2MessageBase):
    ##
    ## @brief      Init method
    ##
    ## @param      self  refers to the class itself
    ## @param      teid  refers to the tunnel end point identifier to set
    ## @param      source_ip  source ip to set into information elements
    ## @param      nit   node type id    
    ## @param      sqn  sequence number to set into GTP HDR
    ## @param      ebi  refers to EPSBearerID. Default 5
    ## @param      interface to use (e.g. S5/S8, S11). Default S8
    ##
    def __init__(self, teid, source_ip, nit = 0, sqn = 0x00, ebi = 5, interface = 7, 
                 cause = 3, mcc=333, mnc=88):
        GTPV2MessageBase.__init__(self, t = 0x01, sequence = sqn, 
            msg_type = GTPmessageTypeDigit['delete-bearer-request'])
        self.set_teid(teid)
        self.add_ie(EPSBearerID(ebi = ebi))
        self.add_ie(Cause(cause = cause))
        self.add_ie(FQCSID(node_id_type = nit, ip = source_ip, mcc = mcc, 
                           mnc = mnc))

##
## @brief  Class implementing a Delete Bearer Response message
##
class DeleteBearerResponse(GTPV2MessageBase):
    ##
    ## @brief      Init method
    ##
    ## @param      self  refers to the class itself
    ## @param      teid  refers to the tunnel end point identifier to set
    ## @param      source_ip  source ip to set into information elements
    ## @param      sqn  sequence number to set into GTP HDR
    ## @param      ebi  refers to EPSBearerID. Default 5
    ## @param      interface to use (e.g. S5/S8, S11). Default S8
    ## 
    def __init__(self, teid, nit = 0, source_ip = '127.0.0.1', sqn = 0x00):
        '''
        Constructor
        '''
        GTPV2MessageBase.__init__(self, t = 0x01, sequence = sqn,
            msg_type = GTPmessageTypeDigit['delete-bearer-response'])
        self.set_teid(teid)
        self.add_ie(Cause())
        self.add_ie(FQCSID(node_id_type = nit, ip = source_ip))        
