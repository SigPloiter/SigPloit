'''
Created on 12 Dec 2017

@author: lia
'''
import threading
import errno
from socket import *
import time


GTP_C_PORT = 2123
class SenderListener(threading.Thread):
    '''
    classdocs
    '''
    def __init__(self, open_sock, messages, peer, start_time=None, isVerbose = False, 
                 msg_freq=1, wait_time=20):
        threading.Thread.__init__(self)
        
        self.TAG_NAME = 'SENDER_LISTENER'
        
        if messages is None or len(messages) == 0 :
            raise Exception("%s :: no messages" % (self.TAG_NAME))             
        
        if open_sock is None :
            print "Working in client mode"
            self.sock = socket(AF_INET, SOCK_DGRAM)
        else :
            print "Working in server mode"
            self.sock = open_sock
        #self.connection.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        
        self.is_verbose = isVerbose
        
        if not isinstance(messages, list):
            self.messages = [messages]
        else:
            self.messages = messages

        self.start_time = start_time
        self.msg_freq = msg_freq
        self.wait_time = wait_time
        self.peer = peer
        
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
            print "\n--: Acting as SENDER :--"
                
        if self.is_running and self.sock is not None:
            ''' Prepare the messages to send '''
            if self.is_verbose: 
                print "%s: Preparing GTP messages"%(self.TAG_NAME)
            mdatas = []
            if self.messages is not None and len(self.messages) > 0:
                count = 0
                for m in self.messages:
                    print "preparing msg #%d - type %d"%(count, m.get_msg_type())
                    mdatas.append(m.get_message())
                    count += 1
            tot_count = len(mdatas)
          
            if self.is_verbose: 
                print "%s: Prepared %d GTP messages"%(self.TAG_NAME, tot_count)
                
            try:
                ''' SENDS MESSAGES '''
                curr_count = 1                    
                for data in mdatas:
                    if self.is_verbose:
                        print ("%s: Sending message (#%d of %d)..."
                               %(self.TAG_NAME,curr_count, tot_count))
        
                    sent_bytes = self.sock.sendto(data, (self.peer, GTP_C_PORT))
                    if sent_bytes is not None and sent_bytes > 0:
                        if self.is_verbose: 
                            print "%s: Bytes sent %d"%(self.TAG_NAME, sent_bytes)
                    else:
                        if self.is_verbose: 
                            print "%s: NO bytes sent"%(self.TAG_NAME)
                    curr_count += 1
                    time.sleep(self.msg_freq)                 
            except timeout, e:
                print "%s: TIMEOUT_ERROR : %s"%(self.TAG_NAME, e)
                pass
            except error, e:
                if e.errno == errno.ECONNREFUSED:
                    print "%s: CONNECTION_REFUSED: %s"%(self.TAG_NAME, e)
                if e.errno == errno.EBADFD:
                    print "%s: BAD_FILE_DESCRIPTOR_ERROR: %s"%(self.TAG_NAME, e)
                elif e.errno == errno.EPIPE:
                    print "%s: BROKEN_PIPE_ERROR: %s"%(self.TAG_NAME, e)
                elif e.errno == errno.ECONNRESET:
                    print "%s: CONNECTION_RESET_ERROR: %s"%(self.TAG_NAME, e)
                else:
                    print "%s: UNKNOWN_ERROR: %s"%(self.TAG_NAME, e)
                    pass
            except Exception, e:
                print "%s:GENERIC ERROR : %s"%(self.TAG_NAME, e)
                pass                               
            if self.start_time is not None:
                stop_time = time.time()
                hours, rem = divmod(stop_time - self.start_time, 3600)
                minutes, seconds = divmod(rem, 60)
                print "Elapsed time: {:0>2}:{:0>2}:{:05.4f}".format(
                    int(hours), int(minutes), seconds)

                        
                
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
            print "%s: Stopped"%(self.TAG_NAME)
