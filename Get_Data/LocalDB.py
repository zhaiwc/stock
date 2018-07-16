# -*- coding: utf-8 -*-
"""
Created on Tue Aug  8 17:15:21 2017

@author: zhai
"""
import os
import shelve
import math
import pdb
from  dateutil.parser import parse
from datetime import datetime

class LocalDB(object):
    '''
    功能：
    1.指定dbname 获取本地DB存放路径
    2.定义保存，提取，删除本地DB的方法
    
    '''
    def __init__(self,dbname):
        _cwp=os.path.split(os.path.realpath(__file__))[0]
        self.localdb_path=_cwp+'\\LocalDB_Files\\'
        self.dbname=dbname
        self.DB=self._get_db()
        
    def _get_db(self):
        if self.dbname=='tushare':
            DB=self.localdb_path+'tusharedb.dat'
        elif self.dbname=='QT': 
            DB=self.localdb_path+'QT.db.dat'
        return DB
    
    def _get_db_by_code(self,code):
        if self.dbname == 'QT':
            bycodepath = self.localdb_path +str(code) +'\\'
            if os.path.exists(bycodepath):
                DB = bycodepath + 'QT.db.dat'
            else:
                os.mkdir(bycodepath)
                DB = bycodepath + 'QT.db.dat'
        
        return DB
        
    
    def save_db_data(self,keyname,data,code = None , by_code = False):

        keyname=str(keyname)
        try:
            if by_code:
                db = shelve.open(self._get_db_by_code(code), 'c')
            else:
                db = shelve.open(self.DB, 'c')
            db[keyname]=data
            print('--------保存 '+self.dbname+'_'+ keyname+'成功--------')
        finally:
            db.close()
            
    def get_db_data(self,keyname,code = None , by_code = False):
        keyname=str(keyname)
        data=None

        try:
            if by_code:
                db = shelve.open(self._get_db_by_code(code), 'c')
            else:
                db = shelve.open(self.DB, 'c')

            if keyname in db.keys():
                data=db[keyname]
                
            else:
                print('--------没有该数据！--------') 
        finally:
            db.close()
            return data
            
    def del_db_data(self,keyname,code = None , by_code = False):
        keyname=str(keyname)
        try:
            if by_code:
                db = shelve.open(self._get_db_by_code(code), 'c')
            else:
                db = shelve.open(self.DB, 'c')
            db.pop(keyname)
            print('--------删除 '+self.dbname+'_'+ keyname+'成功--------')
        except:
            return None
        finally:
            db.close()
    
    def choosedate(self,df,st=None,et=None):
        if st is None and et is None:
            return df
        else:
            if st is not None:         
                st=parse(st)
                st_n=int(str(st.year)+'0'+str(math.ceil(st.month/3)))
            else:
                st=parse('1990-01-01')
                st_n=int(str(st.year)+'0'+str(math.ceil(st.month/3)))   
                
            if et is not None:
                
                et=parse(et)
                et_n=int(str(et.year)+'0'+str(math.ceil(et.month/3)))  
            else:
                et=datetime.now()    
                et_n=int(str(et.year)+'0'+str(math.ceil(et.month/3)))  
                
            return df[(df.findate>=st_n) & (df.findate<=et_n)]
        
if __name__=='__main__':
#    LDB=LocalDB('stock_ind')
#    temp1=LDB.get_db_data('Industry')
    LDB=LocalDB('QT')
    temp1=LDB.get_db_data('hfq','000001',by_code=True)
    
        
        