# -*- coding: utf-8 -*-
"""
Created on Mon Aug 19 14:08:32 2024

@author: Lorenzo Ferri based on Fabio Brunetti script

Converto i dati ENU in Intensità e Gradi Nord
""" 

import math 

def Coord_Cart_to_Polar (E,N):
   
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