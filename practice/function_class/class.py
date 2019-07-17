# 一个bean类的getset方法（注解）
from types import MethodType


class Person(object):
    def __init__(self, name, age):
        self._name = name
        self._age = age

    @property
    def name(self):
        return self._name

    @property
    def age(self):
        return self._age

    @name.setter
    def name(self, name):
        self._name = name

    @age.setter
    def age(self, age):
        self._age = age


'''
 访问控制
 1. __开头是私有变量，无法被直接访问
 2. _开头是可以被直接访问的变量，但是不推荐直接访问
 3. __开头且__结尾的是特殊变量，可以被直接访问
 4. 双下划线开头的实例变量是不是一定不能从外部访问呢？其实也不是。不能直接访问__name是因为Python解释器对外把__name变量改成了_Student__name，所以，仍然可以通过_Student__name来访问__name变量：但是强烈建议你不要这么干，因为不同版本的Python解释器可能会把__name改成不同的变量名。总的来说就是，Python本身没有任何机制阻止你干坏事，一切全靠自觉。
'''


class Student(object):
    def __init__(self, name='def', age='0'):
        self.__name = name
        self.__age = age

    def introduce(self):
        print("name %s,age %s" % (self.__name, self.__age))


stu = Student(name='tr', age='18')
#stu = Student()
stu.introduce()

'''
 继承
'''


class Animal(object):
    def run(self):
        print("animal run")


class Dog(Animal):
    def dog(self):
        print("dog run")


dog = Dog()
animal = Animal()

dog.run()
dog.dog()

print(isinstance(dog, Animal))  # true
print(isinstance(dog, Dog))  # true

'''
    多态
'''


class Cat(Animal):
    def run(self):
        print("cat is running")


class Bird(Animal):
    def run(self):
        print("bird is running")


def printAnimalRun(animal):
    animal.run()


cat = Cat()
bird = Bird()
printAnimalRun(cat)
printAnimalRun(bird)


'''
    动态赋予函数：类中没有的对象，在之后生成的实例里，可以动态的赋予方法
    (class/instance).functionX = MethodType(targetFunction,class/isinstance)
'''
# 给实例绑定方法


class Test_Obj(object):
    pass


def func(self):
    print('given function')


def func2(self, name):
    self._name = name


test = Test_Obj()
test.do_func = MethodType(func, test)
test.set_name = MethodType(func2, test)
test.do_func()
test.set_name('tr')
print(test._name)

# 给类绑定方法


class Test_Obj2():
    pass


def func3(self):
    print('given function 3')


Test_Obj2.say_sth = MethodType(func3, Test_Obj2)
test2 = Test_Obj2()
test2.say_sth()


'''
    动态赋予对象或者方法十分强大，所以需要对其限制：__slots__限制，可以指定可被赋予属性的名称
'''


class StudentTest(object):
    __slots__ = ('name', 'age', 'say')  # 允许被绑定的属性 不包括方法
    pass


def sayHello(self):
    print('hello')


class StudentTestSon(StudentTest):  # 父类的slots对子类无效所以需要子类手动声明
    def __init__(self):
        self.__slots = StudentTest.__slots__

    def printFather(self):
        print(StudentTest.__slots__)


StudentTest.sayHello = MethodType(sayHello, StudentTest)
stu1 = StudentTest()
stu1.name = 'tr'  # allowed
# stu1.grade = '199' # not allowed
stu1.sayHello()
stu2 = StudentTestSon()
stu2.printFather() # 访问父类
