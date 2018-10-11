#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
0905更新日志：
2017-2018年的数据不使用 第0列(A)的chatid，改用第13列的reference_id
"""
import re
import csv
import sys
import os

if len(sys.argv)>1:
    arr = os.listdir(sys.argv[1])
else:
    arr = os.listdir()

#print (arr)

arr_csv = [b for b in arr if b[-4:]=='.csv']

print (arr_csv)

output_file = [b[:-4]+"_extraction_0905.txt" for b in arr_csv]

print (output_file)

#%%

for ind, file_name in enumerate(arr_csv):

    with open(file_name,encoding='ISO-8859-1') as f:
        reader = csv.reader(f)
     #   next(reader) # skip header
        data = [r for r in reader]    


    new_text = "Reference ID\tChat Turn\n"


    for index, row in enumerate(data):
        if index<1:
            continue
        if row[16] is None or len(row[16])<50:
            continue
        
        #get agent name
        agent_name = row[16][28:31]
        
        if agent_name[0] =='&':
            agent_name = row[16][34:37]
            
        sents_ = [b for b in re.split(r'\n',row[16])]
        sents = [b[13:] for b in sents_]
        
        matches = [b[:3]==agent_name for b in sents]
        
       # print (index,matches)

        #如果客服的名字没有出现在对话中，或者甄别失败，跳过
        if True not in matches[1:]:
            continue
        
        id_num = 0
        flag_new_chunk = 0
        chunk = ""
        buff = ""
            
        for a,b in zip(sents[1:],matches[1:]):
            
            if (a.find("' disconnected (",0,40)>0):
                if len(chunk)>0:
                    check_buff = str(row[13])+"-"+str(id_num)+"\t"+chunk+"\n"
                    if check_buff != buff:
                        new_text += str(row[13])+"-"+str(id_num)+"\t"+chunk+"\n"
                continue

            #chunk = ""

            if b is not True:
                client_text_pos =a.find(": ",0,50)
                client_text = a[client_text_pos+2:]
                
                if flag_new_chunk == 0:
                    chunk = client_text+ " "
                    id_num += 1
                    flag_new_chunk = 1
                else:
                    chunk += client_text+ " "
                    
            else:
                if flag_new_chunk == 0:
                    continue
                else:
                    if len(chunk)>0:
                      
                        buff = str(row[13])+"-"+str(id_num)+"\t"+chunk+"\n"
                        new_text += str(row[13])+"-"+str(id_num)+"\t"+chunk+"\n"
                        flag_new_chunk = 0
                        continue
    """
    @0905
    更新：
    1. ref-id不是chat-id 将第一行的row[0]改为row[13]
    
    """

    text_file = open(output_file[ind], "w")

    text_file.write(new_text)

    text_file.close()

