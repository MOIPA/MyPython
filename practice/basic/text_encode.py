# in RAM all text would be translated to Unicode
# while in Disk there are UTF-8

str = u'编码' # Unicode now
str = str.encode('utf-8') # UTF-8
print(str)

str = str.decode('utf-8')
print(str)

# riverse
a = u'\u5916'
print(a)
a = a.encode('utf-8')
print(a)

# -*- coding: utf-8 -*-
# the above line means read the code file in utf-8

# format string
str = 'hello,%s, the num is %d' % ('world',10)
print(str)
str = '%.2f' % 3.14111
print(str)
str = '%d%%' % 10
print(str)