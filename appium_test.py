import sys, time
import unittest
from appium import webdriver
from appium.webdriver.common.touch_action import TouchAction

def passIntro(actions):
  time.sleep(5)
  for i in range(1,7):	    
    actions.press(x=700,y=1200).release().perform()
    time.sleep(2)
  
  time.sleep(2)
  actions.press(x=600,y=1210).release().perform()
  time.sleep(5)
  
class AppTest(unittest.TestCase): 
   
  def setUp(self):
    desired_caps = {}
    desired_caps['platformName'] = 'Android'
    desired_caps['platformVersion'] = '5.1.1'
    desired_caps['deviceName'] = 'android-48d224b0497f4952'
    desired_caps['appPackage'] = 'it.feio.android.omninotes'
    desired_caps['appActivity'] = '.MainActivity'

    self.wd = webdriver.Remote('http://localhost:4723/wd/hub', desired_caps)
    self.wd.implicitly_wait(60)
    self.actions = TouchAction(self.wd)
	
    passIntro(self.actions)  


  def test_Category(self):
    #Create Category Test
    test_text = 'aaa'
	
    AppTest.create_note(self, 'ccc', '123')

    #self.actions.press(x=400,y=200).release().perform()
    notes = AppTest.getNotesInNoteList(self)
    notes[0].click()
   
    time.sleep(1)
    #self.wd.find_element_by_id('it.feio.android.omninotes:id/menu_category').click
    self.actions.press(x=500,y=100).release().perform() #click category menu
    time.sleep(1)	
    self.wd.find_element_by_id('it.feio.android.omninotes:id/buttonDefaultPositive').click()
    time.sleep(1)
    self.wd.find_element_by_id('it.feio.android.omninotes:id/category_title').set_value(test_text)
    self.wd.find_element_by_id('it.feio.android.omninotes:id/save').click()
    self.actions.press(x=40,y=90).release().perform() #click back
	
    #

  def getNotesInNoteList(self): #App must show note list
    note_list = self.wd.find_element_by_id('it.feio.android.omninotes:id/list')
    notes = note_list.find_elements_by_id('it.feio.android.omninotes:id/root')
    return notes

  def create_note(self, title, content):
    time.sleep(1)
    self.wd.find_element_by_id('it.feio.android.omninotes:id/fab_expand_menu_button').click()  
    time.sleep(1)
	#click Article Comment 
    self.actions.press(x=660,y=1100).release().perform() 
    time.sleep(1)
    self.wd.find_element_by_id('it.feio.android.omninotes:id/detail_title').set_value(title)
    self.wd.find_element_by_id('it.feio.android.omninotes:id/detail_content').set_value(content)
    time.sleep(1)
    #click back
    self.actions.press(x=40,y=90).release().perform() #click back
    time.sleep(2)
	

if __name__ == "__main__":
  unittest.main()
