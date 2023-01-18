import queue
import os


# queue测试

q = queue.Queue(5)  #如果不设置长度,默认为无限长
print(q.maxsize)  #注意没有括号
q.put(123)
q.put(456)
q.put(789)
q.put(100)
q.put(111)
#q.put(233)
print(q.get())
print(q.get())
