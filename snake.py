from turtle import *
from random import randrange
from freegames import square, vector

# Initialize food and snake
food = vector(0, 0)
snake = [vector(10, 0)]
aim = vector(0, -10)

# Function to change the snake's direction
def change(x, y):
    aim.x = x
    aim.y = y

# Function to check if the head is inside the boundaries
def inside(head):
    return -280 < head.x < 260 and -280 < head.y < 260

# Function to move the snake
def move():
    head = snake[-1].copy()
    head.move(aim)

    if not inside(head) or head in snake:
        square(head.x, head.y, 9, 'red')
        update()
        return

    snake.append(head)

    if head == food:
        print('Snake:', len(snake))
        food.x = randrange(-15, 15) * 10
        food.y = randrange(-15, 15) * 10
    else:
        snake.pop(0)

    clear()

    for body in snake:
        square(body.x, body.y, 9, 'green')

    square(food.x, food.y, 9, 'red')
    update()
    ontimer(move, 150)

# Set up the screen
hideturtle()
tracer(False)
listen()

# Key bindings for controlling the snake
onkey(lambda: change(10, 0), 'Right')
onkey(lambda: change(-10, 0), 'Left')
onkey(lambda: change(0, 10), 'Up')
onkey(lambda: change(0, -10), 'Down')

move()
done()
