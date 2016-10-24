# -*- coding: utf-8 -*-
"""
Created on Wed Oct 19 14:09:47 2016

@author: slide22
"""

from infoRiegoData import dataManager as dM
from infoRiegoData import csvManager as cM
import pandas

dM.downloadData(2001, 2002, 'data/zipFiles/')
dM.uncompressData('data/zipFiles/', 'data/csvFiles/')
dM.correctCharacters('data/csvFiles/')

conditions = dict()
conditions['dateStart'] = 20010101
conditions['dateEnd'] = 20020101
conditions['hourStart'] = 100
conditions['hourEnd'] = 200
conditions['ubication'] = ['Nava de Arevalo']

cM.createCSVWithConditions('data/csvFiles/', 'data/filteredFile.csv', conditions)

df = pandas.read_csv('data/filteredFile.csv')
print df