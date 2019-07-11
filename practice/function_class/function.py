# default arguments
def student(name, age, city='none', sex='m'):
    pass


# enroll
student('tr', 18)
student('tr', 18, city='bj')

# changable arguments


def calc(*num):
    for n in num:
        print(n)


calc(1)
calc(1, 2)
# changable arguments by **


def person(name, age, **arg):
    print(name)
    print(arg)


person('tr', 18, city='333')

# ***********************************note
# 默认参数很有用，但使用不当，也会掉坑里。默认参数有个最大的坑，演示如下：
# 先定义一个函数，传入一个list，添加一个END再返回：


def add_end(L=[]):
    L.append('END')
    return L
# 当你正常调用时，结果似乎不错：


add_end([1, 2, 3])
[1, 2, 3, 'END']
add_end(['x', 'y', 'z'])
['x', 'y', 'z', 'END']
# 当你使用默认参数调用时，一开始结果也是对的：

add_end()
['END']
# 但是，再次调用add_end()时，结果就不对了：

add_end()
['END', 'END']
add_end()
['END', 'END', 'END']
# 很多初学者很疑惑，默认参数是[]，但是函数似乎每次都“记住了”上次添加了'END'后的list。

# 原因解释如下：
# Python函数在定义的时候，默认参数L的值就被计算出来了，即[]，因为默认参数L也是一个变量，它指向对象[]，每次调用该函数，如果改变了L的内容，则下次调用时，默认参数的内容就变了，不再是函数定义时的[]了。
# 所以，定义默认参数要牢记一点：默认参数必须指向不变对象！
# 要修改上面的例子，我们可以用None这个不变对象来实现：


def add_end_new(L=None):
    if L is None:
        L = []
    L.append('END')
    return L
# 现在，无论调用多少次，都不会有问题：

# 可变参数调用ｃａｌｃ( *nums) ****************************
def calc(*num):
    for i in num:
        print("%d" % i)
        
# calc(0,1)
# 如果这时候是一个list怎么办
nums = [0, 1, 2, 3]
calc(*nums)

 # 关键字参数××××××××××××××××××××××××××××××××××××××
 # 可变参数允许你传入0个或任意个参数，这些可变参数在函数调用时自动组装为一个tuple。而关键字参数允许你传入0个或任意个含参数名的参数，这些关键字参数在函数内部自动组装为一个dict。
def person(name,age,**kwargs):
        print ('name',name,'age',age,'kw',kwargs)

# person('mic',18)
# 这时候瞎传一些参数也可以,但是瞎传的参数要带上关键字，不然咋叫关键字参数
# 这些参数带关键字，那么肯定可以传入dict参数
person('mic',18,sis=18,nickname='gg')

# dict参数传入，但是参数前要使用**
kw={'kw1':1,'kw2':'2'}
person('tr',18,**kw)


# ******************************
# 参数组合
# 在Python中定义函数，可以用必选参数、默认参数、可变参数和关键字参数，这4种参数都可以一起使用，或者只用其中某些，但是请注意，参数定义的顺序必须是：必选参数、默认参数、可变参数和关键字参数。

# 比如定义一个函数，包含上述4种参数：

def func(a, b, c=0, *args, **kw):
    print 'a =', a, 'b =', b, 'c =', c, 'args =', args, 'kw =', kw
# 在函数调用的时候，Python解释器自动按照参数位置和参数名把对应的参数传进去。


>> > func(1, 2)
a = 1 b = 2 c = 0 args = () kw = {}
>> > func(1, 2, c=3)
a = 1 b = 2 c = 3 args = () kw = {}
>> > func(1, 2, 3, 'a', 'b')
a = 1 b = 2 c = 3 args = ('a', 'b') kw = {}
>> > func(1, 2, 3, 'a', 'b', x=99)
a = 1 b = 2 c = 3 args = ('a', 'b') kw = {'x': 99}
# 最神奇的是通过一个tuple和dict，你也可以调用该函数：

>> > args = (1, 2, 3, 4)
>> > kw = {'x': 99}
>> > func(*args, **kw)
a = 1 b = 2 c = 3 args = (4,) kw = {'x': 99}
# 所以，对于任意函数，都可以通过类似func(*args, **kw)的形式调用它，无论它的参数是如何定义的。
