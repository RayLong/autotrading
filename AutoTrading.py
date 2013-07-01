#!\python27\python

from sinastock import SinaStockQuery, TestQuery
from stocks import Stock, Stocks
from CMSTrade import CMSTrade
#from faketrade import CMSTrade
import logger
import time
import sys
import re
import sqlite3
import os

class AutoTrading:
   stocks_config={} #{'stock_id':[cost, amount, max_price, state, loss_stop]}
   stocks=[]
   debugging_mode=False
   sh_user_account='A383601817'
   sz_user_account='0151050482'
   def loadData(self):
       data_db=sqlite3.connect("data.db")
       cu = data_db.cursor()
       cu.execute("select * from holds")
       r=cu.fetchall()
       #  0   1     2        3       4    5     6      7
       #( id, name, account, amount, max, cost, state, loss_stop )
       for v in r:
	       if v[2] == self.sh_user_account:
		       prefix='sh'
	       elif v[2] == self.sz_user_account:
		       prefix='sz'
	       else:
		       logger.log.out("Unknown account:"+v[2])
		       sys.exit(1)
	       self.stocks_config[prefix+("%06d" % v[0])]=[v[5],v[3],v[4],v[6],v[7]]
       data_db.close()

   def __init__(self,timeout,query):
      self.stock_query=query
      self.loadData()
      self.timeout=timeout
      self.shutdown_flag=False
      if self.stocks_config != {}:
	    self.running = 1
      else:
	    self.running = 0

   def is_market_closed(self):
	   st=time.localtime()
	   if st.tm_hour > 15:
		   return True
	   elif st.tm_hour == 15 and st.tm_min >= 0:
		   return True
	   return False

   def is_lunch_time(self):
	   st=time.localtime()
	   if st.tm_hour > 11 and st.tm_hour < 13:
		   return True
	   elif st.tm_hour == 11 and st.tm_min >= 30:
		   return True
	   return False

   def is_market_opened(self):
	   st=time.localtime()
	   if st.tm_hour > 9:
		   return True
	   elif st.tm_hour == 9 and st.tm_min >= 30:
		   return True
	   return False

   def run(self,trading_window):
      while self.running:
	  tm_stamp1=time.time()
	  trading_window.wakeUp()
	  if self.is_market_opened() == True or self.debugging_mode:
	     ret=self.get_stocks()
	     if ret == 0:
                logger.log.out("failed to get stocks")
	        trading_window.wakeUp()
	        continue

	     if self.is_lunch_time() != True or self.debugging_mode:
	          stocks_selling=self.process_stocks()
	          if len(stocks_selling) != 0 :
			  for s in stocks_selling:
				  trading_window.sell(s.Id,s.amount,s.BuyPrice1)

	          if len(self.stocks_config) == 0:
	                 logger.log.out("no stocks to monitor")
	                 self.running = 0
                         break
                  if self.is_market_closed() == True and not self.debugging_mode:
                         logger.log.out("Market closed")
                         break
	  else:
		  logger.log.out("waiting for market open")
	  tm_stamp2=time.time()
          time.sleep(max(0,int(self.timeout+tm_stamp1-tm_stamp2)))        
      logger.log.out("auto trading stopped")
      auto.shutdown_flag=True


   def get_stocks(self):
       stocks=self.stocks_config.keys()
       ret=self.stock_query.query_timeout(self.timeout-10,*stocks)
       if ret == 1:
         sina_data=self.stock_query.in_stocks
         if self.stocks == []:
            self.stocks=Stocks.createFromSinaData(sina_data)
            for s in self.stocks:
              sc=self.stocks_config[s.Id]
              #[0]=Cost Price, [1]= Amount, [2]= max_price, [3]= state, [4]=loss stop
              s.setTargets(sc[0],sc[1],sc[2],sc[3],sc[4])
         else:
              self.stocks.updateFromSinaData(sina_data)
       return ret

   def removeDB(self, stock_id):
	   data_db=sqlite3.connect('data.db')
           cu=data_db.cursor()
	   cu.execute('DELETE from holds where id='+stock_id)
	   data_db.commit()
	   data_db.close()

   def updateDB(self):
           data_db=sqlite3.connect('data.db')
           cu=data_db.cursor()
	   for s in self.stocks:
		   cu.execute('UPDATE holds set max_price='+str(s.max_price)+', state='+str(s.state)+' where id='+s.Id[2:])
	   	   data_db.commit()
	   data_db.close()

   def process_stocks(self):
	  stocks=[]
	  for s in self.stocks:
	      sell=s.checkPriceLinear()
	      if sell:
		 self.stocks_config.pop(s.Id)
		 self.removeDB(s.Id[2:])
		 stocks.append(s)
          return stocks

   def shutdown(self):
	  if self.shutdown_flag == True:
		  os.system('shutdown -s')


if __name__ == "__main__":
    log_file="log-"+time.strftime("%Y-%b-%d.txt")
    logger.log.open(log_file)
    auto=AutoTrading(60,SinaStockQuery())
    trading_window=CMSTrade() 
    #auto.debugging_mode=True
    try:
	    auto.run(trading_window)
    finally:
            auto.updateDB()
	    logger.log.close()
	    auto.shutdown()
