# 切片测试
vec = [0, 1, 2, 3, 4, 5, 6, 7, 8 ,9]
vec_1 = vec[0:-1]
print(vec_1)

vec_str = ''
for ele in vec:
    vec_str += '{:.2f}_'.format(ele)
print(vec_str)