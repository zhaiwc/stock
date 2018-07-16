# -*- coding: utf-8 -*-
"""
Created on Tue Aug  1 10:21:22 2017

@author: zhai
"""

import pdb 
import os
import numpy as np 
import pandas as pd
from OperateFile import OperateFile
from dateutil.parser import parse
from datetime import datetime
from LocalDB import LocalDB


class getQtData(OperateFile,LocalDB):
    '''
    本类主要实现：
    1.单只股票行情数据txt文件提取。----------------_getStockData
    2.所有股票行情数据保存至本地文件。--------------save_QTdata
    3.指定code的股票行情数据本地文件提取------------get_QTdata_LocalDB
    4.提取或有股票的codelist-----------------------get_all_code
    
    '''
    Qt_hfq_path='E:\\基金策略\\FQData\\'
    Qt_bfq_path='E:\\基金策略\\CQData_python\\'
    
    def __init__(self):
        LocalDB.__init__(self,'QT')
        
    @staticmethod    
    def get_all_code():
        path='E:\\基金策略\\FQData\\'
        txtlist=os.listdir(path)
        stlist=[x[0:6] for x in txtlist]
        stlist.remove('399300')
        return stlist
        
    def _getStockData(self,Code,fq='hfq'):
        if fq=='hfq':
            path=getQtData.Qt_hfq_path
        elif fq=='bfq':
            path=getQtData.Qt_bfq_path
            
        filename=Code+'.txt'
        
        df=self.readtxt(path,filename)
        
        if len(df) and df is not None:
            
            if len(df.columns)==1:
                df=df.T
            #----------------列名转换------------------------------------
            df.rename(columns={'      日期':'date','    开盘':'op','    最高':'hp','    最低':'lp','    收盘':'cp','    成交量':'vol','    成交额':'val'},inplace=True)
            C=pd.DataFrame(np.ones(len(df))*int(Code),columns=['Code'])
            df=pd.concat([C,df],axis=1)
            #---------------时间轴---------------------------------------
            datecol=[parse(str(int(x))) for x in df.date]
            df.date=datecol
            df=df.set_index('date')
            return df 
        else:
            print('---------------No Data!-------------------')
            return None
        
    def save_QTdata(self,fq='hfq'):
        codelist=getQtData.get_all_code()
        res=pd.DataFrame([])
        for code in codelist:
            print(code)

            df=self._getStockData(code,fq=fq)
            if df is not None:
                self.save_db_data(fq,df,code,by_code =True)
            
#            if df is not None:
#                res=pd.concat([res,df])
#        self.save_db_data(fq,res)
    
    def save_QTdata_index(self):
        code_index=['399300']
        res=pd.DataFrame([])
        for code in code_index:
            print(code)
            df=self._getStockData(code,fq='hfq')
            if df is not None:
                res=pd.concat([res,df])
        self.save_db_data('Index_QT',res,)
            
        
    def get_QTdata_LocalDB(self,code,st=None,et=None,fq='hfq'):
        '''
        提取股票的行情数据
        '''

        all_data=self.get_db_data(fq,code,by_code =True)

        if isinstance(code,str):
            code=int(code)
#            pdb.set_trace()
            chose_data=all_data[all_data.Code==code]
        elif isinstance(code,list):   
            code=[int(x) for x in code]
            chose_data=all_data[all_data.Code.isin(code)]
        else:
            print('------------------输入code错误-------------------')
            return None
        if len(all_data):
            if st is None and et is None:
                return chose_data
            else:
                if st is not None:
                    st=parse(st)
                else:
                    st=parse('1990-01-01')
                if et is not None:
                    et=parse(et)
                else:
                    et=datetime.now()
                return chose_data[(chose_data.index>=st)& (chose_data.index<=et)]                 
        else:
            print('---------------No Data!-------------------')
            return None
        
    def get_Ind_QTdata_LocalDB(self,code,st=None,et=None):
        '''
        提取指数的行情数据
        '''

        all_data=self.get_db_data('Index_QT')
        
        if isinstance(code,str):
            code=int(code)
            chose_data=all_data[all_data.Code==code]
            
        elif isinstance(code,list):   
            code=[int(x) for x in code]
            chose_data=all_data[all_data.Code.isin(code)]
        else:
            print('------------------输入code错误-------------------')
            return None
        if len(all_data):
            if st is None and et is None:
                return chose_data
            else:
                if st is not None:
                    st=parse(st)
                else:
                    st=parse('1990-01-01')
                if et is not None:
                    et=parse(et)
                else:
                    et=datetime.now()
                return chose_data[(chose_data.index>=st)& (chose_data.index<=et)]                 
        else:
            print('---------------No Data!-------------------')
            return None
if __name__=='__main__':

    A=getQtData()
#    A.save_QTdata()
    data = A.get_QTdata_LocalDB('000001',fq='hfq')
