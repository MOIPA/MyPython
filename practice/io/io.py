# *******************************************8 文件读写
try:
import json
import os
import codecs
f = open('/home/william/Documents/mysql_save.py', 'r')
text = f.read()
print(text)
finally:
    f.close()
# 使用with就可以自动close
with open('/home/william/Documents/mysql_save.py', 'r') as f:
    f.read()
    for line in f.readlines():
        print(line)

# Python还提供了一个codecs模块帮我们在读文件时自动转换编码，直接读出unicode：
with codecs.open('/Users/michael/gbk.txt', 'r', 'gbk') as f:
    f.read()  # u'\u6d4b\u8bd5'

# 写文件

f = open('/xxx', 'w')
f.write('hello')
f.close()
# 只有close的瞬间才会写入磁盘
with open('/assas', 'w') as f:
    f.write('test')

# ************************************************** 文件目录
os.name
os.uname
os.environ
os.getenv('PATH')

# 操作文件和目录的函数一部分放在os模块中，一部分放在os.path模块中，这一点要注意一下。查看、创建和删除目录可以这么调用：

# 查看当前目录的绝对路径:
os.path.abspath('.')
'/Users/michael'
# 在某个目录下创建一个新目录，
# 首先把新目录的完整路径表示出来:
os.path.join('/Users/michael', 'testdir')
'/Users/michael/testdir'
# 然后创建一个目录:
os.mkdir('/Users/michael/testdir')
# 删掉一个目录:
os.rmdir('/Users/michael/testdir')
# 把两个路径合成一个时，不要直接拼字符串，而要通过os.path.join()函数，这样可以正确处理不同操作系统的路径分隔符。在Linux/Unix/Mac下，os.path.join()返回这样的字符串：
# part-1/part-2
# 而Windows下会返回这样的字符串：
# part-1\part-2
# 同样的道理，要拆分路径时，也不要直接去拆字符串，而要通过os.path.split()函数，这样可以把一个路径拆分为两部分，后一部分总是最后级别的目录或文件
os.path.split('/Users/michael/testdir/file.txt')
# ('/Users/michael/testdir', 'file.txt')
os.path.splitext()  # 可以直接让你得到文件扩展名，很多时候非常方便：

os.path.splitext('/path/to/file.txt')
# ('/path/to/file', '.txt')
# 这些合并、拆分路径的函数并不要求目录和文件要真实存在，它们只对字符串进行操作。

# 文件操作使用下面的函数。假定当前目录下有一个test.txt文件：

# 对文件重命名:
os.rename('test.txt', 'test.py')
# 删掉文件:
os.remove('test.py')

# 但是复制文件的函数居然在os模块中不存在！原因是复制文件并非由操作系统提供的系统调用。理论上讲，我们通过上一节的读写文件可以完成文件复制，只不过要多写很多代码。

# 幸运的是shutil模块提供了copyfile()的函数，你还可以在shutil模块中找到很多实用函数，它们可以看做是os模块的补充。

# 最后看看如何利用Python的特性来过滤文件。比如我们要列出当前目录下的所有目录，只需要一行代码：

[x for x in os.listdir('.') if os.path.isdir(x)]
# ['.lein', '.local', '.m2', '.npm', '.ssh', '.Trash', '.vim', 'Adlm', 'Applications', 'Desktop', ...]
# 要列出所有的.py文件，也只需一行代码：

[x for x in os.listdir('.') if os.path.isfile(
    x) and os.path.splitext(x)[1] == '.py']
# ['apis.py', 'config.py', 'models.py', 'pymonitor.py', 'test_db.py', 'urls.py', 'wsgiapp.py']

# *******************************************序列化
# 序列化内存的东西存储到磁盘中,也可以用于网络传输：叫pickling
# iPython提供两个模块来实现序列化：cPickle和pickle。这两个模块功能是一样的，区别在于cPickle是C语言写的，速度快，pickle是纯Python写的，速度慢，跟cStringIO和StringIO一个道理。用的时候，先尝试导入cPickle，如果失败，再导入pickle：
try:
    import cPickle as pickle
except ImportError:
    import pickle
d = dict(name='tr', age=18)
result = pickle.dumps(d)
print(result)
# 可以将这个str存入本地文件

# 打开序列化
l_d = pickle.load(result)


# 序列化还有一个是json
# json.dumps()
# json序列化类 由于类不可以被序列化，只能序列化dict，可以写一个转化函数


def student(object):
    def __init__(self, name, age, score):
        self.name = name
        self.age. = age
        self.score = score


def student2dict(std):
    return{
        'name': std.name,
        'age': std.age,
        'score': std.score
    }


s = student('tr', 11, 11)
print(json.dumps(s, default=student2dict))

# 但是写函数比较麻烦，可以使用lambda 每个类都有dict属性，
print(json.dumps(s, default=lambda obj: obj.__dict__))

# json转为类对象 需要写转换函数


def dict2student(d):
    return Student(d['name'], d['age'], d['score'])


json_str = '{"age": 20, "score": 88, "name": "Bob"}'
s = json.loads(json_str, object_hook=dict2student)
