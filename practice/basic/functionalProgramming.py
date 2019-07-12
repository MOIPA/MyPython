# 函数式编程

# 高阶函数：可以接受其他函数

def add(x,y,f):
    return f(x)+f(y)

result = add(1,-1,abs)
print(result)

# 函数作为返回值  闭包：do_sum作为内部函数可以调用外部函数的参数和变量并且都保存在返回的函数中
# 闭包函数只有调用才执行，所以如果返回的函数中调用后续可能变化的变量，这是不行的
from functools import reduce
def lazy_sum(*args):
    def do_sum():
        return reduce(lambda x,y:x+y,args)
    return do_sum

f = lazy_sum(1,2,3,4)
f1 = lazy_sum(1,2,3,4)
print(f==f1)
print(f())
