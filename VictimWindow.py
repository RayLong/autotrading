#!\python27\python.exe
import win32gui, win32con
import time
from logger import log

class VictimWindow:
     victim_window = 0 
     children = []
     def __init__(self,window_name):
         def callback(hwnd,empty):
           caption=win32gui.GetWindowText(hwnd)
           if caption.find(window_name) == 0:
                self.victim_window=hwnd
         win32gui.EnumWindows(callback,None)
	 if self.victim_window:
	    self.EnumChildren()
	    #self.root_position = win32gui.GetWindowRect(self.victim_window)
	 else:
	    log.out("no CMS software running")
     
     def hooked(self):
	 return (self.victim_window != 0)

     def EnumChildren(self):
	 self.children=[]
         def callback(hwnd,hwnds):
            hwnds.append(hwnd)
	 if self.victim_window != 0:
	    win32gui.EnumChildWindows(self.victim_window,callback,self.children)
             
     def findChildren(self, class_name, window_name, x , y):
         ret=[]
	 root_position = win32gui.GetWindowRect(self.victim_window)
	 if x >=0:
		 x += root_position[0]
	 if y >=0:
		 y += root_position[1]
         def contain_point(h, x, y):
	     if x < 0 or y < 0: 
		     return True
             left, top, right, bottom = win32gui.GetWindowRect(h)
	     if x > left and x < right and y > top and y < bottom:
		     return True
	     else:
	             return False
         for h in self.children:
             if class_name == win32gui.GetClassName(h): 
	        if ( window_name == "" or window_name == win32gui.GetWindowText(h) ) and contain_point(h, x, y) and win32gui.IsWindowVisible(h):
                   ret.append(h)
         if ret == []: 
		 raise Exception("failed to find child window:"+window_name)
         return ret
     
     def clickIt(self, hwnd, offset_x, offset_y):
	 wparam=offset_y*65536+offset_x
         win32gui.PostMessage(hwnd,win32con.WM_LBUTTONDOWN, 0x0001, wparam)
	 win32gui.PostMessage(hwnd,win32con.WM_LBUTTONUP, 0x0001, wparam)
	 time.sleep(1)

     def setText(self, edit_handle, text):
	 win32gui.SetFocus(edit_handle)
	 time.sleep(1)
	 win32gui.SendMessage(edit_handle,win32con.WM_SETTEXT, 0, text)
     

