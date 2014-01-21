#! /usr/bin/env python
"""
 @ name = 'cipher.py'

 @ decription = 'encry file and decry file'

 @ author = ygrdhj
 @ 1-17-2014
"""
import os
import time
import shutil
from ctypes import *
BUFFER_LENGTH = 1024*1024*8
TEMP_FILE_NAME = "tempfile.txt"
AES_PATHNAME='./aes.so'

class Cipher(object):
    def __init__(self,ciphering_info):
        self.key = ciphering_info['key']
        pass
    def encrypt_file(self,des_file_name,src_file_name):
        pass
    def decrypt_file(self,des_file_name,src_file_name):
        pass
class AESCipher(Cipher):
    def __init__(self,ciphering_info):
        self.buffer_length = BUFFER_LENGTH
        self.tempfile = TEMP_FILE_NAME
        # if  'key' in ciphering_info:
        self.key = ciphering_info['key']
    def encrypt_file(self,des_file_name,src_file_name):
        '''
        1.two part:des_file_name == src_file_name and des_file_name
        2.before encrypt:add some padding('\0') to make filesize % 16==0
        3.in encrypt:first:use tempfile to write encrypt content.
        4.after encrypt:os.renames(des_file_name,tempfile)
        5.return value: os.path.getsize(des_file_name) if success else False
        '''
        try:
            pdll = CDLL(AES_PATHNAME)
        except OSError  as err:
            print "OSError happend",str(err)
            return False
        if not os.path.exists(src_file_name):
            print "src_file_name= %s is not exist!" % (src_file_name)
            return False
        filesize = os.path.getsize(src_file_name)
        if des_file_name == src_file_name:
            if filesize % 16 == 0:
                pdll.encrypt_file(self.key,self.tempfile,src_file_name,self.buffer_length)  
            else:
                strpad = '\0' * (16-(filesize % 16))
               # print "strpad",len(strpad)
                try:
                    with open(src_file_name,'ab') as fin:
                        fin.write(strpad)
                except IOError as err:
                    print "FILE Error:",str(err)
                    return False
                except ValueError as err:
                    print "Value Error",str(err)
                    return False
                except Exception as err:
                    print "Exception add padding happend error",str(err)
                    return False
               # print "des_file_name == src_file_name,encrypt_file happend"
                pdll.encrypt_file(self.key,self.tempfile,src_file_name,self.buffer_length)          
            try:
                os.renames(self.tempfile,src_file_name)
            except OSError as err:
                print "OSError happend",str(err)
                return False
            except Exception as err:
                print "Exception renames happend",str(err)
            return os.path.getsize(src_file_name)
        else:
           # print "des_file_name != src_file_name"
            des_file_path = os.path.dirname(des_file_name)
           #print 'des_file_path=',des_file_path
            if des_file_path:
                if not os.path.exists(des_file_path):
                    print des_file_path    
                    os.makedirs(des_file_path)
            if filesize % 16 == 0:
              #print "des------"
                pdll.encrypt_file(self.key,des_file_name,src_file_name,self.buffer_length)
              #print "heheh"
            else:
                # copy src_file_name to tempfile
                shutil.copyfile(src_file_name,self.tempfile)
                #add some padding to make filesize % 16 == 0
                strpad = '\0' * (16-(filesize % 16))
                try:
                    with open(self.tempfile,'ab') as fin:
                        fin.write(strpad)
                except IOError as err:
                    print "FILE Error:",str(err)
                    return False
                except ValueError as err:
                    print  "Value Error",str(err)
                    return False
               # print "encrypt_file,tempfile size is",os.path.getsize(self.tempfile)
                pdll.encrypt_file(self.key,des_file_name,self.tempfile,self.buffer_length)
                os.remove(self.tempfile)
            return os.path.getsize(des_file_name) 
             
    def decrypt_file(self,des_file_name,src_file_name):
        '''
        1.two part:des_file_name == src_file_name and des_file_name != src_file_name
        2.after decrypt:decrypt file may be have some padding(if encrypt file %16 !=0).we need delete
        some padding to recovery src_file_name
        3.delete padding char step:data = filehandler.seek(-16,0),len(data.rstrip('\0'))[padding number]
        the size of(src_file_name) = filesize[src_file_name] + len(data.strip('\0')) -16
        filehandler.truncate(size of(src_file_name))             
        '''
        try:
            pdll = CDLL(AES_PATHNAME)
        except OSError as err:
            print "OSError happend",str(err)
            return False
        if not os.path.exists(src_file_name):
            print "src_file_name=%s is not exist" % (src_file_name) 
            return False
        filesize = os.path.getsize(src_file_name)
        pdll.decrypt_file(self.key,self.tempfile,src_file_name,self.buffer_length)  
        if des_file_name == src_file_name:
            translate_filename = src_file_name
        else:
            des_file_path = os.path.dirname(des_file_name)
            if des_file_path:
                if not os.path.exists(des_file_path):
                    os.makedirs(des_file_path)
            translate_filename = des_file_name
        with open(self.tempfile,'rb') as fin:
            fin.seek(-16,2)
            data = fin.read(16)
           #print data
            string = data.rstrip('\0')
           #print "string length =",len(string)
            if not len(string):
                pass
            else:
               #print "before truncate filesize:",filesize
                filesize = filesize + len(string) -16
        fin = open(self.tempfile,'ab+')
        try:
            #print "filesize is ",filesize 
            fin.truncate(filesize)
        except Exception,e:
            print " Exception happend ",str(e)
            return False
        finally:
            fin.close()
            #print os.path.getsize(self.tempfile)
        try:
            os.renames(self.tempfile,translate_filename)
        except OSError as err:
            print "OSError happend ",str(err)
            return False
        return os.path.getsize(translate_filename)
        
