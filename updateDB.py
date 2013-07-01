import sqlite3
import re

class CreateDB:
   sh_user_account='sh'
   stocks_config={} #{'stock_id':[cost, amount, max_price, name, id]}

   def loadConfig(self,filename):
       text_file = open(filename, "r")
       lines = text_file.readlines()
       if len(lines) > 4:
	    stocks=lines[4:len(lines)]
	    for stock in stocks:
		stock_info=[]
		match=re.search(r"(\d+)",stock)
		if match == None:
		    raise Exception("invalid configure file")
	        stock_info.append(stock[:match.start(1)].strip())
		stock_info=stock_info+(stock[match.start(1):].split())
		# cost = [3]
		# name = [0]
		# currentPrice = [7]
		# total amount = [1]
		# soldable amount = [2]
		# stock number = [10]
		# user account = [11]
		if stock_info[11]==self.sh_user_account:
		   prefix="sh"
		else:
		   prefix="sz"
		stock_info[0]=stock_info[0].decode('GB2312').encode('utf8')
		if int(stock_info[2]) > 0:
			self.stocks_config[prefix+stock_info[10]]=[ stock_info[3], stock_info[2], "0", stock_info[0],stock_info[10],stock_info[11]]
       else:
	       raise Exception('invalid configure file')
       text_file.close()
       db=sqlite3.connect('data.db')
       cu=db.cursor()
       try:
	       cu.execute('SELECT 1 FROM holds')
       	       db.commit()
       except sqlite3.OperationalError:
	       print cu.fetchall()
       	       cu.execute('CREATE TABLE if not exists holds(id integer primery key, name varchar(32), account varchar(20), amount integer, max_price float, cost_price float, state integer, loss_stop float)')
               db.commit()
       for key, value in self.stocks_config.iteritems():
	       cu.execute('SELECT id from holds where id='+value[4])
	       if len(cu.fetchall()) == 0:
	           cu.execute('INSERT into holds values(' + value[4] +',"'+ value[3] +'","'+value[5]+'",'+value[1]+','+value[2]+','+value[0]+',0,0.0)')
       	       db.commit()
       cu.execute('select * from holds')
       print cu.fetchall()
       db.close()

if  __name__ == "__main__":
    c=CreateDB()
    c.loadConfig('data.txt')

       
