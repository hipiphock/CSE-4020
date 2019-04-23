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
        self.v = normalize(np.cross(direction, u))

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
        return viewPoint, s - viewPoint

class Sphere:
    def __init__(self, center, radius, shader):
        self.center = center
        self.radius = radius
        self.shader = shader

class Box:
    def __init__(self, minPt, maxPt, shader):
        self.minPt = minPt
        self.maxPt = maxPt
        self.shader = shader

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

    for c in root.findall('shader'):
        diffuseColor_c = np.array(c.findtext('diffuseColor').split()).astype(np.float)
        print('name', c.get('name'))
        print('diffuseColor', diffuseColor_c)
        specularColor_c = np.array(c.findtext('specularColor').split()).astype(np.float)
        print('specularColor', specularColor_c)
        exponent_c = c.findtext('exponent')
        print('exponent', exponent_c)
        obj_colors.append([diffuseColor_c, specularColor_c, exponent_c])

    type = 0
    for c in root.findall('surface'):
        if c.get('type') == 'Box':
            minPt = np.array(c.findtext('minPt').split()).astype(np.float)
            maxPt = np.array(c.findtext('maxPt').split()).astype(np.float)
            print('minPt', minPt)
            print('maxPt', maxPt)
            type = 0
            obj_details.append(['Box', minPt, maxPt])
        elif c.get('type') == 'Sphere':
            center = np.array(c.findtext('center').split()).astype(np.float)
            radius = float(c.findtext('radius'))
            print('center', center)
            print('radius', radius)
            type = 1
            obj_details.append(['Sphere', center, radius])
        else:
            type = -1

    for c in root.findall('light'):
        light_pos = np.array(c.findtext('position').split()).astype(np.float)
        light_int = np.array(c.findtext('intensity').split()).astype(np.float)
        print('light position', light_pos)
        print('light intensity', light_int)

    #code.interact(local=dict(globals(), **locals()))  

    # Create an empty image
    channels=3
    img = np.zeros((imgSize[1], imgSize[0], channels), dtype=np.uint8)
    img[:,:]=0
    
    # replace the code block below!
    camera = Camera(viewPoint, viewDir, viewUp, projDistance, viewWidth, viewHeight, imgSize)
    for j in np.arange(imgSize[1]):
        for i in np.arange(imgSize[0]):
            # get ray
            rayPoint, rayDir = camera.getRay(i, j)
            # get intersection
            if type == 0:
                t = intersect_plane(rayPoint, rayDir, minPt, maxPt)
            elif type == 1:
                t = intersect_sphere(rayPoint, rayDir, center, radius)
            else:
                return
            # get details
            if t == np.inf:
                continue
            img[i][j] = diffuseColor_c
            

    rawimg = Image.fromarray(img, 'RGB')
    #rawimg.save('out.png')
    #rawimg.save(sys.argv[1]+'.png')
    rawimg.save(sys.argv[1] + '_test.png')
    
if __name__=="__main__":
    main()
