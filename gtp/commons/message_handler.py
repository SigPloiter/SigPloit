'''
Created on 12 Dec 2017

@author: lia
'''
import threading, time, signal
from socket import socket, SOL_SOCKET, AF_INET, SO_REUSEADDR, SOCK_DGRAM


from sender import Sender

from listener import Listener
#from commons.globals import GTP_C_PORT

class MessageHandler(threading.Thread):
   
    def __init__(self, peer, messages, isVerbose = True, listening_mode = False,
                 msgs_freq=1, wait_time=20, port = 2123):

        threading.Thread.__init__(self)
        self.sock = None
        self.TAG_NAME = 'GTPV2 SERVER_LISTENER'
             
        self.peer = peer
        
        self.is_verbose = isVerbose
        self.messages = messages
        self.is_listening = listening_mode
        self.gtp_port = port
        
        self.sock = socket(AF_INET, SOCK_DGRAM)
        self.sock.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)
        self.sock.bind(('0.0.0.0', self.gtp_port))

        self.msgs_freq = msgs_freq
        self.wait_time = wait_time
        
        self.listener= None
        self.sender = None
        
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
                  
        if self.is_listening:     
            if self.is_verbose: 
                print "\033[34m[*]\033[0m starting the listener ...."                
            ''' START Listener '''
            self.listener= Listener(open_sock = self.sock, 
                                    isVerbose = self.is_verbose)            
            self.listener.daemon = True
            self.listener.start()
        
        if self.is_verbose : 
            print "\033[34m[*]\033[0m starting the sender ...."
        ''' START Sender'''        
        self.sender= Sender(sock = self.sock, messages = self.messages, 
                            peers = self.peer, isVerbose = self.is_verbose, 
                            msg_freq= self.msgs_freq, 
                            wait_time= self.wait_time, gtp_port = self.gtp_port
                            )
        self.sender_daemon = True
        self.sender.start()               
        self.sender.join()
        time.sleep(5)
        self.stop()
        
    ##
    ## @brief      Stops the execution of the thread
    ##
    ## @param      self  refers to the class itself
    ##
    def stop(self):
               
        if self.sender:
            self.sender.stop()    
        
        if self.listener:
            self.listener.stop()                  
        
        if self.sock:   
            self.sock.close()
        self.is_running = False
        
        if self.is_verbose:
            print "%s: Stopped"%(self.TAG_NAME)
