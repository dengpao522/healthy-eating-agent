#oop三大特征 封装 继承 多态
# 抽象：类  具体：对象


# #1.定义汽车类
# class Car:
#
#    def run(self):
#        print(f"{self}跑...")
#
#    def work(self):
#        print(f"我是work函数，self值为:{self}")
#
#
#    def __init__(self,color,number):
#        self.color=color
#        self.number=number
#
#    def __str__(self):
#        return f'颜色:{self.color},轮胎数:{self.number}'
#
#    def __del__(self):
#        print(f'{self}被销毁了')
#
#
#
#
# #2. 创建汽车类对象
# c1=Car('绿色',4)
# print(c1)
# c1.run()   #调用Car类的run()函数  简写：调用Car#run()
# c1.work()
#
# print("-"*60)
#
# c2=Car('红色',6)
# print(c2)
# c2.run()   #调用Car类的run()函数  简写：调用Car#run()
# c2.work()




# class Student:
#
#     def __init__(self,name):
#         self.name = name
#         self.weight=70
#
#
#     def run(self):
#         print('跑步')
#         self.weight-=0.5
#
#     def eat(self):
#         print('大吃一顿')
#         self.weight+=1
#
#     def __str__(self):
#         return f'姓名:{self.name},当前体重:{self.weight}'
#
# a=Student('jianhui')
#
# a.run()
# a.run()
# a.run()
#
# a.eat()
#
# print(a)


# class SweetPotato():
#
#     def __init__(self):
#         self.cook_time = 0
#         self.state ='生的'
#         self.condiments=[]
#
#     def cook(self,time):
#         if time<0:
#             print('无效值')
#
#         else:
#             self.cook_time+=time
#
#             if 0<=self.cook_time<3 :
#                 self.state='生的'
#             elif 3<=self.cook_time<7:
#                 self.state='半生不熟'
#             elif 7<=self.cook_time<12:
#                 self.state='熟了'
#             else:
#                 self.state='糊了'
#
#     def add_condiment(self,condiment):
#         self.condiments.append(condiment)
#
#     def __str__(self):
#         return f'烘烤时间:{self.cook_time},状态:{self.state},调料:{self.condiments}'
#
# if __name__=='__main__':    # 只有直接运行这个文件时，才会执行这里的代码
#
#     dg=SweetPotato()
#
#     dg.cook(5)
#     dg.add_condiment('辣椒')
#
#     print(dg)



# #闭包
# def fn_outer():
#     a=100
#     def fn_inter():
#         nonlocal a
#         a=a+1
#         print(f'a={a}')
#
#     return fn_inter
#
# if __name__ =='__main__':
#     fn_inter=fn_outer()
#     fn_inter()
#     fn_inter()
#     fn_inter()


# #装饰器
# def my_decorator(fn_name):
#     def fn_inner():
#         print('正在努力计算中')
#         return fn_name()  # 调用原函数
#     return fn_inner  # 返回内部函数
#
# @my_decorator
# def get_sum():
#     a=10
#     b=1
#     return a+b
#
# print(f'求和{get_sum()}')


# def my_decorator(fn_name):
#     def fn_inner():
#         print('.........')
#         return fn_name()
#     return fn_inner
#
# @my_decorator
# def get_sum(*args,**kwargs):
#     sum=0
#     for i in args:
#         sum+=i
#     for v in kwargs.values():
#         sum+=v
#
# sum = get_sum(1,2,3,a=4,b=5)
# print(sum)


# def logging(flag):
#     def my_decorator(fn_name):
#         def fn_inner(a,b):
#             if flag =='+':
#                 print('正在计算加法中...')
#             elif flag =='-':
#                 print('正在计算减法中...')
#             return fn_name(a,b)
#         return fn_inner
#     return my_decorator
#
# @logging('+')
# def get_sum(a,b):
#     return a+b
# @logging('-')
# def get_sub(a,b):
#     return a-b
#
# print(get_sum(10,20))
# print(get_sub(20,5))

#优化
# def my_decorator(fn_name):
#     def fn_inner(a,b):
#         if fn_name.__name__ == 'get_sum':
#             print('正在计算加法')
#         elif fn_name.__name__ == 'get_sub':
#             print('正在计算减法')
#         return fn_name(a,b)
#     return fn_inner
# @my_decorator
# def get_sum(a,b):
#     return a+b
# @my_decorator
# def get_sub(a,b):
#     return a-b
# print(get_sum(10,20))
# print(get_sub(20,5))


# import multiprocessing
# import time
#
# def coding():
#     for i in range(1,11):
#         time.sleep(0.1)
#         print(f'正在写第{i}行代码...')
#
# def music():
#     for i in range(1,11):
#         time.sleep(0.1)
#         print(f'正在听第{i}首音乐')
#
# if __name__ == '__main__':
#     p1=multiprocessing.Process(target=coding)
#     p2=multiprocessing.Process(target=music)
#
#     p1.start()
#     p2.start()



import multiprocessing,time
import os


# def coding(name,num):
#     for i in range(1,num+1):
#         time.sleep(0.1)
#         print(f'{name}正在写第{i}行代码...')
#     print(f'p1进程的id:{os.getpid()},{multiprocessing.current_process().pid},父进程id(ppid为):{os.getppid()}')
# def music(name,count):
#     for i in range(1,count+1):
#         time.sleep(0.1)
#         print(f'{name}正在听第{i}首音乐')
#     print(f'p2进程的id:{os.getpid()},{multiprocessing.current_process().pid},父进程id(ppid为):{os.getppid()}')
#
# if __name__ == '__main__':
#     p1 = multiprocessing.Process(target=coding,args=('jianhui',10))
#     p2 = multiprocessing.Process(target=music,kwargs={'count':20,'name':'jianhui'})
# #args方式：接受所有的位置参数
# #lwargs方式：接受所有的关键字参数
#     p1.start()
#     p2.start()
#     print(f'main进程的id:{os.getpid()},{multiprocessing.current_process().pid},父进程id(ppid为):{os.getppid()}')

#进程之间不共享全局变量
#主进程会等待所有子进程执行结束再结束

# 线程与进程的关系:
# 进程是CPU分配资源的基本单位，线程是CPU调度资源的最小单位
# 线程是依赖于进程的的，每一个进程至少有一个线程（主线程栈）
# 进程间数据相互隔离，（同一个进程的）线程间数据可以共享




