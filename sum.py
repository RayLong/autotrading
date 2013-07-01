#!python

import sys
import re

f=open(sys.argv[1],'r')
current_price=float(sys.argv[2])
sold=0.0
bought=0.0
s_amount=0.0
b_amount=0.0
for line in f:
    if re.match(r'^[0-9]{4}-[0-9]{2}-[0-9]{2}',line) == None:
      print 'ignore:', line
    else:
      items=line.split()
      if len(items) != 0:
	  if items[3] != '\xc2\xf2\xc8\xeb':
             sold=sold+float(items[8].replace(',',''))
	     s_amount=s_amount+float(items[7])
	     print "sold:",items[8]
	     print "sold amount:",items[7]
          else:
	     bought=bought+float(items[8].replace(',',''))
	     b_amount=b_amount+float(items[7])
	     print "bought:",items[8]
	     print "bought amount:",items[7]
f.close()
print "total sold:", sold
print "total bought:", bought
print "balance:",sold-bought
print "total sold amount:",s_amount
print "total bought amount:",b_amount
print "potential gain:", sold-bought+(b_amount-s_amount)*current_price
