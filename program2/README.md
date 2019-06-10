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

실제로 구현한 코드에서는 원래 평면과 수직인 평면으로 normal vector = (1, 0, 0)인 평면을 만들었으며, 그 평면에서 z좌표는 고정을 시키는 동작을 하였습니다.

``` python
p = Plane(np.array((1, 0, 0)), getTranslation(cow2wld))
c = ray.intersectsPlane(p)

currentPos = ray.getPoint(c[1])
currentPos[2] = getTranslation(cow2wld)[2]
```

## Design - Catmull-Rom Spline

이번 과제의 핵심이 되는 부분입니다.

Catmull-Rom Spline을 구하는 방법에는 여러가지가 있습니다.

이번 과제에서는 다음 식을 사용했습니다.

```
 P(t) = 0.5 * ((2.0 * P1) + (-P0 + P2) * t + (2.0 * P0 - 5.0 * P1 + 4.0 * P2 - P3) * t^2 + (-P0 + 3.0 * P1 - 3.0 * P2 + P3) * t^3)
```

이번 과제는 주어진 object(소)가 선택한 6개의 점을 통과하면서 머리의 방향이 해당 경로의 진행방향을 따라가는 것을 요구하고 있습니다. 여기에서 spline을 구하는 식을 미분하면서 방향을 구할 수도, 아니면 이전 지점과 다음 지점의 차이를 통해서 진행 방향을 알아낼 수도 있습니다.

이번 과제에서는 다음지점과 이전지점의 차이를 구하여 진행 방향을 알아냈습니다.

## Implementation - Catmull-Rom Spline
실제로 spline의 위치를 주는 함수는 위의 식을 사용해서 구현했습니다.

``` python
# function that gives the position of spline
def getParam(p0, p1, p2, p3, t):
    retval = 0.5*((2.0*p1)+(-p0+p2)*t+(2.0*p0-5.0*p1+4.0*p2-p3)*t**2+(-p0+3.0*p1-3.0*p2+p3)*t**3)
    return retval
```

이를 기반으로 미분을 해서 방향을 구하는 함수도 구현하긴 했지만, 실제로 사용하지는 않았습니다.

``` python
# function that gives rotation matrix of current position
def getDerivate(p0, p1, p2, p3, t):
    retval = 0.5*((p2-p0) + (2.0*p0-5.0*p1+4.0*p2-p3)*2.0*t + (-p0+3.0*p1-3.0*p2+p3)*3.0*t**2)
    return retval
```

소가 주어진 방향을 보도록 rotation함수를 다음과 같이 만들었습니다.

``` python
# function that rotates cow
def getRotation(original, prevPos, nextPos):
    retval = original
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
    retval[0:3, 0:3] = (Ry @ Rx @ Rz).T
    return retval
```

실제로 소를 출력하는 함수는 다음과 같이 구현했습니다.

``` python
# if all six points are saved, rotate the cow for three times
    if savedCount == 6:
        # initializing job should be done
        # initialize time before start
        if not timeInitialized:
            startTime = glfw.get_time()
            timeInitialized = True
            rollerCow = savedLoc[0]
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
            cow2wld = savedLoc[0]
            timeInitialized = False
            savedCount = -1
            glFlush()
            return
        # rotate the cow
        rollerCow = getRotation(rollerCow, getTranslation(rollerCow), getTranslation(splinepos))
        # move the cow
        setTranslation(rollerCow, getTranslation(splinepos))
        drawCow(rollerCow, False)
```
시간 t에 따라서 구간을 나눠서 spline을 구하도록 하였습니다.

## Result

지금 첫 번째 점과 마지막 점에서 이상하게 돌아갑니다.

## Troubleshooting

이번 과제를 수행하면서 기존 코드에서 저장했던 점들이 날라가는 일이 발생했습니다. 지금도 왜 그런지 모르겠습니다. 흑흑 