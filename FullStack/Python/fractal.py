import turtle

def fractal():
    window = turtle.Screen()
    window.bgcolor("white")

    l = 25
    mike = turtle.Turtle()
    mike.speed(0)
    
    
    draw_trianglesss(mike,l)

def draw_trianglesss(turtle, length):
    draw_triangless(turtle, length)

    turtle.left(60)
    turtle.forward(length)
    turtle.right(60)
    draw_triangless(turtle, length)

    turtle.right(120)
    turtle.forward(7*length)
    turtle.left(120)
    turtle.forward(4*length)
    draw_triangless(turtle, length)

def draw_triangless(turtle, length):
    draw_triangles(turtle, length)

    turtle.forward(length)
    turtle.right(60)
    turtle.forward(length)
    turtle.left(60)

    draw_triangles(turtle, length)

    turtle.left(60)
    turtle.forward(length)
    turtle.left(120)
    turtle.forward(length*2)
    turtle.right(180)

    draw_triangles(turtle, length)
    

def draw_triangles(turtle,length):
    #1st tri
    draw_triangle(turtle, length)
    #2nd tri
    turtle.forward(length)
    draw_triangle(turtle,length)
    #3rd tri
    turtle.left(120)
    turtle.forward(length)
    turtle.right(120)
    draw_triangle(turtle,length)
    
    
def draw_triangle(turtle,length):
    x = 0
    turtle.fillcolor("blue")
    turtle.begin_fill()
    while x < 3:
        turtle.forward(length)
        turtle.left(120)
        x += 1
    turtle.end_fill()

fractal()
