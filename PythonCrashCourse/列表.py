laptop = ['dell', 'apple', 'lenovo', 'acer']
# 通过索引访问列表元素
print(laptop[0])
print(laptop[0].title())
print(laptop[-1])
msg = f'my first laptop is {laptop[2].title()}'
print(msg)

# 修改列表元素的值
laptop[1] = 'huawei'
print('laptop list after modification', laptop)

# 列表末尾添加元素
laptop.append('xiaomi')
print('laptop list after add element at the end', laptop)

# 列表中任意位置添加元素，注意如果插入到-1位置，并非占据倒数第一个位置，而是插入倒数第一个元素之前的位置
laptop.insert(0, 'sumsung')
print('laptop list after add element into any position', laptop)

# 列表中删除元素---已知元素下标
del laptop[-1]
print('laptop list after delete element in any position', laptop)

# 列表中删除元素---弹出末尾元素pop()
last_one = laptop.pop()
print('laptop list after delete last element', laptop)
print('last element', last_one)

# 列表中删除元素---弹出任意位置元素pop(idx)
ele_pop = laptop.pop(0)
print('laptop list after pop first element', laptop)
print('element pop', ele_pop)

ele_pop_last = laptop.pop(-1)
print('laptop list after pop last element', laptop)
print('element pop', ele_pop_last)

# 列表中删除元素---根据值删除
laptop.remove('dell')
print('laptop list after remove dell', laptop)

# 组织列表---永久排序
cars = ['bmw', 'audi', 'toyota,', 'subaru']
cars.sort()
print('cars list after sort', cars)

# 组织列表---反向永久排序
cars.sort(reverse=True)
print('cars list after reversed sort', cars)

# 组织列表---临时排序
food = ['rice', 'apple', 'cabbage', 'banana']
food_sorted = sorted(food)
print('food original', food)
print('food sorted', food_sorted)

# 组织列表---反转列表，永久反转
food.reverse()
print('food reversed', food)

# 组织列表---确定列表长度
print('food length', len(food))

# 组织列表---使用range()创建数字列表
num_list = list(range(12))
print('num_list', num_list)
