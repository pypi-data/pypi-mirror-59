# 独立使用 django orm

## 安装

`pip install django-orm-layer`

## 创建项目

运行 `django-orm create` 可以得到如下目录:

```
.
└── orm
    ├── __init__.py
    ├── example_1
    │   ├── __init__.py
    │   ├── migrations
    │   │   └── __init__.py
    │   └── models.py
    ├── example_2
    │   ├── __init__.py
    │   ├── migrations
    │   │   └── __init__.py
    │   └── models
    │       ├── __init__.py
    │       ├── base.py
    │       └── many_to_many.py
    ├── manage.py
    └── settings.py
```

`example_1`和`example_2`为相应示例

## 创建新示例

`django-orm addapp your_app_name template_no`

`template_no`取`1`或`2`

`1`对应`example_1`示例

`2`对应`example_2`示例


## makemigrations

`django-orm makemigrations`


## migrate

`django-orm migrate`


## 使用内建的User

参考`settings.py`中的`INSTALLED_APPS`


## 原生命令使用

`python -m orm.manage <subcommand>`


## 由已有数据据生成model

1. `settings.py`中配置好连接
2. `python -m orm.manage inspectdb`


## 测试

```
In [1]: from orm.example_1.models import *

In [2]: Person
Out[2]: orm.example_1.models.Person

In [3]: Person.objects.all()
Out[3]: <QuerySet []>

```
