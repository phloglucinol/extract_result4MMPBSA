#!/usr/bin/env python
# coding: utf-8

# In[ ]:


class File_line():
    
    def __init__(self, filename, search_pattern = None, mch_pattern = None, repl_pattern = None):
        self.filename = filename
        self.search_pattern = search_pattern
        self.mch_pattern = mch_pattern
        self.repl_pattern = repl_pattern
        self.PB_GB_dict = {}
        #self.rm_line = rm_line
    
    #Reading lines from file and save them into a dictionary.
    @property
    def rd_line(self):
        text_file = open(self.filename, 'rt')
        #Initialization
        text_dict = {}
        line_count = -1
        #read the lines from file
        for line in text_file:
            #line = line.strip()
            line_count+=1
            text_dict[line_count] = line
            #text_list.append(line)
        text_file.close()
        return text_dict
    
    @property
    def extract_PB_GB(self):
        target_dict = self.rd_line
        pb_mean = target_dict[31][11:23].strip()
        pb_std = target_dict[31][25:34].strip()
        gb_mean = target_dict[36][11:23].strip()
        gb_std = target_dict[36][25:34].strip()
        self.PB_GB_dict['pb_mean'] = pb_mean
        self.PB_GB_dict['pb_std'] = pb_std
        self.PB_GB_dict['gb_mean'] = gb_mean
        self.PB_GB_dict['gb_std'] = gb_std
        return self.PB_GB_dict

    

import os
import re
import csv

file_list = os.listdir()
matched_pattern = re.compile(r'.{2}-.{3}_.{8}-pbsa\.out')
matched_filelist = []
for file in file_list:
    if not matched_pattern.search(file) == None:
        matched_filelist.append(file)

final_dict = {}
for name in matched_filelist:
    locals()[name] = File_line(name)
    final_dict[str(name)] = locals()[name].extract_PB_GB

f = open('PB_GB_out.csv', 'w', encoding = 'utf-8', newline='')
csv_writer = csv.writer(f)
csv_writer.writerow(['ID', 'PB_MEAN(kcal/mol)','PB_STD','GB_MEAN(kcal/mol)', 'GB_STD'])

matched_id_pattern = re.compile(r'[A-Z]{2}-\d{3}_\d{8}')

for key, value in final_dict.items():
    csv_writer.writerow([''.join(re.findall(matched_id_pattern, key)), value['pb_mean'], value['pb_std'], value['gb_mean'], value['gb_std']])

f.close()

