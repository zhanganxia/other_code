#coding=utf-8

from widget import Widget
import unittest

#执行测试的类
class WidgetTestCase(unittest.TestCase):
    
        def setUp(self):#setUp()方法进行测试前的初始化工作
            self.widget = Widget()
        
        #testSize()中调用assertEqual()方法，对Widget类中getSize()方法的返回值和预期值进行比较，确保两者是相等的
        #assertEqual()方法也是TestCase类中定义的方法
        def testSize(self):
            self.assertEqual(self.widget.getSize(),(40,40))
        
        def tearDown(self):#tearDown执行测试后的清除工作，是TestCase类中定义的方法
            self.widget = None

#构造测试集
def suite():
    suite=unittest.TestSuite()
    suite.addTest(WidgetTestCase("testSize"))
    return suite

#测试
if __name__=="__main__":
    unittest.main(defaultTest='suite')