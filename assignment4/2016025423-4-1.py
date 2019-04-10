import numpy as np

def myLookAt():

def myOrtho(left, right, bottom, top, zNear, zFar):

def render():
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    glEnable(GL_DEPTH_TEST)
    glPolygonMode(GL_FRONT_AND_BACK, GL_LINE)
    glLoadIdentity()

    myOrtho(-5, 5, -5, 5, -8, 8)
    myLookAt(np.array([5, 3, 5]), np.array([1, 1, -1]), np.array([0, 1, 0]))

    # above is equivalent to:
    # glOrtho(-5, 5, -5, 5, -8, 8)
    # gluLookAt(5, 3, 5, 1, 1, -1, 0, 1, 0)

    drawFrame()

    glColor3ub(255, 255, 255)
    drawCubeArray()

def main():
    if not glfw.init():
        return 
    window = glfw.create_window(480, 480, "2016025423-4-1", None, None)
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
