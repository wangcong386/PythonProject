#!/usr/bin/python
# -*- coding: UTF-8 -*-

print('这是字符串，', end="")
print('这里的字符串不会另起一行')

# 多变量赋值
a = [1, 2]
b = a
a[1] = 3
print('b changed=', b)

a = [1, 2]
b = a[:]
a[1] = 3
print('b not changed=', b)
