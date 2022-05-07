from .base import FunctionalTest
from selenium.webdriver.common.keys import Keys

class ItemValidationTest(FunctionalTest):
    def get_error_element(self):
        return self.browser.find_element_by_css_selector('.has-error')
    
    def test_cannot_add_empty_list_items(self):
       # 伊迪丝访问首页，不小心提交了一个空待办事项
       # 输入框中没输入内容，她就按下了回车键
       self.browser.get(self.live_server_url)
       inputbox=self.get_item_input_box().send_keys(Keys.ENTER)
       
       # 浏览器截获了请求
       # 清单页面不会加载
       self.wait_for(lambda: self.browser.find_elements_by_css_selector('#id_text:invalid'))
       
       # 她在待办事项中输入了一些文字
       # 错误消失了
       inputbox=self.get_item_input_box().send_keys('Buy milk')
       self.wait_for(lambda: self.browser.find_elements_by_css_selector('#id_text:valid'))

       # 现在能提交了
       inputbox=self.get_item_input_box().send_keys(Keys.ENTER)
       self.wait_for_row_in_list_table('1: Buy milk')
       
       # 她有点儿调皮，又提交了一个空待办事项
       inputbox=self.get_item_input_box().send_keys(Keys.ENTER)

       # 在清单页面她看到了一个类似的错误消息
       self.wait_for_row_in_list_table('1: Buy milk')
       self.wait_for(lambda: self.browser.find_elements_by_css_selector('#id_text:invalid'))

       # 输入文字之后就没问题了
       inputbox=self.get_item_input_box().send_keys('Make tea')
       inputbox=self.get_item_input_box().send_keys(Keys.ENTER)
       self.wait_for_row_in_list_table('1: Buy milk')
       self.wait_for_row_in_list_table('2: Make tea')

    def test_cannot_add_duplicate_items(self):
        # 伊迪丝访问首页，新建一个清单
        self.browser.get(self.live_server_url)
        inputbox=self.get_item_input_box().send_keys('Buy wellies')
        inputbox=self.get_item_input_box().send_keys(Keys.ENTER)
        self.wait_for_row_in_list_table('1: Buy wellies')
        
        # 她不小心输入了一个重复的待办事项
        inputbox=self.get_item_input_box().send_keys('Buy wellies')
        inputbox=self.get_item_input_box().send_keys(Keys.ENTER)
        
        # 她看到一条有帮助的错误消息
        self.wait_for(lambda: self.assertEqual(self.get_error_element().text,
            "You've already got this in your list"))

    def test_error_messages_are_cleared_on_input(self):
        # 伊迪丝新建一个清单，但方法不当，所以出现了一个验证错误
        self.browser.get(self.live_server_url)
        inputbox=self.get_item_input_box().send_keys('Banter too thick')
        inputbox=self.get_item_input_box().send_keys(Keys.ENTER)
        self.wait_for_row_in_list_table('1: Banter too thick')
        inputbox=self.get_item_input_box().send_keys('Banter too thick')
        inputbox=self.get_item_input_box().send_keys(Keys.ENTER)

        self.wait_for(lambda: self.assertTrue(self.get_error_element().is_displayed()))

        # 为了消除错误，她开始在输入框中输入内容
        self.get_item_input_box().send_keys('a')

        # 看到错误消息消失了，她很高兴
        self.wait_for(lambda: self.assertFalse(self.get_error_element().is_displayed()))

      
      
        	
