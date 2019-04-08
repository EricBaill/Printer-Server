# -*- coding: utf-8 -*-

import turtle
import math
wn = turtle.Screen()
#此处可修改，正负号不要动，大小自己选
wn.setworldcoordinates(-4, -4, 4, 4)
alex = turtle.Turtle()
#这里是颜色可以是其他颜色英语单词，别傻得弄个黑心
alex.color("red")
alex.pensize(5)
alex.penup()
alex.speed(9)
walkStart = -1
walkEnd = 1
i = walkStart
j = walkEnd
while i <= 0 and j >= 0:
    y1 = math.sqrt(1 - i * i) + (i * i) ** (1/4.0)
    y2 = -math.sqrt(1 - i * i) + (i * i) ** (1/4.0)
    y3 = math.sqrt(1 - j * j) + (j * j) ** (1/4.0)
    y4 = -math.sqrt(1 - j * j) + (j * j) ** (1/4.0)
    alex.setx(i)
    alex.sety(y1)
    alex.dot()
    alex.sety(y2)
    alex.dot()
    alex.setx(j)
    alex.sety(y3)
    alex.dot()
    alex.sety(y4)
    alex.dot()
#这里貌似是点稀疏度，老规矩，正负号不动
    i += 0.1
    j -= 0.1
wn.exitonclick()

