import turtle

def draw_square():
    window = turtle.Screen()
    window.bgcolor("red")

    brad = turtle.Turtle()
    brad.shape("turtle")
    brad.color('blue')

    angie = turtle.Turtle()

    charlie = turtle.Turtle()
    charlie.color("green")

    #square
    x = 0
    while x < 4:
        brad.forward(100)
        brad.right(90)
        x += 1
    

    #circle
    angie.circle(100)

    #triangle
    x = 0
    while x < 3:
        charlie.forward(100)
        charlie.right(120)
        x += 1
    
    window.exitonclick()

draw_square()
