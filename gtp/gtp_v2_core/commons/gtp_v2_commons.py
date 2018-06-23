#!/usr/bin/env  python
# -*- coding: utf-8 -*-

import struct
import IPy


RESERVED_IE_TYPES = [0, 98, 101, 102, 122, 130, 161]
RESERVED_IE_TYPES.extend(range(4,51))
RESERVED_IE_TYPES.extend(range(52,71))
RESERVED_IE_TYPES.extend(range(187,255))

DEBUG = 0

RATTypeStr = {
    1 :"UTRAN",
    2 : "GERAN",
    3 : "WLAN",
    4 : "GAN",
    5 : "HSPA Evolution",  
    6: "E-UTRAN", 
}

RATTypeDigit = {
    "UTRAN" : 1,
    "GERAN" : 2,
    "WLAN" : 3,
    "GAN" : 4,
    "HSPA Evolution" : 5,
    "E-UTRAN" : 6,  
}

#TS 29.274 Table 6.1-1
GTPmessageTypeStr = {
    1: "echo-request",
    2: "echo-response",
    32: "create-session-request",
    33: "create-session-response",
    34: "modify-bearer-request",
    35: "modify-bearer-response",
    36: "delete-session-request",
    37: "delete-session-response",
    38: "change-notification-request",
    39: "change-notification-response", 
    64: "modify-bearer-command",   
    65: "modify-bearer-failure-indication",
    66: "delete-bearer-command",   
    67: "delete-bearer-failure-indication",    
    68: "bearer-resource-command",   
    69: "bearer-resource-failure-indication",     
    70: "downlink-data-notify-failure-indication",
    71: "trace-session-activation",
    72: "trace-session-deactivation",
    73: "stop-paging-indication",
    95: "create-bearer-request",
    96: "create-bearer-response",
    97: "update-bearer-request",
    98: "update-bearer-response",
    99: "delete-bearer-request",
    100: "delete-bearer-response",  
    101: "delete-pdn-connection-set-request",
    102: "delete-pdn-connection-set-response",         
    170: "realease-bearers-request",
    171: "realease-bearers-response",
    176: "downlink-data-notify",
    177: "downlink-data-notify-acknowledge",
}


GTPmessageTypeDigit = {
    "echo-request" : 1,
    "echo-response" : 2,
    "create-session-request" : 32,
    "create-session-response" : 33,
    "modify-bearer-request" : 34,
    "modify-bearer-response" : 35,
    "delete-session-request" : 36,
    "delete-session-response" : 37,
    "change-notification-request" : 38,
    "change-notification-response" : 39, 
    "modify-bearer-command" : 64,   
    "modify-bearer-failure-indication" : 65,
    "delete-bearer-command" : 66,   
    "delete-bearer-failure-indication" : 67,    
    "bearer-resource-command" : 68,   
    "bearer-resource-failure-indication" : 69,     
    "downlink-data-notify-failure-indication" : 70,
    "trace-session-activation" : 71,
    "trace-session-deactivation" : 72,
    "stop-paging-indication" : 73,
    "create-bearer-request" : 95,
    "create-bearer-response" : 96,
    "update-bearer-request" : 97,
    "update-bearer-response" : 98,
    "delete-bearer-request" : 99,
    "delete-bearer-response" : 100,
    "delete-pdn-connection-set-request" : 101,
    "delete-pdn-connection-set-response" : 102,      
    "realease-bearers-request" : 170,
    "realease-bearers-response" : 171,
    "downlink-data-notify" : 176,
    "downlink-data-notify-acknowledge" : 177,
}


class MobileNetworkIdentifier:
    def __init__(self, mcc = '222', mnc = '01'):
        self.__mcc = mcc
        if len(mnc) == 2 :
            mnc += "f"
        self.__mnc = mnc
                    
    def get_packed_val(self):
        hex_val =  self.__mcc[1]
        hex_val += self.__mcc[0]
        hex_val += self.__mnc[2]
        hex_val += self.__mcc[2]
        hex_val += self.__mnc[1]
        hex_val += self.__mnc[0]
        return bytearray.fromhex(hex_val)  


class AI :
    def __init__(self, mni, val = 0x00):
        self.__mni = mni  
        self.__val = val
        
    def get_packed_val(self):
        out = self.__mni.get_packed_val()
        out += struct.pack("!H", self.__val)
        return out

class LocationInformation:
    def __init__(self, lai, others = 0x00):
        self.__lai = lai
        self.__other = others

    def get_packed_val(self):
        out = self.__lai.get_packed_val()
        out += struct.pack("!H", self.__other)
        return out 

class ECGI:
    def __init__(self,mni, ecgi = 0x00):
        self.__mni = mni
        self.__ecgi = ecgi
    
    def get_packed_val(self):
        out = self.__mni.get_packed_val()
        out += struct.pack("!L", (self.__ecgi & 0x00ffffff))
        return out

#from TS 24.008 clause 10.5.6.3.1

ProtoIDType = {
    'PAP' : 0xC023,
    'LCP' : 0xC021,
    'CHAP': 0xC223,
    'IPCP': 0x8021,
    'PCSCFIPV6' : 0x0001,
    'IMCN' : 0x0002,
    'DNSIPV6': 0x0003,
    'MSS': 0x0005,
    'DSMIPV6A': 0x0007,
    'DSMIPV6N':0x0008,
    'DSMIPV6V4A':0x0009,
    'IPNAS': 0x000A,
    'IPDHCP': 0x000B,
    'PCSCFIPV4': 0x000C,
    'DNSIPV4': 0x000D,
    'MSISDNR': 0x000E,
    'IFOM': 0x000F,
    'MTUIPV4': 0x0010,
    'MSLA':0x0011,
    'PCSCFR': 0x0012,
    'NBIFOMRI': 0x0013,
    'NBIFOMM': 0x0014,
    'NOIPMTU': 0x0015,
    'APNRC': 0x0016,
    '3GPPPS': 0x0017,
    'RDSR': 0x0018,        
    }

class ProtocolID:
    def __init__(self, proto_id, data = ''):
        if data != '' :
            self.__data = data.get_packed()
        else:
            self.__data = data
        if not ProtoIDType.has_key(proto_id):
            raise Exception("invalid Proto ID %s"%(proto_id))
        self.__type = ProtoIDType[proto_id]
    
    def get_length(self):
        if type(self.__data) == str :
            return len(self.__data)
        return self.__data.get_length()
        
    
    def set_data(self, data):
        self.__data = data
        
    def get_packed(self):
        out = struct.pack("!HB", self.__type, self.get_length())
        out += self.__data
        return out
  
class PAPData:
    def __init__(self, peer_id = '', pwd = ''):
        self.__pwd = pwd
        self.__pwd_len = len(pwd)
        self.__peer_id = peer_id
        self.__peer_id_len = len(peer_id)
        self.__code = 0x01
        self.__identifier = 0x00
        self.__len = 6 + self.__pwd_len + self.__peer_id_len
        
    def get_packed(self):
        out = struct.pack("!BB", self.__code, self.__identifier)   
        out += struct.pack("!HB", self.__len, self.__peer_id_len)
       
        if self.__peer_id :
            out += self.__peer_id
        out += struct.pack("!B", self.__pwd_len)
        if self.__pwd :
            out += self.__pwd
        return out
    
    def get_length(self):
        return self.__len

class DNSServer :
    def __init__(self, type, dns="0.0.0.0"):      
        self.__type = int(type) # 1 byte

        self.__len = 0x06 # 1 byte
        self.__dns = int(IPy.IP(dns).strHex(), 16) #4 bytes
    
    def get_packed(self):
        return struct.pack("!BBL", self.__type, self.__len, self.__dns)

    def get_length(self):
        return self.__len 

            
class IPCPData:
    def __init__(self, p_dns = '0.0.0.0', s_dns = '0.0.0.0'):
        self.__code = 0x01
        self.__identifier = 0x00
        self.__len = 16
        self.__p_dns = DNSServer(129, p_dns)
        self.__s_dns = DNSServer(131, s_dns)
        
    def get_packed(self):
        out = struct.pack("!BBH", self.__code, self.__identifier, self.__len)
        out += self.__p_dns.get_packed()
        out += self.__s_dns.get_packed()
        return out
                      
    def get_length(self):
        return self.__len        
            
            
        
        
        
        
        