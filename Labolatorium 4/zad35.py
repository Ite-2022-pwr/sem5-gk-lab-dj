#!/usr/bin/env python3
import math
import random
import sys

from glfw.GLFW import *

from OpenGL.GL import *
from OpenGL.GLU import *

viewer = [0.0, 0.0, 10.0]

theta = 0.0
phi = 0.0
pix2angle = 0.1

isCamera = False
theta2 = 0.0
phi2 = 0.0

x,z = 0.0,0.0



left_mouse_button_pressed = 0
mouse_x_pos_old = 0
delta_x = 0
mouse_y_pos_old = 0
delta_y = 0


def startup():
    update_viewport(None, 400, 400)
    glClearColor(0.0, 0.0, 0.0, 1.0)
    glEnable(GL_DEPTH_TEST)


def shutdown():
    pass


def axes():
    global x,z
    glBegin(GL_LINES)

    glColor3f(1.0, 0.0, 0.0)
    glVertex3f(-5.0+x, 0.0, 0.0+z)
    glVertex3f(5.0+x, 0.0, 0.0+z)

    glColor3f(0.0, 1.0, 0.0)
    glVertex3f(0.0+x, -5.0, 0.0+z)
    glVertex3f(0.0+x, 5.0, 0.0+z)

    glColor3f(0.0, 0.0, 1.0)
    glVertex3f(0.0+x, 0.0, -5.0+z)
    glVertex3f(0.0+x, 0.0, 5.0+z)

    glEnd()


def example_object():
    random.seed(666)
    glColor3f(random.random(), random.random(), random.random())

    quadric = gluNewQuadric()
    gluQuadricDrawStyle(quadric, GLU_FILL)
    glRotatef(90, 1.0, 0.0, 0.0)
    glRotatef(-90, 0.0, 1.0, 0.0)

    gluSphere(quadric, 1.5, 10, 10)

    glTranslatef(0.0, 0.0, 1.1)
    glColor3f(random.random(), random.random(), random.random())
    gluCylinder(quadric, 1.0, 1.5, 1.5, 10, 5)
    glTranslatef(0.0, 0.0, -1.1)

    glTranslatef(0.0, 0.0, -2.6)
    glColor3f(random.random(), random.random(), random.random())
    gluCylinder(quadric, 0.0, 1.0, 1.5, 10, 5)
    glTranslatef(0.0, 0.0, 2.6)

    glRotatef(90, 1.0, 0.0, 1.0)
    glTranslatef(0.0, 0.0, 1.5)
    glColor3f(random.random(), random.random(), random.random())
    gluCylinder(quadric, 0.1, 0.0, 1.0, 5, 5)
    glTranslatef(0.0, 0.0, -1.5)
    glRotatef(-90, 1.0, 0.0, 1.0)

    glRotatef(-90, 1.0, 0.0, 1.0)
    glTranslatef(0.0, 0.0, 1.5)
    glColor3f(random.random(), random.random(), random.random())
    gluCylinder(quadric, 0.1, 0.0, 1.0, 5, 5)
    glTranslatef(0.0, 0.0, -1.5)
    glRotatef(90, 1.0, 0.0, 1.0)

    glRotatef(90, 0.0, 1.0, 0.0)
    glRotatef(-90, 1.0, 0.0, 0.0)
    gluDeleteQuadric(quadric)


def render(time):
    global theta2
    global phi2
    global x,z

    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    glLoadIdentity()

    if left_mouse_button_pressed:
        theta2 += delta_x / 10.0


    glRotatef(theta2, 0.0, 1.0, 0.0)
    gluLookAt(viewer[0], viewer[1], viewer[2],
              0.0, 0.0, 0.0, 0.0, 1.0, 0.0)

    axes()
    glTranslatef(x, 0.0, z)
    example_object()

    glFlush()


def update_viewport(window, width, height):
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()

    gluPerspective(70, 1.0, 0.1, 300.0)

    if width <= height:
        glViewport(0, int((height - width) / 2), width, width)
    else:
        glViewport(int((width - height) / 2), 0, height, height)

    glMatrixMode(GL_MODELVIEW)
    glLoadIdentity()


def keyboard_key_callback(window, key, scancode, action, mods):
    global isCamera,x,z,theta2
    if key == GLFW_KEY_ESCAPE and action == GLFW_PRESS:
        glfwSetWindowShouldClose(window, GLFW_TRUE)
    if key == GLFW_KEY_SPACE and action == GLFW_PRESS:
        isCamera = not isCamera
    if key == GLFW_KEY_W and action == GLFW_PRESS:
        tps = (theta2 * 3.14159 / 180) % 6.28318
        z=z+math.cos(tps)
        x=x-math.sin(tps)
    if key == GLFW_KEY_S and action == GLFW_PRESS:
        tps = (theta2 * 3.14159 / 180) % 6.28318
        z=z-math.cos(tps)
        x=x+math.sin(tps)
    if key == GLFW_KEY_A and action == GLFW_PRESS:
        tps = (theta2 * 3.14159 / 180) % 6.28318
        x=x+math.cos(tps)
        z=z+math.sin(tps)
    if key == GLFW_KEY_D and action == GLFW_PRESS:
        tps = (theta2 * 3.14159 / 180) % 6.28318
        x=x-math.cos(tps)
        z=z-math.sin(tps)


def mouse_motion_callback(window, x_pos, y_pos):
    global delta_x
    global mouse_x_pos_old

    delta_x = x_pos - mouse_x_pos_old
    mouse_x_pos_old = x_pos


def mouse_button_callback(window, button, action, mods):
    global left_mouse_button_pressed

    if button == GLFW_MOUSE_BUTTON_LEFT and action == GLFW_PRESS:
        left_mouse_button_pressed = 1
    else:
        left_mouse_button_pressed = 0


def main():
    if not glfwInit():
        sys.exit(-1)

    window = glfwCreateWindow(400, 400, __file__, None, None)
    if not window:
        glfwTerminate()
        sys.exit(-1)

    glfwMakeContextCurrent(window)
    glfwSetFramebufferSizeCallback(window, update_viewport)
    glfwSetKeyCallback(window, keyboard_key_callback)
    glfwSetCursorPosCallback(window, mouse_motion_callback)
    glfwSetMouseButtonCallback(window, mouse_button_callback)
    glfwSwapInterval(1)

    startup()
    while not glfwWindowShouldClose(window):
        render(glfwGetTime())
        glfwSwapBuffers(window)
        glfwPollEvents()
    shutdown()

    glfwTerminate()


if __name__ == '__main__':
    main()
