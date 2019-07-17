# logging 模块记录错误
import logging
logging.basicConfig(level=logging.INFO) # 指定输出什么级别的信息

def foo(s):
    return 10 / int(s)


def bar(s):
    return foo(s) * 2


def main():
    logging.info('start program')
    try:
        bar('0')
    except Exception as e:
        logging.exception(e)


main()
'''
这就是logging的好处，它允许你指定记录信息的级别，有debug，info，warning，error等几个级别，当我们指定level=INFO时，logging.debug就不起作用了。同理，指定level=WARNING后，debug和info就不起作用了。这样一来，你可以放心地输出不同级别的信息，也不用删除，最后统一控制输出哪个级别的信息。

logging的另一个好处是通过简单的配置，一条语句可以同时输出到不同的地方，比如console和文件。
'''