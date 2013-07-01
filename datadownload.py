import datetime
import urllib
import os
import sys
baseurl="http://down.compass.cn:8080/resource/marketdata/%E6%AF%8F%E6%97%A5%E6%95%B0%E6%8D%AE/"
#20120104.zip
day=datetime.date(2012,1,3)

def report(count, blocksize, totalsize):
   print 100.0*(count*blocksize)/totalsize,'%'

while day < datetime.date(2012,7,5):
   url=baseurl+day.strftime("%Y%m%d")+'.zip'
   filename=day.strftime("%Y%m%d")+'.zip'
   print 'getting', url
   try:
      #ret=urllib.urlretrieve(url,day.strftime("%Y%m%d")+".zip",report)
      #if ret[1].status=='':
      #      os.unlink(ret[0])
      f=urllib.urlopen(url)
      buf=f.read(8192)
      if buf[:9] == '<!DOCTYPE':
	  f.close()
          day+=datetime.timedelta(1)
	  continue
      fw=open(filename, "w")
      while len(buf) > 0:
	 fw.write(buf)
	 sys.stdout.write('.')
	 buf=f.read(8192)
      f.close()
      fw.close()
      print "!"
   except KeyboardInterrupt:
      print "Ctrl+C exit"
      break
   day+=datetime.timedelta(1)
