# %% 整数---加减乘除/乘方/运算次序

a0 = 3+2
a1 = 3-4
a2 = 3*8
a3 = 3/5
print('a0={}, a1={}, a2={}, a3={}'.format(a0, a1, a2, a3))

a4 = 3**4
print('a4={}'.format(a4))

a5 = (2+4)*3
print('a5={}'.format(a5))

# %% 浮点数---加减乘除
a6 = 0.1+0.04
a7 = 0.1-0.05
a8 = 0.04*0.03
a9 = 0.1/0.6
print('a6={}, a7={}, a8={}, a9={}'.format(a6, a7, a8, a9))

# 包含小数位数不确定
print(0.2+0.1)

# %% 整数和浮点数
# 任意两个数相除时结果总是浮点数，无论是否能整除
a10 = 4/2
print('a10={}'.format(a10))

# 任何其他运算，操作数只要有浮点数出现，结果总是浮点数
a11 = 1+2.0
a12 = 2*3.0
a13 = 3.0**2
print('a11={}, a12={}, a13={}'.format(a11, a12, a13))

# %% 数字中的下划线
# 书写很大的数，可以使用下划线将数字分组，python解析时会将下划线自行去掉
a14 = 14_00_0_00_0_001
print('a14={}'.format(a14))

# %% 同时赋值多个变量
a15, a16, a17 = 1, 2, 3
print('a15={}, a16={}, a17={}'.format(a15, a16, a17))

# %% 常量---全部大写将某个变量视为常量
ABCD = 1234
print('ABCD={}'.format(ABCD))

# %% python之禅 import this
'''
The Zen of Python, by Tim Peters

Beautiful is better than ugly.
Explicit is better than implicit.
Simple is better than complex.
Complex is better than complicated.
Flat is better than nested.
Sparse is better than dense.
Readability counts.
Special cases aren't special enough to break the rules.
Although practicality beats purity.
Errors should never pass silently.
Unless explicitly silenced.
In the face of ambiguity, refuse the temptation to guess.
There should be one-- and preferably only one --obvious way to do it.
Although that way may not be obvious at first unless you're Dutch.
Now is better than never.
Although never is often better than *right* now.
If the implementation is hard to explain, it's a bad idea.
If the implementation is easy to explain, it may be a good idea.
Namespaces are one honking great idea -- let's do more of those!
'''
# %%
