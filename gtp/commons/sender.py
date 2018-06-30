'''
Created on 12 Dec 2017

@author: lia
'''
import threading
import os
import sys
sys.path.insert(0, os.path.join(os.getcwd(), 'gtp/'))

from socket import socket, error, AF_INET, SOCK_DGRAM, timeout, errno
import time
from IPy import IP
from gtp_v2_core.utilities.utilities import logNormal, logErr, logOk 

from globals import message_queue

class Sender(threading.Thread):
    '''
    classdocs
    '''
   
    def __init__(self, sock, messages, peers, start_time=None, isVerbose = False, 
                 msg_freq=1, wait_time=20, gtp_port = 2123):

        threading.Thread.__init__(self)
        
        self.TAG_NAME = 'GTP SENDER'
        self.is_verbose = isVerbose        
    
        
        self.sock = sock


        self.start_time = start_time
        self.msg_freq = msg_freq
        self.wait_time = wait_time
        self.peers = IP(peers)
        self.gtp_port = gtp_port
        self.messages = []
        if messages is None or len(messages) == 0 :
            logErr("no messages", TAG = self.TAG_NAME)
            return       
         
        if not isinstance(messages, list):
            self.messages = [messages]
        else:
            self.messages = messages       
        
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
        self.is_running = True
        
        logNormal("--: Acting as SENDER :--", verbose = self.is_verbose, 
                   TAG = self.TAG_NAME)
                
        if self.is_running and self.sock is not None:
            ''' Prepare the messages to send '''

            logNormal("Preparing GTP messages", verbose = self.is_verbose, 
                   TAG = self.TAG_NAME)                
            mdatas = []
            if self.messages is not None and len(self.messages) > 0:
                count = 0
                for m in self.messages:
                    logNormal("preparing msg #%d - type %d"%(count, 
                        m.get_msg_type()), verbose = self.is_verbose, 
                        TAG = self.TAG_NAME)                     
                    mdatas.append(m.get_message())
                    count += 1
            tot_count = len(mdatas)
            logOk("Prepared %d GTP messages"%(tot_count), verbose = self.is_verbose, 
                   TAG = self.TAG_NAME)                
        
            curr_count = 1                    
        
            for num, data in enumerate(mdatas):
                logNormal("Sending message (#%d of %d)..."%(curr_count, 
                        tot_count), verbose = self.is_verbose, 
                        TAG = self.TAG_NAME)                     
                for ip in self.peers:
                    try: 
                        ip_str = ip.strNormal()
                                              
                        msg_info = {'reply' : 0}
                        msg_type = self.messages[num].get_msg_type()
                        if msg_type == 32 or msg_type == 34:
                            msg_info['local_teid'] = self.messages[num].get_fteid()
                       
                        if not message_queue.has_key(ip_str) or \
                            not message_queue[ip_str].has_key(msg_type):
                            message_queue[ip_str] = {} 
                            message_queue[ip_str][msg_type] = [msg_info]
                        else:
                            message_queue[ip_str][msg_type].append(
                                msg_info) 
                  
                        sent_bytes = self.sock.sendto(data, (ip_str, 
                                                             self.gtp_port))
                                                
                        if sent_bytes is not None and sent_bytes > 0:
                            info_msg = "Bytes sent to %s %d"%(ip_str, sent_bytes)
                        else:
                            info_msg = "NO bytes sent to %s"%(ip_str)
                        logNormal(info_msg, verbose = self.is_verbose, 
                                TAG = self.TAG_NAME)                              
                    except timeout, e:
                        logErr("%s TIMEOUT_ERROR"%(ip_str), TAG = self.TAG_NAME)                         
                        pass
                    except error, e:
                        if e.errno == errno.ECONNREFUSED:
                            logErr("%s CONNECTION_REFUSED"%(ip_str), 
                                TAG = self.TAG_NAME)                                   
                        elif e.errno == errno.EBADFD:
                            logErr("%s BAD_FILE_DESCRIPTOR_ERROR"%(ip_str), 
                                TAG = self.TAG_NAME)     
                            break                        
                        elif e.errno == errno.EPIPE:
                            logErr("%s BROKEN_PIPE_ERROR"%(ip_str), 
                                TAG = self.TAG_NAME)  
                            break                           
                        elif e.errno == errno.ECONNRESET:
                            logErr("%s CONNECTION_RESET_ERROR"%(ip_str), 
                                TAG = self.TAG_NAME)                             
                        else:
                            logErr("%s UNKNOWN_ERROR: %s"%(ip_str, e), 
                                TAG = self.TAG_NAME)    
                            break                         
                        pass
                    except Exception, e:
                        logErr("%s GENERIC ERROR : reason %s"%(ip_str, e), 
                            TAG = self.TAG_NAME)                         
                        break                                 
                curr_count += 1
                time.sleep(self.msg_freq)                 
                              
            if self.start_time is not None:
                stop_time = time.time()
                hours, rem = divmod(stop_time - self.start_time, 3600)
                minutes, seconds = divmod(rem, 60)
                logOk("Elapsed time: {:0>2}:{:0>2}:{:05.4f}".format(
                    int(hours), int(minutes), seconds), verbose = self.is_verbose, 
                   TAG = self.TAG_NAME)

                        
                
    ##
    ## @brief      Stops the execution of the thread
    ##
    ## @param      self  refers to the class itself
    ##
    def stop(self):
        if not self.is_running:
            return        
        self.is_running = False
        logOk("Stopped", verbose = self.is_verbose, TAG = self.TAG_NAME)
