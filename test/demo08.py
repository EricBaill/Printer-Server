import turtle
import time

t = turtle.Pen()


def fun1(t, x, y):
    t.forward(x)
    t.left(y)


def fun2(t, x, y):
    t.forward(x)
    t.right(y)


'''
color函数有三个参数
第一个参数指定有多少红色
第二个参数指定有多少绿色
第三个参数指定有多少蓝色
都为0的时候此时为黑色
都为1的时候此时为白色
这种红色，绿色，蓝色的混搭叫做RGB
蓝色和红色混合产生紫色
黄色和红色混合产生橙色
'''

t.color(1, 0, 0)

t.begin_fill()

fun1(t, 100, 90)
fun1(t, 20, 90)
fun2(t, 20, 90)
fun1(t, 20, 90)
fun1(t, 60, 90)
fun2(t, 20, 90)
fun1(t, 20, 90)
t.forward(20)

t.end_fill()

time.sleep(3)

t.color(0, 0, 0)
t.up()
t.forward(10)
t.down()
# 开始位置
t.begin_fill()
# 画圆
t.circle(10)
# 结束位置
t.end_fill()

# 设置当前的指定角度为0度
t.setheading(0)
t.up()
t.forward(90)
t.right(90)
t.forward(10)
t.setheading(0)
t.down()

t.begin_fill()
t.circle(10)
t.end_fill()

time.sleep(2)
