# -*- coding: utf-8 -*-
"""
Created on Mon Aug 19 14:08:32 2024
@author: Lorenzo Ferri 

""" 

import math 

#questa funzione è praticamente la matrice di rotazione 2d in forma di sistema con angolo in gradi
def componentAxisTranslationDegree(oldX,oldY,theta):
    newX=oldX*math.cos(math.radians(theta))+oldY*math.sin(math.radians(theta))
    newY=oldY*math.cos(math.radians(theta))-oldX*math.sin(math.radians(theta))
    return newX,newY

#questa funzione serve per trasformare da coordinate cartesiane a coordianate
#polari (NB i gradi vanno da 0 a +360)
def Coord_Cart_to_Polar (x,y):
    intensity = round(math.sqrt(x*x+y*y),3)
    direction=round(math.degrees(math.atan2(y,x)),2)
    if direction <0 : direction =direction +360
    return intensity, direction

#questa funzione serve per trasformare da coordinate cartesiane a coordianate
#polari riferite a nord con grai positivi in senso orario
def Coord_Cart_to_Polar_North (E,N):
   
    Int = round(math.sqrt(E*E+N*N),3)
    if E>0 and N>0:
        Dir = round(90-math.degrees(math.atan2(N,E)),2)
       # print ("Primo Quadrante", E, N, Int, Dir)
    elif E>0 and N<0:
        alfa = math.degrees(math.atan2(N, E))
        Dir = round(90 + abs(alfa),2)
        #print ("Secondo Quadrante", E, N, Int, Dir)
    elif E<0 and N<0:
        alfa = math.degrees(math.atan2(N, E))
        Dir = round(90 + abs(alfa),2)
        #print ("Terzo Quadrante", E, N, Int, Dir) #, round(alfa,2))
    elif E<0 and N>0:
        alfa = math.degrees(math.atan2(N, E))
        Dir = round(360 - (abs(alfa) - 90),2)
        #print ("Quarto Quadrante", E, N, Int, Dir) #, round(alfa,2))
    elif E==0 and N>0:
        Dir=0.00
        #print ("Nord secco", E, N, Int, Dir) #, round(alfa,2))
    elif E==0 and N<0:
        Dir=180.00
        #print ("Sud secco", E, N, Int, Dir) #, round(alfa,2))
    elif E>0 and N==0:
        Dir=90.00
        #print ("Est secco", E, N, Int, Dir) #, round(alfa,2))
    elif E<0 and N==0:
        Dir=270.00
        #print ("Ovest secco", E, N, Int, Dir) #, round(alfa,2))
    elif E==0 and N==0:
        Dir=0.00
        #print ("Non c'é corrente", E, N, Int, Dir) #, round(alfa,2))
                
    return Int, Dir