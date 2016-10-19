# -*- coding: utf-8 -*-
"""
Created on Wed Oct 19 14:09:47 2016

@author: slide22
"""

from infoRiegoData import dataManager as dM
from infoRiegoData import csvManager as cM

dM.downloadData(2001, 2001, 'zipFiles/')
dM.uncompressData('zipFiles/', 'csvFiles/')
dM.correctCharacters('csvFiles/')

conditions = dict()
conditions['dateStart'] = 20010101
conditions['dateEnd'] = 20010102
conditions['hourStart'] = 100
conditions['hourEnd'] = 200
conditions['ubication'] = ['Nava de Arevalo', 'Miranda de Ebro']

cM.createCSVWithConditions('csvFiles/', 'file.csv', conditions)

