from tkinter import *
from random import randint
from time import sleep, time
from math import sqrt

print('''Règles:
Tu as 30 sec. dans le minuteur, si le temps est écoulé, la partie est terminée.
1 Bulle = 32 à 36 points
À chaque 1250 points, tu as 30 sec. de plus.

Commandes:

Arrow up ou W: Haut
Arrow left ou A: Gauche
Arrow down ou S: Bas
Arrow right ou D: Droite

ATTENTION!: Plus la résolution de votre écran est grande,
plus le jeu consomme des ressources.''', '\n')

mode = input('''Quel mode veux-tu ?,
Tape 1 pour le mode: Facile 
Tape 2 pour le mode: Normal
Tape 3 pour le mode: Difficile

> ''')


sleep(0.5)

# init écran
scr = Tk()

width_scr = scr.winfo_screenwidth()
height_scr = scr.winfo_screenheight()

scr.title("Le débullator")
scr.iconbitmap("icon.ico")

c = Canvas(scr, height = height_scr, width = width_scr, bg = 'darkblue')
c.pack()

X_MID = width_scr / 2
Y_MID = height_scr / 2

# init sousmarin
id_submarine_in = c.create_polygon(5, 5, 5, 25, 30, 15, fill='red')
id_submarine_out = c.create_oval(0, 0, 30, 30, outline='red')
r_submarine = 15

speed_submarine = 10

c.move(id_submarine_in, X_MID, Y_MID)
c.move(id_submarine_out, X_MID, Y_MID)

# mouvement sousmarin
def move_submarine(event):
    if event.keysym == 'Up':
        c.move(id_submarine_in, 0, -speed_submarine)
        c.move(id_submarine_out, 0, -speed_submarine)
    elif event.keysym == 'Down':
        c.move(id_submarine_in, 0, speed_submarine)
        c.move(id_submarine_out, 0, speed_submarine)
    elif event.keysym == 'Left':
        c.move(id_submarine_in, -speed_submarine, 0)
        c.move(id_submarine_out, -speed_submarine, 0)
        #c.move(id_submarine_avant, -speed_submarine, 0)
        #c.move(id_submarine_avant2, -speed_submarine, 0)
    elif event.keysym == 'Right':
        c.move(id_submarine_in, speed_submarine, 0)
        c.move(id_submarine_out, speed_submarine, 0)
        #c.move(id_submarine_avant, speed_submarine, 0)
        #c.move(id_submarine_avant2, speed_submarine, 0)
    elif event.keysym == 'w':
        c.move(id_submarine_in, 0, -speed_submarine)
        c.move(id_submarine_out, 0, -speed_submarine)
        #c.move(id_submarine_avant, 0, -speed_submarine)
        #c.move(id_submarine_avant2, 0, -speed_submarine)
    elif event.keysym == 's':
        c.move(id_submarine_in, 0, speed_submarine)
        c.move(id_submarine_out, 0, speed_submarine)
        #c.move(id_submarine_avant, 0, speed_submarine)
        #c.move(id_submarine_avant2, 0, speed_submarine)
    elif event.keysym == 'a':
        c.move(id_submarine_in, -speed_submarine, 0)
        c.move(id_submarine_out, -speed_submarine, 0)
        #c.move(id_submarine_avant, -speed_submarine, 0)
        #c.move(id_submarine_avant2, -speed_submarine, 0)
    elif event.keysym == 'd':
        c.move(id_submarine_in, speed_submarine, 0)
        c.move(id_submarine_out, speed_submarine, 0)
        #c.move(id_submarine_avant, speed_submarine, 0)
        #c.move(id_submarine_avant2, speed_submarine, 0)
        
c.bind_all('<Key>', move_submarine)

id_bubble = list()
r_bubble = list()
speed_bubble = list()
R_MIN_BUBBLE = 10
R_MAX_BUBBLE = 30
SPEED_BUBBLE_MAX = 10
GAP = 100

def create_bubble():
    x = width_scr + GAP
    y = randint(0, height_scr)
    r = randint(R_MIN_BUBBLE, R_MAX_BUBBLE)
    id_1 = c.create_oval(x - r, y - r, x + r, y + r, outline='white')
    id_bubble.append(id_1)
    r_bubble.append(r)
    speed_bubble.append(randint(1, SPEED_BUBBLE_MAX))

def move_bubble():
    for i in range(len(id_bubble)):
        c.move(id_bubble[i], -speed_bubble[i], 0)

def find_coords(num_id):
    pos = c.coords(num_id)
    x = (pos[0] + pos[2]) / 2
    y = (pos[1] + pos[3]) / 2
    return x, y

def delete_bubble(i):
    del r_bubble[i]
    del speed_bubble[i]
    c.delete(id_bubble[i])
    del id_bubble[i]

BUBBLE_COUNTER = 0

def erase_bubble():
    global BUBBLE_COUNTER
    for i in range(len(id_bubble)-1, -1, -1):
        x, y = find_coords(id_bubble[i])
        if x < -GAP:
            delete_bubble(i)
            BUBBLE_COUNTER -= 1
        if y < -100:
            delete_bubble(i)
            BUBBLE_COUNTER -= 1    

def distance(id_1, id_2):
    x1, y1 = find_coords(id_1)
    x2, y2 = find_coords(id_2)
    return sqrt((x2 - x1)**2 + (y2 - y1)**2)

def collision():
    points = 0
    for bubble in range(len(id_bubble)-1, -1, -1):
        if distance(id_submarine_out, id_bubble[bubble]) < (r_submarine + r_bubble[bubble]):
            points += 30
            delete_bubble(bubble)
    return points

c.create_text(100, 30, text='Temps Restant', fill='white')
c.create_text(200, 30, text='Score', fill='white')
text_time = c.create_text(100, 50, fill='white')
text_score = c.create_text(200, 50, fill='white')

def show_score(score):
    c.itemconfig(text_score, text=str(score))
def show_time(time_remain):
    c.itemconfig(text_time, text=str(time_remain))

LUCK_BUBBLE = 3
BUBBLE_LIMIT = 250

if mode == "1":
    LUCK_BUBBLE = 2
    BUBBLE_LIMIT = 300
elif mode == "2":
    LUCK_BUBBLE = 4
    BUBBLE_LIMIT = 225
elif mode == "3":
    LUCK_BUBBLE = 6
    BUBBLE_LIMIT = 125


TIME_LIMIT = 30
SCORE_BONUS = 1250
score = 0
bonus = 0
endgame = time() + TIME_LIMIT 

# MAIN GAME LOOP 
while time() < endgame:
     if randint(1, LUCK_BUBBLE) == 1 and BUBBLE_COUNTER <= BUBBLE_LIMIT:
         create_bubble()
         BUBBLE_COUNTER += 1
     move_bubble()
     erase_bubble()
     score += collision()
     if (int(score/SCORE_BONUS)) > bonus:
         bonus += 1
         endgame += TIME_LIMIT
     show_score(score)
     show_time(int(endgame - time()))
     scr.update()

c.create_text(X_MID, Y_MID - 100, text='Partie Terminée', fill='white', font=('Helvetica', 30))
c.create_text(X_MID, Y_MID - 70, text='Score : ' + str(score), fill='white')
c.create_text(X_MID, Y_MID - 50, text='Temps Bonus Accumulé : ' + str(bonus*TIME_LIMIT), fill='white') 



btn_cls = Button(scr, text = "  Fermer  ", command = scr.destroy, font = ('Helvetica', 10), bg='white')
btn_cls.place(x = X_MID - 30, y = Y_MID - 20)





   
        
    

