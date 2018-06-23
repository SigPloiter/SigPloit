'''
Created on 12 Dec 2017

@author: lia
'''
import threading, time, signal
from socket import *


from gtpv2_sender_listener import SenderListener

from path_managment_listener import PathMgmtListener

GTP_C_PORT = 2123

class ServerListener(threading.Thread):
    def __init__(self, peer, messages, isVerbose = True, msgs_freq=1, 
                 wait_time=20):
        threading.Thread.__init__(self)
        
        self.TAG_NAME = 'GTPV2 SERVER_LISTENER'
        
        self.sock = socket(AF_INET, SOCK_DGRAM)
        self.sock.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)
        
        self.sock.bind(('0.0.0.0', GTP_C_PORT))
       
        
        self.peer = peer
        
        self.is_verbose = isVerbose
        self.messages = messages
        
        self.msgs_freq = msgs_freq
        self.wait_time = wait_time
        
        self.lsntPathMgmt= None
        self.lsntSender = None
        
        signal.signal(signal.SIGQUIT, self.stop)
        signal.signal(signal.SIGINT, self.stop)
        signal.signal(signal.SIGTERM, self.stop)
        
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
        
        if self.is_verbose: 
            print "Working in server mode"
           
        ''' START PATH MGMT  LISTENER '''
        self.lsntPathMgmt = PathMgmtListener(self.sock, self.is_verbose)
        self.lsntPathMgmt_daemon = True
        self.lsntPathMgmt.start()
            
        ''' START SENDER CLIENT '''
        self.lsntSender= SenderListener(self.sock, self.messages, self.peer,
                                            self.is_verbose, self.msgs_freq, 
                                            self.wait_time)            
        self.lsntSender.daemon = True
        self.lsntSender.start()
        self.lsntSender.join()
        time.sleep(15)
        self.stop()
        
    ##
    ## @brief      Stops the execution of the thread
    ##
    ## @param      self  refers to the class itself
    ##
    def stop(self):
        if self.lsntPathMgmt is not None:
            self.lsntPathMgmt.stop()
        
        if self.lsntSender is not None:
            self.lsntSender.stop()
            
        self.sock.close()
        self.is_running = False
        
        if self.is_verbose:
            print "%s: Stopped"%(self.TAG_NAME)