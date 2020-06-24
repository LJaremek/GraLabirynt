### Author: ŁJ
### Date: 04.02.2020

from win32api import GetSystemMetrics
from copy import deepcopy
import pygame as PG

import labirynt as Game


dirt_gif = PG.image.load("Graphics/dirt_30.gif")
wall_gif = PG.image.load("Graphics/wall_30.gif")
player_gif = PG.image.load("Graphics/player_30.gif")
hole_gif = PG.image.load("Graphics/hole_30.gif")
nothing_gif = PG.image.load("Graphics/nothing_30.gif")
menu_gif = PG.image.load("Graphics/menu_01.gif")
menu_gif_height = menu_gif.get_height()
menu_gif_width = menu_gif.get_width()



dimension = 40#35

dirt_gif = PG.transform.scale(dirt_gif, (dimension, dimension))
wall_gif = PG.transform.scale(wall_gif, (dimension, dimension))
player_gif = PG.transform.scale(player_gif, (dimension, dimension))
hole_gif = PG.transform.scale(hole_gif, (dimension, dimension))
nothing_gif = PG.transform.scale(nothing_gif, (dimension, dimension))

black_colour = (0,   0,   0)
red_colour   = (255, 0,   0)
green_colour = (0,   255, 0)
white_colour = (255, 255, 255)


history = False
view = False

PG.init()
screen = PG.display.set_mode((11*dimension, 11*dimension+50))
screen.fill((100, 100, 100))

test_01 = PG.image.load("Graphics/menu_02.gif")
lewy = test_01.subsurface((0, 0, 125, 490))
srodek = test_01.subsurface((125, 0, 190, 490))
prawy = test_01.subsurface((125+190, 0, 125, 490))

def move(screen): # Chyba nigdzie tego nie uzywam xD mam taka funkcje w pliku labirynt.py (GAME.)
    key = PG.key.get_pressed()
    if key[PG.K_w] or key[PG.K_UP]:
        return "N"
    elif key[PG.K_d] or key[PG.K_RIGHT]:
        return "E"
    elif key[PG.K_s] or key[PG.K_DOWN]:
        return "W"
    elif key[PG.K_a] or key[PG.K_LEFT]:
        return "S"
    return None
Mmax = int((GetSystemMetrics(1)-100)//dimension-1)
if Mmax%2 == 0:
    Mmax -= 1
Nmax = int((GetSystemMetrics(0)-50)//dimension)
if Nmax%2 == 0:
    Nmax -= 1
mode = "menu"
Px = 0
Py = 1

font =  PG.font.SysFont("comicsansms", 19)
font1 = PG.font.SysFont("comicsansms", 24)
font2 = PG.font.SysFont("comicsansms", 30)

menu_info_1 = font1.render("START", True, white_colour)
menu_info_1_colour = red_colour
menu_info_2 = font1.render("SETTINGS", True, white_colour)
menu_info_2_colour = red_colour
menu_info_3 = font1.render("EXIT", True, white_colour)
menu_info_3_colour = red_colour

game_reset = font2.render("R", True, (0, 0, 0))
game_reset_colour = red_colour
game_exit  = font2.render("E", True, (0, 0, 0))
game_exit_colour = red_colour

set_enter_colour = red_colour

def button_start():
    m = 11
    n = 11
    world = Game.create_world(m, n, 1)
    world[0][1] = 2

    lvl_counter = 1
    steps_counter = 0
    mode = "game"
    lvl_info = font.render("LVL: "+str(lvl_counter), True, (0, 0, 0))
    return world, mode, lvl_counter, steps_counter, m, n, lvl_info

def button_menu(number_mode):
    world = number_mode
    mode = "menu"
    return world, mode

def button_end():
    game_end_1 = font2.render("Game Over", True, white_colour)
    game_end_2 = font2.render("Levels: " + str(lvl_counter), True, white_colour)
    game_end_3 = font2.render("Steps: " + str(steps_counter), True, white_colour)
    game_end_y = font2.render("Menu", True, white_colour)
    game_end_n = font2.render("Exit", True, white_colour)
    mode = "end"
    return mode, game_end_1, game_end_2, game_end_3, game_end_y, game_end_n

def button_settings():
    set_history = font1.render("[S] - save steps", True, (0, 0, 0))
    set_view = font1.render("[V] - limited view", True, (0, 0, 0))
    set_save1 = font1.render("[ENTER]", True, (0, 0, 0))
    set_save2 = font1.render("save and back", True, (0, 0, 0))
    return "settings", set_history, set_view, set_save1, set_save2
    
running = True # Czy gra ma byc wlaczona?
world, mode = button_menu(1)
button = None
clock = PG.time.Clock()
while running:
    #print(PG.display.get_surface().get_size())
    for event in PG.event.get():
        if event.type == PG.KEYDOWN:
            if event.key == PG.K_r and mode == "game":                ### G A M E ###
                if game_reset_colour == red_colour:
                    game_reset_colour = green_colour
                    game_exit_colour = red_colour
                else:
                    game_reset_colour = red_colour
                    world = deepcopy(world_save)
            elif event.key == PG.K_e and mode == "game":
                if game_exit_colour == red_colour:
                    game_exit_colour = green_colour
                    game_reset_colour = red_colour
                else:
                    game_exit_colour = red_colour
                    mode, game_end_1, game_end_2, game_end_3, game_end_y, game_end_n = button_end()
                    game_end_y_colour = red_colour
                    game_end_n_colour = red_colour
                    world = 1
            if mode == "game" and event.key in (PG.K_w, PG.K_UP, PG.K_d, PG.K_RIGHT, PG.K_s, PG.K_DOWN, PG.K_a, PG.K_LEFT): # Resetowanie koloru R i E po ruszeniu sie
                    game_reset_colour  = red_colour
                    game_exit_colour = red_colour

            elif event.key == 13 and mode == "end":                 ### E N D ###
                if world == 1:
                    world, mode = button_menu(1)
                    event.key = PG.K_a  # Zmiana wcisnietego klawisza z enter na inny, zeby wcisniecie nie przechodzilo do menu
                elif world == 2:
                    running = False

            elif (event.key == PG.K_a or event.key == PG.K_d) and mode == "end":    # Sprawdzanie, czy wciśnięto "a" lub "d" i mode == "end"
                game_end_y_colour = red_colour
                game_end_n_colour = red_colour
                
            if event.key == 13 and mode == "menu": # 13=enter       ### M E N U ###
                if world == 1:
                    world, mode, lvl_counter, steps_counter, m, n, lvl_info = button_start()
                    world_save = deepcopy(world)
                if world == 2:
                    mode, set_history, set_view, set_save1, set_save2 = button_settings()
                    event.key = PG.K_a # Zmiana wcisnietego klawisza dla bezpieczenstwa
                if world == 3:
                    running = False
            
            if event.key == 13 and mode == "settings":              ### S E T T I N G S ###
                world, mode = button_menu(2)
            if event.key == PG.K_s and mode == "settings": # Jesli wcisnieto "s" - save steps
                if history == True:
                    history = False
                else:
                    history = True
            elif event.key == PG.K_v and mode == "settings": # Jesli wcisnieto "v" - view
                if view == True:
                    view = False
                else:
                    view = True
                    
            if event.key == PG.K_w or event.key == PG.K_UP:                 # Sprawdzanie, czy wciśnięto "w"
                button = "N"
            elif event.key == PG.K_d or event.key == PG.K_RIGHT:               # Sprawdzanie, czy wciśnięto "d"
                button = "E"
            elif event.key == PG.K_s or event.key == PG.K_DOWN:               # Sprawdzanie, czy wciśnięto "s"
                button = "W"
            elif event.key == PG.K_a or event.key == PG.K_LEFT:               # Sprawdzanie, czy wciśnięto "a"
                button = "S"
        if event.type == PG.KEYUP:
            if event.key in (PG.K_w, PG.K_d, PG.K_s, PG.K_a, PG.K_UP, PG.K_RIGHT, PG.K_LEFT, PG.K_DOWN):
                button = None
    if button != None:
        world, if_move = Game.move(world, button, history, mode)

                
        if if_move == True:
            steps_counter += 1
        elif event.type == PG.QUIT:
            exit()


    screen.fill((100, 100, 100))
    if mode == "game":                      ########## GAME ##########
        for i in range(len(world)):
            for j in range(len(world[0])):
                if world[i][j] == 2:
                    Player_x = i
                    Player_y = j
        steps_info = font.render("Steps: " + str(steps_counter), True, (0, 0, 0))
        for i in range(len(world)):
            for j in range(len(world[0])):
                if view and int(((Player_x - i)**2 + (Player_y-j)**2)**(1/2)) >= 3:
                    screen.blit(nothing_gif, (j*dimension, i*dimension+50))
                else:
                    if world[i][j] == 0:
                        screen.blit(dirt_gif, (j*dimension, i*dimension+50))
                    elif world[i][j] == 1:
                        screen.blit(wall_gif, (j*dimension, i*dimension+50))
                    elif world[i][j] == 2:
                        screen.blit(player_gif, (j*dimension, i*dimension+50))
                    elif world[i][j] == 3:
                        screen.blit(hole_gif, (j*dimension, i*dimension+50))
        screen.blit(lvl_info, ((- lvl_info.get_width() + dimension*len(world[0]))//2, 0))
        screen.blit(steps_info, ((- steps_info.get_width() + dimension*len(world[0]))//2, 23))

        rect_Reset = PG.Rect(0, 0, 50, 50)
        PG.draw.rect(screen, game_reset_colour, rect_Reset)
        screen.blit(game_reset, ((50 - game_reset.get_width())//2, (50 - game_reset.get_height())//2))
        
        rect_Exit = PG.Rect(dimension*len(world[0]) - 50, 0, 50, 50)
        PG.draw.rect(screen, game_exit_colour, rect_Exit)
        screen.blit(game_exit, ((dimension*len(world[0]) -(50 + game_exit.get_width())//2), (50 - game_exit.get_height())//2))
        
        PG.display.flip()
        if world[-1][-2] == 2: # Co jesli dojdzie gracz do końca?
            m += 2
            n += 2
            lvl_counter += 1
            lvl_info = font.render("LVL: "+str(lvl_counter), True, (0,0,0))
            if n > Nmax:
                n = Nmax
            if m > Mmax:
                m = Mmax
            world = Game.create_world(m, n, 1)
            world[0][1] = 2
            world_save = deepcopy(world)
            Px = 0
            Py = 1
            screen = PG.display.set_mode((dimension*len(world[0]),dimension*len(world)+50))
            
    elif mode == "menu":
        PG.display.set_mode(size = (11*dimension, 11*dimension+50))
        screen.blit(menu_gif, (0, 0))
        if world == 1: #1047.7 1428.4
            screen.blit(srodek, ((125,0)))#8 + int(1428.4/menu_start_y_ratio)))
        elif world == 2:
            screen.blit(lewy, (0, 0,))
        elif world == 3:
            screen.blit(prawy, (125+190, 0))
        PG.display.flip()

    elif mode == "end":
        game_end_2 = font2.render("Levels: " + str(lvl_counter), True, white_colour)
        game_end_3 = font2.render("Steps: " + str(steps_counter), True, white_colour)
        PG.display.set_mode(size = (11*dimension, 11*dimension+50))
        if world == 1:
            rect1 = PG.Rect(0, (11*dimension+50)*(7/10), (11*dimension+50)*(4/10)+1, (11*dimension+50)*(2/10))
            PG.draw.rect(screen, game_end_y_colour, rect1)
        elif world == 2:
            rect2 = PG.Rect((11*dimension+50)*(4/10)+3, (11*dimension+50)*(7/10), (11*dimension+50)*(5/10)+1, (11*dimension+50)*(2/10))
            PG.draw.rect(screen, game_end_n_colour, rect2)
        
        screen.blit(game_end_1, ((11*dimension - game_end_1.get_width())//2, ( (11*dimension+50)*(1/10) - game_end_1.get_height()//2)))
        screen.blit(game_end_2, ((11*dimension - game_end_2.get_width())//2, ( (11*dimension+50)*(3/10) - game_end_2.get_height()//2)))
        screen.blit(game_end_3, ((11*dimension - game_end_3.get_width())//2, ((11*dimension+50)*(5/10) - game_end_3.get_height()//2)))
        screen.blit(game_end_y, ((11*dimension//2 - game_end_y.get_width())//2, ((11*dimension+50)*(8/10) - game_end_y.get_height()//2)))
        screen.blit(game_end_n, ((16.5*dimension - game_end_n.get_width())//2, ((11*dimension+50)*(8/10) - game_end_n.get_height()//2)))
        PG.display.flip()

    elif mode == "settings":
        rect1 = PG.Rect(0, 0, 11*dimension, (11*dimension+50)//3-1)
        if history == True:
            PG.draw.rect(screen, green_colour, rect1)
        else:
            PG.draw.rect(screen, red_colour, rect1)
        rect2 = PG.Rect(0, (11*dimension+50)//3+1, 11*dimension, (11*dimension+50)//3-1)
        if view == True:
            PG.draw.rect(screen, green_colour, rect2)
        else:
            PG.draw.rect(screen, red_colour, rect2)
        rect3 = PG.Rect(0, (11*dimension+50)*(2/3)+1, 11*dimension, (11*dimension+50)//3-1)
        PG.draw.rect(screen, set_enter_colour, rect3)
        screen.blit(set_history, (11*dimension//2 - set_history.get_width()//2, (11*dimension+50)*(3/18) - set_history.get_height()//2))
        screen.blit(set_view, (11*dimension//2 - set_view.get_width()//2, (11*dimension+50)*(9/18) - set_view.get_height()//2))
        screen.blit(set_save1, (11*dimension//2 - set_save1.get_width()//2, (11*dimension+50)*(13/18)))
        screen.blit(set_save2, (11*dimension//2 - set_save2.get_width()//2, (11*dimension+50)*(15/18)))
        PG.display.flip()
    clock.tick(10)
PG.quit()
