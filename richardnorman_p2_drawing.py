import stddraw
import picture
import richardnorman_p2_taffy
from random import randint
import math
import copy 

square = picture.Picture("Taffy Tangle Shapes/Square.png") #0
circle = picture.Picture("Taffy Tangle Shapes/Circle.png") #1
triangle = picture.Picture("Taffy Tangle Shapes/Triangle.png") #2
diamond = picture.Picture("Taffy Tangle Shapes/Diamond.png") #3
pentagon = picture.Picture("Taffy Tangle Shapes/Pentagon.png") #4
parallelogram = picture.Picture("Taffy Tangle Shapes/Parallelogram.png") #5
test = picture.Picture("Taffy Tangle Shapes/None.png")

shapes_array = [square,circle,triangle,diamond,pentagon,parallelogram]

taffy_spacing_horizontal = 0.14285714285
padding_horizontal = 0.075

taffy_spacing_vertical = 0.105
padding_vertical = 0.06

selected_rectangle_offset = 0.0075

stddraw.setCanvasSize(350,450)

board_array = []

first_taffy_connected = False
second_taffy_connected = False

score = 0

def redraw_board():
    stddraw.clear()
    for i in range (9):
        for j in range(7):
            if board_array[i][j] != 6:
                stddraw.picture(shapes_array[board_array[i][j]],padding_horizontal + j*taffy_spacing_horizontal, 1- (padding_vertical + i*taffy_spacing_vertical))

def draw_score():
    stddraw._fontSize = 24
    stddraw.text(0.5,0.015,"Score: " + str(score))

def check_if_valid_swap(first_taffy,second_taffy):
    #first check if adjacent and three after swap
    if ((first_taffy.row == second_taffy.row) and (abs(first_taffy.column - second_taffy.column) == 1)) or ((first_taffy.column == second_taffy.column) and (abs(first_taffy.row - second_taffy.row) == 1)):
        is_three_after_swap = check_if_three_after_swap(first_taffy,second_taffy)
        if is_three_after_swap:
            return True
    return False

def check_if_three_after_fall():
    global score
    three_found = False
    for i in range (9):
        for j in range(7):
            #check row
            if ((1 < j < 6) and (board_array[i][j-1] == board_array[i][j]) and (board_array[i][j-2] == board_array[i][j])):
                three_found = True
                board_array[i][j] = 6
                board_array[i][j-1] = 6
                board_array[i][j-2] = 6
                #check horz + 1
                if (1 < j < 6) and (board_array[i][j+1] == board_array[i][j]):
                    board_array[i][j+1] = 6
                    score += 1
                #check horz - 1
                if (1 < j < 6) and (board_array[i][j-3] == board_array[i][j]):
                    board_array[i][j-3] = 6
                    score += 1
                score += 3
            #check column
            if ((1 < i < 8) and (board_array[i-1][j] == board_array[i][j]) and (board_array[i-2][j] == board_array[i][j])):
                three_found = True
                board_array[i][j] = 6
                board_array[i-1][j] = 6
                board_array[i-2][j] = 6
                #check vert + 1
                if (2 < i < 8) and (board_array[i-3][j] == board_array[i][j]):
                    board_array[i-3][j] = 6
                #check vert - 1
                if (0 < i < 8) and (board_array[i+1][j] == board_array[i][j]):
                    board_array[i+1][j] = 6
                score += 3
    redraw_board()
    draw_score()
    if three_found:
        return True
    else:
        return False

def load_more_taffies():
    shift_taffies_down()
    for j in range(7):
        stddraw.clear()
        redraw_board()
        stddraw.show(100)
        if board_array[0][j] == 6:
            board_array[0][j] = randint(0,5)
        if board_array[1][j] == 6:
            shift_taffies_down()
            load_more_taffies()
    
def shift_taffies_down():
    #any(6 in sublist for sublist in board_array)
    shifting = True
    while shifting:
        for j in range(7):
            if board_array[0][j] == 6:
                shifting = False
                return

        for i in range (9):
            for j in range(7):
                if i < 8:
                    if board_array[i+1][j] == 6:
                        board_array[i+1][j] = board_array[i][j]
                        board_array[i][j] = 6
                        stddraw.clear()
                        redraw_board()
                        stddraw.show(250)

def check_if_three_after_swap(first_taffy,second_taffy):
    global first_taffy_connected
    global second_taffy_connected

    array_after_swap = copy.deepcopy(board_array)

    valid_swap_found = False

    #swap to see if three line exists
    array_after_swap[first_taffy.column][first_taffy.row] = second_taffy.taffy_type
    array_after_swap[second_taffy.column][second_taffy.row] = first_taffy.taffy_type

    #check above and below: 4
    if (0 < second_taffy.column < 8) and (array_after_swap[second_taffy.column+1][second_taffy.row] == first_taffy.taffy_type) and (array_after_swap[second_taffy.column-1][second_taffy.row] == first_taffy.taffy_type):
        first_taffy_connected = True
        destroy_taffies(first_taffy,second_taffy,1,4)
        valid_swap_found = True
    if (0 < first_taffy.column < 8) and (array_after_swap[first_taffy.column+1][first_taffy.row] == second_taffy.taffy_type) and (array_after_swap[first_taffy.column-1][first_taffy.row] == second_taffy.taffy_type):
        second_taffy_connected = True
        destroy_taffies(first_taffy,second_taffy,2,4)
        valid_swap_found = True
    #check right and left:5
    if not valid_swap_found:
        if (0 < second_taffy.row < 6) and (array_after_swap[second_taffy.column][second_taffy.row-1] == first_taffy.taffy_type) and (array_after_swap[second_taffy.column][second_taffy.row+1] == first_taffy.taffy_type):
            first_taffy_connected = True
            destroy_taffies(first_taffy,second_taffy,1,5)
            valid_swap_found = True
        if (0 < first_taffy.row < 6) and (array_after_swap[first_taffy.column][first_taffy.row-1] == second_taffy.taffy_type) and (array_after_swap[first_taffy.column][first_taffy.row+1] == second_taffy.taffy_type):
            second_taffy_connected = True
            destroy_taffies(first_taffy,second_taffy,2,5)
            valid_swap_found = True
    #check above: 0
    if not valid_swap_found:
        if (second_taffy.column > 1) and (array_after_swap[second_taffy.column-1][second_taffy.row] == first_taffy.taffy_type) and (array_after_swap[second_taffy.column-2][second_taffy.row] == first_taffy.taffy_type):
            first_taffy_connected = True
            destroy_taffies(first_taffy,second_taffy,1,0)
            valid_swap_found = True
        if (first_taffy.column > 1) and (array_after_swap[first_taffy.column-1][first_taffy.row] == second_taffy.taffy_type) and (array_after_swap[first_taffy.column-2][first_taffy.row] == second_taffy.taffy_type):
            second_taffy_connected = True
            destroy_taffies(first_taffy,second_taffy,2,0)
            valid_swap_found = True
    #check right: 1
    if not valid_swap_found:
        if (second_taffy.row < 5) and (array_after_swap[second_taffy.column][second_taffy.row+1] == first_taffy.taffy_type) and (array_after_swap[second_taffy.column][second_taffy.row+2] == first_taffy.taffy_type):
            first_taffy_connected = True
            destroy_taffies(first_taffy,second_taffy,1,1)
            valid_swap_found = True
        if (first_taffy.row < 5) and (array_after_swap[first_taffy.column][first_taffy.row+1] == second_taffy.taffy_type) and (array_after_swap[first_taffy.column][first_taffy.row+2] == second_taffy.taffy_type):
            second_taffy_connected = True
            destroy_taffies(first_taffy,second_taffy,2,1)
            valid_swap_found = True
    #check left: 2
    if not valid_swap_found:
        if (second_taffy.row > 1) and (array_after_swap[second_taffy.column][second_taffy.row-1] == first_taffy.taffy_type) and (array_after_swap[second_taffy.column][second_taffy.row-2] == first_taffy.taffy_type):
            first_taffy_connected = True
            destroy_taffies(first_taffy,second_taffy,1,2)
            valid_swap_found = True
        if (first_taffy.row > 1) and (array_after_swap[first_taffy.column][first_taffy.row-1] == second_taffy.taffy_type) and (array_after_swap[first_taffy.column][first_taffy.row-2] == second_taffy.taffy_type):
            second_taffy_connected = True
            destroy_taffies(first_taffy,second_taffy,2,2)
            valid_swap_found = True
    #check below: 3
    if not valid_swap_found:
        if (second_taffy.column < 7) and (array_after_swap[second_taffy.column+1][second_taffy.row] == first_taffy.taffy_type) and (array_after_swap[second_taffy.column+2][second_taffy.row] == first_taffy.taffy_type):
            first_taffy_connected = True
            destroy_taffies(first_taffy,second_taffy,1,3)
            valid_swap_found = True
        if (first_taffy.column < 7) and (array_after_swap[first_taffy.column+1][first_taffy.row] == second_taffy.taffy_type) and (array_after_swap[first_taffy.column+2][first_taffy.row] == second_taffy.taffy_type):
            second_taffy_connected = True
            destroy_taffies(first_taffy,second_taffy,2,3)
            valid_swap_found = True

    if valid_swap_found:
        return True
    return False

def swap(first_taffy,second_taffy):
    global first_taffy_connected
    global second_taffy_connected
    board_array[first_taffy.column][first_taffy.row] = second_taffy.taffy_type
    board_array[second_taffy.column][second_taffy.row] = first_taffy.taffy_type
    if first_taffy_connected:
        board_array[second_taffy.column][second_taffy.row] = 6
    if second_taffy_connected:
        board_array[first_taffy.column][first_taffy.row] = 6
    first_taffy_connected = False
    second_taffy_connected = False

def destroy_taffies(first_taffy,second_taffy,taffy_connected,connection_type):
    global score
    if taffy_connected == 1:
        #0: above,1:right,2:left,3:below,4: vertical mid,5: horizontal mid
        #connection formed on taffy 1
        if connection_type == 4:
            four_in_a_row = False
            board_array[second_taffy.column][second_taffy.row] = 6
            board_array[second_taffy.column+1][second_taffy.row] = 6
            board_array[second_taffy.column-1][second_taffy.row] = 6
            score += 3

            #check if any taffy above also forms a line
            i = second_taffy.column - 2
            while 0 < i < 8 and board_array[i][second_taffy.row] == first_taffy.taffy_type:
                board_array[i][second_taffy.row] = 6
                four_in_a_row = True
                score += 1
                i -= 1
            #check if any taffy below also forms a line
            i = second_taffy.column + 2
            while 0 < i < 8 and board_array[i][second_taffy.row] == first_taffy.taffy_type:
                board_array[i][second_taffy.row] = 6
                four_in_a_row = True
                score += 1
                i += 1
        elif connection_type == 5:
            four_in_a_row = False
            board_array[second_taffy.column][second_taffy.row] = 6
            board_array[second_taffy.column][second_taffy.row-1] = 6
            board_array[second_taffy.column][second_taffy.row+1] = 6
            score += 3

            #check if any taffy to the right also forms a line
            i = second_taffy.row + 2
            while 0 < i < 6 and board_array[second_taffy.column][i] == first_taffy.taffy_type:
                board_array[second_taffy.column][i] = 6
                four_in_a_row = True
                score += 1
                i += 1
            #check if any taffy to the left also forms a line
            i = second_taffy.row - 2
            while 0 < i < 6 and board_array[second_taffy.column][i] == first_taffy.taffy_type:
                board_array[second_taffy.column][i] = 6
                four_in_a_row = True
                score += 1
                i -= 1
        elif connection_type == 0:
            board_array[second_taffy.column][second_taffy.row] = 6
            board_array[second_taffy.column-1][second_taffy.row] = 6
            board_array[second_taffy.column-2][second_taffy.row] = 6
            score += 3
            #check if any taffy below also forms a line
            i = second_taffy.column + 1
            while 0 < i < 8 and board_array[i][second_taffy.row] == first_taffy.taffy_type:
                board_array[i][second_taffy.row] = 6
                score += 1
                i += 1
        elif connection_type == 1:
            board_array[second_taffy.column][second_taffy.row] = 6
            board_array[second_taffy.column][second_taffy.row+1] = 6
            board_array[second_taffy.column][second_taffy.row+2] = 6
            score += 3

            #check if any taffy to the left also forms a line
            i = second_taffy.row - 1
            while 0 < i < 6 and board_array[second_taffy.column][i] == first_taffy.taffy_type:
                board_array[second_taffy.column][i] = 6
                score += 1
                i -+ 1
        elif connection_type == 2:
            board_array[second_taffy.column][second_taffy.row] = 6
            board_array[second_taffy.column][second_taffy.row-1] = 6
            board_array[second_taffy.column][second_taffy.row-2] = 6
            score += 3

            #check if any taffy to the right also forms a line
            i = second_taffy.row + 1
            while 0 < i < 6 and board_array[second_taffy.column][i] == first_taffy.taffy_type:
                board_array[second_taffy.column][i] = 6
                score += 1
                i += 1
        elif connection_type == 3:
            board_array[second_taffy.column][second_taffy.row] = 6
            board_array[second_taffy.column+1][second_taffy.row] = 6
            board_array[second_taffy.column+2][second_taffy.row] = 6
            score += 3

            #check if any taffy above also forms a line
            i = second_taffy.column - 1
            while 0 < i < 8 and board_array[i][second_taffy.row] == first_taffy.taffy_type:
                board_array[i][second_taffy.row] = 6
                score += 1
                i -= 1
    else:
        #connection formed on taffy 2
        if connection_type == 4:
            four_in_a_row = False
            board_array[first_taffy.column][first_taffy.row] = 6
            board_array[first_taffy.column+1][first_taffy.row] = 6
            board_array[first_taffy.column-1][first_taffy.row] = 6
            score += 3

            #check if any taffy above also forms a line
            i = first_taffy.column - 2
            while 0 < i < 8 and board_array[i][first_taffy.row] == second_taffy.taffy_type:
                board_array[i][first_taffy.row] = 6
                four_in_a_row = True
                score += 1
                i -= 1
            #check if any taffy below also forms a line
            i = first_taffy.column + 2
            while 0 < i < 8 and board_array[i][first_taffy.row] == second_taffy.taffy_type:
                board_array[i][first_taffy.row] = 6
                four_in_a_row = True
                score += 1
                i += 1
            #if four_in_a_row:
                #score -= 2
        elif connection_type == 5:
            four_in_a_row = False
            board_array[first_taffy.column][first_taffy.row] = 6
            board_array[first_taffy.column][first_taffy.row-1] = 6
            board_array[first_taffy.column][first_taffy.row+1] = 6
            score += 3

            #check if any taffy to the right also forms a line
            i = first_taffy.row + 2
            while 0 < i < 6 and board_array[first_taffy.column][i] == second_taffy.taffy_type:
                board_array[first_taffy.column][i] = 6
                four_in_a_row = True
                score += 1
                i += 1
            #check if any taffy to the left also forms a line
            i = first_taffy.row - 2
            while 0 < i < 6 and board_array[first_taffy.column][i] == second_taffy.taffy_type:
                board_array[first_taffy.column][i] = 6
                four_in_a_row = True
                score += 1
                i -= 1
            #if four_in_a_row:
                #score -= 2
        elif connection_type == 0:
            board_array[first_taffy.column][first_taffy.row] = 6
            board_array[first_taffy.column-1][first_taffy.row] = 6
            board_array[first_taffy.column-2][first_taffy.row] = 6
            score += 3

            #check if any taffy below also forms a line
            i = first_taffy.column + 1
            while 0 < i < 8 and board_array[i][first_taffy.row] == second_taffy.taffy_type:
                board_array[i][first_taffy.row] = 6
                score += 1
                i += 1
        elif connection_type == 1:
            board_array[first_taffy.column][first_taffy.row] = 6
            board_array[first_taffy.column][first_taffy.row+1] = 6
            board_array[first_taffy.column][first_taffy.row+2] = 6
            score += 3

            #check if any taffy to the left also forms a line
            i = first_taffy.row - 1
            while 0 < i < 6 and board_array[first_taffy.column][i] == second_taffy.taffy_type:
                board_array[first_taffy.column][i] = 6
                score += 1
                i -+ 1
        elif connection_type == 2:
            board_array[first_taffy.column][first_taffy.row] = 6
            board_array[first_taffy.column][first_taffy.row-1] = 6
            board_array[first_taffy.column][first_taffy.row-2] = 6
            score += 3

            #check if any taffy to the right also forms a line
            i = first_taffy.row + 1
            while 0 < i < 6 and board_array[first_taffy.column][i] == second_taffy.taffy_type:
                board_array[first_taffy.column][i] = 6
                score += 1
                i += 1
        elif connection_type == 3:
            board_array[first_taffy.column][first_taffy.row] = 6
            board_array[first_taffy.column+1][first_taffy.row] = 6
            board_array[first_taffy.column+2][first_taffy.row] = 6
            score += 3

            #check if any taffy above also forms a line
            i = first_taffy.column - 1
            while 0 < i < 8 and board_array[i][first_taffy.row] == second_taffy.taffy_type:
                board_array[i][first_taffy.row] = 6
                score += 1
                i -= 1

def clicked_handler(posx,posy,first_taffy):
    row = (int(posx / taffy_spacing_horizontal)) #row of selected taffy
    column = (int(((posy - 1)*-1) / taffy_spacing_vertical)) #column of selected taffy

    if first_taffy:
        #draw rectangular selection for taffy 1
        stddraw.rectangle((row*taffy_spacing_horizontal)+selected_rectangle_offset,(1-(column*taffy_spacing_vertical)) - taffy_spacing_vertical,taffy_spacing_horizontal,taffy_spacing_vertical)

    #return the taffy type selected, and location
    taffy = richardnorman_p2_taffy.Taffy()
    taffy.row = row
    taffy.column = column
    taffy.taffy_type = board_array[column][row]
    return taffy

#checks two above and to the left
def check_if_three(row,column,shape_to_draw):
    #check row
    if ((board_array[row][column-1] == shape_to_draw) and (board_array[row][column-2] == shape_to_draw)):
        return True
    #check column
    if ((board_array[row-1][column] == shape_to_draw) and (board_array[row-2][column] == shape_to_draw)):
        return True
    return False

#0.14 horizontal, 0.12 vertical
def choose_new_number(shape_to_draw):
    #remove shape from list and choose new one
    number_list = [0,1,2,3,4,5]
    number_list.remove(shape_to_draw)
    new_number = randint(0,4)
    return number_list[new_number]

#populate board array
for y in range(9):
    column = []
    for x in range (7):
        column.append(0)
    board_array.append(column)

#random fill board
for i in range (9):
    for j in range(7):
        shape_to_draw = randint(0,5)
        #choose different shape
        line_exists = check_if_three(i,j,shape_to_draw)
        if line_exists:
            shape_to_draw = choose_new_number(shape_to_draw)
        stddraw.picture(shapes_array[shape_to_draw],padding_horizontal + j*taffy_spacing_horizontal, 1- (padding_vertical + i*taffy_spacing_vertical))
        board_array[i][j] = shape_to_draw