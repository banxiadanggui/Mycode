import random
import copy

# 创建一个包含可变对象的原始列表
original_list = [1, 2, 3, [4, 5], {'key': 'value'}]

# 深拷贝原始列表
copied_list = copy.deepcopy(original_list)

# 在复制的列表上随机选择元素
# k 参数指定要选取的元素数量
new_list = random.choices(copied_list, k=3)

# 打印原始列表和新列表
print("Original List:", original_list)
print("New List:", new_list)

# 修改新列表中的一个可变对象
if [4, 5] in new_list:
    new_list[new_list.index([4, 5])].append(6)
if {'key': 'value'} in new_list:
    new_list[new_list.index({'key': 'value'})]['new_key'] = 'new_value'

# 打印修改后的新列表
print("Modified New List:", new_list)

# 验证原始列表是否未被改变
print("Original List After Modification:", original_list)