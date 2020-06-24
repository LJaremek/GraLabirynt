# KLUCZ WINDOWS
# wmic path SoftwareLicensingService get OA3xOriginalProductKey
# powershell "(Get-WmiObject -query ‘select * from SoftwareLicensingService’).OA3xOriginalProductKey"

### Author: ŁJ
### Date: 02.02.2020

from random import randint
from time import sleep
from copy import deepcopy

# # # CREATING CLEAR MAP # # #

def create_empty_map(rows, columns, sb_walls):
    rows, columns = columns, rows
    mapa = [[]] # Przy nieparzystym rows powstaie przestrzen na dwie kratki
    for i in range(rows):
        mapa[0].append(1)
    for i in range(1, columns-1):
        row = [1]
        for i in range(1, rows-1):
            row.append(0)
        row.append(1)
        mapa.append(row)
    mapa.append([])
    for i in range(rows):
        mapa[-1].append(1)
    for i in range(sb_walls):
        mapa[0][i + 1] = 0
        mapa[-1][- i - 2] = 0
    return mapa

# # # BUILDING BEARING WALLS # # #

def doors(mapa, sb_walls):
    rows = len(mapa)
    columns = len(mapa[0])
    number_doors = int((rows-2)*0.35)
    doors = []
    last = []
    for column in range(sb_walls + 1, columns-2, sb_walls + 1):
        row = randint(1, 3)
        actual = []
        while row <= rows-2:
            if row not in last:
                doors.append([row, column])
                actual.append(row)
                row += randint(2,5)
            else:
                row += randint(1,3)
        last = actual
    return doors


def build_bearing_walls(mapa, sb_walls):
    door = doors(mapa, sb_walls)
    rows = len(mapa)
    columns = len(mapa[0])
    for column in range(sb_walls + 1, columns-2, sb_walls + 1):
        for row in range(1, rows):
            if [row, column] not in door:
                mapa[row][column] = 1
            else:
                mapa[row][column] = 0
    return mapa

# # # BUILDING PARITION WALLS # # #

def flood_fill(mapa, x, y, Ax, Ay, sb_walls):
    points = 0
    i,j = 0, 1
    save = deepcopy(mapa)
    stos = [(x, y)]
    for m in range(sb_walls):
        if (i,j) == (0,1):
            save[-1][-2-m] = 1
        else:
            save[0][1+m] = 1
    while len(stos) > 0:
        x, y = stos.pop()
        if save[x][y] == 0:
            save[x][y] = "x"
            stos.append((x+1, y))
            stos.append((x-1, y))
            stos.append((x, y+1))
            stos.append((x, y-1))
        if save[i][j] == "x":
            points += 1
            break
    i, j = -1, -2
    save = deepcopy(mapa)
    stos = [(Ax, Ay)]
    for m in range(sb_walls):
        if (i,j) == (0,1):
            save[-1][-2-m] = 1
        else:
            save[0][1+m] = 1
    while len(stos) > 0:
        x, y = stos.pop()
        if save[x][y] == 0:
            save[x][y] = "x"
            stos.append((x+1, y))
            stos.append((x-1, y))
            stos.append((x, y+1))
            stos.append((x, y-1))
        if save[i][j] == "x":
            points += 1
            break
    if points == 2:
        return True
    else:
        return False

def from_up(mapa, col_nr, sb_walls):
    free_space = 0
    great_fields = []
    rows = len(mapa)
    changed = 0
    for row in range(1, rows-2):
        if mapa[row][col_nr - 1] == mapa[row][col_nr + sb_walls] == 1 and free_space >= 1:
            great_fields.append((row, col_nr))
            free_space = 0
        else:
            free_space += 1
    for test in great_fields:
        test_map = deepcopy(mapa)
        for i in range(sb_walls):
            test_map[test[0]][test[1] + i] = 1
        if flood_fill(test_map, test[0] + 1, test[1], test[0] + 1, test[1], sb_walls) == True:
            test_map = deepcopy(mapa)
            for i in range(sb_walls):
                test_map[test[0]][test[1] + i] = 1
            if flood_fill(test_map, test[0] - 1, test[1], test[0] - 1, test[1], sb_walls) == True:
                los = randint(1, 10)
                if los > 2:
                    for i in range(sb_walls):
                        mapa[test[0]][test[1] + i] = 1
                    changed += 1
    if changed == 0:
        pass#print(0)
    return mapa

def from_down(mapa, col_nr, sb_walls):
    free_space = 0
    great_fields = []
    rows = len(mapa)
    changed = 0
    for row in range(1, rows-2):
        row = len(mapa) - row
        if mapa[row][col_nr - 1] == mapa[row][col_nr + sb_walls] == 1 and free_space >= 1:
            great_fields.append((row, col_nr))
            free_space = 0
        else:
            free_space += 1
    for test in great_fields:
        test_map = deepcopy(mapa)
        for i in range(sb_walls):
            test_map[test[0]][test[1] + i] = 1
        if flood_fill(test_map, test[0] + 1, test[1], test[0] + 1, test[1], sb_walls) == True:
            test_map = deepcopy(mapa)
            for i in range(sb_walls):
                test_map[test[0]][test[1] + i] = 1
            if flood_fill(test_map, test[0] - 1, test[1], test[0] - 1, test[1], sb_walls) == True:
                los = randint(1, 10)
                if los > 2:
                    for i in range(sb_walls):
                        mapa[test[0]][test[1] + i] = 1
                    changed += 1
##    if changed == 0:
##        print(0)
    return mapa
    

def build_partition_walls(mapa, sb_walls):
    rows = len(mapa)
    columns = len(mapa[0])
    great = []
    for column in range(1, columns, sb_walls + 1):
        fate = randint(0, 1)
        if fate == 0:
            mapa = from_up(mapa, column, sb_walls)
        else:
            mapa = from_down(mapa, column, sb_walls)
    return mapa

def build_partition_walls_old(mapa):
    rows = len(mapa)
    columns = len(mapa[0])
    great = []
    for column in range(1, columns//2 + 1, 2): # do polowy od przodu
        fate = randint(0,1)
        if fate == 0:
            mapa = from_up(mapa, column)
            #print("up")
        else:
            mapa = from_down(mapa, column)
            #print("down")
            
    for row_number in range(1, len(mapa)-1):
        mapa[row_number] = mapa[row_number][::-1]
        
    for column in range(1, columns//2 + 1, 2): # do polowy od tylu
        fate = randint(1,2)
        if fate == 0:
            mapa = from_up(mapa, column)
            #print("up")
        else:
            mapa = from_down(mapa, column)
            #print("down")
    for row_number in range(1, len(mapa)-1):
        mapa[row_number] = mapa[row_number][::-1]
    return mapa

def create_room(mapa):
    rows = len(mapa)
    columns = len(mapa[0])
    if rows > 12 and columns > 12:
        max_room_w = columns//3
        min_room_w = 3
        max_room_h = rows//3
        min_room_h = 3
        while dimension:
            pass

# # # PRINTING MAP # # #

def print_map_simple(mapa):
    for x in mapa:
        x = list(map(lambda y: str(y), x))
        print(" ".join(x))

def print_map(save, sciana, puste, hipek, iks, old):
    for x in save:
        for y in x:
            if y == 1:
                print(sciana, end = " ")
            elif y == 0:
                print(puste, end = " ")
            elif y == 2:
                print(hipek, end = " ")
            elif y == 3:
                print(old, end = " ")
            elif y == "x":
                print(iks, end = " ")
        print()

def move(mapa, direction, history = False, mode = False):
    if mode == "menu":
        if direction == "N":
            if mapa != 1:
                mapa -= 1
            else:
                mapa = 3
        elif direction == "W":
            if mapa != 3:
                mapa += 1
            else:
                mapa = 1
        return mapa, False
    
    elif mode == "end":
        if direction == "E":
            mapa += 1
        elif direction == "S":
            mapa -= 1
        mapa = mapa%2
        if mapa == 0:
            mapa = 2
        return mapa, False

    elif mode == "settings":
        return mapa, False
    
    if history == True:
        history = 3
    else:
        history = 0
    rows = -1
    columns = -1            #  N
    for i in mapa:          # S E
        rows += 1           #  W
        for j in i:
            columns += 1
            if j == 2:
                if direction == "N":
                    if mapa[rows-1][columns] not in (1, 3):
                        mapa[rows][columns] = history
                        mapa[rows-1][columns] = 2
                        return mapa, True
                    else:
                        return mapa, False
                elif direction == "E":
                    if mapa[rows][columns+1] not in (1, 3):
                        mapa[rows][columns] = history
                        mapa[rows][columns+1] = 2
                        return mapa, True
                    else:
                        return mapa, False
                elif direction == "W":
                    if mapa[rows+1][columns] not in (1, 3):
                        mapa[rows][columns] = history
                        mapa[rows+1][columns] = 2
                        return mapa, True
                    else:
                        return mapa, False
                elif direction == "S":
                    if mapa[rows][columns-1] not in (1, 3):
                        mapa[rows][columns] = history
                        mapa[rows][columns+-1] = 2
                        return mapa, True
                    else:
                        return mapa, False
        columns = -1
    return mapa, False


def create_world(m, n, sb_walls):
    mapa = create_empty_map(m,n, sb_walls)
    mapa = build_bearing_walls(mapa, sb_walls)
    mapa = build_partition_walls(mapa, sb_walls)
    return mapa

#print_map(mapa, "#", ".", "@", "x")
#print_map(mapa, "▓", "░", "☺", "x", "#")

##for i in range(27, 29, 2):
##    world = create_empty_map(i,i)
####    print_map(world, "▓", "░", "☺", "x", "#")
####    print()
##    world = build_bearing_walls(world)
####    print_map(world, "▓", "░", "☺", "x", "#")
##    print()
##    world = build_partition_walls(world)
##    print_map(world, "▓", "░", "☺", "x", "#")

##world = create_empty_map(15, 15, 1) # Mapa o wymiarach 15x15 szerokosc miedzy scianami 1
##world = build_bearing_walls(world, 1)
##wolrd = build_parition_walls(world, 1)
###print_map(world, "▓", "░", "☺", "x", "#")
##print()
##world = create_empty_map(34, 34, 2) # Mapa o wymiarach 16x16 szerokosc miedzy scianami 2
##world = build_bearing_walls(world, 2)
##wolrd = build_partition_walls(world, 2)
###print_map(world, "▓", "░", "☺", "x", "#")
##print()
##world = create_empty_map(37, 37, 3) # Mapa o wymiarach 17x17 szerokosc miedzy scianami 3
##world = build_bearing_walls(world, 3)
##wolrd = build_partition_walls(world, 3)
##print_map(world, "▓", "░", "☺", "x", "#")
