# -*- coding: utf-8 -*-
"""
Created on Tue Aug  8 15:22:59 2017

@author: zhai
"""
import pdb
import tushare as ts
import numpy as np
import pandas as pd
from datetime import datetime

class getTushareData():
    def __init__(self):
        self.Basic = None #基础数据 行业，地域，pe,股本
        
    def get_Basicdata(self):
        '''
        保存tushare当前全部股票基本面数据
        code,代码
        name,名称
        industry,所属行业
        area,地区
        pe,市盈率
        outstanding,流通股本(亿)
        totals,总股本(亿)
        totalAssets,总资产(万)
        liquidAssets,流动资产
        fixedAssets,固定资产
        reserved,公积金
        reservedPerShare,每股公积金
        esp,每股收益
        bvps,每股净资
        pb,市净率
        timeToMarket,上市日期
        undp,未分利润
        perundp, 每股未分配
        rev,收入同比(%)
        profit,利润同比(%)
        gpr,毛利率(%)
        npr,净利润率(%)
        holders,股东人数
        '''
        #获取数据
        if self.Basic is None:
            Basic_data=ts.get_stock_basics()
            self.Basic = Basic_data
        else:
            pass
        return self.Basic

if __name__=='__main__':
    t=getTushareData()
#    t.save_Basicdata()
    A = t.get_Basicdata()
    
    
    
    


        