#!/usr/bin/env python
from cipher import AESCipher
import time
import os
ciphering_info = {'key':'1111111111111111'}
aes =  AESCipher(ciphering_info)
src_filename = 'test0'
des_filename = 'filename'
tempfile = 'test.txt'
print "encrypt_file begin"
items = []
for i in range(1):
    start_time = time.time()
    aes_length = aes.encrypt_file(des_filename,src_filename)
   # print "hello"
    end_time = time.time()
    duration =  end_time - start_time
    print duration
    items.append(duration)
print 'item',items
times = sum(items) / len(items)
print "the time is = %f,the speed is = %f MB/s" % (times,os.path.getsize(des_filename)/1024/1024/times)
print aes_length
print "decrypt_file begin"

detm = []

for i in range(1):
    start1_time = time.time()
    dec_length = aes.decrypt_file(tempfile,des_filename)
    #print "test decry"
    end1_time = time.time()
    duration1 = end1_time - start1_time
    detm.append(duration1)
print detm
time1 = sum(detm) / len(detm)
print "the time is =%f, the speed is = %f MB/s" % (time1,os.path.getsize(tempfile) /1024/1024/time1)
print dec_length 
