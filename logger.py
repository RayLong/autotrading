import time
class Log:
     def open(self,filename):
	 self.f=open(filename,"w")


     def out(self,string):
	 time_str=time.strftime("%Y%m%d-%H:%M:%S",time.localtime())
	 self.f.write("["+time_str+"] "+string+"\n")
	 print string

     def close(self):
	 if (self.f is not None):
	     self.f.close()

log=Log()
