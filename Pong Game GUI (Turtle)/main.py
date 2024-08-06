#left controls : w and s ; right controls : up and down
from turtle import Screen,Turtle
from time import sleep
screen = Screen()
screen.bgcolor("black")
screen.setup(width=800,height=600)
screen.title("Pong game")

class Paddle(Turtle):
    def __init__(self,position):
        super().__init__()
        screen.tracer(0)
        self.shape("square")
        self.color("white")
        self.shapesize(stretch_wid=5,stretch_len=1)
        self.penup()
        self.goto(position)
        screen.tracer(1)

    def go_up(self):
        new_y = self.ycor() + 20
        self.goto(self.xcor(),new_y)
    def go_down(self):
        new_y = self.ycor() - 20
        self.goto(self.xcor(),new_y)
        
class Ball(Turtle):
    def __init__(self):
        super().__init__()
        self.shape("circle")
        self.color("white")
        self.penup()
        self.speed(1)
        self.xmove = 10
        self.ymove = 10
    def move(self):
        new_x_cor = self.xcor() + self.xmove
        new_y_cor = self.ycor() + self.ymove
        self.goto(new_x_cor,new_y_cor)
    def bounce_y(self):
        self.ymove*=-1
    def bounce_x(self):
        self.xmove*=-1
    def reset_position(self):
        screen.tracer(0)
        self.goto(0,0)
        screen.tracer(1)
        sleep(1)
        self.bounce_x()
class Scoreboard(Turtle):
    def __init__(self):
        super().__init__()
        self.color("white")
        self.penup()
        self.hideturtle()
        self.l_score = 0
        self.r_score = 0
        self.update_scoreboard()
    def update_scoreboard(self):
        self.clear()
        self.goto(-100,180)
        self.write(self.l_score,align="center" ,font =("Courier",88,"normal"))
        self.goto(100,180)
        self.write(self.r_score,align="center" ,font =("Courier",88,"normal"))
class Middle_line(Turtle):
    def __init__(self):
        super().__init__()
        screen.tracer(0)
        self.shape("square")
        self.hideturtle()
        self.color("white")
        self.pensize(3)
        self.penup()
        self.goto(0,-270)
        self.x=0
        self.left(90)
        while(self.x <= 25):
            self.pendown()
            self.forward(10)
            self.penup()
            self.forward(20)
            self.x+=1
        screen.tracer(1)
        
line = Middle_line()
rpaddle = Paddle((350,0))
lpaddle = Paddle((-350,0))

ball1 = Ball()
score = Scoreboard()
screen.listen()
screen.onkey(rpaddle.go_up,"Up")
screen.onkey(rpaddle.go_down,"Down")
screen.onkey(lpaddle.go_up,"w")
screen.onkey(lpaddle.go_down,"s")

game = True
while game:
    ball1.move()
    if ball1.ycor()>280 or ball1.ycor()<-280:
        ball1.bounce_y()
    if (ball1.distance(rpaddle) < 50 and ball1.xcor() > 320)or (ball1.distance(lpaddle) < 50 and ball1.xcor() < -320) :
        ball1.bounce_x()
    if ball1.xcor()>340:
        ball1.reset_position()
        score.l_score+=1
        score.update_scoreboard()
    if ball1.xcor()<-340:
        ball1.reset_position()
        score.r_score+=1
        score.update_scoreboard()
screen.exitonclick()