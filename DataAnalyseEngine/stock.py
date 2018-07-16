# -*- coding: utf-8 -*-
"""
Created on Thu Aug 10 16:35:53 2017

@author: zhai
"""
import pdb
import numpy as np
import pandas as pd
from Get_DataFile.getQtData import getQtData
from Get_DataFile.getTechdata import getTechdata
from Get_DataFile.LocalDB import LocalDB 
from DataAnalyseEngine.Factor import Tech_Index
#import python.Get_DataFile
class Stock(getQtData,getTechdata):
    '''
    股票类
    该类用于创建单只股票的实例：
    实例属性：
    code:股票代码
    chname:股票中文名
    Industry:股票所属行业
    实例方法：
    get_QTdata_hfq:股票后复权行情数据
        QTdata_bfq:股票不复权行情数据
    get_Findata_BS:股票资产负债表数据
        Findata_IS:股票利润表数据
        Findata_CF:股票现金流表数据
        Findata_Fa:股票财务因子数据
    PE:计算该股的PE
    N_period_return:N日收益率,Type:f:  N日前到现在的收益率  b:现在到N日后的收益率
                                  
    '''
    def __init__(self,code):
        getQtData.__init__(self)
        getTechdata.__init__(self)
        self.code=code
        self.qtdata=self.getQtdata()
    

#  -----------------提取行情数据,技术指标----------------------------------------------
    def getQtdata(self,st=None,et=None,fq='hfq'):
        return self.get_QTdata_LocalDB(self.code,st,et,fq=fq)
    
    def getTechdata(self,st=None,et=None):
        return self.get_Techdata(self.code,st,et)
        
#  -----------------提取tushare数据----------------------------------------------        
    def getsttusharedata(self,keyname):
        df=self.gettusharevalue(keyname)
        if df is not None:
            return df[df.code==self.code]
        else:
            return None
            
    
    def getForecastdt(self,st,et):
        df=self.getsttusharedata('Forecast')
        return self.choosedate(df,st,et)
        
    def getReportdt(self,st,et):    
        df= self.getsttusharedata('Report')
        return self.choosedate(df,st,et)
        
    def getProfitdt(self,st,et):
        df= self.getsttusharedata('Profit')
        return self.choosedate(df,st,et)
        
    def getOperationdt(self,st,et):
        df= self.getsttusharedata('Operation')
        return self.choosedate(df,st,et)
        
    def getGrowthdt(self,st,et):
        df= self.getsttusharedata('Growth')
        return self.choosedate(df,st,et)
        
    def getdebtpayingdt(self,st,et):
        df= self.getsttusharedata('Debtpaying')
        return self.choosedate(df,st,et)
        
    def getcashflowdt(self,st,et):
        df= self.getsttusharedata('cashflow')
        return self.choosedate(df,st,et)

#  -----------------计算数据----------------------------------------------  
    def period_return(self,st=None,et=None):
        '''
        计算st,et区间内的收益率。
        '''
        if st is None and et is None:
            qt_data=self.qtdata
        else:
            qt_data=self.qtdata
            qt_data=qt_data[(qt_data.index>=st)&(qt_data.index<=et)]
   
        return (qt_data.cp.iloc[-1] - qt_data.cp.iloc[0])/qt_data.cp.iloc[0]
    
    def N_period_return(self,st=None,et=None,N_period=1,lag=[0],Type='b'):
#        qt_data=self.getQtdata(st,et)

        '''
        未来或者过去N天的收益率。
        '''
        if st is None and et is None:
            qt_data=self.qtdata
        else:
            qt_data=self.qtdata
            qt_data=qt_data[(qt_data.index>=st)&(qt_data.index<=et)]
            
        cp=pd.DataFrame(qt_data.cp,columns={'cp'})       
        res=pd.DataFrame([])
        
        if Type=='f': #f:  N日前到现在的收益率 
            cp_rtn=cp.pct_change(N_period)       
            cp_rtn=pd.DataFrame(cp_rtn).rename(columns={'cp':'rtn'})
        else:
            cp_rtn=cp.pct_change(N_period)       
            cp_rtn=pd.DataFrame(cp_rtn).rename(columns={'cp':'rtn'})
            nanmat1=np.ones(N_period)*np.nan
            nanmat1=pd.DataFrame(nanmat1,index=cp.index[-N_period:],columns={'rtn'})
            cp_rtn=pd.concat([cp_rtn.iloc[N_period:],nanmat1])
            cp_rtn.index=cp_rtn.index
        return cp_rtn
        
#        for ilag in lag:
##            pdb.set_trace()
#            cp_lag=Tech_Index.lag(cp,ilag)
#            if Type=='f': #f:  N日前到现在的收益率 
#                cp_rtn_temp=cp_lag.pct_change(N_period)       
#                cp_rtn_temp=pd.DataFrame(cp_rtn_temp).rename(columns={'cp':'rtn'})
#            elif Type=='b': # b:现在到N日后的收益率
#                cp_rtn=cp_lag.pct_change(N_period)       
#                cp_rtn_temp=pd.DataFrame(cp_rtn).rename(columns={'cp':'rtn'})
#                if ilag>0:
#                    nanmat1=np.ones(N_period)*np.nan
#                    nanmat2=np.ones(ilag)*np.nan
#                    nanmat1=pd.DataFrame(nanmat1,index=cp.index[-N_period:],columns={'rtn'})
#                    nanmat2=pd.DataFrame(nanmat2,index=cp.index[-ilag:],columns={'rtn'})
#                    cp_rtn_temp=pd.concat([nanmat2,cp_rtn_temp.iloc[ilag+N_period:],nanmat1])
#                    cp_rtn_temp.index=cp_rtn.index
#                else:
#                    nanmat1=np.ones(N_period)*np.nan
#                    nanmat1=pd.DataFrame(nanmat1,index=cp.index[-N_period:],columns={'rtn'})
#                    cp_rtn_temp=pd.concat([cp_rtn_temp.iloc[ilag+N_period:],nanmat1])
#                    cp_rtn_temp.index=cp_rtn.index
#            
#            res=pd.concat([res,cp_rtn_temp],axis=1)
#                                
#        return res
    
    def N_period_mean_rtn(self,st=None,et=None,N_period=1,lag=[0],):
        '''
        未来或者过去N天的均价的收益率。
        
        '''
        if st is None and et is None:
            qt_data=self.qtdata
        else:
            qt_data=self.qtdata
            qt_data=qt_data[(qt_data.index>=st)&(qt_data.index<=et)]
        pdb.set_trace()
#        tot_val=pd.rolling_sum()
#        mean_cp=pd.DataFrame()
    def MA_Vol_change(self,st=None,et=None,N_period=5,lag=[0],Type='b'):
        
        '''
        当日交易量与MA（N）交易量比较
        '''
#        qt_data=self.getQtdata(st,et)
        if st is None and et is None:
            qt_data=self.qtdata
        else:
            qt_data=self.qtdata
            qt_data=qt_data[(qt_data.index>=st)&(qt_data.index<=et)]
        vol=pd.DataFrame(qt_data.vol,columns={'vol'})   
        res=pd.DataFrame([])

        for ilag in lag:
            vollag=Tech_Index.lag(vol,ilag)
            vol_change=vollag/vollag.rolling(window=N_period,center=False).mean()
            vol_change=pd.DataFrame(vol_change).rename(columns={'vol':'vol_change'})
            res=pd.concat([res,vol_change],axis=1)    
        return res
    
    def HL_Rtn(self,st=None,et=None,lag=[0]):
        '''
        当日最高价与最低价的比较收益
        '''
        
#        qt_data=self.getQtdata(st,et)
        if st is None and et is None:
            qt_data=self.qtdata
        else:
            qt_data=self.qtdata
            qt_data=qt_data[(qt_data.index>=st)&(qt_data.index<=et)]
        hp=pd.DataFrame(qt_data.hp,columns={'hp'})
        lp=pd.DataFrame(qt_data.lp,columns={'lp'})
        res=pd.DataFrame([])
        
        for ilag in lag:
            hplag=Tech_Index.lag(hp,ilag)           
            lplag=Tech_Index.lag(lp,ilag)
            hl_rtn=pd.DataFrame((hplag.hp-lplag.lp)/lplag.lp,columns={'HL_rtn'})
            res=pd.concat([res,hl_rtn],axis=1)
        return res
    
    def OC_Rtn(self,st=None,et=None,lag=0):
        '''
        当日开盘价与收盘价的比较收益
        '''
        
#        qt_data=self.getQtdata(st,et)
        if st is None and et is None:
            qt_data=self.qtdata
        else:
            qt_data=self.qtdata
            qt_data=qt_data[(qt_data.index>=st)&(qt_data.index<=et)]
        op=pd.DataFrame(qt_data.op,columns={'op'})
        cp=pd.DataFrame(qt_data.cp,columns={'cp'})
        res=pd.DataFrame([])
        
        for ilag in lag:
            oplag=Tech_Index.lag(op,ilag)           
            cplag=Tech_Index.lag(cp,ilag)
            oc_rtn=pd.DataFrame((oplag.op-cplag.cp)/cplag.cp,columns={'OC_rtn'})
            res=pd.concat([res,oc_rtn],axis=1)
        return res
        
    
    def MA(self,st=None,et=None,N_period=[5],lag=0,type='None'):
        '''
        计算当日价格MA序列，当type='pct'时，计算的是以收盘价为基准，计算均线与收盘价的比例
        '''
#        qt_data=self.getQtdata(st,et)
        if st is None and et is None:
            qt_data=self.qtdata
        else:
            qt_data=self.qtdata
            qt_data=qt_data[(qt_data.index>=st)&(qt_data.index<=et)]
            
        cp=pd.DataFrame(qt_data.cp,columns={'cp'})
        cp=Tech_Index.lag(cp,lag)
        res=pd.DataFrame([])
        
        for N_p in N_period:
            if type=='None':
                MA_temp=cp.rolling(window=N_p,center=False).mean()
            elif type=='pct':
                MA_temp=cp/cp.rolling(window=N_p,center=False).mean()
            res=pd.concat([res,MA_temp],axis=1)
            
        return res
        
    def MACD(self,st=None,et=None,p1=12,p2=26,p3=9):
#        qt_data=self.getQtdata(st,et)
        if st is None and et is None:
            qt_data=self.qtdata
        else:
            qt_data=self.qtdata
            qt_data=qt_data[(qt_data.index>=st)&(qt_data.index<=et)]
            
        cp=pd.DataFrame(qt_data.cp,columns={'cp'})
        
        return Tech_Index.MACD(cp,p1,p2,p3)
    
    def KDJ(self,st=None,et=None,p1=9,p2=3,p3=3):
#        qt_data=self.getQtdata(st,et)
        if st is None and et is None:
            qt_data=self.qtdata
        else:
            qt_data=self.qtdata
            qt_data=qt_data[(qt_data.index>=st)&(qt_data.index<=et)]
            
        cp=pd.DataFrame(qt_data.cp,columns={'cp'})
        hp=pd.DataFrame(qt_data.hp,columns={'hp'})
        lp=pd.DataFrame(qt_data.lp,columns={'lp'})
        return Tech_Index.KDJ(cp,hp,lp,p1,p2,p3)
                
if __name__=='__main__':

    st='2016-01-01'
    et='2018-10-30'
    A=Stock('000001')
#    print(A.qtdata)
    rtn = A.N_period_return(st=st,et=et,N_period = 30 ,Type = 'b')
    rtn = A.N_period_return(st=st,et=et,N_period = 30 ,Type = 'f')
#    Tech=A.getTechdata(st,et)
#    pdb.set_trace()
#    rtn=A.N_period_return(st,et,N_period=2,lag=[0,1,3],Type='b')
#    vol_c=A.MA_Vol_change(st,et,lag=[0,1])
#    diff,dea,macd=A.MACD(st,et)
#    K,D,J=A.KDJ(st,et)
#    hl_rtrn=A.HL_Rtn(st,et,lag=[0,1,2])
#    vol=A.MA_Vol_change(st,et,lag=0)
#    
#    ma5=A.MA(st,et,N_period=[5,10],lag=0,type='pct')
#    lagma=Tech_Index.lag(ma5,2)
#    print(Tech)
#    print(lagma)

        