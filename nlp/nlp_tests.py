#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Sep 29 12:13:46 2020

@author: pmchozas
"""

import csv
#import stanza
from csv import writer
from csv import reader
#from googletrans import Translator

#translator = Translator()
#stanza.download('es')
#nlp = stanza.Pipeline('es')
#pos_file = open('pos_redondo_2005.txt', 'w+')
poslist=[]
featlist=[]
translist=[]
source="redondo_2005"

#Este script añade traducciones y el pos a los datos de redondo 2005 (habría que pasar a función)
'''
with open('emofinder_base_redondo_2005.csv', 'r') as f:
    read = csv.reader(f)
    for row in read:
        emoterm=row[1]
        trans=translator.translate(emoterm, src='es', dest='en')
        transterm=trans.text
        translist.append(transterm)
        pos=nlp(emoterm)
        for sentence in pos.sentences:
            for word in sentence.words:
                poslist.append(word.upos)
                featlist.append(word.feats)
         
f.close()            

write_obj=open('outfile.csv', 'w',  newline='')

csv_writer=writer(write_obj)

with open('emofinder_base_redondo_2005.csv', 'r') as read_obj:
    csv_reader=reader(read_obj)
    i=0
    for row in csv_reader:
        row.append(poslist[i])
        row.append(featlist[i])
        row.append(translist[i])
        row.append(source)
        i=i+1
        csv_writer.writerow(row)


f.close()         

'''

#Este script saca la frecuencia del crea y las añade al archivo resultante anterior


e= open('../data/nlp_redondo_2005.csv', 'r') 
f= open('../data/CREA_total.csv', 'r')
emofile = csv.reader(e)
creafile=csv.reader(f, delimiter=';')


emowords=[]
freqset=[]
freqlist=list(creafile)
emolist=list(emofile)

resultlist=[]
count=0
for item in emolist:
    # print(item[1])
    for row in freqlist:
        # print(row[0])

        if item is not None and item[1] == row[0]:
            print('YES')
            count=count+1
            item1=item.append(row[1])
            newitem=item.append(row[2])
            if newitem is not None and newitem not in resultlist:
                resultlist.append(newitem)
                break
        else:
            #print(item)
            if item is not None and item not in resultlist:
                resultlist.append(item)
            

with open('../data/resultsredondo2005_2.csv', 'w', newline='') as myfile:
     writer = csv.writer(myfile, delimiter=';', quotechar='"')
     for item in resultlist:
         writer.writerow(item)


# código de ejemplo
'''
for emo_row in emolist:
    print(emo_row[1])
    row = 1
    found = False
    for freq_row in freqlist:
        print(freq_row[0])
        result_row = emo_row

        if emo_row[1] == freq_row[0]:
            print('Yes')
            result_row.append(emo_row[1]+'='+freq_row[0])
            found = True
            break
            row = row + 1
        if not found:
            result_row.append(emo_row[1]+' NOT FOUND')
'''
'''
f1 = file('hosts.csv', 'r')
f2 = file('masterlist.csv', 'r')
f3 = file('results.csv', 'w')

c1 = csv.reader(f1)
c2 = csv.reader(f2)
c3 = csv.writer(f3)

masterlist = list(c2)

for hosts_row in c1:
    row = 1
    found = False
    for master_row in masterlist:
        results_row = hosts_row
        if hosts_row[3] == master_row[1]:
            results_row.append('FOUND in master list (row ' + str(row) + ')')
            found = True
            break
        row = row + 1
    if not found:
        results_row.append('NOT FOUND in master list')
    c3.writerow(results_row)

f1.close()
f2.close()
f3.close()
   '''         

    
        
        
        

        
        
        
        
        
        
        
        
        
        
        
        
