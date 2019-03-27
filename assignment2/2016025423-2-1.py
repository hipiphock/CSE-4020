import numpy as np
import glfw
from OpenGL.GL import *

v = np.linspace(0, np.pi * 2, 13)
cos_v = np.cos(v)
sin_v = np.sin(v)
num = 4

def key_callback(window, key, scancode, action, mods):
    global num
    if key == glfw.KEY_1:
        if action == glfw.PRESS:
            num = 1
    elif key == glfw.KEY_2:
        if action == glfw.PRESS:
            num = 2
    elif key == glfw.KEY_3:
        if action == glfw.PRESS:
            num = 3
    elif key == glfw.KEY_4:
        if action == glfw.PRESS:
            num = 4
    elif key == glfw.KEY_5:
        if action == glfw.PRESS:
            num = 5
    elif key == glfw.KEY_6:
        if action == glfw.PRESS:
            num = 6
    elif key == glfw.KEY_7:
        if action == glfw.PRESS:
            num = 7
    elif key == glfw.KEY_8:
        if action == glfw.PRESS:
            num = 8
    elif key == glfw.KEY_9:
        if action == glfw.PRESS:
            num = 9
    elif key == glfw.KEY_0:
        if action == glfw.PRESS:
            num = 0
            
    elif key == glfw.KEY_SPACE and action == glfw.PRESS:
        print('press space: (%d %d)' %glfw.get_cursor_pos(window))

def render(key):
    if key == 1:
        glClear(GL_COLOR_BUFFER_BIT)
        glLoadIdentity()
        glBegin(GL_POINTS)
        for i in range(0, 12):
            glVertex2f(cos_v[i],sin_v[i])
        glEnd()
    elif key == 2:
        glClear(GL_COLOR_BUFFER_BIT)
        glLoadIdentity()
        glBegin(GL_LINES)
        for i in range(0, 12):
            glVertex2f(cos_v[i],sin_v[i])
        glEnd()
    elif key == 3:
        glClear(GL_COLOR_BUFFER_BIT)
        glLoadIdentity()
        glBegin(GL_LINE_STRIP)
        for i in range(0, 12):
            glVertex2f(cos_v[i],sin_v[i])
        glEnd()
    elif key == 4:
        glClear(GL_COLOR_BUFFER_BIT)
        glLoadIdentity()
        glBegin(GL_LINE_LOOP)
        for i in range(0, 12):
            glVertex2f(cos_v[i],sin_v[i])
        glEnd()
    elif key == 5:
        glClear(GL_COLOR_BUFFER_BIT)
        glLoadIdentity()
        glBegin(GL_TRIANGLES)
        for i in range(0, 12):
            glVertex2f(cos_v[i],sin_v[i])
        glEnd()
    elif key == 6:
        glClear(GL_COLOR_BUFFER_BIT)
        glLoadIdentity()
        glBegin(GL_TRIANGLE_STRIP)
        for i in range(0, 12):
            glVertex2f(cos_v[i],sin_v[i])
        glEnd()
    elif key == 7:
        glClear(GL_COLOR_BUFFER_BIT)
        glLoadIdentity()
        glBegin(GL_TRIANGLE_FAN)
        for i in range(0, 12):
            glVertex2f(cos_v[i],sin_v[i])
        glEnd()
    elif key == 8:
        glClear(GL_COLOR_BUFFER_BIT)
        glLoadIdentity()
        glBegin(GL_QUADS)
        for i in range(0, 12):
            glVertex2f(cos_v[i],sin_v[i])
        glEnd()
    elif key == 9:
        glClear(GL_COLOR_BUFFER_BIT)
        glLoadIdentity()
        glBegin(GL_QUAD_STRIP)
        for i in range(0, 12):
            glVertex2f(cos_v[i],sin_v[i])
        glEnd()
    elif key == 0:
        glClear(GL_COLOR_BUFFER_BIT)
        glLoadIdentity()
        glBegin(GL_POLYGON)
        for i in range(0,12):
            glVertex2f(cos_v[i],sin_v[i])
        glEnd()


def main():
    global state
    if not glfw.init():
        return
    
    window = glfw.create_window(480, 480, "2016025423", None, None)
    if not window:
        glfw.terminate()
        return

    glfw.set_key_callback(window, key_callback)
    glfw.make_context_current(window)
    
    while not glfw.window_should_close(window):
        glfw.poll_events()

        render(state)
        
        glfw.swap_buffers(window)

    glfw.terminate()

if __name__ == "__main__":
    main()




    