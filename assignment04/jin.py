def render():
    # enable depth test (we'll see details later)
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    glEnable(GL_DEPTH_TEST)
    glPolygonMode(GL_FRONT_AND_BACK,GL_LINE)
    glLoadIdentity()

    # use orthogonal projection (we'll see details later)
    myOrtho(-5,5,-5,5,-8,5)
   # glOrtho(-5,5,-5,5,-8,5)

    myLookAt(np.array([5,3,5]),np.array([1,1,-1]),np.array([0,1,0]))
    drawFrame()

    glColor3ub(255, 255, 255)
    
    drawCubeArray()

def myLookAt(eye,at,up):
    w = (eye-at)/(np.sqrt(np.dot(eye-at,eye-at)))
    u = ( np.cross(up,w) )/np.sqrt(np.dot(np.cross(up,w),np.cross(up,w)))
    v = np.cross(w,u)#w x u

    M = np.array([[u[0],u[1],u[2],-np.dot(u,eye)],
                  [v[0],v[1],v[2],-np.dot(v,eye)],
         [w[0],w[1],w[2],-np.dot(w,eye)],
                  [0,0,0,1]])
    
    glMultMatrixf(M.T)