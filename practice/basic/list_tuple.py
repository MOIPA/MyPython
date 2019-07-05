list_num = [1, 2, 3, 4, 5]
print(list_num[-1])  # 3

# delete
list_num.pop()  # delete the end one
list_num.pop(2)  # delete the third one
print(list_num)

# add
list_num.append(6)
list_num.insert(0, -1)

# update
list_num[0] = 0

# tow dimensional array
one = [2.1, 2.2, 2.3]
array = [1, one, 2, 3]
print(array[1][0])

# tuple ,can't be changed once inited
t = (1, 2, 3)
