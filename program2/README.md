# Program 2 - Cow Rollercoaster

이번 과제는 주어진 소가 사용자가 지정한 6개의 좌표를 Catmull-Rom spline을 돌면서 회전하도록 하는 과제입니다.

이번 과제에서 구현을 해야하는 부분은 크게 두 가지로

 * V_DRAG를 통해서 소가 수직으로 움직이도록 하기

 * Cow가 Catmull-Rom spline을 돌도록 하기

로 나눠집니다.

## Design - Vertical Dragging

기본 과제에 있는 Horizontal Dragging은 기존의 평면과 같은 normal vector를 공유하는 평면을 만든 뒤, 그 위에서 소를 움직입니다.

Vertical Dragging은 이와 달리 위-아래, 즉 두 방향으로만 움직여야 하므로, 기존의 평면에 수직으로 움직이면서 y좌표를 제외한 나머지 좌표는 고정시키는 동작이 필요합니다.

## Implementation - Vertical Dragging

실제로 구현한 코드에서는 원래 평면과 수직인 평면으로 normal vector = (1, 0, 0)인 평면을 만들었으며, 그 평면 위에서는 실제로 y와 z 좌표만이 움직이기 때문에 z좌표는 고정을 시키는 동작을 하였습니다.

``` python
p = Plane(np.array((1, 0, 0)), getTranslation(cow2wld))
c = ray.intersectsPlane(p)

currentPos = ray.getPoint(c[1])
currentPos[2] = getTranslation(cow2wld)[2]
```

뿐만 아니라 기존의 onMouseButton함수의 경우, 마우스 좌클릭 시 무조건 Vertical Dragging을 하도록 설정했고, 그 상태에서 마우스를 땔 경우 위치를 저장하도록 했습니다.

``` python
if button == glfw.MOUSE_BUTTON_LEFT:
        if state == GLFW_DOWN:
            isDrag = V_DRAG
            print( "Left mouse down-click at %d %d\n" % (x,y))
            # start vertical dragging
        elif state == GLFW_UP and isDrag!=0:
            isDrag = H_DRAG
            # TODO: handle concurrency
            if 0 <= savedCount and savedCount <= 5 and cursorOnCowBoundingBox:
                # save point
                # savedLoc[savedCount] = cow2wld.copy()
                # print(savedCount)
                # print(savedLoc[savedCount])
                savedCount += 1
                savedLoc.append(cow2wld.copy())
                if savedCount == 6:
                    isDrag = 0
            elif savedCount == -1 and cursorOnCowBoundingBox:
                # case: initial click done.
                # initial click does not count or save the point
                savedCount += 1
            elif not cursorOnCowBoundingBox:
                isDrag = 0
            print( "Left mouse up\n")
```

추가로 onMouseButton, onMouseDrag 두 함수 모두 savedCount가 6일 경우, 진입 자체를 불허함으로써 마우스 사용을 비활성화했습니다.

``` python
if savedCount == 6:
    return
```

## Design - Catmull-Rom Spline

이번 과제의 핵심이 되는 부분입니다.

Catmull-Rom Spline을 구하는 방법에는 여러가지가 있습니다.

이번 과제에서는 다음 식을 사용했습니다.

```
 P(t) = 0.5 * ((2.0 * P1) + (-P0 + P2) * t + (2.0 * P0 - 5.0 * P1 + 4.0 * P2 - P3) * t^2 + (-P0 + 3.0 * P1 - 3.0 * P2 + P3) * t^3)
```

이번 과제는 주어진 object(소)가 선택한 6개의 점을 통과하면서 머리의 방향이 해당 경로의 진행방향을 따라가는 것을 요구하고 있습니다. 여기에서 spline을 구하는 식을 미분하면서 방향을 구할 수도, 아니면 이전 지점과 다음 지점의 차이를 통해서 진행 방향을 알아낼 수도 있습니다.

이번 과제에서는 다음지점과 이전지점의 차이를 구하여 진행 방향을 알아냈습니다. 컴퓨터라는 도구를 사용해서 이번 과제를 구현하다 보니 실제 시간 t를 이용하여 미래 위치 - 현재 위치를 하더라도 충분히 유의미한 값을 만들 수 있다는 생각을 하게 되어서 이 방법을 택하게 되었습니다.

뿐만 아니라, 단순히 뺄셈을 요구하는 평균변화율에 비해서 미분은 곱셈을 요구하고, 이는 조금이나마 더 긴 시간을 소모할 수도 있겠다는 생각을 하게 되었과, 따라서 미분을 사용하지 않고 구현을 하였습니다.

## Implementation - Catmull-Rom Spline

실제로 spline의 위치를 주는 함수는 위의 식을 사용해서 구현했습니다.

``` python
# function that gives the position of spline
def getParam(p0, p1, p2, p3, t):
    retval = 0.5*((2.0*p1)+(-p0+p2)*t+(2.0*p0-5.0*p1+4.0*p2-p3)*t**2+(-p0+3.0*p1-3.0*p2+p3)*t**3)
    return retval
```

이를 토대로 getParam 함수는 시간 t와 점 p0~p3에 따라서 소가 있어야 할 위치를 알려줍니다.
이 위치는 추후에 소의 머리 방향을 설정하는데도 중요한 정보가 됩니다.


이를 기반으로 미분을 해서 방향을 구하는 함수도 구현하긴 했지만, 실제로 사용하지는 않았습니다.
실제로 이게 옳게 돌아가는지는 잘 모르겠습니다. 보라색 소가 더 이상 보기 싫어서 미분은 포기합니다.
``` python
# function that gives rotation matrix of current position
def getDerivate(p0, p1, p2, p3, t):
    retval = 0.5*((p2-p0) + (2.0*p0-5.0*p1+4.0*p2-p3)*2.0*t + (-p0+3.0*p1-3.0*p2+p3)*3.0*t**2)
    return retval
```


소가 주어진 방향을 보도록 rotation함수를 다음과 같이 만들었습니다.
``` python
# function that rotates cow to heading direction
def getCowDir(prevPos, nextPos):
    global rollerCow
    direction = normalize(nextPos - prevPos)

    roll = 0
    pitch = np.arcsin(direction[1])
    yaw = np.arctan2(direction[2], direction[0])

    if yaw == 0:
        pitch = -pitch

    Rx = np.array([
        [1., 0., 0.],
        [0., np.cos(pitch), -np.sin(pitch)],
        [0., np.sin(pitch), np.cos(pitch)]
    ])
    Ry = np.array([
        [np.cos(yaw), 0., np.sin(yaw)],
        [0., 1., 0.],
        [-np.sin(yaw), 0., np.cos(yaw)]
    ])
    Rz = np.array([
        [np.cos(roll), -np.sin(roll), 0.],
        [np.sin(roll), np.cos(roll), 0.],
        [0., 0., 1.]
    ])
    rollerCow[0:3, 0:3] = (Ry @ Rx @ Rz).T
```

실제로 소를 출력하는 함수는 다음과 같이 구현했습니다.

``` python
# if all six points are saved, rotate the cow for three times
    elif savedCount == 6:
        # initializing job should be done
        # initialize time before start
        if not timeInitialized:
            startTime = glfw.get_time()
            timeInitialized = True
            rollerCow = savedLoc[0].copy()
        t = glfw.get_time() - startTime

        # get the spline position
        splinepos = initialCow
        if (0<=t and t<1) or (6<=t and t<7) or (12<=t and t<13):
            t = float(t) - int(t)
            splinepos = getParam(savedLoc[5], savedLoc[0], savedLoc[1], savedLoc[2], t)

        elif (1<=t and t<2) or (7<=t and t<8) or (13<=t and t<14):
            t = float(t) - int(t)
            splinepos = getParam(savedLoc[0], savedLoc[1], savedLoc[2], savedLoc[3], t)

        elif (2<=t and t<3) or (8<=t and t<9) or (14<=t and t<15):
            t = float(t) - int(t)
            splinepos = getParam(savedLoc[1], savedLoc[2], savedLoc[3], savedLoc[4], t)

        elif (3<=t and t<4) or (9<=t and t<10) or (15<=t and t<16):
            t = float(t) - int(t)
            splinepos = getParam(savedLoc[2], savedLoc[3], savedLoc[4], savedLoc[5], t)

        elif (4<=t and t<5) or (10<=t and t<11) or (16<=t and t<17):
            t = float(t) - int(t)
            splinepos = getParam(savedLoc[3], savedLoc[4], savedLoc[5], savedLoc[0], t)

        elif (5<=t and t<6) or (11<=t and t<12) or (17<=t and t<18):
            t = float(t) - int(t)
            splinepos = getParam(savedLoc[4], savedLoc[5], savedLoc[0], savedLoc[1], t)

        else:
            # end the rotation
            cow2wld = rollerCow
            timeInitialized = False
            savedCount = -1
            savedLoc.clear()
            glFlush()
            return
        # rotate the cow to heading direction
        getCowDir(getTranslation(rollerCow), getTranslation(splinepos))
        # move the cow
        setTranslation(rollerCow, getTranslation(splinepos))
        drawCow(rollerCow, False)
```
시간 t에 따라서 구간을 나눠서 spline을 구하도록 하였습니다. 코드를 더 보기 좋게 간소화할 수는 있을 것 같습니다만, 더 이상 보라색 소를 보기 싫어서 여기에서 마무리했습니다.

기본적인 메커니즘은 시간 구간에 따라서 주어지는 spline 경로의 값과 그 이전 위치의 차이를 바탕으로 소의 방향을 설정한 뒤, spline 경로의 위치만큼 이동시킨 후, 소를 그리는 형태로 작동합니다.

## Result

정말 잘 돌아갑니다.

## Troubleshooting

이번 과제를 수행하면서 기존 코드에서 저장했던 점들이 날라가는 일이 발생했습니다. 이는 Python에서 np.array와 같은 변수를 그냥 등호로 복사하는 경우, shallow copy가 되기 때문에 일어나는 일이었습니다. 이는 수 많은 변수들을 deep copy를 하면서 해결할 수 있었습니다.