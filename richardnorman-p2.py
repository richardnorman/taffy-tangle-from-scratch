import richardnorman_p2_drawing
import stddraw
import pygame
import richardnorman_p2_taffy

game_over = False
first_taffy_selected = False

richardnorman_p2_drawing.draw_score()

first_taffy = richardnorman_p2_taffy.Taffy
second_taffy = richardnorman_p2_taffy.Taffy

while not game_over:
    stddraw.show(350)
    if not first_taffy_selected:
        if stddraw.mousePressed():
            first_taffy = richardnorman_p2_drawing.clicked_handler(stddraw.mouseX(),stddraw.mouseY(),True)
            first_taffy_selected = True
    else:
        if stddraw.mousePressed():
            second_taffy = richardnorman_p2_drawing.clicked_handler(stddraw.mouseX(),stddraw.mouseY(),False)
            #check if valid swap
            valid_swap = richardnorman_p2_drawing.check_if_valid_swap(first_taffy,second_taffy)
            if not valid_swap:
                print("The taffy swap is not valid, try selecting another taffy")
            else:
                #swap is valid, commence taffy swap
                print("Swapping...")
                richardnorman_p2_drawing.swap(first_taffy,second_taffy)
                richardnorman_p2_drawing.shift_taffies_down()
                richardnorman_p2_drawing.load_more_taffies()
                three_line_found = richardnorman_p2_drawing.check_if_three_after_fall()
                while three_line_found:
                    richardnorman_p2_drawing.shift_taffies_down()
                    richardnorman_p2_drawing.load_more_taffies()
                    three_line_found = richardnorman_p2_drawing.check_if_three_after_fall()

            richardnorman_p2_drawing.redraw_board()
            richardnorman_p2_drawing.draw_score()
            first_taffy_selected = False
