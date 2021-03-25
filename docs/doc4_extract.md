# 

变量提取和引用主要是为了解决接口之间的参数依赖问题

使用场景：接口A的参数中需要使用接口B返回的某个数据，那么就要在请求B接口之后，提取数据保存，给请求A接口时使用。

## 1、变量提取

在用例集或用例数据中，通过extract字段指定要提取的变量。

**语法**

```python
"extract": {
   "变量名": ("变量保存的级别", "提取方式", "提取表达式"),
}
```

**变量保存的级别**：

- EVN: 全局变量，settings文件中的EVN

- env : 为局部变量(只对当前用例集有效)：用例集的env字段

**提取方式**

- re: 正则表达式提取

- jsonpath： 通过jsonpath提取

**案例**

```python
"extract": {
    # 通过jsonpath提取
   "token": ("env", "jsonpath", "$..token"),
    # 通过正则表达式提取
   'member_id': ("env", "re", r'"id":(.+?),')
}
```



## 2、变量引用

- **变量引用表达式**：`${{变量名}}`

    在用例数据中引用变量，需要安装apin中定义的变量引用语法`${{name}}`来

- **引用优先级**

    优先引用该用例的局部变量(用例的`env`中的变量)，如果局部变量不存在，则会引用全局变量(`setting.py`中`ENV`中保存的变量)。
