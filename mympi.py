# from mpi4py import MPI
import hashlib
import sys
from sys import exit
import time
import math

#ba7816bf8f01cfea414140de5dae2223b00361a396177a9cb410ff61f20015ad
#abc

comm = MPI.COMM_WORLD
rank = comm.Get_rank()
size = comm.Get_size()
name = MPI.Get_processor_name()
maxLen = 5

char_list = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z']
index_temp = {}
for i in range(len(char_list)) :
    index_temp[char_list[i]] = i

def split_code (node_size) :
    my_suffle_list = set()
    temp_char_list = char_list + ['']
    for i in range(len(temp_char_list)) :
        for j in range(len(temp_char_list)) :
            my_suffle_list.add(temp_char_list[i] + temp_char_list[j])
    my_suffle_list.remove('')
    my_suffle_list = list(my_suffle_list)
    working_list = []
    for i in range(node_size) : 
        working_list.append([])
    for i in range(len(my_suffle_list)) :
        working_list[i%node_size].append(my_suffle_list)
    
    return char_list


def next_code (current) : 
    if current == '' : return char_list[0]  
    for i in range(len(current)-1, -1, -1) :
        s = current[i]
        if s == char_list[-1] : continue
        else :
            result = current[:i] + char_list[index_temp[s]+1] + current[i+1:]
            return result
    return ''.join([char_list[0] for x in range(len(current)+1)])

def check_sha(encr, code) :
    hashStr = str(hashlib.sha256(code.encode('utf-8')).hexdigest())
    if hasattr == encr :
        message = {"found": True, "result": code}
        comm.send(message, dest=0, tag=1)
        return True
    return False


##-=====================
if rank == 0:
    
    encrypt = '36bbe50ed96841d10443bcb670d6554f0a34b761be67ec9c4a8ad2c0c44ca42c'
    clear_text = 'abcde'
    start_time = time.time()
    
    init_list = split_code(size-1)
    
    for i in range(1, size): 
        message = {"encrypt": encrypt, "list": init_list[i-1]}
        comm.send(message, dest=i, tag=0)
    
    while True :
        for j in range(1, size):
            res = comm.recv(source=j, tag=1)
            found = res.get('found')
            if found :
                decrypted = res.get("result")
                print ("the result :" + decrypted)
                for i in range(1,size):
                    newMessage = {"shutdown": True}
                    comm.send(newMessage, dest=i,tag=0)
                exit()

# Compute node
else :
    while True :
        data = comm.recv(source=0, tag=0)
        encr = data.get("encrypt")
        my_list = data.get('list')
        for code in my_list :
            current = ''
            while True :
                current = next_code(current)
                current_code = code + current
                if (check_sha(encr, current_code)) :
                    break
        

            
