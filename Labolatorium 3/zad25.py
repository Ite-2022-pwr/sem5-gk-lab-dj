#!/usr/bin/env python3
import math
import random
import sys

from glfw.GLFW import *

from OpenGL.GL import *
from OpenGL.GLU import *

N=25

def startup():
    update_viewport(None, 400, 400)
    glClearColor(0.0, 0.0, 0.0, 1.0)
    glEnable(GL_DEPTH_TEST)


def shutdown():
    pass


def axes():
    glBegin(GL_LINES)

    glColor3f(1.0, 0.0, 0.0)
    glVertex3f(-5.0, 0.0, 0.0)
    glVertex3f(5.0, 0.0, 0.0)

    glColor3f(0.0, 1.0, 0.0)
    glVertex3f(0.0, -5.0, 0.0)
    glVertex3f(0.0, 5.0, 0.0)

    glColor3f(0.0, 0.0, 1.0)
    glVertex3f(0.0, 0.0, -5.0)
    glVertex3f(0.0, 0.0, 5.0)

    glEnd()


def render(time, tab):
    random.seed(0)
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    glLoadIdentity()
    spin(time * 100 / 3.1415)

    axes()

    for j in range(0, (2*N)):
        glBegin(GL_TRIANGLE_STRIP)
        for i in range(0, 2*N):
            glColor3f(random.random(), random.random(), random.random())
            glVertex3f(tab[i][j][0], tab[i][j][1], tab[i][j][2])
            glColor3f(random.random(), random.random(), random.random())
            glVertex3f(tab[(i + 1) % (2*N)][j][0], tab[(i + 1) % (2*N)][j][1], tab[(i + 1) % (2*N)][j][2])
            glColor3f(random.random(), random.random(), random.random())
            glVertex3f(tab[i][(j + 1) % (2*N)][0], tab[i][(j + 1) % (2*N)][1], tab[i][(j + 1) % (2*N)][2])
            glColor3f(random.random(), random.random(), random.random())
            glVertex3f(tab[(i + 1) % (2*N)][(j + 1) % (2*N)][0], tab[(i + 1) % (2*N)][(j + 1) % (2*N)][1],
                       tab[(i + 1) % (2*N)][(j + 1) % (2*N)][2])
        glEnd()

    glFlush()

def spin(angle):
    glRotatef(angle, 1.0, 0.0, 0.0)
    glRotatef(angle, 0.0, 1.0, 0.0)
    glRotatef(angle, 0.0, 0.0, 1.0)

def update_viewport(window, width, height):
    if width == 0:
        width = 1
    if height == 0:
        height = 1
    aspect_ratio = width / height

    glMatrixMode(GL_PROJECTION)
    glViewport(0, 0, width, height)
    glLoadIdentity()

    if width <= height:
        glOrtho(-7.5, 7.5, -7.5 / aspect_ratio, 7.5 / aspect_ratio, 7.5, -7.5)
    else:
        glOrtho(-7.5 * aspect_ratio, 7.5 * aspect_ratio, -7.5, 7.5, 7.5, -7.5)

    glMatrixMode(GL_MODELVIEW)
    glLoadIdentity()


def main():
    if not glfwInit():
        sys.exit(-1)

    window = glfwCreateWindow(400, 400, __file__, None, None)
    if not window:
        glfwTerminate()
        sys.exit(-1)

    glfwMakeContextCurrent(window)
    glfwSetFramebufferSizeCallback(window, update_viewport)
    glfwSwapInterval(1)
    R=2
    tab = [[[0] * 3 for i in range(2*N)] for j in range(2*N)]
    for u in range(2*N):
        for v in range(2*N):
            pu = math.pi * (u / N)
            pv = math.pi * (v / N)
            tab[u][v][0] = R* math.sin(3 * pu) / (2 + math.cos(pv))
            tab[u][v][1] = R*(math.sin(pu) + 2 * math.sin(2 * pu)) / (2 + math.cos(pv + math.pi * 2 / 3))
            tab[u][v][2] = R/2 * (math.cos(pu) - 2 * math.cos(2 * pu)) * (2 + math.cos(pv)) * (2 + math.cos(pv + math.pi * 2 / 3)) / 4


    startup()
    while not glfwWindowShouldClose(window):
        render(glfwGetTime(), tab)
        glfwSwapBuffers(window)
        glfwPollEvents()
    shutdown()

    glfwTerminate()


if __name__ == '__main__':
    if len(sys.argv) == 2:
        N=int(sys.argv[1])
    main()

