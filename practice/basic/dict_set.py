d = {'name': 'tr', 'age': 18}
print(d['name'])
for key in d:
    print(key)

# delete
d.pop('name')
print(d)

# read
d['none']  # error occured
d.get('none')  # return none

# judge
'name' in d  # False

# set***********
s = set([1, 2, 3, 1, 2])  # no repeat data
s2 = set([7, 9, 1, 3])
print(s)

# add
s.add(4)

# remove
s.remove(1)

# s U s2
print(s | s2)

# s n s2
print(s & s2)
