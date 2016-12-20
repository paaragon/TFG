# -*- coding: utf-8 -*-
"""
Created on Wed Oct 19 14:09:47 2016

@author: slide22
"""

from infoRiegoData import dataManager as dM
from infoRiegoData import csvManager as cM
import pandas

#dM.downloadData(2015, 2015, 'data/zipFiles/')
#dM.uncompressData('data/zipFiles/', 'data/csvFiles/')
#dM.correctCharacters('data/csvFiles/')

conditions = dict()
conditions['dateStart'] = 20150601
conditions['dateEnd'] = 20150930
conditions['hourStart'] = 800
conditions['hourEnd'] = 2000
conditions['ubication'] = ['Nava de Arevalo']

cM.createCSVWithConditions('data/csvFiles/', 'data/filteredFile.csv', conditions, verbose = False)

df = pandas.read_csv('data/filteredFile.csv')
#print df