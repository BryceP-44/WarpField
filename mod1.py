from math import *

#this is going to lay out framework to make G for a thermal sim
#after making G, M can be made at sim time

#G[0]: 
#1: temperature solution
#2: dirichlet BC
#3: neumann BC
#4: Q gen

#M
#[0]:k types
#[1]: c types
#[2]: rho times



def createG(general, simulate, material, slate):
    width,height=general[0],general[1]
    G=[]
    for i in range(width+1):
        add=[]
        for j in range(height+1):
          add.append([simulate,material,slate]) #[simulate, material type, starter]
        G.append(add)
    return G


def createC(general, G):
    width,height=general[0],general[1]
    C=[]
    for i in range(width):
        for j in range(height):
            if G[i][j][0]==1:
              C.append([i,j]) #[x, y]
    return C

def circle(x, y, r, X_input,X):
    for i in range(x-r,x+r+1):
        for j in range(y-r,y+r+1):
            dist=((i-x)**2+(j-y)**2)**.5
            if dist<=r:
                X[i][j]=X_input.copy()
    return X


def rect(x1, y1, x2, y2, X_input,X):
    for i in range(x1,x2+1):
        for j in range(y1, y2+1):
            X[i][j]=X_input.copy()
    return X


def hexcolor(r,g,b):
    rgb_tuple=(r,g,b)
    hex_color="#{:02x}{:02x}{:02x}".format(*rgb_tuple)
    return(hex_color)



















