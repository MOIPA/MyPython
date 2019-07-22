# tuple 可以表示不变集合: namedtuple
# 定义坐标
from collections import defaultdict
from collections import deque
from collections import namedtuple
# p = (1, 2)
# 但是这样不容易看出p的作用

Point = namedtuple('Point', ['x', 'y'])
p = Point(1, 2)
print('x:%s y:%s' % (p.x, p.y))

# deque
# list 便于访问但是插入删除速度慢，python的list类似array
q = deque(['a', 'b', 'c'])
q.append('d')
q.appendleft('x')
print(q)

# defaultdict
# 使用dict时如果没有会跑出异常，如果希望返回一个默认值可以用这个
dd = defaultdict(lambda: 'NO/Data')
dd['key1'] = 'abc'
dd['key2'] = '2'
print(dd['key3'])

# orderedDict 如果希望使用的key有顺序
from collections import OrderedDict

d = dict((['b',2],['a',1]))
od = OrderedDict((['b',2],['a',1]))
print(d)
print(od)
od.keys()

# Counter 简单计数，统计字符出现个数
from collections import Counter
c = Counter() #本质是个dict

for ch in 'test string':
    c[ch]+=1

print(c)
