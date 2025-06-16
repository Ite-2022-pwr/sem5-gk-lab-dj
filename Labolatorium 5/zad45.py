#!/usr/bin/env python3
import math
import sys
import random

from glfw.GLFW import *

from OpenGL.GL import *
from OpenGL.GLU import *

display=True

N = 40
current = 0
r,g,b = 0.0, 0.0, 0.0

x,y,z = 0.0, 0.0, 10.0

viewer = [0.0, 0.0, 10.0]

theta = 0.0
phi = 0.0
pix2angle = 1.0

left_mouse_button_pressed = 0
mouse_x_pos_old = 0
mouse_y_pos_old = 0
delta_x = 0
delta_y = 0

mat_ambient = [1.0, 1.0, 1.0, 1.0]
mat_diffuse = [1.0, 1.0, 1.0, 1.0]
mat_specular = [1.0, 1.0, 1.0, 1.0]
mat_shininess = 20.0

light_ambient = [0.1, 0.1, 0.0, 1.0]
light_diffuse = [0.8, 0.8, 0.0, 1.0]
light_specular = [1.0, 1.0, 1.0, 1.0]
light_position = [0.0, 0.0, 10.0, 1.0]

light1_ambient = [0.0, 0.1, 0.1, 1.0]
light1_diffuse = [0.0, 0.8, 0.8, 1.0]
light1_specular = [1.0, 1.0, 1.0, 1.0]
light1_position = [0.0, 10.0, 0.0, 1.0]

att_constant = 1.0
att_linear = 0.05
att_quadratic = 0.001


def startup():
    update_viewport(None, 400, 400)
    glClearColor(0.0, 0.0, 0.0, 1.0)
    glEnable(GL_DEPTH_TEST)

    glMaterialfv(GL_FRONT, GL_AMBIENT, mat_ambient)
    glMaterialfv(GL_FRONT, GL_DIFFUSE, mat_diffuse)
    glMaterialfv(GL_FRONT, GL_SPECULAR, mat_specular)
    glMaterialf(GL_FRONT, GL_SHININESS, mat_shininess)

    glLightfv(GL_LIGHT0, GL_AMBIENT, light_ambient)
    glLightfv(GL_LIGHT0, GL_DIFFUSE, light_diffuse)
    glLightfv(GL_LIGHT0, GL_SPECULAR, light_specular)
    glLightfv(GL_LIGHT0, GL_POSITION, light_position)

    glLightf(GL_LIGHT0, GL_CONSTANT_ATTENUATION, att_constant)
    glLightf(GL_LIGHT0, GL_LINEAR_ATTENUATION, att_linear)
    glLightf(GL_LIGHT0, GL_QUADRATIC_ATTENUATION, att_quadratic)

    # glLightfv(GL_LIGHT1, GL_AMBIENT, light1_ambient)
    # glLightfv(GL_LIGHT1, GL_DIFFUSE, light1_diffuse)
    # glLightfv(GL_LIGHT1, GL_POSITION, light1_position)
    #
    # glLightf(GL_LIGHT1, GL_CONSTANT_ATTENUATION, att_constant)
    # glLightf(GL_LIGHT1, GL_LINEAR_ATTENUATION, att_linear)
    # glLightf(GL_LIGHT1, GL_QUADRATIC_ATTENUATION, att_quadratic)

    glShadeModel(GL_SMOOTH)
    glEnable(GL_LIGHTING)
    glEnable(GL_LIGHT0)
    # glEnable(GL_LIGHT1)


def shutdown():
    pass


def render(time, tab):
    global theta,r,g,b
    global phi
    random.seed(0)

    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    glLoadIdentity()

    gluLookAt(viewer[0], viewer[1], viewer[2],
              0.0, 0.0, 0.0, 0.0, 1.0, 0.0)

    if left_mouse_button_pressed:
        theta += delta_x * pix2angle
        phi += delta_y * pix2angle

    glRotatef(theta, 0.0, 1.0, 0.0)
    glRotatef(phi, 1.0, 0.0, 0.0)

    quadric = gluNewQuadric()
    # gluQuadricDrawStyle(quadric, GLU_FILL)
    # gluSphere(quadric, 3.0, 10, 10)

    for j in range(0, N):
        glBegin(GL_TRIANGLE_STRIP)
        for i in range(0, N):
            glNormal3f(tab[i][j][3], tab[i][j][4], tab[i][j][5])
            glVertex3f(tab[i][j][0], tab[i][j][1], tab[i][j][2])
            glNormal3f(tab[(i+1)%N][j][3], tab[(i+1)%N][j][4], tab[(i+1)%N][j][5])
            glVertex3f(tab[(i+1)%N][j][0], tab[(i+1)%N][j][1], tab[(i+1)%N][j][2])
            glNormal3f(tab[i][(j+1)%(N+1)][3], tab[i][(j+1)%(N+1)][4], tab[i][(j+1)%(N+1)][5])
            glVertex3f(tab[i][(j+1)%(N+1)][0], tab[i][(j+1)%(N+1)][1], tab[i][(j+1)%(N+1)][2])
            glNormal3f(tab[(i+1)%N][(j+1)%(N+1)][3], tab[(i+1)%N][(j+1)%(N+1)][4], tab[(i+1)%N][(j+1)%(N+1)][5])
            glVertex3f(tab[(i+1)%N][(j+1)%(N+1)][0], tab[(i+1)%N][(j+1)%(N+1)][1], tab[(i+1)%N][(j+1)%(N+1)][2])
        glEnd()
    if display:
        for j in range(0, N):
            glBegin(GL_LINES)
            for i in range(0, N):
                glVertex3f(tab[i][j][0], tab[i][j][1], tab[i][j][2])
                glVertex3f(tab[i][j][0]+tab[i][j][3], tab[i][j][1]+tab[i][j][4], tab[i][j][2]+tab[i][j][5])
            glEnd()

    gluQuadricDrawStyle(quadric, GLU_LINE)
    glTranslatef(x, y, z)
    glLightfv(GL_LIGHT0, GL_DIFFUSE, [r, g, b, 1.0])
    glLightfv(GL_LIGHT0, GL_POSITION, [x, y, z, 1.0])
    gluSphere(quadric, 0.5, 6, 5)
    gluDeleteQuadric(quadric)
    glTranslatef(.0,.0,.0)

    glFlush()


def update_viewport(window, width, height):
    global pix2angle
    pix2angle = 360.0 / width

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
    global current, r,g,b,x,y,z, display
    if key == GLFW_KEY_SPACE and action == GLFW_PRESS:
        display = not display
    if key == GLFW_KEY_ESCAPE and action == GLFW_PRESS:
        glfwSetWindowShouldClose(window, GLFW_TRUE)
    if key == GLFW_KEY_R and action == GLFW_PRESS:
        current = 0
    if key == GLFW_KEY_G and action == GLFW_PRESS:
        current = 1
    if key == GLFW_KEY_B and action == GLFW_PRESS:
        current = 2
    if key == GLFW_KEY_C and action == GLFW_PRESS:
        current = 3
    if key == GLFW_KEY_UP and action == GLFW_PRESS:
        if current == 0:
            r += 0.1
            if r > 1.0:
                r = 1.0
        if current == 1:
            g += 0.1
            if g > 1.0:
                g = 1.0
        if current == 2:
            b += 0.1
            if b > 1.0:
                b = 1.0

    if key == GLFW_KEY_DOWN and action == GLFW_PRESS:
        if current == 0:
            r -= 0.1
            if r < 0.0:
                r = 0.0
        if current == 1:
            g -= 0.1
            if g < 0.0:
                g = 0.0
        if current == 2:
            b -= 0.1
            if b < 0.0:
                b = 0.0
    if key == GLFW_KEY_W and action == GLFW_PRESS:
        z -= 1
    if key == GLFW_KEY_S and action == GLFW_PRESS:
        z += 1
    if key == GLFW_KEY_A and action == GLFW_PRESS:
        x -= 1
    if key == GLFW_KEY_D and action == GLFW_PRESS:
        x += 1
    if key == GLFW_KEY_Q and action == GLFW_PRESS:
        y -= 1
    if key == GLFW_KEY_E and action == GLFW_PRESS:
        y += 1


def mouse_motion_callback(window, x_pos, y_pos):
    global delta_x
    global mouse_x_pos_old
    global delta_y
    global mouse_y_pos_old

    delta_x = x_pos - mouse_x_pos_old
    mouse_x_pos_old = x_pos
    delta_y = y_pos - mouse_y_pos_old
    mouse_y_pos_old = y_pos



def mouse_button_callback(window, button, action, mods):
    global left_mouse_button_pressed
    global right_mouse_button_pressed

    if button == GLFW_MOUSE_BUTTON_LEFT and action == GLFW_PRESS:
        left_mouse_button_pressed = 1
    else:
        left_mouse_button_pressed = 0

    if button == GLFW_MOUSE_BUTTON_RIGHT and action == GLFW_PRESS:
        right_mouse_button_pressed = 1
    else:
        right_mouse_button_pressed = 0


def main():
    if not glfwInit():
        sys.exit(-1)

    window = glfwCreateWindow(400, 400, __file__, None, None)
    if not window:
        glfwTerminate()
        sys.exit(-1)

    tab = [[[0] * 6 for i in range(N + 1)] for j in range(N + 1)]
    for u in range(N + 1):
        for v in range(N + 1):
            pu = u / N
            pv = v / N
            a = (-90 * pu ** 5 + 225 * pu ** 4 - 270 * pu ** 3 + 180 * pu ** 2 - 45 * pu)
            tab[u][v][0] = a * math.cos(math.pi * pv)
            tab[u][v][1] = 160 * pu ** 4 - 320 * pu ** 3 + 160 * pu ** 2 - 5
            tab[u][v][2] = a * math.sin(math.pi * pv)
            if u == 0:
                tab[u][v][3] = 0.0
                tab[u][v][4] = -1.0
                tab[u][v][5] = 0.0
            elif u == 20:
                tab[u][v][3] = 0.0
                tab[u][v][4] = 1.0
                tab[u][v][5] = 0.0
            elif u == 40:
                tab[u][v][3] = 0.0
                tab[u][v][4] = 1.0
                tab[u][v][5] = 0.0
            else:
                try:
                    s1 = (-450 * (pu ** 4) + 900 * (pu ** 3) - 810 * (pu ** 2) + 360 * pu - 45)
                    s2 = math.pi * (90 * (pu ** 5) - 225 * (pu ** 4) + 270 * (pu ** 3) - 180 * (pu ** 2) + 45 * pu)

                    xu = s1 * math.cos(math.pi * pv)
                    zu = s1 * math.sin(math.pi * pv)
                    xv = s2 * math.sin(math.pi * pv)
                    zv = -s2 * math.cos(math.pi * pv)
                    yv = 0.0
                    yu = 640 * (u ** 3) - 960 * (u ** 2) + 320 * u
                    xn = yu * zv - zu * yv
                    yn = zu * xv - xu * zv
                    zn = xu * yv - yu * xv
                    d = math.sqrt(xn * xn + yn * yn + zn * zn)
                    tab[u][v][3] = xn / d
                    tab[u][v][4] = yn / d
                    tab[u][v][5] = zn / d
                except Exception:
                    print(u,v)

    glfwMakeContextCurrent(window)
    glfwSetFramebufferSizeCallback(window, update_viewport)
    glfwSetKeyCallback(window, keyboard_key_callback)
    glfwSetCursorPosCallback(window, mouse_motion_callback)
    glfwSetMouseButtonCallback(window, mouse_button_callback)
    glfwSwapInterval(1)

    startup()
    while not glfwWindowShouldClose(window):
        render(glfwGetTime(), tab)
        glfwSwapBuffers(window)
        glfwPollEvents()
    shutdown()

    glfwTerminate()


if __name__ == '__main__':
    main()
