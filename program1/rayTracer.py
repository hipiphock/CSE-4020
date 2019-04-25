#!/usr/bin/env python3
# -*- coding: utf-8 -*
# sample_python aims to allow seamless integration with lua.
# see examples below

import os
import sys
import pdb  # use pdb.set_trace() for debugging
import code # or use code.interact(local=dict(globals(), **locals()))  for debugging.
import xml.etree.ElementTree as ET
import numpy as np
from PIL import Image

def normalize(vector):
    size = np.sqrt(np.sum(vector**2))
    return vector / size

class Color:
    def __init__(self, R, G, B):
        self.color=np.array([R,G,B]).astype(np.float)

    # Gamma corrects this color.
    # @param gamma the gamma value to use (2.2 is generally used).
    def gammaCorrect(self, gamma):
        inverseGamma = 1.0 / gamma;
        self.color=np.power(self.color, inverseGamma)

    def toUINT8(self):
        return (np.clip(self.color, 0,1)*255).astype(np.uint8)

class Camera:
    def __init__(self, viewPoint, direction, up, projDist, viewWidth, viewHeight, imgSize):
        self.viewPoint = viewPoint
        self.direction = normalize(direction)
        self.u = normalize(np.cross(up, direction))
        self.v = normalize(np.cross(direction, self.u))

        self.viewDist = projDist
        self.viewWidth = viewWidth
        self.viewHeight = viewHeight
        self.imgWidth = imgSize[0]
        self.imgHeight = imgSize[1]

    def getRay(self, i, j):
        uc = j - self.imgWidth / 2
        vc = -i + self.imgHeight / 2
        wc = (self.viewDist / self.viewWidth) * self.imgWidth
        s = self.viewPoint + self.u * uc + self.v * vc - self.direction * wc
        return self.viewPoint, normalize(s - self.viewPoint)

class Sphere:
    def __init__(self, center, radius):
        self.center = center
        self.radius = radius

    # returns t, hitPoint, hitNormal
    def intersect(self, rayPoint, rayVec, tmin, tmax):
        b = np.dot(rayPoint - self.center, rayVec)
        c = np.dot(rayPoint - self.center) * np.dot(rayPoint - self.center) - self.radius * self.radius
        insideRoot = b * b - c
        if insideRoot < 0:
            return np.inf
        elif insideRoot == 0:
            return -b
        else:
            t1 = -b - np.sqrt(b * b - c)
            t2 = -b + np.sqrt(b * b - c)
            # return t1 if t1 * t1 < t2 * t2 else t2
            if t1 * t1 < t2 * t2:
                t = t1
                hitPoint = rayPoint + t * rayVec
                hitNormal = hitPoint - self.center
                return t, hitPoint, hitNormal
            else:
                t = t2
                hitPoint = rayPoint + t * rayVec
                hitNormal = hitPoint - self.center
                return t, hitPoint, hitNormal

class Box:
    def __init__(self, minPt, maxPt):
        self.minPt = minPt
        self.maxPt = maxPt

    def intersect(self, rayPoint, rayVec, tmin, tmax):
        tx0 = np.inf
        tx1 = np.inf
        ty0 = np.inf
        ty1 = np.inf
        tz0 = np.inf
        tz1 = np.inf

        vx = -1
        vy = -1
        vz = -1

        if rayVec[0] != 0:
            tx0 = (self.minPt[0] - rayPoint[0]) / rayVec[0]
            tx1 = (self.maxPt[0] - rayPoint[0]) / rayVec[0]
        if rayVec[1] != 0:
            ty0 = (self.minPt[1] - rayPoint[1]) / rayVec[1]
            ty1 = (self.maxPt[1] - rayPoint[1]) / rayVec[1]
        if rayVec[2] != 0:
            ty0 = (self.minPt[2] - rayPoint[2]) / rayVec[2]
            ty1 = (self.maxPt[2] - rayPoint[2]) / rayVec[2]
        
        if tx0 > tx1:
            tmp = tx0
            tx0 = tx1
            tx1 = tmp
            vx = 1
        if ty0 > ty1:
            tmp = ty0
            ty0 = ty1
            ty1 = tmp
            vy = 1
        if tz0 > tz1:
            tmp = tz0
            tz0 = tz1
            tz1 = tmp
            vz = 1

        tminarr = np.array([tx0, ty0, tz0])
        tminidx = 0
        if ty0 > tminarr[tminidx]:
            tminidx = 1
        if tz0 > tminarr[tminidx]:
            tminidx = 2
        
        tmaxarr = np.array([tx1, ty1, tz1])
        tmaxidx = 0
        if ty1 > tmaxarr[tmaxidx]:
            tmaxidx = 1
        if tz1 > tmaxarr[tmaxidx]:
            tmaxidx = 2

        t0 = np.inf
        hitPoint = np.array([0, 0, 0])
        hitNormal = np.array([0, 0, 0])
        if tmaxarr[tmaxidx] > tminarr[tminidx]:
            t0 = tminarr[tminidx]
            if tminidx == 0:
                hitNormal = np.array([vx, 0, 0])
            elif tminidx == 1:
                hitNormal = np.array([0, vy, 0])
            elif tminidx == 2:
                hitNormal = np.array([0, 0, vz])
            hitPoint = rayPoint + t0 * rayVec
        if t0 < 0:
            t0 = np.inf
        return t0, hitPoint, hitNormal


class Shader:
    def __init__(self, diffuseColor, specularColor, exponent):
        self.diffuseColor = diffuseColor
        self.specularColor = specularColor
        self.exponent = exponent

class Light:
    def __init__(self, position, intensity):
        self.position = position
        self.intensity = intensity
        

def main():

    tree = ET.parse(sys.argv[1])
    root = tree.getroot()

    # set default values
    viewDir=np.array([0,0,-1]).astype(np.float)
    viewUp=np.array([0,1,0]).astype(np.float)
    viewProjNormal=-1*viewDir  # you can safely assume this. (no examples will use shifted perspective camera)
    viewWidth=1.0
    viewHeight=1.0
    projDistance=1.0
    intensity=np.array([1,1,1]).astype(np.float)  # how bright the light is.
    print(np.cross(viewDir, viewUp))

    # get camera
    imgSize=np.array(root.findtext('image').split()).astype(np.int)
    for c in root.findall('camera'):
        viewPoint = np.array(c.findtext('viewPoint').split()).astype(np.float)
        print('viewpoint', viewPoint)
        viewDir = np.array(c.findtext('viewDir').split()).astype(np.float)
        print('viewDir', viewDir)
        projNormal = np.array(c.findtext('projNormal').split()).astype(np.float)
        print('projNormal', projNormal)
        viewUp = np.array(c.findtext('viewUp').split()).astype(np.float)
        print('viewUp', viewUp)
        projDistance = float(c.findtext('projDistance'))
        print('projDistance', projDistance)
        viewWidth = float(c.findtext('viewWidth'))
        print('viewWidth', viewWidth)
        viewHeight = float(c.findtext('viewHeight'))
        print('viewHeight', viewHeight)
    camera = Camera(viewPoint, viewDir, viewUp, projDistance, viewWidth, viewHeight, imgSize)

    obj_shader = []
    # get shader
    for c in root.findall('shader'):
        diffuseColor = np.array(c.findtext('diffuseColor').split()).astype(np.float)
        print('name', c.get('name'))
        print('diffuseColor', diffuseColor)
        specularColor = np.array(c.findtext('specularColor').split()).astype(np.float)
        print('specularColor', specularColor)
        exponent = c.findtext('exponent')
        print('exponent', exponent)
        shader = Shader(diffuseColor, specularColor, exponent)
        obj_shader.append(shader)

    obj_surface = []
    # get surface
    for c in root.findall('surface'):
        if c.get('type') == 'Box':
            minPt = np.array(c.findtext('minPt').split()).astype(np.float)
            maxPt = np.array(c.findtext('maxPt').split()).astype(np.float)
            print('minPt', minPt)
            print('maxPt', maxPt)
            box = Box(minPt, maxPt)
            obj_surface.append(box)
            
        elif c.get('type') == 'Sphere':
            center = np.array(c.findtext('center').split()).astype(np.float)
            radius = float(c.findtext('radius'))
            print('center', center)
            print('radius', radius)
            sphere = Sphere(center, radius)
            obj_surface.append(sphere)
        else:
            print("ERROR")
            pass

    light_list = []
    # get light
    for c in root.findall('light'):
        light_pos = np.array(c.findtext('position').split()).astype(np.float)
        light_int = np.array(c.findtext('intensity').split()).astype(np.float)
        print('light position', light_pos)
        print('light intensity', light_int)
        light = Light(light_pos, light_int)
        light_list.append(light)

    #code.interact(local=dict(globals(), **locals()))  

    # Create an empty image
    channels=3
    img = np.zeros((imgSize[1], imgSize[0], channels), dtype=np.uint8)
    img[:,:]=0
    
    # replace the code block below!
    for i in np.arange(imgSize[1]):
        for j in np.arange(imgSize[0]):
            # get ray
            rayPoint, rayVec = camera.getRay(i, j)
            # find intersect
            tmin = np.inf
            intidx = 0
            hitPoint = np.array([0, 0, 0])
            hitNormal = np.array([0, 0, 0])
            color = np.array([0, 0, 0])
            for index, obj in enumerate(obj_surface):
                t, hp, hn = obj.intersect(rayPoint, rayVec, 0, float('inf'))
                if t < tmin:
                    tmin = t
                    hitPoint = hp
                    hitNormal = hn
                    intidx = index
            if tmin < np.inf:

                # handle shadows
                for light in light_list:
                    # Lambertian
                    I = normalize(light.position - hitPoint)
                    shadowPoint = hitPoint
                    shadowNormal = I
                    # Phong
                    h = normalize(I + rayVec)
                    tShadow = np.inf
                    shadowIdx = 0
                    for index, obj in enumerate(obj_surface):
                        t, hp, hn = obj.intersect(shadowPoint, shadowNormal, 0, float('inf'))
                        if t < tShadow:
                            tShadow = t
                            shadowIdx = index
                    if tShadow == np.inf:
                        color += shader[shadowIdx].diffuseColor * light.intensity * max([0, I @ hitNormal])
                        color += shader[shadowIdx].specularColor * light.intensity * (max([0, h @ hitNormal])**shader[shadowIdx].exponent)
            color = 255 * color
            for idx in range(3):
                if(color[idx] > 255):
                    color[idx] = 255
            img[i][j] = color

    rawimg = Image.fromarray(img, 'RGB')
    #rawimg.save('out.png')
    #rawimg.save(sys.argv[1]+'.png')
    rawimg.save(sys.argv[1] + '_test.png')
    
if __name__=="__main__":
    main()
