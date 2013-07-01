#!/usr/bin/python
import re
import logger

class Stock:
    UNKNOWN = 0
    FLUCTUATING = 1
    PROFITABLE = 2
    @staticmethod
    def createFromSinaData(stock_str):
        stockInfo=Stock()
	stockInfo.updateWithSinaData(stock_str)
	return stockInfo

    def setTargets(self, cost, amount, max_price, init_state,loss_stop):
	self.costprice=cost
	self.amount=amount
	self.state=init_state
	self.max_price = max_price
	self.loss_stop=loss_stop

    def updateWithSinaData(self, stock_str):
	stockInfo=self
	temp=stock_str.split('=')
	stockinfolist=temp[1][1:len(temp[1])-2].split(',')
	stockInfo.Id=temp[0][11:len(temp[0])]
	stockInfo.name = stockinfolist[0]
	stockInfo.PriceOpenToday =float(stockinfolist[1])
	stockInfo.PriceCloseYestoday=float(stockinfolist[2])
	stockInfo.CurrentPrice=float(stockinfolist[3])
	stockInfo.HighestPriceToday=float(stockinfolist[4])
	stockInfo.LowestPriceToday=float(stockinfolist[5])
	stockInfo.BuyPriceNow=float(stockinfolist[6])
	stockInfo.SellPriceNow=float(stockinfolist[7])
	stockInfo.TurnoverNum=stockinfolist[8]
	stockInfo.TurnoverMoney=stockinfolist[9]
	stockInfo.BuyNum1=stockinfolist[10]
	stockInfo.BuyPrice1=stockinfolist[11]
	stockInfo.BuyNum2=stockinfolist[12]
	stockInfo.BuyPrice2=stockinfolist[13]
	stockInfo.BuyNum3=stockinfolist[14]
	stockInfo.BuyPrice3=stockinfolist[15]
	stockInfo.BuyNum4=stockinfolist[16]
	stockInfo.BuyPrice4=stockinfolist[17]
	stockInfo.BuyNum5=stockinfolist[18]
	stockInfo.BuyPrice5=stockinfolist[19]
	stockInfo.SellNum1=stockinfolist[20]
	stockInfo.SellPrice1=stockinfolist[21]
	stockInfo.SellNum2=stockinfolist[22]
	stockInfo.SellPrice2=stockinfolist[23]
	stockInfo.SellNum3=stockinfolist[24]
	stockInfo.SellPrice3=stockinfolist[25]
	stockInfo.SellNum4=stockinfolist[26]
	stockInfo.SellPrice4=stockinfolist[27]
	stockInfo.SellNum5=stockinfolist[28]
	stockInfo.SellPrice5=stockinfolist[29]
	stockInfo.Date=stockinfolist[30]
	stockInfo.Time=stockinfolist[31]     
  

    """
    1. unknown state
       1.1 cost*1.05 > current ---> Fluctuating state
       1.1 current > cost*1.05 ---> profit state  

    2. Fluctuating state
       2.1 current < cost * 0.9 ---> terminate and sell
       2.2 current > cost * 1.05 ---> profit state

    3. profit state
       3.1 max_price=max(current, max_price)
       3.2 current < get_loss_stop(max_price,cost) ---> terminate and sell
    """

    def get_loss_stop(self, max_price, cost):
	    ratio=max_price/cost
	    if ratio < 1.06 :
		    factor=0.96
	    elif ratio < 1.07:
		    factor=0.97
	    else:
		    factor=0.98
	    return max_price * factor

    def checkPrice_unknown(self):
	    if self.CurrentPrice < self.costprice * 1.05:
		    self.state = self.FLUCTUATING
	    else:
		    self.state = self.PROFITABLE
	    return 0

    def checkPrice_fluctuating(self):
	    if self.CurrentPrice < self.loss_stop:
		    return 1
	    elif self.CurrentPrice > self.costprice * 1.05:
		    self.state = self.PROFITABLE
	    return 0

    def checkPrice_profitable(self):
	    self.max_price=max(self.CurrentPrice, self.max_price)
	    if self.CurrentPrice < self.get_loss_stop(self.max_price, self.costprice):
		    return 1
	    return 0

    def checkPriceLinear(self):
	ret = 0
	if self.CurrentPrice == 0:
	   logger.log.out("data is zero, ignore "+self.name)
	   return ret
        logger.log.out(self.name+" price "+str(self.CurrentPrice))
	while True:
	   old_state = self.state
	   ret = { self.UNKNOWN : self.checkPrice_unknown, 
		   self.FLUCTUATING : self.checkPrice_fluctuating,
		   self.PROFITABLE : self.checkPrice_profitable
	         }[self.state]()
	   if old_state == self.state or ret == 1:
	       break
           state_string=['unknown','fluctuating','profitable']
           logger.log.out("state changed %s -> %s" % (state_string[old_state],state_string[self.state]))
	if ret == 1:	
	    logger.log.out("stop at %f, %f%%" % (self.CurrentPrice,(self.CurrentPrice/self.costprice-1)*100))
	return ret
        
class Stocks(list):
    @staticmethod
    def createFromSinaData(sina_str):
	ret=Stocks()
	if Stocks.validSinaString(sina_str):
           for s in sina_str.split("\n"):
	       if s != '':
	          ret.append(Stock.createFromSinaData(s))
	return ret
    
    def updateFromSinaData(self, sina_str):
	if not Stocks.validSinaString(sina_str):
           return	
	ss=sina_str.split("\n")
	remove_list=[]
	mapping={}
	for idx in range(len(self)):
	   mapping[self[idx].Id]=idx
	for s in ss:
          if s != '':
	   Id=s.split('=')[0]
	   Id=Id[11:len(Id)]
           self[mapping[Id]].updateWithSinaData(s)
	   mapping[Id]=-1
	for idx in mapping.keys():
	   if mapping[idx] != -1:
	      remove_list.append(mapping[idx])
	remove_list.sort(reverse=True)
	for x in remove_list:
	   self.pop(x)
     
    @staticmethod
    def validSinaString(sina_str):
        m=re.match('var', sina_str)
	if m:
	   ret=True
	else:
           ret=False
	return ret
