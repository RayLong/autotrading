import win32gui, win32con, time
import logger
from VictimWindow import VictimWindow
class CMSTrade(VictimWindow):
     tick_tok=0
     timeout = 20
     def __init__(self):
	 VictimWindow.__init__(self,'\xd5\xd0\xc9\xcc\xd6\xa4\xc8\xaf\xc8\xab\xc4\xdc\xb0\xe6')
	 self.tick_tok=time.time()

     def wakeUp(self):
	 if not self.hooked():
	    logger.log.out( "no CMS software running")
	    return
         t=time.time()
	 if (t - self.tick_tok) > self.timeout:
	       button=self.findChildren('MHPToolBar','MainViewBar', -1, -1)
	       self.clickIt(button[0], 60 , 20)
	       self.tick_tok = t

     def sell(self, code, amount, price):
      victim=self #VictimWindow('\xd5\xd0\xc9\xcc\xd6\xa4\xc8\xaf\xc8\xab\xc4\xdc\xb0\xe6')
      if not victim.hooked():
	  logger.log.out( "no CMS software running")
	  return
      button=victim.findChildren('MHPToolBar','MainViewBar', -1, -1)

      victim.clickIt(button[0], 60 , 20)
      victim.EnumChildren()

      market_h=victim.findChildren('ComboBox','',300,74)
      if 'sh' in code[:2]:
         win32gui.SendMessage(market_h[0],win32con.CB_SETCURSEL, 0, 0)
      elif 'sz' in code[:2]:
         win32gui.SendMessage(market_h[0],win32con.CB_SETCURSEL, 1, 0)

      stock_codes=victim.findChildren('Edit','',308,96)
      victim.setText(stock_codes[0],code[2:])

      price_edit_handle=victim.findChildren('Edit', '', 310, 136)
      victim.setText(price_edit_handle[0], str(price))

      amount_edit_handle=victim.findChildren('Edit', '', 317, 196)
      victim.setText(amount_edit_handle[0], str(amount))

      price_mode=victim.findChildren('ComboBox', '', 308, 119)
      win32gui.SendMessage(price_mode[0], win32con.CB_SETCURSEL, 0, 0)
     
      time.sleep(2)
      button_handle=victim.findChildren('Button','',350,220)
      win32gui.SetFocus(button_handle[0])
      victim.clickIt(button_handle[0], 10, 10)
 
      time.sleep(3)
      dialog=VictimWindow('\xcc\xe1\xca\xbe')
      button_h=dialog.findChildren('Button','\xc8\xb7\xc8\xcf',-1,-1)
      dialog.clickIt(button_h[0],5,5)
      #for h in dialog.children:
      #    print win32gui.GetClassName(h), win32gui.GetWindowText(h), win32gui.GetWindowRect(h)

if __name__ == "__main__":
     victim=CMSTrade() #VictimWindow('\xd5\xd0\xc9\xcc\xd6\xa4\xc8\xaf\xc8\xab\xc4\xdc\xb0\xe6')
     victim.sell('sz600809', 100, 8.9)



