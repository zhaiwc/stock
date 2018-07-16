# -*- coding: utf-8 -*-
"""
Created on Mon Aug  7 17:33:25 2017

@author: 31394
"""

import pandas as pd
import numpy as np
import os
import pdb

class OperateFile():
    """
    本类主要实现读取文件
    1.读取txt文件
    2.读取csv文件
    3.保存txt文件
    4.保存csv文件
    
    """    
    def readtxt(self,path,filename,header = 1,skipfooter =1):
        file_path=path+filename;
        if os.path.exists(file_path):        
            df=pd.read_table(file_path,header = header,skipfooter=skipfooter)
            return df
        else:
            return None
                
    
    def readcsv(self,path,filename):
        file_path=path+filename;
        if os.path.exists(file_path):        
            df=pd.read_csv(file_path)
            df=pd.DataFrame(df)
            return df
        else:
            return None
            
    def savetxt(self,path,data):
        pass
        
    def savecsv(self,path,data):
        pass
       
    
if __name__=='__main__':
    A=OperateFile()
    path='E:\\基金策略\\FQData\\'
    filename='000001.txt'
    test=A.readtxt(path,filename)