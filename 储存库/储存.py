#Python是面向对象的解释型高级编程语言。
#Python是强类型的动态脚本语言。
# ctrl+/ :添加注释
# ctrl+d :复制到下一行
# ctrl+f :查找
#标识符：必须是数字·下划线·字母组成，数字不能开头，字母严格区分大小写。
# 布尔型：布尔值可以当作整形对待，True相当于1，False相当于0.
# 占位符：%s (字符串) , %d (整数) , %f (小数）（输出小数点后六位）
# %4d : 设置位数，补足前面空白
a=123
print("%4d" %a)
print("%3d" %a)
print("%6d" %a)
print("%06d" %a)
b=1.23
print("%f" %b) #(默认到小数点后六位）
b=1.2345678
print("%f" %b) #(到小数点后六位四舍五入)
print("%.3f" %b) #(输出到小数点后几位,要在百分号后面加".")
print("%.2f" %b)
name="冯欣羽"
age=19
love="赵建辉"
print(f"我的名字叫{name},我今年{age}了,我长得很漂亮，我爱{love},他也爱我。")
print("我的名字叫%s,我今年%d了" %(name,age))
print("zhao","jian","hui",sep=",")  # sep=" " :将字符之间隔开
print("zhao","jian","hui",sep="|")
print("zhao",end=",")               # end=" " :连接下一行
print("feng")

print(True+1)                       # Ture相当于1，False相当于0.
print(False+1)







#转义字符
print("zhao\tjianhui")  # \t : 制表符，表示空四个字符，也称缩进。
print("姓名\t年龄\t电话")