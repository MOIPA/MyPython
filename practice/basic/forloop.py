# input form user
name = input('name:')

# for loop
x = [i for i in range(10)]
print(x)

for i in [x*2 for x in range(10)]:
    print(i)

f = [x + y for x in 'ABCDE' for y in '1234567']
print(f)

for x,y in [(1,1),(2,4)]:
    print(x,y)

# 判断是否可迭代
from collections.abc import Iterable
print(isinstance('str',Iterable))

# 想同时迭代下标和值怎么办
# 原始的
count=0
for i in ['a','b','c']:
    print(i,count)
    count+=1
# 方便的
for i,value in enumerate(['a','b','c']):
    print(i,value)

# 同时迭代dict的key和value要使用dict的items python2是iteritems
d = {'a':'b','b':'c'}
for i,value in d.items():
    print(i,value)


# 双遍历
for x,y in [(1,2),(3,4)]:
    print(x,y)

# 遍历和判断的结合

test = [x for x in range(1,10) if x%2==0]
print(test)
test = [x if x%2==0 else -x for x in range(1,10)]
print(test)

# 总结用法：列表生成式
# （对被遍历的值k,v进行操作） for k,v(被遍历的值) in ....
#  双重循环就是 ：（对m和n的操作）for m in .. for n in ..

L = ['Hello', 'World', 18, 'Apple', None]
out = [s.lower() for s in L if isinstance(s,str)]
print(out)