# -*- coding: utf-8 -*-
"""
Created on Mon Jul 16 20:38:47 2018

@author: 31394
"""
from DataAnalyseEngine.stock import Stock
st='2016-01-01'
et='2018-10-30'
A=Stock('000001')
#    print(A.qtdata)
rtn = A.N_period_return(st=st,et=et,N_period = 30 ,Type = 'f')
rtn = A.N_period_return(st=st,et=et,N_period = 30 ,Type = 'f')