'''
Created on 8 Feb 2018

@author: lia
'''
import sys, re
import datetime
import time

def FUNC( back = 0):
    return sys._getframe( back + 1 ).f_code.co_name

##
## @brief      This method prints the passed text in GREEN
##
## @param      text     the string to be printed
## @param      newLine  an optional boolean to specify if it's an inline print
##                      or not
##
def printGreen(text, newLine=True):
    if newLine:
        print '\033[0;32m%s\033[0m'%text
    else:
        print '\033[0;32m%s\033[0m'%text,
        
##
## @brief      This method prints the passed text in RED
##
## @param      text     the string to be printed
## @param      newLine  an optional boolean to specify if it's an inline print
##                      or not
##
def printRed(text, newLine=True):
    if newLine:
        print '\033[0;31m%s\033[0m'%text
    else:
        print '\033[0;31m%s\033[0m'%text,

##
## @brief      This method prints the passed text in YELLOW
##
## @param      text     the string to be printed
## @param      newLine  an optional boolean to specify if it's an inline print
##                      or not
##
def printYellow(text, newLine=True):
    if newLine:
        print '\033[1;33m%s\033[0m'%text
    else:
        print '\033[1;33m%s\033[0m'%text,

##
## @brief      Gets the current timestamp in log format (Y-m-d H:M:S)
##
## @return     the current timestamp
##
def getCurrTimestamp():
    return datetime.datetime.fromtimestamp(time.time()).strftime('%Y-%m-%d %H:%M:%S')

##
## @brief      Logs a normal message
##
## @param      text     the text to be logged
## @param      TAG      the reference of the file that call the log function
## @param      newLine  an optional boolean to specify if it's an inline print
##                      or not
##
def logNormal(text, verbose = False, TAG=None, newLine=True):
    if not verbose :
        return
    if TAG is not None:
        s_text = "%s\t%s :: %s" % (getCurrTimestamp(), TAG, text)
    else:
        s_text = text
    
    if newLine:
        print s_text
    else:
        print s_text,

##
## @brief      Logs an ok message
##
## @param      text     the text to be logged
## @param      TAG      the reference of the file that call the log function
## @param      newLine  an optional boolean to specify if it's an inline print
##                      or not
##
def logOk(text, verbose = False, TAG=None, newLine=True):
    if not verbose :
        return
    if TAG is not None:
        s_text = "%s\t%s :: %s" % (getCurrTimestamp(), TAG, text)
    else:
        s_text = text
    
    printGreen(s_text, newLine)

##
## @brief      Logs a warning message
##
## @param      text     the text to be logged
## @param      TAG      the reference of the file that call the log function
## @param      newLine  an optional boolean to specify if it's an inline print
##                      or not
##
def logWarn(text, verbose = False, TAG=None, newLine=True):
    if not verbose :
        return    
    if TAG is not None:
        s_text = "%s\t%s :: %s" % (getCurrTimestamp(), TAG, text)
    else:
        s_text = text
    
    printYellow(s_text, newLine)

##
## @brief      Logs an error message
##
## @param      text     the text to be logged
## @param      TAG      the reference of the file that call the log function
## @param      newLine  an optional boolean to specify if it's an inline print
##                      or not
##
def logErr(text, TAG=None, newLine=True):
    if TAG is not None:
        s_text = "%s\t%s :: %s" % (getCurrTimestamp(), TAG, text)
    else:
        s_text = text
    
    printRed(s_text, newLine)



##
## @brief      Generates a slug form of the passed text (a dash separated text)
##
## @param      text  the text to be converted
##
## @return     the slug of the text
##
def slugfy(text):
    s = text.lower()
    s = re.sub(r"(_|\s+)", "-", s)
    
    return s