#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Sep 29 12:13:46 2020

@author: pmchozas
"""

import csv
import stanza
from csv import writer
from csv import reader
from googletrans import Translator

translator = Translator()
stanza.download('es')
nlp = stanza.Pipeline('es')
#pos_file = open('pos_redondo_2005.txt', 'w+')
poslist=[]
featlist=[]
translist=[]
source="redondo_2005"

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

