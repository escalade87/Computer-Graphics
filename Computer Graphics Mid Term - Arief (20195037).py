# -*- coding: utf-8 -*-
"""
Created on Fri May  1 11:56:14 2020

@author: wad
"""

import pygame
from sys import exit
import numpy as np
    
width = 1024
height = 768
XMARGIN    = 25
YMARGIN    = 25
MAX = 1024
pygame.init()
screen = pygame.display.set_mode((width, height), 0, 32)

#background_image_filename = 'curve_pattern.png'

#background = pygame.image.load(background_image_filename).convert()
#width, height = background.get_size()
screen = pygame.display.set_mode((width, height), 0, 32)
pygame.display.set_caption("ImagePolylineMouseButton")
  
# Define the colors we will use in RGB format
BLACK = (  0,   0,   0)
WHITE = (255, 255, 255)
BLUE =  (  0,   0, 255)
GREEN = (  0, 255,   0)
RED =   (255,   0,   0)

CP = [] 
dots = []
T = [None] * MAX

count = 0
#screen.blit(background, (0,0))
screen.fill(WHITE)

# https://kite.com/python/docs/pygame.Surface.blit
clock= pygame.time.Clock()
    
      
def drawPoint(pt, color=GREEN, thick=3):
    # pygame.draw.line(screen, color, pt, pt)
    pygame.draw.circle(screen, color, pt, thick)

            
def drawLine(pt0, pt1, color=GREEN, thick=3):
    alpha=0
    while alpha < 1:     
        pt_x = (1 - alpha) * pt0[0] + alpha * pt1[0]
        pt_y = (1 - alpha) * pt0[1] + alpha * pt1[1]
        drawPoint([int(pt_x), int(pt_y)], color, thick)
        alpha+=0.001

def drawPolylines(color=GREEN, thick=3):
    #if(count < 2): return
    for i in range(count-1):
        drawLine(CP[i], CP[i+1], color)
        if mode == 4:
            hermite(i)
        elif mode == 5:
            spline(i)
        #pygame.draw.line(screen, color, CP[i], CP[i+1], thick)
    
    if count > 2:
        if mode == 2:
            myLagrange()
        elif mode == 3:
            myBezier()
        
        
def drawRectangles():     
    for i in range(count):
        if i == checkCoord(x,y):
            pygame.draw.rect(screen, RED, (CP[i][0]-margin, CP[i][1]-margin, 2*margin, 2*margin), 5)
        else:
            pygame.draw.rect(screen, BLUE, (CP[i][0]-margin, CP[i][1]-margin, 2*margin, 2*margin), 5)
            
def drawCircles():
    for i in range(len(dots)):
        pygame.draw.circle(screen, RED, dots[i], 0)
    

def    myLagrange():
    v = [None]*2

    if count<=0 or count > 200: return
    
    for i in range(MAX):
        x=(T[count-1]-T[0])*i/MAX+T[0]
        v = myLagrangeCalculate(v, T, x, count)
        drawPoint((int(v[0]),int(v[1])),color=RED)
    

def    myLagrangeCalculate(v, t, x, size):
    v[0]=v[1]=0.
    for i in range(size):
        l=1.
        for j in range(size):
            if j != i:
                l*=(x-t[j])/(t[i]-t[j])
        
        v[0]+=CP[i][0]*l
        v[1]+=CP[i][1]*l
    
    return v
        
def    myBezier():
    v = [None]*2

    if(count<=0 or count > 200): return
    for i in range(MAX):
        x=i/MAX
        myBezierCalculate(v, T, x, count)
        drawPoint((int(v[0]),int(v[1])),color=RED)
    

def    myBezierCalculate(v, t, x, size):
    v[0]=v[1]=0.
    
    for i in range(size):
        l=combi(size-1,i)*pow(x, i)*pow(1.-x, size-1-i)
        v[0]+=CP[i][0]*l
        v[1]+=CP[i][1]*l
    
    return v
    

def myMakeKnotVectors():    
    for i in range(count):
        T[i]=i
           
    
def    combi(n,m):
    total = 1.
    if (m==0 or m==n):
        return 1.
    elif (m<0 or m>n): return 1.     
    
    for i in range(n, m, -1):
        total *= i
    for i in range(n-m, 0, -1):
        total /= i
    return total

def checkCoord(x,y):
    for i in range(count):
        x1, y1, w, h = (CP[i][0]-2*margin, CP[i][1]-2*margin, 3.1*margin, 3.1*margin)
        x2, y2 = x1+w, y1+h
        if (x1 < x and x < x2):
            if (y1 < y and y < y2):
                return i
        
    return -1
    
def deletePoint(x,y):
    global count
    i=checkCoord(x, y)
    if i >=0 :
        del CP[i]
        count -= 1 
        
        
def movePoint(x, y):    
    i = checkCoord(x, y)
    if i >= 0:
        CP[i] = (x, y)


def hermite(i):
    if i == 0:
        T1 = (0, 0)
        T2 = (0.5*(CP[i+1][0]-CP[i][0]), 0.5*(CP[i+1][1]-CP[i][1]))
    elif i == (count-2):
        T1 = (0.5*(CP[i+1][0]-CP[i-1][0]), 0.5*(CP[i+1][1]-CP[i-1][1]))
        T2 = (0, 0)
    else:
        T1 = (0.5*(CP[i+1][0]-CP[i-1][0]), 0.5*(CP[i+1][1]-CP[i-1][1]))
        T2 = (0.5*(CP[i+2][0]-CP[i][0]), 0.5*(CP[i+2][1]-CP[i][1]))

    for t in range(0, MAX):
        s = t / MAX
        h1 = 2 * pow(s, 3) - 3 * pow(s, 2) + 1
        h2 = (-2) * pow(s, 3) + 3 * pow(s, 2)
        h3 = pow(s, 3) - 2 * pow(s, 2) + s
        h4 = pow(s, 3) - pow(s, 2)
        p_x = int(h1 * CP[i][0] + h2 * CP[i+1][0] + h3 * T1[0] + h4 * T2[0])
        p_y = int(h1 * CP[i][1] + h2 * CP[i + 1][1] + h3 * T1[1] + h4 * T2[1])
        drawPoint((p_x,p_y),color=RED)

def calculateDforSpline():
    list = []
    temp = []
    plist = []
    for i in range(count):
        if i == 0:
            plist.append(3 * np.subtract(np.array(CP[i+1]), np.array(CP[i])))
            temp.append(2)
        elif i == 1:
            temp.append(1)
        else:
            temp.append(0)
    list.append(temp)

    for i in range(count-2):
        temp = []
        for j in range(count):
            if j == i+1:
                temp.append(4)
            elif j == i:
                temp.append(1)     
                plist.append(3 * np.subtract(np.array(CP[i + 2]), np.array(CP[i])))
            elif j == (i+2):
                temp.append(1)
            else:
                temp.append(0)
        list.append(temp)
    list.append(list[0][::-1])
    plist.append(3 * np.subtract(np.array(CP[count - 1]), np.array(CP[count-2])))
   
    return(np.matmul(np.linalg.inv(np.array(list)),np.array(plist)))



def spline(i):
    c=[0,0]
    d=[0,0]
    
    D = calculateDforSpline()
   
    a = CP[i]
    b = D[i]
    c[0] = 3 * (CP[i+1][0] - CP[i][0]) - 2 * D[i][0] - D[i+1][0]
    c[1] = 3 * (CP[i+1][1] - CP[i][1]) - 2 * D[i][1] - D[i+1][1]
    d[0] = 2 * (CP[i][0] - CP[i + 1][0]) + D[i][0] + D[i+1][0]
    d[1] = 2 * (CP[i][1] - CP[i + 1][1]) + D[i][1] + D[i+1][1]

    for t in range(0, MAX):
        s = t / MAX
        y_x = int(a[0] + b[0] * s + c[0] * pow(s,2) + d[0] * pow(s,3))
        y_y = int(a[1] + b[1] * s + c[1] * pow(s,2) + d[1] * pow(s,3))
        drawPoint((y_x,y_y),color=RED)

def drawInstruction():
    font = pygame.font.SysFont("Arial", 18)
  
    strPoint1 = "Press 1 to show only lines, 2 to show Lagrange Interpolation, 3 to show Bezier Curves, 4 to show Hermite Interpolation, 5 to show Spline Interpolation"
    point1 = font.render(strPoint1, True, BLACK) 
    textRect = point1.get_rect()  
    screen.blit(point1, textRect)
    
    strPoint1 = "Default is 1, you can also use right mouse button to cycle through the mode"
    point1 = font.render(strPoint1, True, BLACK) 
    textRect = point1.get_rect()  
    textRect.centery += 20
    screen.blit(point1, textRect)
    
    strPoint1 = "To delete a point, please use middle mouse button, to clear all lines press escape"
    point1 = font.render(strPoint1, True, BLACK) 
    textRect = point1.get_rect()  
    textRect.centery += 40
    screen.blit(point1, textRect)
    
    strPoint1 = "Mode : "+getMode()
    point1 = font.render(strPoint1, True, BLACK) 
    textRect = point1.get_rect()  
    textRect.centery += 60
    screen.blit(point1, textRect)
    
def getMode():
    if mode == 1:
        return "Lines"
    elif mode == 2:
        return "Lagrange Interpolation"
    elif mode == 3:
        return "Bezier Curves"
    elif mode == 4:
        return "Piecewise Cubic Hermite Interpolation"
    elif mode == 5:
        return "Cubic Spline Interpolation"

def clearAll():
    global CP  
    global dots 
    global count 
    CP = [] 
    dots = []
    count = 0

#Loop until the user clicks the close button.
done = False
pressed = 0
margin = 6
old_pressed = 0
old_button1 = 0
old_button2 = 0
old_button3 = 0
x = 0
y = 0
mode = 1


while not done:   
    # This limits the while loop to a max of 10 times per second.
    # Leave this out and we will use all CPU we can.
    time_passed = clock.tick(30)

    for event in pygame.event.get():
        if event.type == pygame.MOUSEBUTTONDOWN:
            pressed = -1            
        elif event.type == pygame.MOUSEBUTTONUP:
            pressed = 1            
        elif event.type == pygame.QUIT:
            done = True
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_1:
                mode = 1
            elif event.key == pygame.K_2:
                mode = 2
            elif event.key == pygame.K_3:
                mode = 3
            elif event.key == pygame.K_4:
                mode = 4
            elif event.key == pygame.K_5:
                mode = 5
            elif event.key == pygame.K_ESCAPE:
                clearAll()
        else:
            pressed = 0

    screen.fill(WHITE)
    drawInstruction()
    button1, button2, button3 = pygame.mouse.get_pressed()
    x, y = pygame.mouse.get_pos()
    pt = [x, y]
    dots.append(pt)
    drawCircles()
    
    

    if old_pressed == -1 and pressed == 1 and old_button1 == 1 and button1 == 0 :     
        if checkCoord(x,y) < 0:
            CP.append(pt) 
            count += 1
    elif button1 == 1:     
        movePoint(x,y)
    elif old_pressed == -1 and pressed == 1 and old_button3 == 1 and button3 == 0 :     
        mode = (mode % 5)+1
    elif old_pressed == -1 and pressed == 1 and old_button2 == 1 and button2 == 0 :        
        deletePoint(x,y)
        
    #print("len:"+repr(len(CP))+" mouse x:"+repr(x)+" y:"+repr(y)+" button:"+repr(button1)+" pressed:"+repr(pressed)+" add CP ...")
    #else:
        #print("len:"+repr(len(CP))+" mouse x:"+repr(x)+" y:"+repr(y)+" button:"+repr(button1)+" pressed:"+repr(pressed))
    
    drawRectangles()
    if len(CP)>1:
        
        myMakeKnotVectors()
        drawPolylines(GREEN, 1)
        
        # drawLagrangePolylines(BLUE, 10, 3)
    
    # Go ahead and update the screen with what we've drawn.
    # This MUST happen after all the other drawing commands.
    pygame.display.update()
    old_button1 = button1
    old_button2 = button2
    old_button3 = button3
    old_pressed = pressed

pygame.quit()

