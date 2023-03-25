import numpy as np
import tkinter
from PIL import Image, ImageTk
from math import floor
import time

# Préparation du plateau
def gameSet (color1,color2):
    global M
    global Imgs
    global Pieces
    M = np.array([['R','N','B',0,0,'B','N','R'],['P','P','P','P','P','P','P','P'],
                  [0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0],
                  ['P2','P2','P2','P2','P2','P2','P2','P2'],['R2','N2','B2',0,0,'B2','N2','R2']])
    if color1=='W':
        M[0][3] ='K'
        M[0][4] = 'Q'
        M[7][3] = 'K2'
        M[7][4] = 'Q2'
    if color1=='B':
        M[0][3] = 'Q'
        M[0][4] = 'K'
        M[7][3] = 'Q2'
        M[7][4] = 'K2'
    M = M.T
    for x in range (dim):
        Pieces.append([])
        for y in range (dim):
            if M[x][y]=='0':
                Pieces[x].append(None)
            else:
                if M[x][y]!='0' and len(M[x][y])==1:
                    name = color1+M[x][y]
                elif len(M[x][y])==2:
                    name = color2+M[x][y][0]
                Imgs.append(tkinter.PhotoImage(file='assets/'+piecesSet+'/'+name+'.png'))
                Pieces[x].append(canvas.create_image(x*size+size/2,y*size+size/2,image=Imgs[-1],anchor='c'))

# Calcul des déplacements légaux
def moves (M,x,y,check=True) :
    player = len(M[x][y])
    C = []
    p = M[x][y]
    if p=='P' :
        if y<=7 and M[x][y+1]=='0' :
            C.append((x,y+1))
            if y==1 and M[x][y+2]=='0' :
                C.append((x,y+2))
        if x<dim-1 and y<dim-1 and len(M[x+1][y+1])>1 :
            C.append((x+1,y+1))
        if x>0 and y<dim-1 and len(M[x-1][y+1])>1 :
            C.append((x-1,y+1))
    if p=='R' :
        dx = 1
        while x+dx<=7 and M[x+dx][y]=='0' :
            C.append((x+dx,y))
            dx += 1
        if  x+dx<=7 and len(M[x+dx][y])==2 : C.append((x+dx,y))
        dx =- 1
        while x+dx>=0 and M[x+dx][y]=='0' :
            C.append((x+dx,y))
            dx -= 1
        if x+dx>=0 and len(M[x+dx][y])==2 : C.append((x+dx,y))
        dy = 1
        while y+dy<=7 and M[x][y+dy]=='0' :
            C.append((x,y+dy))
            dy += 1
        if y+dy<=7 and len(M[x][y+dy])==2 : C.append((x,y+dy))
        dy =- 1
        while y+dy>=0 and M[x][y+dy]=='0' :
            C.append((x,y+dy))
            dy -= 1
        if y+dy>=0 and len(M[x][y+dy])==2 : C.append((x,y+dy))
    if p=='N' :
        for dx in range (-2,3) :
            if dx!=0 :
                if dx%2==0 :
                    for dy in range (-1,2,2) :
                        if x+dx>=0 and x+dx<=7 and y+dy>=0 and y+dy<=7 :
                            if (M[x+dx][y+dy]=='0' or len(M[x+dx][y+dy])==2) :
                                C.append((x+dx,y+dy))
                else :
                    for dy in range (-2,3,4) :
                        if x+dx>=0 and x+dx<=7 and y+dy>=0 and y+dy<=7 :
                            if (M[x+dx][y+dy]=='0' or len(M[x+dx][y+dy])==2) :
                                C.append((x+dx,y+dy))
    if p=='B' :
        for sens_x in range (-1,2,2) :
            for sens_y in range (-1,2,2) :
                dx,dy=sens_x,sens_y
                while x+dx>=0 and x+dx<=7 and y+dy>=0 and y+dy<=7 and M[x+dx][y+dy]=='0' :
                    C.append((x+dx,y+dy))
                    if dx>0 : dx += 1
                    else : dx -= 1
                    if dy>0 : dy += 1
                    else : dy -= 1
                if x+dx>=0 and x+dx<=7 and y+dy>=0 and y+dy<=7 and len(M[x+dx][y+dy])==2 :
                    C.append((x+dx,y+dy))
    if p=='Q' :
        dx = 1
        while x+dx<=7 and M[x+dx][y]=='0' :
            C.append((x+dx,y))
            dx += 1
        if  x+dx<=7 and len(M[x+dx][y])==2 : C.append((x+dx,y))
        dx =- 1
        while x+dx>=0 and M[x+dx][y]=='0' :
            C.append((x+dx,y))
            dx -= 1
        if x+dx>=0 and len(M[x+dx][y])==2 : C.append((x+dx,y))
        dy = 1
        while y+dy<=7 and M[x][y+dy]=='0' :
            C.append((x,y+dy))
            dy += 1
        if y+dy<=7 and len(M[x][y+dy])==2 : C.append((x,y+dy))
        dy =- 1
        while y+dy>=0 and M[x][y+dy]=='0' :
            C.append((x,y+dy))
            dy -= 1
        if y+dy>=0 and len(M[x][y+dy])==2 : C.append((x,y+dy))
        for sens_x in range (-1,2,2) :
            for sens_y in range (-1,2,2) :
                dx,dy=sens_x,sens_y
                while x+dx>=0 and x+dx<=7 and y+dy>=0 and y+dy<=7 and M[x+dx][y+dy]=='0' :
                    C.append((x+dx,y+dy))
                    if dx>0 : dx += 1
                    else : dx -= 1
                    if dy>0 : dy += 1
                    else : dy -= 1
                if x+dx>=0 and x+dx<=7 and y+dy>=0 and y+dy<=7 and len(M[x+dx][y+dy])==2 :
                    C.append((x+dx,y+dy))
    if p=='K' :
        for dx in range (-1,2) :
            for dy in range (-1,2) :
                if x+dx>=0 and x+dx<=7 and y+dy>=0 and y+dy<=7 and (M[x+dx][y+dy]=='0' or len(M[x+dx][y+dy])==2) :
                    C.append((x+dx,y+dy))
        # roque
        if check and not is_checked(M,player):
            if M[6][0]=='0' and M[5][0]=='0' and M[4][0]=='K' and M[7][0]=='R' and LR1 :
                C.append('LR1')
            if M[1][0]=='0' and M[2][0]=='0' and M[3][0]=='0' and M[4][0]=='K' and M[0][0]=='R' and BR1:
                C.append('BR1')
    if p=='P2' :
        if y>0 and M[x][y-1]=='0' :
            C.append((x,y-1))
            if y==6 and M[x][y-2]=='0' :
                C.append((x,y-2))
        if x<dim-1 and y<dim-1 and M[x+1][y-1]!='0' and len(M[x+1][y-1])==1 :
            C.append((x+1,y-1))
        if x>0 and y<dim-1 and M[x-1][y-1]!='0' and len(M[x-1][y-1])==1 :
            C.append((x-1,y-1))
    if p=='R2' :
        dx = 1
        while x+dx<=7 and M[x+dx][y]=='0' :
            C.append((x+dx,y))
            dx += 1
        if  x+dx<=7 and len(M[x+dx][y])==1 : C.append((x+dx,y))
        dx =- 1
        while x+dx>=0 and M[x+dx][y]=='0' :
            C.append((x+dx,y))
            dx -= 1
        if x+dx>=0 and len(M[x+dx][y])==1 : C.append((x+dx,y))
        dy = 1
        while y+dy<=7 and M[x][y+dy]=='0' :
            C.append((x,y+dy))
            dy += 1
        if y+dy<=7 and len(M[x][y+dy])==1 : C.append((x,y+dy))
        dy =- 1
        while y+dy>=0 and M[x][y+dy]=='0' :
            C.append((x,y+dy))
            dy -= 1
        if y+dy>=0 and len(M[x][y+dy])==1 : C.append((x,y+dy))
    if p=='N2' :
        for dx in range (-2,3) :
            if dx!=0 :
                if dx%2==0 :
                    for dy in range (-1,2,2) :
                        if x+dx>=0 and x+dx<=7 and y+dy>=0 and y+dy<=7 :
                            if (M[x+dx][y+dy]=='0' or len(M[x+dx][y+dy])==1) :
                                C.append((x+dx,y+dy))
                else :
                    for dy in range (-2,3,4) :
                        if x+dx>=0 and x+dx<=7 and y+dy>=0 and y+dy<=7 :
                            if (M[x+dx][y+dy]=='0' or len(M[x+dx][y+dy])==1) :
                                C.append((x+dx,y+dy))
    if p=='B2' :
        for sens_x in range (-1,2,2) :
            for sens_y in range (-1,2,2) :
                dx,dy=sens_x,sens_y
                while x+dx>=0 and x+dx<=7 and y+dy>=0 and y+dy<=7 and M[x+dx][y+dy]=='0' :
                    C.append((x+dx,y+dy))
                    if dx>0 : dx += 1
                    else : dx -= 1
                    if dy>0 : dy += 1
                    else : dy -= 1
                if x+dx>=0 and x+dx<=7 and y+dy>=0 and y+dy<=7 and len(M[x+dx][y+dy])==1 :
                    C.append((x+dx,y+dy))
    if p=='Q2' :
        dx = 1
        while x+dx<=7 and M[x+dx][y]=='0' :
            C.append((x+dx,y))
            dx += 1
        if  x+dx<=7 and len(M[x+dx][y])==1 : C.append((x+dx,y))
        dx =- 1
        while x+dx>=0 and M[x+dx][y]=='0' :
            C.append((x+dx,y))
            dx -= 1
        if x+dx>=0 and len(M[x+dx][y])==1 : C.append((x+dx,y))
        dy = 1
        while y+dy<=7 and M[x][y+dy]=='0' :
            C.append((x,y+dy))
            dy += 1
        if y+dy<=7 and len(M[x][y+dy])==1 : C.append((x,y+dy))
        dy =- 1
        while y+dy>=0 and M[x][y+dy]=='0' :
            C.append((x,y+dy))
            dy -= 1
        if y+dy>=0 and len(M[x][y+dy])==1 : C.append((x,y+dy))
        for sens_x in range (-1,2,2) :
            for sens_y in range (-1,2,2) :
                dx,dy=sens_x,sens_y
                while x+dx>=0 and x+dx<=7 and y+dy>=0 and y+dy<=7 and M[x+dx][y+dy]=='0' :
                    C.append((x+dx,y+dy))
                    if dx>0 : dx += 1
                    else : dx -= 1
                    if dy>0 : dy += 1
                    else : dy -= 1
                if x+dx>=0 and x+dx<=7 and y+dy>=0 and y+dy<=7 and len(M[x+dx][y+dy])==1 :
                    C.append((x+dx,y+dy))
    if p=='K2' :
        for dx in range (-1,2) :
            for dy in range (-1,2) :
                if x+dx>=0 and x+dx<=7 and y+dy>=0 and y+dy<=7 and (M[x+dx][y+dy]=='0' or len(M[x+dx][y+dy])==1) :
                    C.append((x+dx,y+dy))
        # roque
        if check and not is_checked(M,player):
                if M[6][7]=='0' and M[5][7]=='0' and M[4][7]=='K2' and M[7][7]=='R2' and LR2:
                    C.append('LR2')
                if M[1][7]=='0' and M[2][7]=='0' and M[3][7]=='0' and M[4][7]=='K2' and M[0][7]=='R2' and BR2:
                    C.append('BR2')
    if check:
        R = []
        for i in range (len(C)):
            if not is_checked(play_move(M.copy(),((x,y),C[i])),player):
                R.append(C[i])
        return R
    return C

# Evaluation de la situation de la matrice en paramètre
def eval_score(N):
    score = 0
    coef = 0.2
    for x in range(dim):
        for y in range(dim):
            p = N[x][y]
            if p!='0':
                if len(p)==1:
                    score += Values[p]+(Table[p][dim-y-1][x]*coef)
                elif len(p)==2:
                    score += Values[p]+(Table[p[0]][y][x]*coef)
    return score

# Renvoie la matrice avec le coup en paramètre appliqué
def play_move(N,move):
    # 4 roques:
    if len(move[1])!=2:
        if move[1]=='BR1':
            N[2][0] = 'K'
            N[3][0] = 'R'
            N[0][0],N[4][0] = '0','0'
        elif move[1]=='LR1':
            N[6][0] = 'K'
            N[5][0] = 'R'
            N[7][0],N[4][0] = '0','0'
        elif move[1]=='BR2':
            N[2][7] = 'K2'
            N[3][7] = 'R2'
            N[0][7],N[4][7] = '0','0'
        elif move[1]=='LR2':
            N[6][7] = 'K2'
            N[5][7] = 'R2'
            N[7][7],N[4][7] = '0','0'
    else:
        x1,y1,x2,y2 = move[0][0],move[0][1],move[1][0],move[1][1]
        try:   
            N[x2][y2] = N[x1][y1]
        except:
            print('error',move)
        N[x1][y1] = '0'
        # promotion
        if N[x2][y2]=='P' and y2==7:
            N[x2][y2] = 'Q'
        if N[x2][y2]=='P2' and y2==0:
            N[x2][y2] = 'Q2'
    return N

# IA (algo min-max avec récursivité)
def IA(N,t,prof):
    global prof_max
    if prof==prof_max:
        return eval_score(N)
    else:
        global lenghts
        best_score = None
        best_move = []
        for x in range (dim):
            for y in range (dim):
                if N[x][y]!='0' and len(N[x][y])==lenghts[t%2]:
                    if prof<=1:
                        m = moves(N,x,y) 
                    else:
                        m = moves(N,x,y,False)
                    for i in m:
                        score = IA(play_move(N.copy(),((x,y),i)),t+1,prof+1)
                        if not(score is None) and (best_score is None or (prof%2==0 and score>best_score) or (prof%2==1 and score<best_score)):
                            best_score = score
                            best_move = ((x,y),i)
    if best_move==[] and is_checked(N,t%2):
        if prof==0:
            return []
        else:
            return 999*((prof%2)-0.5)
    if prof==0:
        return best_move
    else:
        return best_score

def is_checked(M,player):
    if player==1 :
        king = 'K'
        opp = 2
    else :
        king = 'K2'
        opp = 1
    for x in range (len(M)):
        for y in range (len(M[0])):
            if len(M[x][y])==opp:
                for m in moves(M,x,y,False):
                    if M[m[0]][m[1]]==king:
                        return True
    return False

def glide(move_object,dx,dy):
    frames = 5
    delay = 0.001
    for i in range (frames):
        canvas.move(move_object,dx/frames,dy/frames)
        tk.update()
        time.sleep(delay)

# Gestion de déplacement des pièces
def press(event):
    if is_playing:
        global mouse_x
        global mouse_y
        global move_object
        global start_pos
        global Ind
        global t
        global lenghts
        mouse_x = event.x
        mouse_y = event.y
        x = floor(event.x/size)
        y = floor(event.y/size)
        if not Pieces[x][y] is None and len(M[x][y])==lenghts[t%2]:
            move_object = Pieces[x][y]
            start_pos = (x,y)
            canvas.move(move_object,event.x-(x*size+size/2),event.y-(y*size+size/2))
            C = moves(M,x,y)
            Ind = []
            for c in C:
                if len(c)==2:
                    x,y = c[0],c[1] 
                else:
                    if c=='BR2':
                        x,y = 2,7
                    if c=='LR2':
                        x,y = 6,7
                Ind.append(canvas.create_oval(x*size+size/2-25,y*size+size/2-25,x*size+size/2+25,y*size+size/2+25,width=0,fill='grey'))
            canvas.tag_raise(move_object)

def release(event):
    global move_object
    global Ind
    global is_playing
    global BR1
    global LR1
    global BR2
    global LR2
    if not move_object is None and is_playing:
        is_playing = False
        x = floor(event.x/size)
        y = floor(event.y/size)
        C = moves(M,start_pos[0],start_pos[1])
        for i in Ind:
            canvas.delete(i)
        Ind = []
        if not(x==start_pos[0] and y==start_pos[1]) and (x,y) in C or (x,y)==(6,7) and 'LR2' in C or (x,y)==(2,7) and 'BR2' in C:
            global t
            if (x,y)==(6,7) and 'LR2' in C:
                canvas.move(move_object,(6*size+size/2)-event.x,(7*size+size/2)-event.y)
                glide(Pieces[7][7],-2*size,0)
                Pieces[6][7] = move_object
                Pieces[5][7] = Pieces[7][7]
                Pieces[4][7], Pieces[7][7] = None, None
                M[6][7] = 'K2'
                M[5][7] = 'R2'
                M[7][7],M[4][7] = '0','0'
            elif (x,y)==(2,7) and 'BR2' in C:
                canvas.move(move_object,(2*size+size/2)-event.x,(7*size+size/2)-event.y)
                glide(Pieces[0][7],3*size,0)
                Pieces[2][7] = move_object
                Pieces[3][7] = Pieces[0][7]
                Pieces[0][7], Pieces[4][7] = None, None
                M[3][7] = 'R2'
                M[2][7] = 'K2'
                M[0][7],M[4][7] = '0','0'
            else:
                canvas.move(move_object,(x*size+size/2)-event.x,(y*size+size/2)-event.y)
                if not Pieces[x][y] is None:
                    canvas.delete(Pieces[x][y])
                Pieces[x][y] = move_object
                Pieces[start_pos[0]][start_pos[1]] = None
                M[x][y] = M[start_pos[0]][start_pos[1]]
                M[start_pos[0]][start_pos[1]] = '0'
                # promotion
                if M[x][y]=='P2' and y==0:
                    M[x][y] = 'Q2'
                    Imgs.append(tkinter.PhotoImage(file='Ressources/'+colors[(t+1)%2]+'Q.png'))
                    canvas.itemconfig(Pieces[x][y],image=Imgs[-1])
                    tk.update()
            # roque
            if M[x][y]=='K':
                LR2, BR2 = False, False
            if M[0][7]=='0':
                BR2 = False
            if M[7][7]=='0':
                LR2 = False
            t += 1
            # application du mouvement dans la matrice
            if game[t%2]=='IA':
                for i in Ind:
                    canvas.delete(i)
                    Ind = []
                tk.update()
                play = IA(M.copy(),t,0)
                if len(play)==0:
                    is_playing = False
                    print('Victoire des',colorsNames[colors[t%2]])
                    return
                elif len(play[1])!=2:
                    if play[1]=='LR1':
                        glide(Pieces[4][0],2*size,0)
                        glide(Pieces[7][0],-2*size,0)
                        Pieces[6][0] = Pieces[4][0]
                        Pieces[5][0] = Pieces[7][0]
                        Pieces[4][0], Pieces[7][0] = None, None
                        M[6][0] = 'K'
                        M[5][0] = 'R'
                        M[7][0],M[4][0] = '0','0'
                    if play[1]=='BR1':
                        glide(Pieces[4][0],-2*size,0)
                        glide(Pieces[0][0],3*size,0)
                        Pieces[2][0] = Pieces[4][0]
                        Pieces[3][0] = Pieces[0][0]
                        Pieces[0][0], Pieces[4][0] = None, None
                        M[2][0] = 'K'
                        M[3][0] = 'R'
                        M[0][0],M[4][0] = '0','0'
                else:
                    x1,y1,x2,y2 = play[0][0],play[0][1],play[1][0],play[1][1]
                    canvas.tag_raise(Pieces[x1][y1])
                    glide(Pieces[x1][y1],(x2-x1)*size,(y2-y1)*size)
                    if not Pieces[x2][y2] is None:
                        canvas.delete(Pieces[x2][y2])
                    Pieces[x2][y2] = Pieces[x1][y1]
                    Pieces[x1][y1] = None
                    M[x2][y2] = M[x1][y1]
                    M[x1][y1] = '0'
                    # roque
                    if M[x2][y2]=='K':
                        BR1, LR1 = False, False
                    if M[0][0]=='0':
                        BR1 = False
                    if M[7][0]=='0':
                        LR1 = False
                    # promotion : actualisation de l'affichage pour la reine
                    if M[x2][y2]=='P' and y2==7:
                        M[x2][y2] = 'Q'
                        Imgs.append(tkinter.PhotoImage(file='Ressources/'+colors[(t+1)%2]+'Q.png'))
                        canvas.itemconfig(Pieces[x2][y2],image=Imgs[-1])
                        tk.update()
                t += 1
        elif not (x,y) in C:
            canvas.move(move_object,(start_pos[0]*size+size/2)-event.x,(start_pos[1]*size+size/2)-event.y)
        move_object = None
        checkmate = True
        for x in range (dim):
            for y in range(dim):
                if M[x][y]!='0' and len(M[x][y])==lenghts[t%2]:
                    if len(moves(M,x,y))!=0:
                        checkmate = False
        if checkmate:
            if is_checked(M,t%2):
                print('Victoire des', colorsNames[colors[t%2]])
                return
            else:
                print('Egalité par pat')
                return
        is_playing = True

def move(event):
    if not(move_object is None) and is_playing:
        global mouse_x
        global mouse_y
        canvas.move(move_object,event.x-mouse_x,event.y-mouse_y)
        mouse_x,mouse_y = event.x,event.y

# Variables et paramètres
M = []
Imgs = []
Pieces = []
dim = 8
size = 125
mouse_x,mouse_y = 0,0
start_pos = (0,0)
move_object = 0
Ind = []
game = ('player','IA')
lenghts = (2,1)
t = 0
is_playing = True
# Valeurs des pièces
Values = {'0':0,'P':10,'N':30,'B':30,'R':50,'Q':90,'K':900,'P2':-10,'N2':-30,'B2':-30,'R2':-50,'Q2':-90,'K2':-900}
# Valeurs des placements des pièces sur l'échiquier
Table = {'P':[[0,  0,  0,  0,  0,  0,  0,  0],
              [50, 50, 50, 50, 50, 50, 50, 50],
              [10, 10, 20, 30, 30, 20, 10, 10],
              [5,  5, 10, 25, 25, 10,  5,  5],
              [0,  0,  0, 20, 20,  0,  0,  0],
              [5, -5,-10,  0,  0,-10, -5,  5],
              [5, 10, 10,-20,-20, 10, 10,  5],
              [0,  0,  0,  0,  0,  0,  0,  0]],
         'N':[[-50,-40,-30,-30,-30,-30,-40,-50],
              [-40,-20,  0,  0,  0,  0,-20,-40],
              [-30,  0, 10, 15, 15, 10,  0,-30],
              [-30,  5, 15, 20, 20, 15,  5,-30],
              [-30,  0, 15, 20, 20, 15,  0,-30],
              [-30,  5, 10, 15, 15, 10,  5,-30],
              [-40,-20,  0,  5,  5,  0,-20,-40],
              [-50,-40,-30,-30,-30,-30,-40,-50]],
         'B':[[-20,-10,-10,-10,-10,-10,-10,-20],
              [-10,  0,  0,  0,  0,  0,  0,-10],
              [-10,  0,  5, 10, 10,  5,  0,-10],
              [-10,  5,  5, 10, 10,  5,  5,-10],
              [-10,  0, 10, 10, 10, 10,  0,-10],
              [-10, 10, 10, 10, 10, 10, 10,-10],
              [-10,  5,  0,  0,  0,  0,  5,-10],
              [-20,-10,-10,-10,-10,-10,-10,-20]],
         'R':[[ 0,  0,  0,  0,  0,  0,  0,  0],
              [ 5, 10, 10, 10, 10, 10, 10,  5],
              [-5,  0,  0,  0,  0,  0,  0, -5],
              [-5,  0,  0,  0,  0,  0,  0, -5],
              [-5,  0,  0,  0,  0,  0,  0, -5],
              [-5,  0,  0,  0,  0,  0,  0, -5],
              [-5,  0,  0,  0,  0,  0,  0, -5],
              [ 0,  0,  0,  5,  5,  0,  0,  0]],
         'Q':[[-20,-10,-10, -5, -5,-10,-10,-20],
              [-10,  0,  0,  0,  0,  0,  0,-10],
              [-10,  0,  5,  5,  5,  5,  0,-10],
              [ -5,  0,  5,  5,  5,  5,  0, -5],
              [  0,  0,  5,  5,  5,  5,  0, -5],
              [-10,  5,  5,  5,  5,  5,  0,-10],
              [-10,  0,  5,  0,  0,  0,  0,-10],
              [-20,-10,-10, -5, -5,-10,-10,-20]],
         'K':[[-30,-40,100,-50,-50,-40,100,-30],
              [-30,-40,-40,-50,-50,-40,-40,-30],
              [-30,-40,-40,-50,-50,-40,-40,-30],
              [-30,-40,-40,-50,-50,-40,-40,-30],
              [-20,-30,-30,-40,-40,-30,-30,-20],
              [-10,-20,-20,-20,-20,-20,-20,-10],
              [20, 20,  0,  0,  0,  0, 20, 20],
              [20, 30, 10,  0,  0, 10, 30, 20]]}
prof_max = 3
colors = ['B','W']
colorsNames = {'B':'noirs','W':'blancs'}

# Roque
BR1, LR1 = True, True
BR2, LR2 = True, True

# Interface
tk = tkinter.Tk()
tk.title('Alphamind')
try:
    tk.iconbitmap('assets/icone.ico')
except:
    pass
piecesSet = 'neo' # neo / light
canvas = tkinter.Canvas(tk,width=dim*size,height=dim*size)
canvas.pack()
img = ImageTk.PhotoImage(Image.open('assets/board.png').resize((dim*size,dim*size)))
board = canvas.create_image(0,0,image=img,anchor='nw')
gameSet(colors[0],colors[1])
tk.update()

# Binds des touches
canvas.bind_all('<B1-Motion>',move)
canvas.bind_all('<Button-1>',press)
canvas.bind_all('<ButtonRelease-1>',release)

canvas.mainloop()