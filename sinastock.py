#!/usr/bin/python

import urllib
import httplib
import re
import logger
import time

class SinaStockQuery:
    in_stocks = ''
    def query(self,*stocks):
	try:
             f = urllib.urlopen("http://hq.sinajs.cn/list={0}".format(','.join(stocks)))
	except IOError:
	     logger.log.out("Query sina web service failed")
             self.in_stocks=''
	     return 0
        self.in_stocks=f.read()
	f.close()
        return 1

    def query_timeout(self, timeout, *stocks):
        conn=httplib.HTTPConnection("hq.sinajs.cn",timeout=timeout);
        params="/list="+(','.join(stocks))
	try:
           conn.request("GET",params)
           resp=conn.getresponse()
           if resp.status == 200:
	      self.in_stocks=resp.read()
	      conn.close()
	      return 1
	   else:
              self.in_stocks=""
              conn.close()
              return 0
	except Exception as e:
	    logger.log.out("error:"+str(e))
	    time.sleep(5)
	    conn.close()
	    return 0
        

class TestQuerySingle:
    in_stocks = ''
    data_file = None
    name = ''
    def query(self, stock):
	if self.data_file == None:
	   self.data_file=open(stock.upper()+".TXT",'r')
	   stock_name=self.data_file.readline().split()
	   self.name=stock_name[1]
	   self.data_file.readline()
	x=self.data_file.readline().split()
	if len(x) < 5:
	   logger.log.out("try again")
	   self.data_file.close()
	   self.data_file=open(stock.upper()+".TXT", 'r')
	   self.data_file.readline()
	   self.data_file.readline()
	   x=self.data_file.readline().split()
	self.in_stocks="var hq_str_"+stock+"="+'"'+self.name+',0,0,'
	self.in_stocks+=x[2]+','
	y=[]
	for i in range(28):
	    y.append('0')
	self.in_stocks+=','.join(y)
	self.in_stocks+='";'


class TestQuery:
   stock_queries={}
   in_stocks=''
   def query(self, *stocks):
       self.in_stocks=''
       for s in stocks:
	   if s not in self.stock_queries:
               self.stock_queries[s]=TestQuerySingle()
	   self.stock_queries[s].query(s)
	   self.in_stocks+=self.stock_queries[s].in_stocks+'\n'

