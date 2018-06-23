'''
Created on 24 Jan 2018

@author: lia
'''

#GTP_C_PORT = 2123

#global variable needed to manage request/response pair
message_queue = {}


GTPResponse2Request = {
    2: 1,
    33: 32,
    35: 34,
    37: 36,
    39: 38, 
    96: 95,
    98: 97,
    100: 99,       
    171: 170,
    177: 176,
}


GTPRequest2Response = {
    1: 2,
    32: 33,
    34: 35,
    36: 37,
    38: 39, 
    95: 96,
    97: 98,
    99: 100,       
    170: 171,
    176: 177,
}