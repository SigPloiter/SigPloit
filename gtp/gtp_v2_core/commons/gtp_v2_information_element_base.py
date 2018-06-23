'''
Created on 12 Sep 2017

@author: lia
'''
import random
import struct

from IPy import IP
import gtp_v2_commons 

'''
    8     7     6     5     4     3     2     1    Octets
+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
|                 Type = xxx (decimal)          |   1
+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
|                 IE Length (n)                 |  2-3
|                                               |
+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
|       Spare           |    Instance           |  4
+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
|                IE Specific data or content    | 5-(5+n)
|                    of grouped IE              |
|                                               |
+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+

'''
      
        
class InformationElementBase(object):
    '''
    Virtual base class for an information element
    '''

    def __init__(self, ie_type):
        '''
        Constructor
        '''
        if not isinstance(ie_type, int) :
            raise TypeError('Invalid IE Type %s.Expected int.'%(str(type(ie_type))))
        if self.__is_reserved(ie_type) :
            raise Exception("Invalid IE Type")
        self.__ie_type = ie_type
        self._len = 0 #the length of the TLI fields shall not be included
        self.__instance = 0x00
        self.__spare = 0x00
    
    def __is_reserved(self, ie_type):
        
        if ie_type in gtp_v2_commons.RESERVED_IE_TYPES:
            return True
        return False
    
    def __get_packed_hdr(self):
        hdr = struct.pack("!B", self.__ie_type)
        hdr += struct.pack("!H", self._len)
        other_data = (self.__spare << 4) + (self.__instance & 15)
        hdr += struct.pack("!B", other_data)
        return hdr        
    
    def _get_val(self):
        return
        
    
    def get_packed_ie(self):
        return (self.__get_packed_hdr() + self._get_val())
    
    def get_total_len(self):
        return self._len + 4


class UserLocationInformation(InformationElementBase) :
    def __init__(self, mcc = "222", mnc = "01", lac = 0x00, sac = 0x00, 
                 tac = 0x00, rac = 0x00, cgi = 0x00, ecgi = 0x00):
        InformationElementBase.__init__(self, 86)
        self._len = 1
        
        mni = gtp_v2_commons.MobileNetworkIdentifier(mcc, mnc)
       
        self.__lai = self.__sai = self.__tai = self.__rai = self.__cgi = \
        self.__ecgi = None
        self.__flags = 0x00
        if lac :
            self.__lai = gtp_v2_commons.AI(mni = mni, val = lac)
            self._len += 5
            self.__flags = (self.__flags | (1 << 5))
            if sac :
                self.__sai = gtp_v2_commons.LocationInformation(lai = self.__lai, 
                                                                others = sac)
                self._len += 7
                self.__flags = (self.__flags | (1 << 1))
            if rac :
                self.__rai = gtp_v2_commons.LocationInformation(lai = self.__lai, 
                                                                others = rac)
                self._len += 7
                self.__flags = (self.__flags | (1 << 2))
            if cgi :
                self.__cgi = gtp_v2_commons.LocationInformation(lai = self.__lai, 
                                                                others = cgi)
                self._len += 7
                self.__flags = (self.__flags | 1)                
        if tac :
            self.__tai = gtp_v2_commons.AI(mni = mni, val = tac)    
            self._len += 5
            self.__flags = (self.__flags | (1 << 3))
        if ecgi:
            self.__ecgi = gtp_v2_commons.ECGI(mni = mni, ecgi = ecgi)
            self._len += 7
            self.__flags = (self.__flags | (1 << 4))
    
    def _get_val(self):      
        out = struct.pack("!B", self.__flags)
        if self.__cgi :
            out += self.__cgi.get_packed_val() 
        if self.__sai :
            out += self.__sai.get_packed_val()
        if self.__rai :
            out += self.__rai.get_packed_val()
        if self.__tai :
            out += self.__tai.get_packed_val()
        if self.__ecgi :
            out += self.__ecgi.get_packed_val()
        if self.__lai :
            out += self.__lai.get_packed_val()            
        return out  
      
class Imsi (InformationElementBase):    
    
    def __init__(self, imsi = "222015500003199") :
        InformationElementBase.__init__(self, 1)
        if len(imsi) != 15 :
            raise Exception("invalid imsi length %d"%(len(imsi))) 
        self.__val =  imsi
        self._len = 8
    
    def _get_val(self):
        i = 0
        hex_imsi = ''
        while i < 13 :
            c1 = self.__val[i]
            c2 = self.__val[i+1]
            hex_imsi += c2
            hex_imsi+=c1
            i += 2

        hex_imsi += ("f" + self.__val[14])
        
        if gtp_v2_commons.DEBUG :
            print "imsi :", self.__val
            print "hex imsi:", hex_imsi
        return bytearray.fromhex(hex_imsi)
    
class Msisdn(InformationElementBase):
    def __init__(self, msisdn="393356534399"):
        InformationElementBase.__init__(self, 76)
        self.__val = str(msisdn)
        self._len = 6
    
    def _get_val(self):
        length = len(self.__val)
        to_append = ''
        if length % 2 != 0 :
            length = length - 1
            to_append = 'f' + self.__val[length]
        hex_val = ''
        i = 0
        while i < (length - 1) :
            c1 = self.__val[i]
            c2 = self.__val[i+1]
            hex_val += c2
            hex_val +=c1
            i += 2
        hex_val += to_append
        return bytearray.fromhex(hex_val)

class eMLLPPPriority(InformationElementBase):
    def __init__(self, priority):
        InformationElementBase.__init__(self, 134)
        self.__val = str(priority)
        self._len = 6
        
    def _get_val(self):
        length = len(self.__val)
        to_append = ''
        if length % 2 != 0 :
            length = length - 1
            to_append = 'f' + self.__val[length]
        hex_val = ''
        i = 0
        while i < (length - 1) :
            c1 = self.__val[i]
            c2 = self.__val[i+1]
            hex_val += c2
            hex_val +=c1
            i += 2
        hex_val += to_append
        return bytearray.fromhex(hex_val)
    
class ApnRestriction(InformationElementBase):
    
    def __init__(self, val = 0):
        if val < 0 or val > 5 :
            raise Exception("invalid apn restriction value %d"%(val))
        InformationElementBase.__init__(self, 127)
        self._len = 1    # 2 bytes
        self.__val = val # 1 byte
    
    def _get_val(self):
        return struct.pack("!B", self.__val)

class RatType(InformationElementBase):
    # expected values:
    # 1 UTRAN
    # 2 GERAN
    # 3 WLAN
    # 4 GAN
    # 5 HSPA Evolution
    # 6 E-UTRAN
    # Other values out of scope
    # 0 reserved    
    # 7-255 spare    
    def __init__(self, rat_type = 'E-UTRAN'):
        InformationElementBase.__init__(self, 82)
        self._len = 1 # 2 bytes
        if not gtp_v2_commons.RATTypeDigit.has_key(rat_type) :
            raise Exception("invalid rat type: %d"%(rat_type))
        self.__val = gtp_v2_commons.RATTypeDigit[rat_type] #1 byte
        
    def _get_val(self):
        return struct.pack("!B", self.__val)
    
class AccessPointName(InformationElementBase):
    def __init__(self, apn = "ggsn3.tilab.it") :
        InformationElementBase.__init__(self, 71)      
        self._len= len(apn)# 2 bytes
        self.__val = apn
        
    def _get_val(self):
        return self.__val      
    
class MEIdentity(InformationElementBase) :
    def __init__(self, imei = "3518280450609004") :
        if len(imei) != 16 :
            raise Exception("invalid imei length %d"%len(imei)) 
        InformationElementBase.__init__(self, 75)           
        self._len = 8    #2 bytes
        self.__val = imei # 8 bytes
            
    def _get_val(self):
        i = 0
        hex_imei=''
        while i < 15 :
            c1 = self.__val [i]
            c2 = self.__val [i+1]
            hex_imei+= c2
            hex_imei+=c1
            i += 2
        if gtp_v2_commons.DEBUG:
            print "imei:", self.__val 
            print "hex imei:", hex_imei
        return bytearray.fromhex(hex_imei)   

class ServingNetwork(InformationElementBase):
    def __init__(self, mcc = "222", mnc = "01"):
        InformationElementBase.__init__(self, 83)
        self._len = 3
        self.__val = gtp_v2_commons.MobileNetworkIdentifier(mcc, mnc)    
        
    def _get_val(self):
        return self.__val.get_packed_val()

class FTeid(InformationElementBase):
    def __init__(self, sender_ip, interface):
        if interface > 37 :
            raise Exception('Invalid 3gpp interface %d'%(interface))
      
        InformationElementBase.__init__(self, 87)
        self._len = 9
        self.__ip = int(IP(sender_ip).strHex(), 16) #4 bytes
        self.__3gpp_interface = interface 
        
        self.__ip_ver_flag = (1 << 7)
        
        self.__teid = random.getrandbits(32)
    
    def _get_val(self):
        
        return struct.pack("!BLL", (self.__ip_ver_flag | self.__3gpp_interface),
                           self.__teid, self.__ip) 
    def get_teid(self):
        return self.__teid

class SelectionMode(InformationElementBase):
    def __init__(self, selection_mode = 0):
        InformationElementBase.__init__(self, 128)
        if selection_mode < 0 or selection_mode > 2 :
            raise Exception("Invalid Selection Mode %d"%(selection_mode)) 
        self._len = 1
        self.__val = selection_mode
     
    def _get_val(self):
        return struct.pack("!B", self.__val)    
        
class Recovery(InformationElementBase):
    def __init__(self, rc = 0):
        InformationElementBase.__init__(self, 3)
        self._len = 1 # 1 byte
        self.__val = rc
        
    def _get_val(self):
        return struct.pack("!B", self.__val)
        
class UETimeZone:
    def __init__(self):
        InformationElementBase.__init__(self, 114)
        self._len = 2 # 2 byte
        self.__tz = 128 #1 byte
        self.__dl = 1 # 1 byte
    
    def _get_val(self):
        return struct.pack("!BB", self.__tz, self.__dl)

class ChargingCharacteristic(InformationElementBase):
    def __init__(self, cc = 0x00):
        InformationElementBase.__init__(self, 95)
        self._len = 2
        self.__val = cc
    
    def _get_val(self):
        return struct.pack("!H", self.__val)

class AggregateMaximumBitRate(InformationElementBase):
    def __init__(self, uplink = 50000, downlink = 150000):
        InformationElementBase.__init__(self, 72)
        self._len = 8
        self.__ambr_up = uplink
        self.__ambr_down = downlink
    
    def _get_val(self):
        return struct.pack("!LL", self.__ambr_up, self.__ambr_down)

class PDNAddressAllocation(InformationElementBase):
    def __init__(self, pdn_type = 1, ip = '0.0.0.0'): 
        InformationElementBase.__init__(self, 79)         
        if pdn_type == 1:
            self._len = 5
            self.__ip = int(IP(ip).strHex(), 16)
        elif pdn_type == 2:
            self._len = 18
            self.__ip = bytearray.fromhex(IP(ip).strHex()[2:])
        elif pdn_type == 3:
            self._len = 22
            self.__ip = bytearray.fromhex(IP(ip).strHex()[2:])
        else:
            raise Exception('Invalid PDN Type %d'%(pdn_type))
        self.__pdn_type = pdn_type
        
    def _get_val(self):
        if self._len == 5:
            return struct.pack('!BL', self.__pdn_type, self.__ip)
        return struct.pack('!B', self.__pdn_type) +  self.__ip              
            
class EPSBearerID(InformationElementBase):
    def __init__(self, ebi = 5):
        if ebi >= 1 and ebi <= 4 :
            raise Exception("Reserved EBI %d"%(ebi))
        elif ebi > 15:
            raise Exception("Invalid EBI %d"%(ebi))    
        InformationElementBase.__init__(self, 73)    
        self._len = 1
        self.__val = ebi
        
    def _get_val(self):
        return struct.pack("!B", self.__val)

class BearerQoS(InformationElementBase):
    def __init__(self, pci = 0x01, pl = 0x02, pvi = 0x00, qci = 0x07, 
                 mbr_up = "0000000000", mbr_down = "0000000000", 
                 gbr_up = "0000000000", gbr_down = "0000000000"):
        InformationElementBase.__init__(self, 80)
        self._len = 22
        self.__flags = (pci <<  7) or (pl << 5) or pvi
        self.__qci = qci
        self.__mbr_up = mbr_up
        self.__mbr_down = mbr_down
        self.__gbr_up = gbr_up
        self.__gbr_down = gbr_down
    
    def _get_val(self):
        val = struct.pack("!BB", self.__flags, self.__qci) 
        val += bytearray.fromhex(self.__mbr_up)
        val += bytearray.fromhex(self.__mbr_down)
        val += bytearray.fromhex(self.__gbr_up)
        val += bytearray.fromhex(self.__gbr_down)
        return val
        
class BearerContext(InformationElementBase):
    def __init__(self, ip, ebi = 5, pci = 0x01, pl = 0x02, pvi = 0x00, qci = 0x07, 
                 mbr_up = "0000000000", mbr_down = "0000000000", 
                 gbr_up = "0000000000", gbr_down = "0000000000",
                 interface = 10):
        InformationElementBase.__init__(self, 93)
        self.__ebi = EPSBearerID(ebi)
        self.__teid = FTeid(ip, interface)
        self.__bqos = BearerQoS(pci, pl, pvi, pci, mbr_up, mbr_down, gbr_up, 
                                gbr_down)
        self._len = self.__ebi.get_total_len() + self.__bqos.get_total_len() +\
                    self.__teid.get_total_len()
    
    def _get_val(self):
        return (self.__ebi.get_packed_ie() + self.__bqos.get_packed_ie() + 
                self.__teid.get_packed_ie())
        
class ProtocolConfigurationOptions(InformationElementBase):
    def __init__(self, p_dns = '0.0.0.0', s_dns = '0.0.0.0', pwd = '', 
                 peer_id = ''):
        InformationElementBase.__init__(self, 78)
        self.__octet_three = 0x80
        self.__proto = []
    
        self.__proto.append(gtp_v2_commons.ProtocolID(proto_id = 'PAP', 
                        data = gtp_v2_commons.PAPData(pwd, peer_id)))

        self.__proto.append(gtp_v2_commons.ProtocolID(proto_id = 'IPCP', 
                        data = gtp_v2_commons.IPCPData(p_dns, s_dns)))
       
        self.__proto.append(gtp_v2_commons.ProtocolID(proto_id = 'DNSIPV4'))
       
        self.__proto.append(gtp_v2_commons.ProtocolID(proto_id = 'IPNAS'))
       
        self._len = 1
        for i in self.__proto :

            self._len += i.get_length() + 3
        
    
    def _get_val(self):
        out = struct.pack(("!B"), self.__octet_three)
        for i in self.__proto:
            out += i.get_packed()
        return out

class Cause(InformationElementBase):
    def __init__(self, cause = 16):
        InformationElementBase.__init__(self, 2)
        self.__val = cause
        self._len = 2 # 2 bytes
        self.__spare = 0x00
        
    def _get_val(self):
        return struct.pack("!BB", self.__val, self.__spare)

class FQCSID(InformationElementBase):
    def __init__(self, node_id_type = 0, ip = "127.0.0.1", mcc = 222, mnc = 88):
        InformationElementBase.__init__(self, 132)
        if (node_id_type != 0 and  node_id_type != 2):
            raise Exception("Unsupported node type id %d"%(node_id_type))
        self.__node_id_type = node_id_type
        self.__n_csids = 1
        if self.__node_id_type == 0:
            self.__node_id = bytearray.fromhex(IP(ip).strHex()[2:])           
        else:        
            self.__node_id = struct.pack("!L",
                (((mcc*1000 + mnc) & 0x000fffff) << 12) | 0x00000110)
        self.__csid = 1
        self._len = 7
            
    def _get_val(self):
        out = struct.pack(("!B"), (self.__node_id_type & 0xf0) + 0x0f & self.__n_csids)
        out += self.__node_id
        out += struct.pack("!H", self.__csid)
        return out
        return out        
