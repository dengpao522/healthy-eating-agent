class Student:
    def __init__(self,name,gender,age,phone,desc):
        self.name=name
        self.gender=gender
        self.age=age
        self.phone=phone
        self.desc=desc

    def __str__(self):
        return f'姓名:{self.name},性别:{self.gender},年龄:{self.age},手机:{self.phone},描述:{self.desc}'

if __name__=='__main__':
    s1=Student('jianhui','男',21,17349021487,'工程师')

    print(s1)


