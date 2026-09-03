from re import search

from Student import Student

class StudentCMS(object):
    def __init__(self):
        self.stu_list = []

    def show_view(self):
        print('*'*23)
        print('学生管理系统')
        print('\t1.添加学生信息')
        print('\t2.删除学生信息')
        print('\t3.修改学生信息')
        print('\t4.查询单个学生信息')
        print('\t5.查询所有学生信息')
        print('\t6.保存学生信息')
        print('\t0.退出系统')
        print('*' * 23)


    def add_stu(self):
        name= input('输入学生姓名:')
        age= input('输入学生年龄:')
        gender= input('输入学生性别:')
        phone= input('输入学生手机:')
        desc= input('输入学生描述:')
        stu=Student(name,gender,age,phone,desc)
        self.stu_list.append(stu)

    def delete_stu(self):
        delete_stu = input('请输入要删除学生的姓名:')
        for stu in self.stu_list:
            if stu.name == delete_stu:
                self.stu_list.remove(stu)
                print('删除成功')
                break
        else:
            print('没有此学生')


    def modify_stu(self):
        modify_stu = input('请输入要修改学生的姓名:')
        for stu in self.stu_list:
            if stu.name == modify_stu:
                stu.name= input('输入学生姓名:')
                stu.age= input('输入学生年龄:')
                stu.gender= input('输入学生性别:')
                stu.phone= input('输入学生手机:')
                stu.desc= input('输入学生描述:')
                print('修改成功')
                break
            else:
                print('没有此学生')


    def search_one_stu(self):
        search_stu = input('请输入要查询学生的姓名:')
        for stu in self.stu_list:
            if stu.name == search_stu:
                print(stu)
                break
            else:
                print('没有此学生')

    def search_all_stu(self):
        if len(self.stu_list)==0:
            print('没有学生信息')
        else:
           for stu in self.stu_list:
               print(stu)
           print()

    def save_stu(self):
        pass
    def tuichu_stu(self):
        pass


    def start(self):
        while True:
            self.show_view()

            input_num =input('请输入要操作的编号')

            if input_num =='1':
                print('添加学生信息\n')
                self.add_stu()
            elif input_num =='2':
                print('删除学生信息\n')
                self.delete_stu()
            elif input_num =='3':
                print('修改学生信息\n')
                self.modify_stu()
            elif input_num =='4':
                print('查询单个学生信息\n')
                self.search_one_stu()
            elif input_num =='5':
                print('查询所有学生信息\n')
                self.search_all_stu()
            elif input_num =='6':
                print('保存学生信息\n')
                self.save_stu()
            elif input_num =='0':
                result = input('确定要退出吗Y/N')
                if result == 'Y':
                    self.save_all_stu()
                    print('保存成功\n')
                    break
                else:
                    print('取消保存\n')
                print('退出系统\n')
                break

            else:
                print('输入错误，请重新输入\n')










