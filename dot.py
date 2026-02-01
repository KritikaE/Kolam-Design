import turtle
import math
import time

# ---------------- SCREEN ----------------
screen = turtle.Screen()
screen.bgcolor("black")
screen.title("Kolam")

# ---------------- TURTLES ----------------
dot_t = turtle.Turtle()
dot_t.hideturtle()
dot_t.penup()
dot_t.color("white")

t = turtle.Turtle()
t.hideturtle()
t.speed(0)
t.color("white")
t.pensize(3)
t.penup()

# ---------------- PARAMETERS ----------------
dot_spacing = 50
diag_spacing = dot_spacing
half = dot_spacing / 2
num_lines = 5
line_length = 260
curve_radius = 15

# ---------------- DRAW DOTS ----------------
dot_rows = [1, 3, 5, 5, 3, 1]
rows = len(dot_rows)
start_y = (rows // 2) * dot_spacing

for r, count in enumerate(dot_rows):
    y = start_y - r * dot_spacing
    start_x = -(count - 1) * dot_spacing / 2
    for i in range(count):
        dot_t.goto(start_x + i * dot_spacing, y)
        dot_t.dot(6)

# ---------------- HELPERS ----------------
def draw_diagonal(x, y, angle):
    t.penup()
    t.goto(x, y)
    t.setheading(angle)
    t.pendown()
    t.forward(line_length)

def left_semicircle(cx, cy, radius, heading):
    t.penup()
    t.goto(cx, cy)
    t.setheading(heading)
    t.forward(radius)
    t.setheading(heading + 90)
    t.pendown()

    for _ in range(90):
        t.forward((math.pi * radius) / 90)
        t.left(2)

# ---------------- DIAGONALS (45°) ----------------
base_y = -120
start_x = -2 * diag_spacing

diag_45 = []
for i in range(num_lines):
    x = start_x + i * diag_spacing
    draw_diagonal(x, base_y, 45)
    diag_45.append(x)

# ---------------- DIAGONALS (135°) ----------------
start_x = 2 * diag_spacing

diag_135 = []
for i in range(num_lines):
    x = start_x - i * diag_spacing
    draw_diagonal(x, base_y, 135)
    diag_135.append(x)

# ---------------- SEMICIRCLES BETWEEN LINES ----------------
center_y = base_y + line_length / 2

# joins: (1–2), (3–4)
for i in [0, 2]:
    cx = diag_45[i] + half
    left_semicircle(cx, center_y, curve_radius, 45)

# joins: (2–3), (4–5)
for i in [1, 3]:
    cx = diag_45[i] + half
    left_semicircle(cx, center_y, curve_radius, 45)

# ---------------- END LOOPS ----------------
left_semicircle(0, center_y + 100, curve_radius + 6, 0)
left_semicircle(0, center_y - 100, curve_radius + 6, 180)

# ---------------- DONE ----------------
screen.mainloop()