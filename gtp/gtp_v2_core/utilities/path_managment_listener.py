'''
Created on 12 Dec 2017

@author: lia
'''
import threading
import errno
import struct
from socket import socket, timeout, error
from path_mgmt_messages.echo import EchoResponse
from commons.gtp_v2_commons import GTPmessageTypeDigit
class PathMgmtListener(threading.Thread):
    '''
    classdocs
    '''


    def __init__(self, open_sock, isVerbose=True):
        threading.Thread.__init__(self)
        
        self.TAG_NAME = 'PATH MANAGEMENT_LISTENER'
        
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
                
    ##
    ## @brief      Starts the execution of the thread
    ##
    ## @param      self  refers to the class itself
    ##
    def run(self):          
        if self.is_verbose: 
            print "\n\n--: PATH MANAGEMENT MANAGER :--"            
            print "Keep working on the opened connection"
            
        self.is_running = True
        while self.sock is not None and self.is_running:
            try:
                data = self.sock.recvfrom(1024)            
                if len(data) > 8 : 
                    print len(data)                     
                    (flags, msg_type, length, sequence) = struct.unpack("!BBHL", 
                                                                        data[:8])
                    version = flags & 0x40 
                    teid = flags & 0x01
                    if version != 2 :
                        print "%s:Unsupported GTP version %02x"%(self.TAG_NAME, 
                                                                 version)
                        return
                    if msg_type != GTPmessageTypeDigit['echo-request']:
                        return
                    if teid != 0x00:
                        print "%s:Invalid TEID %02x"%(self.TAG_NAME, teid)
                        return
                    sequence = sequence & 0xffffff00
                    
                    print ("%s: Received valid GTP ECHO REQUEST message with sequence"
                                   " %02x"%(self.TAG_NAME, sequence))
                    if self.is_verbose:                        
                        print "%s: Preparing GTP ECHO RESPONSE message"%(self.TAG_NAME)

                    echo_response = EchoResponse(sequence)
                    if self.is_verbose:   
                        print "%s: Sending GTP ECHO RESPONSE message"%(self.TAG_NAME)
                    sent_bytes = self.connection.send(echo_response.get_message())
                    if sent_bytes is not None and sent_bytes>0:
                        print "%s: Sent GTP ECHO RESPONSE message"%(self.TAG_NAME)
                        print"%s: bytes sent %d"%(sent_bytes)
                    else:
                        print "%s: GTP ECHO RESPONSE message not sent"%(self.TAG_NAME)            
            except timeout, e:
                print "%s: TIMEOUT_ERROR: %s" % (self.TAG_NAME, e)
                break
            except error, e:
                if e.errno == errno.EBADFD:
                    print "%s: BAD_FILE_DESCRIPTOR_ERROR: %s"%(self.TAG_NAME, e)
                    break
                elif e.errno == errno.EPIPE:
                    print "%s: BROKEN_PIPE_ERROR: %s"%(self.TAG_NAME, e)
                    break
                else:
                    print "%s: UNKNOWN_ERROR: %s"%(self.TAG_NAME, e)
                    break
            except Exception, e:
                print "%s:GENERIC ERROR : %s"%(self.TAG_NAME, e)
                break       
    
    ##
    ## @brief      Stops the execution of the thread
    ##
    ## @param      self  refers to the class itself
    ##
    def stop(self):
        if not self.is_running:
            return
        
        self.is_running = False
        
        if self.is_verbose: 
            print"Stopped %s"%(self.TAG_NAME)
                