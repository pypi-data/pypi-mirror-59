# xiaobaiauto

## 介绍
简化现有Selenium、Requests等框架对于页面及接口的操作，也扩展了日志搜集、报告生成、
邮件发送等功能

### 版本说明
    版本：   功能：                        实现：
    1.*     只支持Web端                    √
    2.*     支持Web+API端                  √
    3.*     支持Web+API+Mock               ×
    4.*     支持Web+API+Mock+APP           ×
    5.*     支持Web+API+Mock+APP+Pref      ×

## 软件架构
集成了Selenium、SMTP、HTMLTestRunner、logging、Reuqests等模块

## 安装教程
    pip install xiaobaiauto
    or
    pip install xiaobaiauto==版本号

    **安装之后为方便使用请将auto.*.pyd与HTMLTestRunner.py复制到自己的项目包中

#### 使用代码之前请确保您的电脑中已经安装好浏览器及对应的驱动内容
[chromedriver下载](http://npm.taobao.org/mirrors/chromedriver/) √

<b style="color:red">chrome与chromdriver驱动之间存在不兼容问题，所以最好都下载最新版本为最佳效果</b>



## Case文件实例

    import unittest
    from auto import pageObject, Report, log, EmailHandler, Api  #本行报红属于正常

    class MyTestCase(unittest.TestCase):
        def setUp(self):
            """
                初始化日志
            :return:
            """
            self.logger = log()
            self.client = Api()
            self.page = pageObject()
            self.driver = self.page.init(is_max=True)

        def test_api_xxx(self):
            headers = {'content-type': 'application/json'}
            json = {'type': 1, 'orderno': 'abcdef'}
            path = 'http://127.0.0.1:8080/api/v/1.0/'
            json_res = self.client.api('post', url=path, json=json, headers=headers).json()
            try:
                self.assertEqual(json_res.get('successful'), 'true')
                self.logger.info('xxx接口请求成功')
            except:
                self.logger.error('xxx接口请求失败')
            # self.logger.debug('调试日志信息')
            # self.logger.warning('警告日志信息')
            # self.logger.error('错误日志信息')

        def test_web_12306(self):
            # 通过self.driver 调用原生方法
            # 通过self.page   调用集成方法
            self.page.get(url='https://kyfw.12306.cn/otn/leftTicket/init?linktypeid=dc&fs=%E4%B8%8A%E6%B5%B7,SHH&ts=%E9%83%91%E5%B7%9E,ZZF&date=2020-02-02&flag=N,N,Y')

            #self.page.add_cookie({'name': '', 'value': ''})

            chufa = self.page.xpath('//*[@id="fromStationText"]')
            chufa.clear()
            chufa.send_keys('上海')
            chufa.send_keys(Keys.ENTER)
            sleep(2)

        def tearDown(self):
            pass

    if __name__ == '__main__':
        report_file_name = 'TestReport.html'
        suite = unittest.TestSuite()
        # 添加测试用例
        suite.addTest(MyTestCase('test_web_12306'))
        #suite.addTest(MyTestCase('test_api_xxx'))  # 不运行就注释掉
        fp = open(report_file_name, 'wb')
        #   生成报告
        runner = Report(
            stream=fp,
            title='测试',
            description='备注信息',
            tester='Tser'
        )
        runner.run(suite)
        fp.close()
        #  将测试报告发送指定邮件 数据务必修改
        email = EmailHandler(smtp='smtp.qq.com', port=25, sender_name='qq号', sender_passwd='邮箱密码')
        email.sendemail(
            _to='接收者邮箱',
            _cc='抄送者邮箱',
            title='邮件标题',
            email_content='邮箱内容',
            _type='html',
            filename=report_file_name
        )
        email.close()

### 脚本运行
    1、打开cmd
    2、cd 脚本目录
    3、python 脚本名.py

### 提示
<b style="color:red">QQ邮箱或者其它企业邮箱必须提前开启SMTP服务</b>
<b>部分邮箱对频发发送邮件进行拦截，所以大家在使用邮箱发送消息时请勿频繁尝试</b>

[点击这里了解QQ邮箱如何开启SMTP服务](https://jingyan.baidu.com/article/6079ad0eb14aaa28fe86db5a.html)

### 更新日志
    V2.2.1
    因2.0.0版本不能适用于Pycharm社区版，调用失败问题，已修复
    定时器还未加入！

#### 参与贡献

作者: <b>@Tser</b><br>
©<b title="公众号：big_touch">小白科技</b>