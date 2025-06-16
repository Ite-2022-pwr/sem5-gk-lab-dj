#!/usr/bin/env python3
import math
import sys
import random

from glfw.GLFW import *

from OpenGL.GL import *
from OpenGL.GLU import *

N=20

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
    spin(time/10 * 180 / 3.1415)

    axes()
    for i in range(0, N):
        for j in range(0, N):
            glColor3f(random.random(), random.random(), random.random())
            glBegin(GL_TRIANGLES)
            glVertex3f(tab[i][j][0], tab[i][j][1], tab[i][j][2])
            glVertex3f(tab[(i+1)%N][j][0], tab[(i+1)%N][j][1], tab[(i+1)%N][j][2])
            glVertex3f(tab[i][(j+1)%(N+1)][0], tab[i][(j+1)%(N+1)][1], tab[i][(j+1)%(N+1)][2])
            glEnd()
            glColor3f(random.random(), random.random(), random.random())
            glBegin(GL_TRIANGLES)
            glVertex3f(tab[(i+1)%N][(j+1)%(N+1)][0], tab[(i+1)%N][(j+1)%(N+1)][1], tab[(i+1)%N][(j+1)%(N+1)][2])
            glVertex3f(tab[(i+1)%N][j][0], tab[(i+1)%N][j][1], tab[(i+1)%N][j][2])
            glVertex3f(tab[i][(j+1)%(N+1)][0], tab[i][(j+1)%(N+1)][1], tab[i][(j+1)%(N+1)][2])
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

    tab = [[[0] * 3 for i in range(N+1)] for j in range(N+1)]
    for u in range(N+1):
        for v in range(N+1):
            pu = u/N
            pv = v/N
            a = (-90*pu**5+225*pu**4-270*pu**3+180*pu**2-45*pu)
            tab[u][v][0] = a*math.cos(math.pi*pv)
            tab[u][v][1] = 160*pu**4-320*pu**3+160*pu**2-5
            tab[u][v][2] = a*math.sin(math.pi*pv)


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

