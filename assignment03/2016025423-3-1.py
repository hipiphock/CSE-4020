import numpy as np
import glfw
from OpenGL.GL import *

degree = 10.0 * np.pi / 180
gComposedM = np.identity(3)

def key_callback(window, key, scancode, action, mods):
    global gComposedM
    if key == glfw.KEY_1:
        if action == glfw.PRESS:
            gComposedM = np.identity(3)
    elif key == glfw.KEY_Q:
        if action == glfw.PRESS:
            gComposedM[0][2] -= 0.1
    elif key == glfw.KEY_E:
        if action == glfw.PRESS:
            gComposedM[0][2] += 0.1
    elif key == glfw.KEY_A:
        if action == glfw.PRESS:
            counterClock = np.array([
                [np.cos(degree), -np.sin(degree), 0.],
                [np.sin(degree), np.cos(degree), 0.],
                [0., 0., 1.]
                ])
            gComposedM = gComposedM @ counterClock
    elif key == glfw.KEY_D:
        if action == glfw.PRESS:
            clock = np.array([
                [np.cos(degree), np.sin(degree), 0.],
                [-np.sin(degree), np.cos(degree), 0.],
                [0., 0., 1.]
                ])
            gComposedM = gComposedM @ clock
    elif key == glfw.KEY_W:
        if action == glfw.PRESS:
            scale = np.array([
                [0.9, 0., 0.],
                [0., 1., 0.],
                [0., 0., 1.]
                ])
            gComposedM = scale @ gComposedM
    elif key == glfw.KEY_S:
        if action == glfw.PRESS:
            counterClock = np.array([
                [np.cos(degree), -np.sin(degree), 0.],
                [np.sin(degree), np.cos(degree), 0.],
                [0., 0., 1.]
                ])
            gComposedM = counterClock @ gComposedM

def render(T):
   glClear(GL_COLOR_BUFFER_BIT)
   glLoadIdentity()
   # draw coordinate
   glBegin(GL_LINES)
   glColor3ub(255, 0, 0)
   glVertex2fv(np.array([0., 0.]))
   glVertex2fv(np.array([1., 0.]))
   glColor3ub(0, 255, 0)
   glVertex2fv(np.array([0., 0.]))
   glVertex2fv(np.array([0., 1.]))
   glEnd()
   # draw triangle
   glBegin(GL_TRIANGLES)
   glColor3ub(255, 255, 255)
   glVertex2fv( (T @ np.array([.0, .5, 1.]))[:-1])
   glVertex2fv( (T @ np.array([.0, .0, 1.]))[:-1])
   glVertex2fv( (T @ np.array([.5, .0, 1.]))[:-1])
   glEnd()

def main():
    if not glfw.init():
        return 
    window = glfw.create_window(480, 480, "2016025423-3-1", None, None)
    if not window:
        glfw.terminate()
        return

    glfw.set_key_callback(window, key_callback)
    glfw.make_context_current(window)
    
    while not glfw.window_should_close(window):
        glfw.poll_events()
        render(gComposedM)
        
        glfw.swap_buffers(window)

    glfw.terminate()

if __name__ == "__main__":
    main() 
