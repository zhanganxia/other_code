#coding=utf-8

from widget import Widget
import unittest

#执行测试的类
class WidgetTestCase(unittest.TestCase):
    
        def setUp(self):#setUp()方法进行测试前的初始化工作
            self.widget = Widget()
        
        def tearDown(self):#tearDown执行测试后的清除工作，是TestCase类中定义的方法
            self.widget.dispose()
            self.widget = None

        def testSize(self):
            self.assertEqual(self.widget.getSize(),(40,40))
        
        def testResize(self):
            self.widget.resize(100,100)
            self.assertEqual(self.widget.getSize(),(100,100))  

#测试
if __name__=="__main__":
    unittest.main()
        
    # #构造测试集
    # suite=unittest.TestSuite()
    # suite.addTest(WidgetTestCase("testSize"))
    # suite.addTest(WidgetTestCase("testResize"))

    # #执行测试
    # runner=unittest.TextTestRunner()
    # runner.run(suite)