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
    category_text = 'aaa'
    note_data = [['B.W.','I am batman'],['C.D','I am not superman'],['ccc','123']]
	
    AppTest.create_note(self, note_data[1][0], note_data[1][1])

    note = AppTest.findNotesInNoteList(self, note_data[1][0], note_data[1][1])
    note.click()
   
    time.sleep(1)
    self.actions.press(x=500,y=100).release().perform() #click category menu
    time.sleep(1)	
    self.wd.find_element_by_id('it.feio.android.omninotes:id/buttonDefaultPositive').click()
    time.sleep(1)
    self.wd.find_element_by_id('it.feio.android.omninotes:id/category_title').set_value(category_text)
    self.wd.find_element_by_id('it.feio.android.omninotes:id/save').click()
    self.actions.press(x=40,y=90).release().perform() #click back
    time.sleep(1)
	
    #Edit Category Name Test    
    self.actions.press(x=40,y=90).release().perform() #click slide menu
    time.sleep(1)
    category = AppTest.findCategoryInSlideMenuTagList(self, category_text)
    self.actions.long_press(category)
    self.actions.perform()
    
    category_text='bbb'
    edt_title = self.wd.find_element_by_id('it.feio.android.omninotes:id/category_title')
    edt_title.clear()
    edt_title.send_keys(category_text)
    self.wd.find_element_by_id('it.feio.android.omninotes:id/save').click()
    
    category = AppTest.findCategoryInSlideMenuTagList(self, category_text)
    target_title = category.find_element_by_id('it.feio.android.omninotes:id/title').text
    self.assertEqual(target_title, category_text)
    
    #Edit Category Color Test
    self.actions.long_press(category)
    self.actions.perform()  
    
    self.wd.find_element_by_id('it.feio.android.omninotes:id/color_chooser').click()
    colors_grid = self.wd.find_element_by_id('it.feio.android.omninotes:id/grid')
    colors = colors_grid.find_elements_by_class_name('android.widget.FrameLayout')
    colors[18].click() #select gray group
    colors_grid = self.wd.find_element_by_id('it.feio.android.omninotes:id/grid')
    colors = colors_grid.find_elements_by_class_name('android.widget.FrameLayout')
    colors[9].click() #select deepest gray
    self.wd.find_element_by_id('it.feio.android.omninotes:id/buttonDefaultPositive').click() #Press Done
    self.wd.find_element_by_id('it.feio.android.omninotes:id/save').click() #Press Save
    
    #Edit Category Custom Color Test 01
    self.actions.long_press(category)
    self.actions.perform()  
    self.wd.find_element_by_id('it.feio.android.omninotes:id/color_chooser').click()
    self.wd.find_element_by_id('it.feio.android.omninotes:id/buttonDefaultNeutral').click() #Press custom
    color_code = 'FF1234'
    inp_color_code = self.wd.find_element_by_id('it.feio.android.omninotes:id/hexInput')
    inp_color_code.clear()    
    inp_color_code.send_keys(color_code)
    self.wd.find_element_by_id('it.feio.android.omninotes:id/buttonDefaultPositive').click() #Press done
    self.wd.find_element_by_id('it.feio.android.omninotes:id/save').click() #Press Save
    
    #Edit Category Custom Color With Wrong Color Code Test
    self.actions.long_press(category)
    self.actions.perform()  
    self.wd.find_element_by_id('it.feio.android.omninotes:id/color_chooser').click() 
    color_code = 'AZF01111'
    inp_color_code = self.wd.find_element_by_id('it.feio.android.omninotes:id/hexInput')
    inp_color_code.clear()    
    inp_color_code.send_keys(color_code)
    self.wd.find_element_by_id('it.feio.android.omninotes:id/buttonDefaultPositive').click() #Press done
 
    self.wd.find_element_by_id('it.feio.android.omninotes:id/color_chooser').click() 
    inp_color_code = self.wd.find_element_by_id('it.feio.android.omninotes:id/hexInput') 
    self.assertEqual(inp_color_code.text,'FF000000')  
    #Leave setting color
    self.wd.find_element_by_id('it.feio.android.omninotes:id/buttonDefaultPositive').click() #Press done  
    self.wd.find_element_by_id('it.feio.android.omninotes:id/save').click() #Press Save    
    
    #Add Note To Category Test 01
    self.wd.find_element_by_id('it.feio.android.omninotes:id/fab_expand_menu_button').click()  #click for close slide menu
    AppTest.create_note(self, note_data[0][0], note_data[0][1]) #add new note for set up
    note = AppTest.findNotesInNoteList(self, note_data[0][0], note_data[0][1])
    self.actions.long_press(note)
    self.actions.perform()
    time.sleep(1)
    self.wd.find_element_by_id('it.feio.android.omninotes:id/menu_category').click()
    AppTest.findCategoryInDialogTagList(self, category_text).click()
    self.actions.press(x=40,y=90).release().perform() #click back
    time.sleep(1)
    self.actions.press(x=40,y=90).release().perform() #open slide menu
    self.assertEqual(AppTest.getCategoryCountTextInSlideMenu(self,category_text),'2')
        
    #Add Note To Category Test 02
    self.wd.find_element_by_id('it.feio.android.omninotes:id/fab_expand_menu_button').click()  #click for close slide menu
    AppTest.create_note(self, note_data[2][0], note_data[2][1]) #add new note for set up
    note = AppTest.findNotesInNoteList(self, note_data[2][0], note_data[2][1])
    note.click()
    time.sleep(1)
    self.actions.press(x=500,y=100).release().perform() #click category menu
    AppTest.findCategoryInDialogTagList(self, category_text).click()
    self.actions.press(x=40,y=90).release().perform() #click back
    time.sleep(1)
    self.actions.press(x=40,y=90).release().perform() #open slide menu
    self.assertEqual(AppTest.getCategoryCountTextInSlideMenu(self,category_text),'3') 
    
    #Sort Test
    self.wd.find_element_by_id('it.feio.android.omninotes:id/fab_expand_menu_button').click()  #click for close slide menu
    time.sleep(1)
    self.actions.press(x=600,y=80).release().perform() #Press sort menu
    list = self.wd.find_element_by_class_name('android.widget.ListView')
    selectors = list.find_elements_by_class_name('android.widget.LinearLayout')
    selectors[0].find_element_by_id('it.feio.android.omninotes:id/radio').click() 
    notes = AppTest.getNotesInNoteList(self)
    for i in range(len(notes)):
      self.assertEqual(notes[i].find_element_by_id('it.feio.android.omninotes:id/note_title').text,note_data[i][0])
      self.assertEqual(notes[i].find_element_by_id('it.feio.android.omninotes:id/note_content').text,note_data[i][1])
    
    
    #Remove Note From Category Test
    note = AppTest.findNotesInNoteList(self, note_data[1][0], note_data[1][1])  
    note.click()
    time.sleep(1)
    self.actions.press(x=500,y=100).release().perform() #click category menu
    time.sleep(1)
    self.wd.find_element_by_id('it.feio.android.omninotes:id/buttonDefaultNegative').click()
    self.actions.press(x=40,y=90).release().perform() #click back
    time.sleep(1)
    self.actions.press(x=40,y=90).release().perform() #open slide menu
    self.assertEqual(AppTest.getCategoryCountTextInSlideMenu(self,category_text),'2') 
    
    #Delete Category Test 01
    #set up---
    category_text_2 = 'xyza'
    self.wd.find_element_by_id('it.feio.android.omninotes:id/fab_expand_menu_button').click()  #click for close slide menu
    note = AppTest.findNotesInNoteList(self, note_data[1][0], note_data[1][1])
    note.click()
    #create new category
    time.sleep(1)	
    self.actions.press(x=500,y=100).release().perform() #click category menu
    time.sleep(1)	
    self.wd.find_element_by_id('it.feio.android.omninotes:id/buttonDefaultPositive').click()
    time.sleep(1)
    self.wd.find_element_by_id('it.feio.android.omninotes:id/category_title').set_value(category_text_2)
    self.wd.find_element_by_id('it.feio.android.omninotes:id/save').click()
    time.sleep(1)
    #remove note
    self.actions.press(x=500,y=100).release().perform() #click category menu
    self.wd.find_element_by_id('it.feio.android.omninotes:id/buttonDefaultNegative').click()
    self.actions.press(x=40,y=90).release().perform() #click back
    time.sleep(1)
    self.actions.press(x=40,y=90).release().perform() #open slide menu
    #---------
    category = AppTest.findCategoryInSlideMenuTagList(self, category_text_2)
    self.actions.long_press(category)
    self.actions.perform()
    time.sleep(1)
    self.wd.find_element_by_id('it.feio.android.omninotes:id/delete').click()
    self.wd.find_element_by_id('it.feio.android.omninotes:id/buttonDefaultPositive').click()
    list = AppTest.getCategoriesInSlideMenuTagList(self)
    self.assertEqual(len(list)-1,1) #I am not sure why but there always one more element in list
    

  def getCategoryCountTextInSlideMenu(self, title): #must open slide menu
    category = AppTest.findCategoryInSlideMenuTagList(self, title)
    return category.find_element_by_id('it.feio.android.omninotes:id/count').text 
    
  def getCategoriesInDialogTagList(self): #Must open categories dialog
    list = self.wd.find_element_by_id('it.feio.android.omninotes:id/contentListView')
    categories = list.find_elements_by_class_name('android.widget.LinearLayout')
    return categories
    
  def findCategoryInDialogTagList(self, title): #Must open categories dialog
    categories = AppTest.getCategoriesInDialogTagList(self)
    for category in categories:
      category_title = category.find_element_by_id('it.feio.android.omninotes:id/title')
      if category_title==category_title:
        return category
    
  def getNotesInNoteList(self): #App must show note list
    note_list = self.wd.find_element_by_id('it.feio.android.omninotes:id/list')
    notes = note_list.find_elements_by_id('it.feio.android.omninotes:id/root')
    return notes

  def findNotesInNoteList(self, title, content): #App must show note list
    notes = AppTest.getNotesInNoteList(self)
    for note in notes:
      note_title = note.find_element_by_id('it.feio.android.omninotes:id/note_title').text
      note_content = note.find_element_by_id('it.feio.android.omninotes:id/note_content').text
      if note_title==title and note_content==content:
        return note
        
  def getCategoriesInSlideMenuTagList(self): #must open slide menu
    list = self.wd.find_element_by_id('it.feio.android.omninotes:id/drawer_tag_list')
    elements = list.find_elements_by_class_name('android.widget.LinearLayout')
    for element in reversed(elements):
      try:
        element.find_element_by_id('it.feio.android.omninotes:id/title')
      except:
        elements.remove(element)
    return elements
    
  def findCategoryInSlideMenuTagList(self, title): #must open slide menu
    categories = AppTest.getCategoriesInSlideMenuTagList(self)
    for category in categories:
      if category.find_element_by_id('it.feio.android.omninotes:id/title').text==title:
        return category

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
