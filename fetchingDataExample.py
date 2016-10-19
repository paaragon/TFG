# -*- coding: utf-8 -*-
"""
Created on Wed Oct 19 14:09:47 2016

@author: slide22
"""

from infoRiegoData import dataManager as dM

dM.downloadData(2001, 2001, 'zipFiles/')
dM.uncompressData('zipFiles/', 'csvFiles/')