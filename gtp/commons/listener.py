#!/usr/bin/python

'''
Created on 12 Dec 2017

@author: lia
'''
import threading
import errno, sys
import os
sys.path.insert(0, os.path.join(os.getcwd(), 'gtp/'))

import struct
from socket import socket, timeout, error

from gtp_v2_core.commons.gtp_v2_commons import GTPmessageTypeStr, GTPmessageTypeDigit

from commons.globals import message_queue, GTPResponse2Request
from gtp_v2_core.utilities.utilities import logNormal, logErr, logOk , logWarn
import binascii

class Listener(threading.Thread):
    '''
    classdocs
    '''


    def __init__(self, open_sock, isVerbose=True):
        threading.Thread.__init__(self)
        
        self.TAG_NAME = 'GTP LISTENER'
        
        self.sock = open_sock
        self.is_verbose = isVerbose
        self.is_running = False
        
    ##
    ## @brief      Determines if the thread is running
    ##
    ## @param      self  refers to the class itself
    ##
    ## @return     True if running, False otherwise.
    ##    
    def isRunning(self):
        return self.is_running
      
    def __getFTEID(self, data):          
        if data is None or len(data) == 0:
            raise Exception("%s: invalid data"%self.TAG_NAME)
        i = 0
        teid = 0x00
        while i < len(data) :
            (ie_type, ie_len, spare_instance) = struct.unpack("!BHB", 
                                                                data[i: i+4])
            if ie_type != 87:
                i += (4 + ie_len)
            else:
                teid = struct.unpack("!L", data[i+5: i+9])[0]
                break
        return format(teid, '#08X')
    ##
    ## @brief      Starts the execution of the thread
    ##
    ## @param      self  refers to the class itself
    ##
    def run(self):                    
        self.is_running = True
        count = 0
        while self.sock is not None and self.is_running:
            try:
                data, addr = self.sock.recvfrom(1024)            
                if len(data) > 8 :                      
                    (flags, resp_msg_type, length, sequence_or_teid) = struct.unpack("!BBHL", 
                                                                data[:8])
                    version = flags & 0xF0 
                    if version != 0x40:
                        logWarn("Unsupported GTP version %02x"%(version), 
                                verbose = self.is_verbose, TAG = self.TAG_NAME)
                        continue
                    if not message_queue.has_key(addr[0]):
                        logWarn("Unmanaged IP %s"%(addr[0]),
                                verbose = self.is_verbose, TAG = self.TAG_NAME)                        
                        continue
                    req_msg_type = GTPResponse2Request[resp_msg_type]

                    if not message_queue[addr[0]].has_key(req_msg_type):
                        logWarn("Unsolicited response msg %d"%(resp_msg_type),
                                verbose = self.is_verbose, TAG = self.TAG_NAME) 
                        continue
                    
                    
                    logOk("Received response to sent msg %s from ip %s"%(
                        GTPmessageTypeStr[req_msg_type], addr[0]), 
                            verbose = self.is_verbose, TAG = self.TAG_NAME) 
                    if req_msg_type == GTPmessageTypeDigit["echo-request"] :
                        message_queue[addr[0]][req_msg_type][0]['reply'] = 1
                    else:
                        for elem in message_queue[addr[0]][req_msg_type]:
                            if elem.has_key('local_teid') and \
                                elem['local_teid'] ==  sequence_or_teid :     
                                elem['reply'] = 1
                                elem['remote_teid'] = self.__getFTEID(data[12:])
                                break
                count += 1
                logNormal("RECEIVED #%d messages"%(count), verbose = self.is_verbose,
                          TAG = self.TAG_NAME)            
            except timeout, e:
                if addr[0] :
                    logErr("%s TIMEOUT_ERROR"%(addr[0]), TAG = self.TAG_NAME)
                else:
                    logErr("TIMEOUT_ERROR", TAG = self.TAG_NAME)                         
                pass
            except error, e:
                if e.errno == errno.EBADFD:
                    if addr[0] :                    
                        logErr("%s BAD_FILE_DESCRIPTOR_ERROR"%(addr[0]), 
                                TAG = self.TAG_NAME) 
                    else:
                        logErr("BAD_FILE_DESCRIPTOR_ERROR", TAG = self.TAG_NAME)                    
                    break
                elif e.errno == errno.EPIPE:
                    if addr[0] : 
                        logErr("%s BROKEN_PIPE_ERROR"%(addr[0]), 
                            TAG = self.TAG_NAME)  
                    else:
                        logErr("BROKEN_PIPE_ERROR", TAG = self.TAG_NAME)   
                    break
                else:
                    logErr("UNKNOWN ERROR: %s"%(e), TAG = self.TAG_NAME) 
                    break
            except Exception, e:
                logErr("GENERIC ERROR: %s"%(e), TAG = self.TAG_NAME)
                break 
    
    ##
    ## @brief      Stops the execution of the thread
    ##
    ## @param      self  refers to the class itself
    ##
    def stop(self):
        if not self.is_running:
            logWarn("is not running", verbose = self.is_verbose, 
                    TAG = self.TAG_NAME)            
            return        
        self.is_running = False
        logOk("Stopped", verbose = self.is_verbose, TAG = self.TAG_NAME) 
                
