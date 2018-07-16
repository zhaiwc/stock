# -*- coding: utf-8 -*-
"""
Created on Thu Aug 10 16:31:16 2017

@author: zhai
"""
import pdb
import math
from Get_Data.getTushareData import getTushareData 

import pandas as pd

class Industry(getTushareData):
    '''
    行业类
    该类用于创建单只股票的实例：
    实例属性：
    Industry_code: 行业代码
    Industry_name: 行业中文名
    Industry_stlist: 行业所包含的股票list
    
    实例方法：
    
    该类用于行业分析
    '''
    def __init__(self):
        getTushareData.__init__(self)
        self._stcode=None
#----------------属性输入控制--------------------------------------------        
    @property
    def stcode(self):
        return self._stcode
    @stcode.setter
    def stcode(self,value):
        if not isinstance(value,str):
            raise ValueError('code must be an string!')
        if value[0:2]!='00'  and value[0:2]!='30'  and value[0:2]!='60':
            raise ValueError('code must be start by 00 30 60!') 
        self._stcode=value    
#        self._Indcode=self.getstofIndustryList().Ind_code.iloc[0]
        
        
#---------------提取行业数据------------------------------------------------        
    def getIndustryList(self):
        return self.get_db_data('Industry_list')
        
    def getIndustryofallstList(self):
        return self.gettusharevalue('Industry_info')
        
#-------------获得该股票所在行业的所有股票---------------------------------        
    def getstofIndustryList(self):
        if self._stcode is None:
            print('---------请设置要查询行业的股票代码:stcode---------')
            return None
        else:
            BasicData=self.get_Basicdata()
            industry_name = BasicData.loc[self._stcode,'industry']
            return list(BasicData[BasicData['industry']==industry_name].index)
            
    def getIndtusharedata(self,keyname,colname_input,st=None,et=None):
        
        
#        st=parse(st)
#        st_n=int(str(st.year)+'0'+str(math.ceil(st.month/3)))
#        et=parse(et)
#        et_n=int(str(et.year)+'0'+str(math.ceil(et.month/3)))        
        
#        该股票所在行业的所有股票的code
        ths_stIndList=self.getstofIndustryList().code
        #        相关数据提取
        df=self.gettusharevalue(keyname)
        df= df[df['code'].isin(ths_stIndList)]
#        
        if colname_input =='*':
#            res=df[(df.findate>=st_n) & (df.findate<=et_n)]
            res=self.choosedate(df,st,et)
        else:
            colname=['findate','code','name',colname_input]
            colname=df.columns[df.columns.isin(colname)].tolist()
            res=self.choosedate(df[colname],st,et)
#            res=df[colname][(df.findate>=st_n) & (df.findate<=et_n)]
#        pdb.set_trace()
        res=res.drop_duplicates()
        return res.pivot('findate','code',colname_input)

        
        
        
if __name__=='__main__':
    A=Industry()
    A.stcode='000651'
    df = A.getstofIndustryList()
    print(df)
    
#    print(A.getstofIndustryList())
             
    