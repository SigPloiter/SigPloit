#       create_session.py
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
## @brief  Class implementing a Create Session Request message
##
class CreateSessionRequest(GTPV2MessageBase):
    ##
    ## @brief      Init method
    ##
    ## @param      self  refers to the class itself
    ## @param      source_ip  source ip to set into information elements
    ## @param      interface to use (e.g. S5/S8, S11). Default S8   
    ## @param      imsi  refers to the imsi to use
    ## @param      mcc  mobile country code
    ## @param      mcc  mobile network code    
    ## @param      lac  location area code
    ## @param      rac  routing area code
    ## @param      apn  access point name
    ## @param      p_dns primary dns 
    ## @param      s_dns secondary dns            
    ## @param      imei  ME identity     
    ## @param      rat_type Radio Access Technology  
    ## @param      tac  Type allocation Code       
    ## @param      ecgi Eutran Cell Global Identifier 
    ## @param      sac  Service Area Code     
    ## @param      cgi Cell Global Identifier  
    ## @param      sm  Service Mode    
    ## @param      recovery Recovery Code     
    ## @param      ebi  refers to EPSBearerID. Default 5
    ## 
    def __init__(self, source_ip, interface = 7, imsi = "333885500003199", 
                 mcc = "333", mnc="88", lac = 2788, rac = 1, 
                 apn="abc", p_dns ='127.0.0.1', s_dns ="127.0.0.2", 
                 gsn="127.0.0.1", phone="333282270202", 
                 imei='3518280450609004', rat_type = 'E-UTRAN', tac = 0, 
                 ecgi = 0, sac = 0, cgi = 0, sm = 0, recovery = True, ebi = 5):
       
        GTPV2MessageBase.__init__(self, t = 0x01,
            msg_type = GTPmessageTypeDigit['create-session-request'])
        
     
 
        self.add_ie(Imsi(imsi))
        self.add_ie(RatType(rat_type))
        fteid = FTeid(source_ip, interface)
        self.__fteid = fteid.get_teid()
        self.add_ie(fteid)
        self.add_ie(AccessPointName(apn))
        self.add_ie(BearerContext(ebi = ebi, ip = source_ip, 
                interface = interface))
        self.add_ie(UserLocationInformation(mcc = mcc, mnc = mnc, lac = lac, 
               rac = rac, tac = tac, ecgi = ecgi, 
               sac = sac, cgi = cgi))
        self.add_ie(ServingNetwork(mcc = mcc, mnc = mnc))           
        self.add_ie(SelectionMode(selection_mode = sm))          
        self.add_ie(PDNAddressAllocation())
        self.add_ie(ApnRestriction())
        self.add_ie(AggregateMaximumBitRate())
        self.add_ie(Msisdn(msisdn=phone))
        self.add_ie(MEIdentity(imei))
        self.add_ie(ChargingCharacteristic())   
        self.add_ie(ProtocolConfigurationOptions(p_dns=p_dns, s_dns=s_dns))
        if recovery :
            self.add_ie(Recovery())
    ##
    ## @brief      get_fteid method
    ##
    ## @param      self  refers to the class itself
    ## @return     F-TEID            
    ##         
    
    def get_fteid(self):
        return self.__fteid

##
## @brief  Class implementing a Create Session Response message
##     
class CreateSessionResponse(GTPV2MessageBase):
    ##
    ## @brief      Init method
    ##
    ## @param      self  refers to the class itself
    ## @param      teid Tunnel Endpoint Identifier to set
    ## @param      source_ip  source ip to set into information elements
    ## @param      interface to use (e.g. S5/S8, S11). Default S8   
    ## @param      sqn  GTP header sequence number to set
    ## @param      p_dns primary dns 
    ## @param      s_dns secondary dns            
    ## 
    def __init__(self, teid, source_ip, interface, sqn = 0x00,  
            p_dns ='127.0.0.1', s_dns ="127.0.0.2"):
        '''
        Constructor
        '''
        GTPV2MessageBase.__init__(self, t = 0x01, sequence = sqn, 
            msg_type = GTPmessageTypeDigit['create-session-response'])
        self.set_teid(teid)
        self.add_ie(FTeid(source_ip, interface))
        self.add_ie(Cause())
        self.add_ie(BearerContext(ip = source_ip, interface = interface))        
        self.add_ie(ProtocolConfigurationOptions(p_dns=p_dns, s_dns=s_dns))   
        self.add_ie(PDNAddressAllocation())
        self.add_ie(ApnRestriction())              
