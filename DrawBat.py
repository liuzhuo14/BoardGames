import turtle as t
import math
'''
部分函数及参数说明:
pen_move():画每个部位时，都必须先抬起画笔，移动到指定位置后落下
pen_set():用来设置画笔的颜色尺寸等
t.setup(width,height):入宽和高为整数时,表示像素;为小数时,表示占据电脑屏幕的比例
t.speed()：设置画笔速度
t.goto():以左下角为坐标原点，进行画笔的移动
t.circle(radius，extent):设置指定半径radius的圆，参数为半径，半径为正(负)，表示圆心在画笔的左边(右边)画圆，extent为角度，若画圆则无须添加。如：t.circle(-20,90),顺时针，半径20画弧，弧度90
t.seth(degree)绝对角度，将画笔的方向设置为一定的度数方向，0-东；90-北；180-西；270-南
'''

wight=800
height=600
#t.hideturtle()
t.setup(wight,height)
t.speed(10)

def pen_move(x,y):
    t.penup()
    t.goto(x-wight/2+50,y-height/2+50)
    t.pendown()

def pen_set(size,r1,g1,b1):
    t.pensize(size)
    t.color(r1,g1,b1)

def draw_face():
    #第一个眼睛
    pen_move(300,350)
    pen_set(2,0,0,0)
    t.begin_fill()
    t.circle(15)
    t.end_fill()
    #第二个眼睛
    pen_move(400,350)
    t.begin_fill()
    t.circle(15)
    t.end_fill()
    #第一个眼眶
    pen_move(300,350)
    t.circle(25)
    #第二个眼眶
    pen_move(400,350)
    t.circle(25)
    #右边脸框
    pen_move(370,280)
    t.circle(60,120)
    #左边脸框
    t.seth(180)
    pen_move(330,280)
    t.circle(-60,120)
    #头上一撮
    t.seth(0)
    pen_move(300,400)
    t.forward(100)
    #左鼻孔
    pen_move(335,330)
    t.begin_fill()
    t.circle(3)
    t.end_fill()
    #右鼻孔
    pen_move(375, 330)
    t.begin_fill()
    t.circle(5)
    t.end_fill()
    #嘴巴
    pen_move(310,315)
    t.left(300)
    t.circle(50,140)
    #舌头
    t.seth(270)
    pen_move(350,290)
    t.forward(30)
    pen_move(328,280)
    t.circle(53,60)
    t.left(300)
    pen_move(372,280)
    t.circle(-53,60)
    # 左耳朵
    pen_move(273,345)
    t.left(300)
    t.circle(-80,50)
    pen_move(271,330)
    t.left(40)
    t.circle(-125,50)
    pen_move(277,360)
    t.left(30)
    t.circle(115,30)
    pen_move(280,385)
    t.left(325)
    t.circle(70,60)
    #右耳朵
    pen_move(427,345)
    t.right(140)
    t.circle(80,50)
    pen_move(429,330)
    t.right(40)
    t.circle(120,48)
    pen_move(422,360)
    t.right(30)
    t.circle(-115,30)
    pen_move(420,385)
    t.right(325)
    t.circle(-60,60)
    #头画完了，但看着像青蛙，凑活着用吧

def draw_body():
    #画身子
    pen_move(290,298)
    t.left(250)
    t.circle(250,55)
    pen_move(410, 298)
    t.left(330)
    t.circle(-250, 55)
    #肚脐
    pen_move(340,150)
    t.seth(0)
    t.left(45)
    t.forward(30)
    pen_move(360, 150)
    t.seth(180)
    t.left(45+270)
    t.forward(30)

def draw_feet():
    #画左脚
    pen_move(325,110)
    t.left(80)
    t.circle(50,90)
    pen_move(335,98)
    t.left(270)
    t.circle(20,90)
    pen_move(330,72)
    t.circle(-20,135)
    pen_move(315,40)
    t.right(60)
    t.circle(-25,60)
    #画右脚
    pen_move(377,110)
    t.right(76)
    t.circle(-50,90)
    pen_move(370, 98)
    t.left(85)
    t.circle(-20, 90)
    pen_move(380, 75)
    t.circle(20, 135)
    pen_move(400, 48)
    t.right(270)
    t.circle(25, 60)

def draw_wings():
    #左翅
    pen_move(288,280)
    t.circle(-230,35)
    pen_move(175,355)
    t.circle(58,110)
    pen_move(81,350)
    t.circle(280,30)
    pen_move(43,212)
    t.left(140)
    t.circle(-80,80)
    pen_move(145,230)
    t.left(75)
    t.circle(-75,75)
    pen_move(232,240)
    t.left(60)
    t.circle(-40,90)
    #右翅
    pen_move(350-288+350,280)
    t.left(78)
    t.circle(230,35)
    pen_move(700-175, 355)
    t.circle(-58, 110)
    pen_move(700-81, 350)
    t.circle(-280, 30)
    pen_move(700-43+2, 212)
    t.left(218)
    t.circle(80, 80)
    pen_move(700-145+2, 230)
    t.left(290)
    t.circle(75, 75)
    pen_move(700-232, 240-4)
    t.left(270)
    t.circle(40, 90)





draw_face()
draw_body()
draw_feet()
draw_wings()