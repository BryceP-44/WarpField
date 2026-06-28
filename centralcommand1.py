from tkinter import *
from mod1 import *
import copy
#from solver1 import *

width,height=11,11


root=Tk()
root.title("Scalar Siim")
root.geometry("800x600")
graph=Canvas(root,width=800,height=600,bg="black")
graph.pack()#(fill="both",expand=True)

#width, height
general=[600,500]

#diffusivity and ther material information
mats=[0,2]

#G exists everywhere and contains simulate type, material type, solver information
#put 0s in all of G
G=createG(general,0,1,0)

print(id(G[21][199]))
print(id(G[20][199]))


G=rect(10,10,550,450,[1,2,0],G)
print(id(G[21][199]))
print(id(G[20][199]))
G=rect(0,200,300,250,[0,3,100],G)
G=circle(100,100,30,[0,3,100],G)



#after geometry is created, create C based on G to reduce simulation points
#C contains coordinates of all simulation points
C=createC(general, G)


img=PhotoImage(width=600, height=500)
graph.create_image((200,100),image=img, state="normal", anchor="nw")

for t in range(100):
    print(t/2000)
    Gnew=copy.deepcopy(G)
    for i in range(len(C)):
        x,y=C[i]
        T=G[x][y][2]
        T1,T2,T3,T4=G[x+1][y][2],G[x][y+1][2],G[x-1][y][2],G[x][y-1][2]
        Gnew[x][y][2]=T+(T1+T2+T3+T4-4*T)*.15
        if x==20 and y==199:
            print(T+(T1+T2+T3+T4-4*T)*.15)
    G=Gnew
            


print("start")
cont=1
k=0
for i in range(601):
    for j in range(501):
        if G[i][j][1]==1:
            color=hexcolor(0,0,255)
        if G[i][j][1]==2:
            color=hexcolor(round(255*G[i][j][2]/100),0,round(.3*255))
        if G[i][j][1]==3:
            color=hexcolor(255,0,0)
        img.put(color, (i, -j+500)) #converted y to be correct
        root.update()



#for i in 
#graph.delete("all")









