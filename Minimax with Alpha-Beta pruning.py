import pygame
import numpy as np

class Game:
    def __init__(self):
        self.d = 0
        self.accept_clicks = True 
        self.a_score = 0
        self.b_score = 0
        self.turn = "A"

        self.grid_status = np.zeros((3, 3), np.int)
        self.horizontal_walls_set_flags = np.zeros((3, 4), np.int)
        self.vertical_walls_set_flags = np.zeros((4, 3), np.int)
        
        print(self.grid_status.T)
        print(self.horizontal_walls_set_flags.T)
        print(self.vertical_walls_set_flags.T)
        print(self.a_score,' : ', self.b_score)
        print()
        # initialize pygame
        pygame.init()
        self.screen = pygame.display.set_mode([90 * 3 + 12, 90 * 3 + 12])
        
        # load all images
        self.empty = pygame.image.load("Img/empty.png")
        self.A = pygame.image.load("Img/A.png")
        self.B = pygame.image.load("Img/B.png")
        self.block = pygame.image.load("Img/block.png")
        self.lineX_blue = pygame.image.load("Img/lineX_blue.png")
        self.lineX_red = pygame.image.load("Img/lineX_red.png")
        self.lineY_blue = pygame.image.load("Img/lineY_blue.png")
        self.lineY_red = pygame.image.load("Img/lineY_red.png")
 
        self.screen.fill((255, 255, 255))
        for column in range(4):
            for row in range(4):
                    x, y = column * 90, row * 90
                    self.screen.blit(self.block, (x, y))
        pygame.display.flip()
        pygame.display.set_caption('Dots and Boxes')

        while True:
            self.Human()

#-------------------------------------------------------------------
    def Computer(self):
        self.turn = "B"
        state = [-1, -1, -1]
        Depth = 3
        #make the move for AI
        t, x, y = self.minimax(state, Depth)
        if t == 0:
            if self.horizontal_walls_set_flags[x][y] == 0:
                self.horizontal_walls_set_flags[x][y] = 2
                self.screen.blit(self.lineX_red, (x*90+12, y*90))
                self.d +=1
        else:
            if self.vertical_walls_set_flags[x][y] == 0:
                self.vertical_walls_set_flags[x][y] = 2
                self.screen.blit(self.lineY_red, (x*90, y*90+12))
                self.d +=1

        self.set_all_slots()
                    
        if self.won():
            self.accept_clicks = False

        else:
            pygame.display.flip()
        self.Human()
                
    def Human(self):
        self.turn = "A"
       
        for event in pygame.event.get():
            # quit the game when the player closes it
            if event.type == pygame.QUIT:
                pygame.quit()
                exit(0)

            # vertical click
            elif event.type == pygame.MOUSEBUTTONDOWN and pygame.mouse.get_pressed()[0]:
                if not self.accept_clicks:
                    continue

                # get the current position of the cursor
                x = pygame.mouse.get_pos()[0]
                y = pygame.mouse.get_pos()[1]
                # check whether it was a not set wall that was clicked

                rest_x = x % 90
                rest_y = y % 90

                wall_slot_x = x//90
                wall_slot_y = y//90

                if rest_x < 12:
                    wall_x, wall_y = wall_slot_x*90, wall_slot_y*90 + 12

                elif rest_y < 12:
                    wall_x, wall_y = wall_slot_x*90 + 12, wall_slot_y*90
                    
                else:
                    continue

                horizontal_wall = wall_y % 90 == 0

                if horizontal_wall:
                    if self.horizontal_walls_set_flags[wall_x//90][wall_y//90] == 0:
                        self.horizontal_walls_set_flags[wall_x//90][wall_y//90] = 1
                        self.screen.blit(self.lineX_blue, (wall_x, wall_y))
                        self.d +=1
                    else:
                        continue
                else:
                    if self.vertical_walls_set_flags[wall_x//90][wall_y//90] == 0:
                        self.vertical_walls_set_flags[wall_x//90][wall_y//90] = 1
                        self.screen.blit(self.lineY_blue, (wall_x, wall_y))
                        self.d +=1
                    else:
                        continue

                self.set_all_slots()
                    
                if self.won():
                    self.accept_clicks = False
                else:
                    pygame.display.flip()
                self.Computer()
#-----------------------------------------------------------------
# Minimax algorithm
#-----------------------------------------------------------------
    def minimax(self,state, num):
            
        turn = 2
        t, h, k = state[0], state[1], state[2]
        Min = 1000
        Max = -1000
        self.move = []
        for i in range(3):
            for j in range(4):
                if self.horizontal_walls_set_flags[i][j] == 0:
                    self.horizontal_walls_set_flags[i][j] = turn
                    Result = 0
                    if j == 0:
                        if not (self.grid_status[i][j] != 0 or self.get_number_of_walls(i, j) < 4): 
                            Result = self.get_score(i,j,turn)
                    elif j == 3:
                        if not (self.grid_status[i][j-1] != 0 or self.get_number_of_walls(i, j-1) < 4):
                            Result = self.get_score(i,j-1,turn)
                    else:
                        if not (self.grid_status[i][j] != 0 or self.get_number_of_walls(i, j) < 4):
                            Result = self.get_score(i,j,turn)
                        if not (self.grid_status[i][j-1] != 0 or self.get_number_of_walls(i, j-1) < 4):
                            Result += self.get_score(i,j-1,turn)
                    Result -=self.minimum(num-1)
                    self.horizontal_walls_set_flags[i][j] = 0
                    if Result >= Max:
                        Max, h, k, t = Result, i, j, 0
        for i in range(4):
            for j in range(3):
                if self.vertical_walls_set_flags[i][j] == 0:
                    self.vertical_walls_set_flags[i][j] = turn
                    Result = 0
                    if i == 0:
                        if not (self.grid_status[i][j] != 0 or self.get_number_of_walls(i, j) < 4):
                            Result = self.get_score(i,j,turn)
                    elif i == 3:
                        if not (self.grid_status[i-1][j] != 0 or self.get_number_of_walls(i-1, j) < 4):
                            Result = self.get_score(i-1,j,turn)
                    else:
                        if not (self.grid_status[i][j] != 0 or self.get_number_of_walls(i, j) < 4):
                            Result = self.get_score(i,j,turn)
                        if not (self.grid_status[i-1][j] != 0 or self.get_number_of_walls(i-1,j) < 4):
                            Result +=  self.get_score(i-1,j,turn)
                                    
                    Result -=self.minimum(num-1)
                    self.vertical_walls_set_flags[i][j] = 0

                    if Result >= Max:
                        Max, h, k, t = Result, i, j, 1    
    
        return t,h,k

    def maximum(self, num):
        if num == 0:
            return 0

        turn = 2
        Min = 1000
        Max = -1000
        for i in range(3):
            for j in range(4):
                if self.horizontal_walls_set_flags[i][j] == 0:
                    self.horizontal_walls_set_flags[i][j] = turn
                    Result = 0
                    if j == 0:
                        if not (self.grid_status[i][j] != 0 or self.get_number_of_walls(i, j) < 4): 
                            Result = self.get_score(i,j,turn)
                    elif j == 3:
                        if not (self.grid_status[i][j-1] != 0 or self.get_number_of_walls(i, j-1) < 4):
                            Result = self.get_score(i,j-1,turn)
                    else:
                        if not (self.grid_status[i][j] != 0 or self.get_number_of_walls(i, j) < 4):
                            Result = self.get_score(i,j,turn)
                        if not (self.grid_status[i][j-1] != 0 or self.get_number_of_walls(i, j-1) < 4):
                            Result += self.get_score(i,j-1,turn)

                    Result -=self.minimum(num-1)
                    self.horizontal_walls_set_flags[i][j] = 0

                    if Result >= Max:
                        Max = Result
                    
        for i in range(4):
            for j in range(3):
                if self.vertical_walls_set_flags[i][j] == 0:
                    self.vertical_walls_set_flags[i][j] = turn
                    Result = 0

                    if i == 0:
                        if not (self.grid_status[i][j] != 0 or self.get_number_of_walls(i, j) < 4):
                            Result = self.get_score(i,j,turn)
                    elif i == 3:
                        if not (self.grid_status[i-1][j] != 0 or self.get_number_of_walls(i-1, j) < 4):
                            Result = self.get_score(i-1,j,turn)
                    else:
                        if not (self.grid_status[i][j] != 0 or self.get_number_of_walls(i, j) < 4):
                            Result = self.get_score(i,j,turn)
                        if not (self.grid_status[i-1][j] != 0 or self.get_number_of_walls(i-1,j) < 4):
                            Result +=  self.get_score(i-1,j,turn)
                        
                    Result -=self.minimum(num-1)
                    self.vertical_walls_set_flags[i][j] = 0
                    if Result >= Max:
                        Max = Result
        return Max
 
    def minimum(self, num):
        if num == 0:
            return 0
        
        turn = 1
        Min = 1000
        Max = -1000

        for i in range(3):
            for j in range(4):
                if self.horizontal_walls_set_flags[i][j] == 0:
                    self.horizontal_walls_set_flags[i][j] = turn
                    Result = 0

                    if j == 0:
                        if not (self.grid_status[i][j] != 0 or self.get_number_of_walls(i, j) < 4): 
                            Result = self.get_score(i,j,turn)
                    elif j == 3:
                        if not (self.grid_status[i][j-1] != 0 or self.get_number_of_walls(i, j-1) < 4):
                            Result = self.get_score(i,j-1,turn)
                    else:
                        if not (self.grid_status[i][j] != 0 or self.get_number_of_walls(i, j) < 4):
                            Result = self.get_score(i,j,turn)
                        if not (self.grid_status[i][j-1] != 0 or self.get_number_of_walls(i, j-1) < 4):
                            Result += self.get_score(i,j-1,turn)
                        
                    Result -=self.maximum(num-1)
                    self.horizontal_walls_set_flags[i][j] = 0

                    if Result >= Max:
                        Max = Result
 
        for i in range(4):
            for j in range(3):
                if self.vertical_walls_set_flags[i][j] == 0:
                    self.vertical_walls_set_flags[i][j] = turn
                    Result = 0

                    if i == 0:
                        if not (self.grid_status[i][j] != 0 or self.get_number_of_walls(i, j) < 4):
                            Result = self.get_score(i,j,turn)
                    elif i == 3:
                        if not (self.grid_status[i-1][j] != 0 or self.get_number_of_walls(i-1, j) < 4):
                            Result = self.get_score(i-1,j,turn)
                    else:
                        if not (self.grid_status[i][j] != 0 or self.get_number_of_walls(i, j) < 4):
                            Result = self.get_score(i,j,turn)
                        if not (self.grid_status[i-1][j] != 0 or self.get_number_of_walls(i-1,j) < 4):
                            Result +=  self.get_score(i-1,j,turn)
                        
                    Result -=self.maximum(num-1)
                    self.vertical_walls_set_flags[i][j] = 0
                    if Result >= Max:
                        Max = Result
      
        return Max
#-----------------------------------------------------------------
# update matrices and score
#-----------------------------------------------------------------
    def set_all_slots(self):
        for column_ in range(3):
            for row_ in range(3):
                if self.grid_status[column_][row_] != 0 or self.get_number_of_walls(column_, row_) < 4:
                    continue

                if self.turn == "A":
                    self.grid_status[column_][row_] = 1
                    self.screen.blit(self.A, (column_ * 90 + 12, row_ * 90 + 12))
                    self.a_score += self.get_score(column_, row_, 1)
                elif self.turn == "B":
                    self.grid_status[column_][row_] = 2
                    self.screen.blit(self.B, (column_ * 90 + 12, row_ * 90 + 12))
                    self.b_score += self.get_score(column_, row_, 2)

    def get_number_of_walls(self, slot_column, slot_row):
        number_of_walls = 0

        if self.vertical_walls_set_flags[slot_column + 1][slot_row] != 0:
            number_of_walls += 1

        if self.horizontal_walls_set_flags[slot_column][slot_row + 1] != 0:
            number_of_walls += 1

        if self.vertical_walls_set_flags[slot_column][slot_row] != 0:
            number_of_walls += 1

        if self.horizontal_walls_set_flags[slot_column][slot_row] != 0:
            number_of_walls += 1

        return number_of_walls
    def get_score(self, slot_column, slot_row, player):
        score = 0

        if self.vertical_walls_set_flags[slot_column + 1][slot_row] != player:
                score += 1

        if self.horizontal_walls_set_flags[slot_column][slot_row + 1] != player:
                score += 1

        if self.vertical_walls_set_flags[slot_column][slot_row] != player:
                score += 1

        if self.horizontal_walls_set_flags[slot_column][slot_row] != player:
                score += 1

        return score
#-----------------------------------------------------------------
#def check win
#-----------------------------------------------------------------
    def won(self):

        print('----------------------------')
        print(self.grid_status.T) 
        print(self.horizontal_walls_set_flags.T)
        print(self.vertical_walls_set_flags.T)
        print(self.a_score,' : ', self.b_score)
        
        if self.d != 24:
            check = False
        else:
            check = True
            if self.a_score < self.b_score:
                won_caption = "Computer won!   Congrats"
            elif self.b_score < self.a_score:
                won_caption = "You won!   Congrats"
            else:
                won_caption = "It's a tie!"

            # set the display caption
            print(won_caption)
            # update the players screen
            pygame.display.flip()
        return check
        
# start a game
game = Game()  
