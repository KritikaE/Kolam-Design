import turtle
import time

# ---------------- SCREEN ----------------
screen = turtle.Screen()
screen.bgcolor("black")
screen.title("Kolam – Vertical Skeleton")

# ---------------- DOT TURTLE ----------------
dot_t = turtle.Turtle()
dot_t.hideturtle()
dot_t.penup()
dot_t.color("white")

# ---------------- LINE TURTLE ----------------
line_t = turtle.Turtle()
line_t.hideturtle()
line_t.penup()
line_t.color("white")
line_t.pensize(3)
line_t.speed(0)

# ---------------- PARAMETERS ----------------
rows = 6
dots_per_row = 3
dot_spacing = 100
row_spacing = 40
dot_size = 6

# ---------------- DRAW DOTS ----------------
dot_positions = []

start_y = (rows - 1) * row_spacing / 2

for r in range(rows):
    y = start_y - r * row_spacing

    # alternate horizontal offset
    if r % 2 != 0:
        start_x = -dot_spacing
    else:
        start_x = -dot_spacing / 2

    row = []
    for i in range(dots_per_row):
        x = start_x + i * dot_spacing
        dot_t.goto(x, y)
        dot_t.dot(dot_size)
        row.append((x, y))
        time.sleep(0.05)

    dot_positions.append(row)

# ---------------- DRAW VERTICAL LINES ----------------
# lines are BETWEEN dot columns
vertical_lines_x = []

for i in range(5):
    x = -dot_spacing + i * (dot_spacing / 2)
    vertical_lines_x.append(x)

top_y = start_y + row_spacing/2
bottom_y = start_y - (rows - 1) * row_spacing - row_spacing/2

SHIFT_LEFT = 30  # try 20, 30, 40

for x in vertical_lines_x:
    new_x = x + SHIFT_LEFT
    line_t.goto(new_x, top_y)
    line_t.pendown()
    line_t.goto(new_x, bottom_y)
    line_t.penup()

# ---------------- DRAW HORIZONTAL LINES ----------------
horizontal_lines_y = []

for i in range(5):
    y = start_y - i * (row_spacing / 1.05)
    horizontal_lines_y.append(y)

left_x = -dot_spacing * 1.25
right_x = dot_spacing * 1.75

SHIFT_DOWN = 20   # try 20, 30, 40

for y in horizontal_lines_y:
    new_y = y - SHIFT_DOWN
    line_t.goto(left_x, new_y)
    line_t.pendown()
    line_t.goto(right_x, new_y)
    line_t.penup()
    
# ---------------- DRAW CURVES ----------------    
curve_t = turtle.Turtle()
curve_t.hideturtle()
curve_t.color("white")
curve_t.pensize(3)
curve_t.speed(0)
curve_t.penup()

import math

def draw_curve(cx, cy, radius, start_angle, extent):
    """
    cx, cy      : center of the curve
    radius      : curve radius
    start_angle : turtle heading at start
    extent      : how much arc to draw (90, 180)
    """
    curve_t.penup()
    curve_t.goto(cx, cy)
    curve_t.setheading(start_angle)
    curve_t.forward(radius)
    curve_t.setheading(start_angle + 90)
    curve_t.pendown()

    steps = 60
    step_len = (math.pi * radius * extent / 180) / steps
    step_ang = extent / steps

    for _ in range(steps):
        curve_t.forward(step_len)
        curve_t.left(step_ang)

    curve_t.penup()
    
# ---------------- DRAW CIRCLES AROUND DOTS ----------------

circle_t = turtle.Turtle()
circle_t.hideturtle()
circle_t.color("white")
circle_t.pensize(3)
circle_t.speed(0)
circle_t.penup()

radius = 15  # keep smaller than dot spacing / 2

for row in dot_positions:
    for (x, y) in row:
        circle_t.goto(x, y - radius)
        circle_t.pendown()
        circle_t.circle(radius)
        circle_t.penup()

# ---------------- ROTATE ----------------
# ---------------- ROTATE ----------------

# clear everything already drawn
dot_t.clear()
line_t.clear()
curve_t.clear()
circle_t.clear()

# helper rotation function
def rot(x, y):
    return (x * math.cos(math.radians(50)) - y * math.sin(math.radians(50)),
    x * math.sin(math.radians(50)) + y * math.cos(math.radians(50)))

# -------- REDRAW DOTS --------
for row in dot_positions:
    for (x, y) in row:
        rx, ry = rot(x, y)
        dot_t.goto(rx, ry)
        dot_t.dot(dot_size)

# -------- REDRAW VERTICAL LINES (now horizontal after rotation) --------
for x in vertical_lines_x:
    new_x = x + SHIFT_LEFT
    rx1, ry1 = rot(new_x, top_y)
    rx2, ry2 = rot(new_x, bottom_y)

    line_t.goto(rx1, ry1)
    line_t.pendown()
    line_t.goto(rx2, ry2)
    line_t.penup()

# -------- REDRAW HORIZONTAL LINES (now vertical after rotation) --------
for y in horizontal_lines_y:
    new_y = y - SHIFT_DOWN
    rx1, ry1 = rot(left_x, new_y)
    rx2, ry2 = rot(right_x, new_y)

    line_t.goto(rx1, ry1)
    line_t.pendown()
    line_t.goto(rx2, ry2)
    line_t.penup()

# -------- REDRAW CIRCLES --------
for row in dot_positions:
    for (x, y) in row:
        rx, ry = rot(x, y)
        circle_t.goto(rx, ry - radius)
        circle_t.pendown()
        circle_t.circle(radius)
        circle_t.penup()

# ---------------- DONE ----------------
screen.mainloop()