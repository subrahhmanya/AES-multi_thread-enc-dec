AES-multi_thread-enc-dec
====================================

This project is base on the  AES of  c library . We Use Multi-thread to Optimization the speed of Encrypt and Decrypt. Through the study found.the number of thread exactly the Cpu Cores number,the performance best.By above ways.make a aes.so dynamic library to be call by python.the speed python call the aes.so is  faster than pycrypt which python library.

Usarge:
  1.  you have three size Encrypt/Decrypt Key length:128bits/192bits/256bits
  2.  fisrt: you need create a Enc/Dec Key .ciphering_info= {'key':'key_value'}
  3.  call aes.so(abspath) in the storage_cipher.py(.py is write by python.we use python write encrypt/decrypt to call aes.so to finish Encrypt/Decrypt)(build *.so :g++ -fPIC aes.c -o aes.so -shared)
  4.  aes = AESCipher(ciphering_info)  enc:aes.encrypt_file(des_filename,src_filename) dec:aes.decrypt_file(des_filename,src_filename) Among:des_filename ==/!= src_filename
  5.  Note:you must make sure aes.so is in you path.it in cipher.py line 16 AES_PATHNAME
  
for example:
  1.  ciphering_info = {'key':'0123456789012345'}
  2.  aes = AESCipher(ciphering_info)
  3.  aes.encrypt_file(des_filename,src_filename)
  4.  aes.decrypt_file(des_filename,src_filename)
   
Design Factors:
  1. it only support ecb AES style.THe key length is 128bits/192bits/256bits
  2. you can by modify THREADS_COUNT or THREADS_BUFF_SIZE to choice use diff Encrypt/Decrypt way(single thread/multi_thread or buff_size and so on)
  3. you can modify aes.c line 919(for Encrypt ,line 1083 for Decrypt) ,use int THREADS_COUNT = get_nprocs();to replace #define THREADS_COUNT to according  the Cpu Cores to dynamic choice the Threads numbers.
  4. we use FILE_SIZE(line 781 in aes.c)  to make choice single_thread or multi_thread
  

Test:
  you can use test.py to test.In the test,we use time.time() to test the speed of Encrypt and Decrypt
  
