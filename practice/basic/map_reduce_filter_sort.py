#map()函数接收两个参数，一个是函数，一个是序列，map将传入的函数依次作用到序列的每个元素，并把结果作为新的list返回。
from functools import reduce

def func(x):
    return x*x

res = map(func,[1,2,3,4,5])
for i in res:
    print(i)

# reduce(f, [x1, x2, x3, x4]) = f(f(f(x1, x2), x3), x4)

def func2(x,y):
    return x+y


from functools import reduce
res = reduce(func2,[1,2,3,4])
print(res)

print(reduce(lambda x, y: x + y, [1, 3, 4, 6, 8]))

from functools import reduce
# 字符串转数字
def str2Num(s):
    def toNum(s):
        return {'0': 0, '1': 1, '2': 2, '3': 3, '4': 4, '5': 5, '6': 6, '7': 7, '8': 8, '9': 9}[s]

    def addNum(x,y):
        return x*10+y
    
    return reduce(addNum,map(toNum,s))

# 牛逼的python 一行解决
def str2NumLambda(s):
    return reduce(lambda x,y:x*10+y,map(lambda x:{'0': 0, '1': 1, '2': 2, '3': 3, '4': 4, '5': 5, '6': 6, '7': 7, '8': 8, '9': 9}[x],s))
print(str2NumLambda('123'))


# filter 
def is_odd(num):
    return num%2==1
res = filter(is_odd,[1,2,3,4,5])
print([x for x in res])

# sort
res = sorted([134,1,23,5,1,3,5])
print(res)
# sort 自定义判断函数  一下只有python2可用，python3中函数只能一个参数
def reversed_cmp(x,y):
    if x>y:
        return -1
    if x<y:
        return 1
    return 0
print(sorted([134,1,23,5,1,3,5],reversed_cmp))

# sort 自定义函数 lambda python3写法
students = [(‘john’, ‘A’, 15), (‘jane’, ‘B’, 12), (‘dave’,’B’, 10)]
sorted(students,key=lambda s: x[2]) 
