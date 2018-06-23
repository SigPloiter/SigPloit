#!/usr/bin/env python
# encoding: utf-8
#       teid_predictability_index.py
#       
#       Copyright 2018 Rosalia d'Alessandro 
#                     
#

#       Redistribution and use in source and binary forms, with or without
#       modification, are permitted provided that the following conditions are
#       met:
#       
#       * Redistributions of source code must retain the above copyright
#         notice, this list of conditions and the following disclaimer.
#       * Redistributions in binary form must reproduce the above
#         copyright notice, this list of conditions and the following disclaimer
#         in the documentation and/or other materials provided with the
#         distribution.
#       * Neither the name of the  nor the names of its
#         contributors may be used to endorse or promote products derived from
#         this software without specific prior written permission.
#       
#       THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS
#       "AS IS" AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT
#       LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR
#       A PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT
#       OWNER OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL,
#       SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT
#       LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE,
#       DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY
#       THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT
#       (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE
#       OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
#
##sudo apt-get upgrade python-setuptools
##sudo apt-get install python-pip python-wheel
##sudo pip install numpy 

from numpy import uint32, log2, unique
import time
from os import path

class TeidFixedPart(object):
    '''
    classdocs
    '''
        
    def __init__(self):
        '''
        Constructor
        '''        
        
    def teidFixedPart(self, teids):
        if teids is None or len(teids) == 0 :
            return 0, "No teids list provided"
        tmp = unique(teids).tolist()
        
        i = 0
        common_prefixs = []
        sub_set = tmp[i:i+2]
        run = True
        max_iter = len(tmp)
        while run :            
            cp = path.commonprefix(sub_set)
            if cp == "" or cp == "0x":
                common_prefixs.append(sub_set[0])
                sub_set = tmp[i:i+2]
                i = i + 1
            else :
                i += 2
                if i < max_iter :
                    sub_set = [cp, tmp[i]]
                else:  
                    common_prefixs.append(cp)
                    run = False              
                                        
        return common_prefixs    



class TeidPredictabilityIndex(object):
    '''
    classdocs
    '''


    def __init__(self):
        '''
        Constructor
        '''
    
    def __mod32Diff(self, a,b):
        tmp1 = abs(a - b)
        tmp2 = abs(b - a)
        tmp = min(tmp1, tmp2)
        return uint32(tmp)

    def __GCD(self, seq_diffs):
        if seq_diffs == []:
            raise Exception('no difference values')
        seq_len = len(seq_diffs)
        a = uint32(seq_diffs[0])  #a = *val;
        i = 0
        while i < (seq_len -1) :
            i += 1
            b = uint32(seq_diffs[i])
            if (a < b):
                a,b = b,a
            while b:
                a,b = b, uint32(a%b)
        return a

    def __calculateSeqDiffs(self, teids):
        seq_diffs = []
        i = 0
        seq_len = len(teids)
        if seq_len == 0:
            raise Exception("list of teids empty")
        if seq_len < 6 :
            raise Exception("list of teids too short, minimum 6 elements are required.")
        while i < (seq_len-1):
            t0 = teids[i]
            i += 1
            t1 = teids[i]
            seq_diffs.append(self.__mod32Diff(t0, t1))
        return seq_diffs

    def __calculateAVGSeqDiffs(self, seq_diffs):
        avg = 0
        for sd in seq_diffs:
            avg += sd
        return avg/len(seq_diffs)

    def __calculateModifiedStdSeqDiffs(self, seq_diffs, avg, gcd):
        if seq_diffs == []:
            raise Exception('no difference values')
        div_gcd = 1
        if gcd > 9 :
            div_gcd = gcd
        stddev = 0
        for sd in seq_diffs :
            rtmp = float((sd - avg)/ div_gcd)
            stddev += float(rtmp**2)
        stddev /= len(seq_diffs)
        return float(stddev**(1/2.0))
              
    def __calculateSeqIndex(self, stddev):
        seq_index = 0
        if stddev > 1 :
            stddev = log2(stddev);
            seq_index = int(stddev * 8 + 0.5)
        return seq_index

    def __seqIndex2DifficultyStr(self, seq_index) :
        if seq_index < 3 :
            return "Trivial joke"
        if seq_index < 6 :
            return "Easy"
        if seq_index < 11 :
            return "Medium"
        if seq_index < 12 :
            return "Formidable"
        if seq_index < 16 :
            return  "Worthy challenge"
        return "Teids not consecutives!";
    
    def teidPredictabilityIndex(self, teids):
        if teids is None or len(teids) == 0 :
            return 0, "No teids list provided"
        seq_diffs = self.__calculateSeqDiffs(teids)
        gcd = self.__GCD(seq_diffs)
        if gcd == 0:
            return 0, "FIXED TEIDS"
        if gcd < 0 :
            raise Exception("Negative GCD")
        avg = self.__calculateAVGSeqDiffs(seq_diffs)
        stddev = self.__calculateModifiedStdSeqDiffs(seq_diffs, avg, gcd)
        seq_index = self.__calculateSeqIndex(stddev)
        return seq_index, self.__seqIndex2DifficultyStr(seq_index)           
    