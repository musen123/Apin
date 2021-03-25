# apin(0.1)使用文档

# 一、apin介绍及安装

#### 1、什么是apin

​	apin是一个无需写代码，就可以完成接口自动化测试的框架，只需要通过json或yaml文件编写非常简洁的用例数据，即可完成接口自动化测试，并生成自动化测试报告。

​	apin是柠檬班—木森老师根据多年的自动化工作经验而开发出来的，旨在帮助更多不会写代码的小伙伴掌握接口自动化测试的能力。框架使用起来非常简单，易上手，只需要几个小时就能掌握！	

#### 2、安装apin

apin是基于python3.6开发的，安装前请确认你的python版本>3.6

- #### 安装命令

    ```
    pip install apin
    ```



# 二、快速入门

## 1、项目创建

- #### 创建命令

    ```
     apin create 项目名
    ```

安装好apin之后，打开命令终端输入创建命令，即可在当前路径下创建项目。

cd 切换到项目之中，即可看到如下的项目结构

![1615961932491](C:\课件\images\1615961932491.png) 

- #### 项目文件说明

    - ###### document: apin使用文档

    - ###### casedata: 存放yaml和json格式编写的用例文件

    - ###### testcases:py：存放py编写的用例目录

    - ###### func_tools.py：自定义的函数工具文件

    - ###### setting.py：整个项目的全局配置文件

    - ###### run.py：项目运行入口文件





## 2、用例编写

apin用例编写支持yaml文件，json文件，py文件三种方式，下面通过一个接口的用例demo来快速了解一下

#### 1、接口demo：

- ###### 接口地址：http://httpbin.org/post

- ###### 请求方法：post

- ###### 请求参数类型：application/json

- ###### 请求参数:

    | 参数名 | 类型 | 说明 |
    | ------ | ---- | ---- |
    | user   | str  | 账号 |
    | pwd    | str  | 密码 |

#### 2、json编写用例

在项目的casedata目录下，定义一个以test开头的json文件，按照【apin用例编写规范-json】编写用例即可

- ##### 案例

    ```json
    {
      "host": "http://api.XXX.com/futureloan/",
      "Cases": [
        {
          "title": "普通用户注册",
          "interface": "member/register",
          "method": "post",
          "json":{"mobile_phone":"133010121224","pwd":"lemonban"},
          "verification": []
    
        }
      ]
    }
    ```

#### 3、yaml编写用例

在项目的casedata目录下，定义一个以test开头的yaml文件，按照【apin用例编写规范-yaml】编写用例即可

- ##### 案例

    ```
    # 域名
    host: http://api.XXX.com/futureloan/
    # 用例数据
    Cases:
      - title: 普通用户注册
        interface: member/register
        method: post
        json:
          mobile_phone: ${{user_mobile}}
          pwd: lemonban
    ```

    

#### 4、py文件编写用例

​	在testcases目录中定义一个以test开头的py文件，定义一个以Test开头的类，并且继承于apin.core.httptest.HttpCase类，按照【apin用例编写规范-py】编写用例即可

- ##### 案例

    ```python
    from apin.core.httptest import HttpCase
    
    class TestStreamV3(HttpCase):
        host = "http://api.XXX.com/futureloan/"
        Cases = [
            # 用例1：普通用户注册
            {
                'title': "普通用户注册",
                'interface': "member/register",
                "method": "post",
                'json': {"mobile_phone": "${{user_mobile}}", "pwd": "lemonban"},
            },
        ]
    ```

## 3、用例运行

- ##### 方式1：

    ###### 终端项目路径下输入命令

    ```python
    apin run
    ```

- ##### 方式2

    ###### 直接使用python运行项目的run.py文件



## 4、测试报告和日志

- ##### 日志：项目运行完，会自动在项目路径下生成详细的运行日志

    ![1615984513176](C:\课件\images\1615984513176.png)

- ##### 测试报告：apin的测试报告是基第三方库unittestreport生成的

    ###### 运行完会在项目目录的reports目录中，自动生成详细的html测试报告。

![1615966527547](C:\课件\images\1615966527547.png) 



# 三、用例编写规范

## 1、概念介绍：

- ##### 用例集：apin中创建的每一个test开头的用例文件(py,json,yaml)，被称之为一个用例集。一个用例集下面可以定义多条测试用例。

- ##### 测试用例： 用例集中Cases字段中的一条数据就是一个测试用例

    

## 2、用例集的主要字段介绍

- ##### host：用例接口的host地址(接口的域名) 

    - ###### 类型：字符串

    - ###### 例：

        ```python
        host = "http://api.lemonban.com/futureloan/"
        ```

        

- ##### headers：指定用例使用的请求头

    - ###### 类型：字典

    - ###### 例

        ```python
        headers = {"User-Agent": "apin/musen"}
        ```

- ##### method：指定用例接口的请求方法

    - ###### 类型：字符串

    - ###### 例：post,get

- ##### interface：指定用例接口地址（接口url域名后面的部分）

    - ###### 类型：字符串

- ##### env： 设置用例集运行环境的局部变量

    - ###### 类型：字典

    - ###### 例:

        ```python
         env = {
                "user_mobile": '13109099878',
                "pwd": 'lemonban'
            }
        ```

        

- ##### extract：指定用例请求完要提取的变量（详细介绍见：【四、变量提取和引用】）

- ##### verification：指定用例的断言（详细介绍见：【五、用例断言】）

- ##### Cases:设置该测试集下的用例（详细介绍见：下一节【用例字段介绍】）

## 3、用例字段介绍

### 1、主要字段：

- ##### 用例集中除env字段之外的字段

    - ###### 1、用例集中除env和Cases字段之外，上述用例集中的字段，均支持在用例中自定义。

    - ###### 2、如果用例中定义了用例集中的字段，就使用自己定义的，没定义则引用 用例集中的。

- ##### title：用例的描述字段（必传字段）

    测试报告和日志信息中用例的描述

- ##### json: 用来传递json类型的请求参数

    请求参数类型为：content-type:application/json，使用该字段来传递请求参数

- ##### data：用来传递表单类型的请求参数

    请求参数类型为：content-type: application/x-www-form-urlencoded，使用该字段来传递请求参数

- ##### params: 用来查询字符串参数

    请求参数，以？key=value的形式 拼接在url后面的参数

### 2、其他字段

除了上述主要字段之外，python中的requests库中的requests.request方法所有的请求参数，均支持在用例中定义字段，

这些字段在大多数情况下都用不到，如果有用到

- ##### files:接口用于文件上传

    请求参数类型为：content-type:application/from-data，使用该字段来传递请求参数,常用语文件上传

- ##### cookies：请求的cookie信息（apin中同一个用例集会自动化传递cookie,一遍情况下，不需要使用该字段来传递cookie）

- ##### auth: 用于Basic/Digest/Custom HTTP认证

- ##### timeout：设置http请求超时时间

- ##### allow_redirects：是否运行请求重定向

- ##### proxies：代理请求的

- ##### stream：是否立即下载响应内容

- ##### verify：是否进行证书校验（如果要忽略HTTPS请求的证书校验，则将此参数设置为False）

- ##### cert：指定校验证书的路径

## 4、用例编写

### 1、python编写用例

- ##### 步骤一、在testcases目录中定义一个以test开头的py文件，

- ##### 步骤二、在文件中定义一个以Test开头的类，并且继承于apin.core.httptest.HttpCase类

- ##### 步骤三、在类中，编写测试集的字段值

    - ##### 字段名 = 字段值

    ```python
    from apin.core.httptest import HttpCase
    class TestDomeV3(HttpCase):
        host = "http://api.lemonban.com/futureloan/"
        headers = {"X-Lemonban-Media-Type": "lemonban.v2"}
        # 定义测试前置方法
        setup_hook = {"timestamp": 'F{get_timestamp()}'}
        # 预设变量
        env = {
            "user_mobile": 'F{rand_phone("155")}',
            "admin_mobile": 'F{rand_phone("133")}'
        }
        # 结果校验
        verification = {"method": "eq",
                        "expected": {'code': 0, "msg": "OK"},
                        "actual": {'code': 'V{{$..code}}', "msg": "V{{$..msg}}"}}
    ```

- ##### 步骤四、在Cases字段中编写用例数据

    ```python
    from apin.core.httptest import HttpCase
    class TestDomeV3(HttpCase):
        host = "http://api.XXXX.com/futureloan/"
        headers = {"X-Lemonban-Media-Type": "lemonban.v2"}
        # 定义测试前置方法
        setup_hook = {"timestamp": 'F{get_timestamp()}'}
        # 预设变量
        env = {
            "user_mobile": 'F{rand_phone("155")}',
            "admin_mobile": 'F{rand_phone("133")}'
        }
        # 结果校验
        verification = {"method": "eq",
                        "expected": {'code': 0, "msg": "OK"},
                        "actual": {'code': 'V{{$..code}}', "msg": "V{{$..msg}}"}}
    	Cases = [
            # 用例1：普通用户注册
            {
                'title': "普通用户注册",
                'interface': "member/register",
                "method": "post",
                'json': {"mobile_phone": "${{user_mobile}}", "pwd": "lemonban"},
    
            },
            # 用例2：管理员注册
            {
                'title': "管理员注册",
                'interface': "member/register",
                "method": "post",
                'json': {"mobile_phone": "${{admin_mobile}}", "pwd": "lemonban", "type": 0}
            },
       ]
    ```

### 3、yaml编写用例

​	使用yaml编写用例前 建议先去学习一下yaml的语法

- ##### 步骤一：在casedata中定义一个test开头的yaml文件

- ##### 步骤二：在yaml文件中定义测试集的字段值

    ```yaml
    # 域名
    host: http://api.xxxxx.com/futureloan/
    # 请求头
    headers:
      X-Lemonban-Media-Type: lemonban.v2
    # 用例前置钩子函数
    setup_hook:
      timestamp: F{get_timestamp()}
    # 预设运行变量
    env:
      user_mobile: F{rand_phone("155")}
      admin_mobile: F{rand_phone("133")}
    # 结果校验字段
    verification:
      method: eq
      expected:
        code: 0
        msg: OK
      actual:
        code: 'V{{$..code}}'
        msg: 'V{{$..msg}}'
    ```

- ##### 步骤三：在Cases字段中编写测试用例

    ```yaml
    # 用例数据
    Cases:
      - title: 普通用户注册
        interface: member/register
        method: post
        json:
          mobile_phone: ${{user_mobile}}
          pwd: lemonban
      - title: 管理员注册
        interface: member/register
        method: post
        json:
          mobile_phone: ${{admin_mobile}}
          pwd: lemonban
          type: 0
    ```

### 4、json编写用例

使用yaml编写用例前 建议先去学习一下json的语法，json文件中字段名都需要使用双引号

- ##### 步骤一：在casedata中定义一个test开头的json文件

- ##### 步骤二：在json文件中定义测试集的字段值

- ##### 步骤三：在json文件中定义测试集的字段值

    ```json
    {
      "host": "http://api.XXXXX.com/futureloan/",
      "headers": {"X-Lemonban-Media-Type": "lemonban.v2"},
      "setup_hook": {"timestamp": "F{get_timestamp()}"},
      "env": {
        "user_mobile": "F{rand_phone('155')}",
        "admin_mobile": "F{rand_phone('133')}"
      },
      "verification": {"method": "eq",
                       "expected": {"code": 0,"msg": "OK"},
                       "actual": {"code": "V{{$..code}}","msg": "V{{$..msg}}"}
      },
      "Cases": [
        {
          "title": "普通用户注册",
          "interface": "member/register",
          "method": "post",
          "json": {
            "mobile_phone": "${{user_mobile}}",
            "pwd": "lemonban"
          }
        },
        {
          "title": "管理员注册",
          "interface": "member/register",
          "method": "post",
          "json": {
            "mobile_phone": "${{admin_mobile}}",
            "pwd": "lemonban",
            "type": 0
          }
        }
      ]
    }
    ```



# 四、变量提取和引用

变量提取和引用主要是为了解决接口之间的参数依赖问题

使用场景：接口A的参数中需要使用接口B返回的某个数据，那么就要在请求B接口之后，提取数据保存，给请求A接口时使用。

## 1、变量提取

在用例集或用例数据中，通过extract字段指定要提取的变量。

- ##### 语法

    ```python
    "extract": {
       "变量名": ("变量保存的级别", "提取方式", "提取表达式"),
    }
    ```

    - ##### 变量名：保存数据的变量名

    - ##### 变量保存的级别：

        - ###### EVN: 全局变量，settings文件中的EVN

        - ###### env : 为局部变量(只对当前用例集有效)：用例集的env字段

    - ##### 提取方式

        - ###### re: 正则表达式提取

        - ###### jsonpath： 通过jsonpath提取

- ##### 案例

    ```python
    "extract": {
        # 通过jsonpath提取
       "token": ("env", "jsonpath", "$..token"),
        # 通过正则表达式提取
       'member_id': ("env", "re", r'"id":(.+?),')
    }
    ```

    

## 2、变量引用

- ##### 变量引用表达式：${{变量名}}

- ##### 引用优先级

    优先引用该用例的局部变量(用例的env中的变量)，如果局部变量不存在，则会引用全局变量(setting.py中ENV中保存的变量)。



# 五、用例断言

关于测试用例预期结果和实际结果的比对的,apin中封装了一个verification字段，只需要在verification中定义预期结果，实际结果提取表达式，和断言的方法，即可实现用例的断言！

### 1、基本语法

```python
verification = [
        [断言方式, 预期结果, 实际结果]
    ] 
```

### 2、断言方式

apin中目前支持两种断言方式：

- ###### 1、断言相等 ：eq

    预期结果和实际结果相等

    ```
    verification = [
            ['eq', 预期结果, 实际结果]
        ] 
    ```

- ###### 2、断言包含：contians

    实际结果中包含预期结果的内容

    ```
    verification = [
            ['contians', 预期结果, 实际结果]
        ] 
    ```

### 3、实际结果获取

​	关于断言的实际结果提取，需要使用`V{{表达式}}`来进行提取，表达式支持jsonpath和正则表达式两种提取方式方式。

- ##### 1、正则表达式提取

    ```python
    # 通过正则表达式来提取实际结果中的msg字段。
    verification = [
            ['contians', {'msg':"OK"}, {"msg": "V{{msg:'(.+?)'}}"}]
        ] 
    
    ```

- ##### 2、通过jsonpath提取

    ```python
    # 通过jsonpath来提取实际结果中的msg字段。
    verification = [
            ['contians', {'msg':"OK"}, {"msg": 'V{{$..msg}}']
        ] 
    
    ```

### 4、HTTP状态码的断言

​	上述两种方式，以可提取结果返回的数据，那如果要断言接口http请求的状态码呢？apin中也提供了一个内置的字段名，来表示http状态码

```python
# 断言接口请求的http状态码是否等于200
verification = [
        ['eq', 200, 'status_code']
    ] 
```



# 六、函数工具的使用

apin支持在测试用例中调用自定义的函数来处理数据，如对数据进行加密处理、随机生成数据等等。

#### 1、自定义函数

apin创建的项目中有一个funcTools.py，在该文件中可以自己定义函数，然后在用例中通过F{xxx()}来调用。

- ##### 案例：funcTools.py文件

```python
import hashlib,random

def md5_encrypt(msg):
    """md5加密"""
    md5 = hashlib.md5()  
    md5.update(msg.encode("utf8"))  
    return md5.hexdigest()

def rand_phone():
	"""随机生成手机号的函数"""
    import random
    for i in range(8):
        phone += str(random.randint(0, 9))
    return str(phone)


def get_timestamp():
    """获取时间戳"""
    return time.time()

```

- ##### 注意点：函数处理完的数据需要return返回哦

### 2、用例中引用函数

- ###### 引用表达式：F{函数名()}

- ##### demo1:用例数据中的user，引用前面定义的rand_phone函数

```python
{
	'title': "普通用户注册",
	'interface': "member/register",
	"method": "post",
	'json': {"user": "F{rand_phone()}", "pwd": "lemon123"},
}
```

- ##### demo2:用例数据中的pwd，引用前面定义的md5_encrypt函数对密码进行md加密

    - 注意点：引用的函数，传递的参数如果是变量，则不需要在变量应用表达式外加引号

```python
{
	'title': "普通用户登录",
	'interface': "member/login",
	"method": "post",
	'json': {"user": "13109877890", "pwd": "F{md5_encrypt('lemon123')}"},
}

# 引用函数，变量作为参数传递
{
	'title': "普通用户登录",
	'interface': "member/login",
	"method": "post",
	'json': {"user": "${{user}}", "pwd": "F{md5_encrypt(${{pwd}})}"},
}
```



# 七、项目全局配置

项目中的setting.py文件，是整个项目的配置文件，接下来相信介绍一下项目的配置选项。

### 1、debug模式运行

项目创建之后，默认运行是开启了debug模式，运行过程中会输出详细的debug级别日志。如果不像看运行日志，则将settings中的DEBUG设置为Flase即可。

```
# 是否开启debug模式：True为debug模式，False为关闭debug模式
DEBUG = False
```



### 2、ENV全局的变量

将settings.py中的ENV可以设置项目全局配置，

- #### 全局的域名

    推荐在ENV中设置全局的host,不建议在每一个测试用例中去设置host,切换测试环境切换也更方便(如果用例数据中没有自己定义host，会自动引用全局的host地址)

    ```python
    ENV = {
        "host":"http://WWW.XXX.com/",
    }
    ```

    

- #### 全局的请求头

    如果项目接口有必传的请求头数据，也可以直接在ENV中设置(如果用例数据中没有定义时，也会自动引用全局的headers)。

    ```python
    ENV = {
        "host":"http://WWW.XXX.com/",
        "headers": {"UserAgent": "apin-test01"}
    }
    ```

- #### 全局的测试数据

    如果用例中需要引用事先准备好的一些测试数据，如测试账号、密码之类的

    如：定义一个测试账号、测试密码、用户id

    ```python
    ENV = {
        "host":"http://WWW.XXX.com/",
        "headers": {"UserAgent": "apin-test01"},
        "user":"musen@qq.com",
        "pwd":"lemon123",
        "user_id":111
    }
    ```

    测试用例中直接使用${{}}即可引用，

    ```python
    # 引用user和pwd
    {
     'title': "登录",
     'interface': "member/register",
     "method": "post",
     'json': {"mobile_phone": "${{user}}", "pwd": "${{pwd}}"},
    }
    ```

    - ##### 注意点：如果局部环境和全局变量重名，优先引用局部变量。



### 3、测试报告

​	通过setting中的TEST_RESULT，可以配置测试报告的输出信息。

```python
TEST_RESULT = {
    # 测试报告文件名
    "filename": "report.html",
    # 测试人员
    "tester": "测试员",
    # 报告标题
    "title": "测试报告",
    # 报告样式 ：有1，2，三个样式
    "templates": 1,
    # 报告描述信息
    "desc": "XX项目测试生成的报告"
}
```



### 4、邮件推送测试结果

如果要将测试结果发送到指定的邮箱中，则在settings.py添加EMAIL配置即可

```python
EMAIL = {
    # smtp服务器地址
    "host": 'smtp.qq.com',
    # smtp服务器端口
    "port": 465,
    # 邮箱账号
    "user": "xxxx@qq.com",
    # smtps授权码
    "password": "xxxx",
    # 收件人列表
    "to_addrs": ['xxx@qq.com','xxx@qq.com'],
    # 是否发送附件
    "is_file": True
}
```



### 5、测试结果推送到钉钉群

如果要将测试结果推送到钉钉群，则在settings.py添加DINGTALK配置即可。

```python
DINGTALK = {
    #  钉钉机器人的Webhook地址
    "url": "",
    # 如果钉钉机器人安全设置了关键字，则需要传入对应的关键字
    "key": None,
    # 如果钉钉机器人安全设置了签名，则需要传入对应的密钥
    "secret": None,
    # 钉钉群中要@人的手机号列表，如：[137xxx,188xxx]
    "atMobiles": [],
    # 是否@所有人
    "isatall": False
}
```



### 6、测试结果推送企业微信群

如果要将测试结果推送到企业微信群，则在settings.py添加WECHAT配置即可。

```python
WECHAT = {
    # 企业微信群ID
    "chatid": "",
    # 调用企业微信API接口的凭证
    "access_token": ""
}
```



# 八、用例前后置执行

关于测试用例执行的前后置，apin中提供了四个字段来指定用例前后置执行的函数。

#### 1、setup_hook 

- ###### 指定用例  的前置执行函数

    ```python
    # 设置一个用例级别的前置函数，将前置函数的返回值，保存到局部变量的timestamp
    setup_hook = {"timestamp": 'F{get_timestamp()}'}
    ```

    

#### 2、setup_class_hook

- ###### 指定用例集  的前置执行函数

    ```python
    # 设置一个测试集级别的前置函数，将前置函数的返回值，保存到局部变量的timestamp
    setup_class_hook = {"timestamp": 'F{get_timestamp()}'}
    ```

####  3、teardown_hook

- ###### 指定用例 的后置执行函数

    ```python
    # 设置一个用例级别的后置
    teardown_hook = {"teardowm": 'F{data_clear()}'}
    ```

####  4、teardown_class_hook

- ###### 指定用例集的后置执行函数

    ```python
    # 设置一个测试集级别的后置方法
    teardown_hook = {"teardowm": 'F{data_clear()}'}
    ```

    

1