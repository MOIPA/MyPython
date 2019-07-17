# 单元测试
# 重写dict 用于测试


import unittest


class Dict(dict):
    def __init__(self, **kws):
        super().__init__(**kws)

    def __getarrt__(self, key):
        try:
            return self[key]
        except KeyError:
            raise AttributeError('Dict doesn\'t have such attr %s' % key)

    def __setattr__(self, key, value):
        self[key] = value

# d = Dict(a=1)
# print(d)


# test
class TestDict(unittest.TestCase):
    def setUp(self):
        print('setup')

    def tearDown(self):
        print('teardown')

    def test_init(self):
        d = Dict(a=1, b='test')
        self.assertEquals(d.get('a'), 1)
        self.assertEquals(d.get('b'), 'test')
        self.assertTrue(isinstance(d, dict))

    def test_key(self):
        d = Dict()
        d['key'] = 'value'
        self.assertEquals(d['key'], 'value')

    def test_attr(self):
        d = Dict()
        d['key'] = 'value'
        self.assertTrue('key' in d)
        self.assertEquals(d['key'], 'value')

    def test_keyerror(self):
        d = Dict()
        with self.assertRaises(KeyError):
            value = d['empty']

    def test_attrerror(self):
        d = Dict()
        with self.assertRaises(AttributeError):
            value = d.empty


'''
编写单元测试时，我们需要编写一个测试类，从unittest.TestCase继承。

以test开头的方法就是测试方法，不以test开头的方法不被认为是测试方法，测试的时候不会被执行。

对每一类测试都需要编写一个test_xxx()方法。由于unittest.TestCase提供了很多内置的条件判断，我们只需要调用这些方法就可以断言输出是否是我们所期望的。最常用的断言就是assertEquals()：

self.assertEquals(abs(-1), 1) # 断言函数返回的结果与1相等
另一种重要的断言就是期待抛出指定类型的Error，比如通过d['empty']访问不存在的key时，断言会抛出KeyError：

with self.assertRaises(KeyError):
    value = d['empty']
而通过d.empty访问不存在的key时，我们期待抛出AttributeError：

with self.assertRaises(AttributeError):
    value = d.empty
'''

# 执行单元测试
if __name__ == '__main__':
    unittest.main()
