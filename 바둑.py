#    -*-coding:utf-8-*-

import sys #이거 의미 파악
import pygame
from pygame.locals import *
import numpy as np




empty = 0
black = 1
white = 2

def other_color(color):
    if color == black:
        return white
    else:
        return black


class Go(object):
    def __init__(self, size):
        self.board = np.zeros((size,size))
        self.examined_stone_pos_list = []
        self.ko_count = True
        self.ko = [] #패로 먹힌 돌의 장소

        

    def get_board(self):
        return self.board
    

    def udlr(self, position):
        #return up down left right position list of input position

        col = position[0]
        row = position[1]


        
        up = [col - 1, row]
        down = [col + 1, row]
        left = [col, row - 1]
        right = [col, row + 1]

        udlr = [up, down, left, right]

        
        if col == 0:
            udlr.remove(up)
        if col == 18:
            udlr.remove(down)
        if row == 0:
            udlr.remove(left)
        if row == 18:
            udlr.remove(right)

        return udlr

    def stone_group(self, position, color, lst):
        #find stones that are connected with a stone of input position (same color stone)
        #& append to the list outside of this function
    
        
        for stone_pos in self.udlr(position):
            if self.board[stone_pos[0],stone_pos[1]] == color and (stone_pos not in lst):
                lst.append(stone_pos) 
                self.stone_group(stone_pos, color, lst)

        


    def is_captured(self,position,color):
        
        #그 위치에 있는 돌과 연결되어있는 돌들이 상대돌들에게 둘러쌓여있는지
        #True 이면 return list --> 잡힌거 / return False --> 안 잡힌거

        examined_stone_pos_list = [position] # stone group whose stones are all connected
        self.stone_group(position, color, examined_stone_pos_list)

        


        
        
        for stone_pos in examined_stone_pos_list:
            
            for stone_pos in self.udlr(stone_pos):
                
                
                  
                if self.board[stone_pos[0], stone_pos[1]]== empty:
                    
                    if stone_pos != position:
                        return False # 하나라도 주변이 비었으면 ok = 안잡힌거

        

        return examined_stone_pos_list



    
    def is_move_valid(self, position, color):
        

        

        #return False if move on input position is invalid

        if self.board[position[0],position[1]] != empty: #안비어있으면 FALSE
            return False

        capture_list = self.capture(position, color)
        
        
        if capture_list != False:
            

            #패 관련 문제
            if len(capture_list) == 1:
                
                if self.ko == position and not (self.ko_count):
                    return False
                
            return True

        

        if (self.is_captured(position, color)) == False: #self.is_captured가 False를 내면 안됨

            return True
        
        else:
            return False #내가 낸게 잡히는 경우 즉 불가능

        
        
        

    def update_board(self, position, color):
        #update하는 동시에 따먹는 돌이 있으면 그 값을 return 아니면 무조건 0return

        

        #self.is_move_valid 가 True 이면 바둑판 바로 업데이트
        if self.is_move_valid( position, color):

            self. ko_count = True #패 count가 True로 바뀌고
            self.board[position[0], position[1]] = color #보드 업데이트

            global count

            count += 1 #차례 

            
            

            capture_list = self.capture(position,color)
            
           

            if capture_list != False:
                
                if len(capture_list) == 1:
                    self.ko_count = False 
                    self.ko = capture_list[0] #패 위치 저장 & 패_count가 False로
                
                for i in capture_list:
                    
                    self.board[i[0],i[1]] = empty #다 공백으로 바뀜
                return len(capture_list)

            
                
           
        return 0




    def capture(self, position, color):
        #그 position 자리에 color돌 놓으면 다른 돌을 따먹는지
        #따먹으면 그 따먹는 리스트 return/ 아니면 False return


        captured_list = []
        for stone_pos in self.udlr(position):
                if self.board[stone_pos[0]][stone_pos[1]] == other_color(color):
                    
                    
                    # 주위 돌이 다른 색깔의 돌일때, 그돌들을 따먹는지

                    # 놓여있는 상태로 만들기 
                    previous_color = self.board[position[0], position[1]]
                    self.board[position[0], position[1]] = color
                    
                    
                    
                    small_captured_list = self.is_captured(stone_pos,other_color(color))
                    
                    self.board[position[0],position[1]] = previous_color #원상태 복귀

                    
                    
                    
                    if small_captured_list != False:
                        captured_list += small_captured_list #따먹히는 돌들 다 추가


        

        
        if len(captured_list) == 0: #따먹히는 돌이 없으면 return False
            
            return False


        return captured_list #따먹히는 돌이 있으면 그 돌들의 position이 있는 리스트
                    
                    
        

                

         


   


class Player:

    def __init__(self, stone_color, board):
        self.color = stone_color
        self.board = board
        self.captured_num = 0

    def move(self,column, row):
        
        self.captured_num += self.board.update_board([column, row], self.color)
        
        
my_board = Go(19)



player1 = Player(black, my_board)
player2 = Player(white, my_board)







   


class Player:

    def __init__(self, stone_color, board):
        self.color = stone_color
        self.board = board
        self.captured_num = 0

    def move(self,column, row):
        
        self.captured_num += self.board.update_board([column, row], self.color)
        
        
my_board = Go(19)



player1 = Player(black, my_board)
player2 = Player(white, my_board)







 


pygame.init()
board_img = pygame.image.load('바둑판_1.jpg')
edge_size = [26,23]
area_add = 0
screen_size = (board_img.get_size()[0] + area_add, board_img.get_size()[1] + area_add) 

#전체, 하드웨어 가속 사용(전체모드에서만), 더블 버퍼 모드 사용
screen = pygame.display.set_mode(screen_size, DOUBLEBUF) # FULLSCREEN | HWSURFACE | DOUBLEBUF)
pygame.display.set_caption("합스고")







image_list = np.zeros((len(my_board.get_board()), len(my_board.get_board()))) #[image load, coordinate]

TARGET_FPS = 30
square_size = 666.0/18.0 #바둑판 한칸 크기



clock = pygame.time.Clock()
global count
count = 0


black_stone_img = pygame.image.load('검은돌_수정.png')
white_stone_img = pygame.image.load('흰돌_수정.png')

[ stone_width, stone_height] = black_stone_img.get_size() 








def decide_position((x_pixel,y_pixel)):
    # 바둑판 어디에 놓아야할지

    x_return = int((x_pixel + square_size/2.0 - area_add/2.0 - edge_size[0])/square_size )
    y_return = int((y_pixel + square_size/2.0 - area_add/2.0 - edge_size[1])/square_size )

    
    return [x_return, y_return]
        
def click_handler((x_board, y_board)):
    
    #바둑판 어디에 놓아야할지에 대한 정보를 픽셀로 바꿔서 이미지 전달
        
        
    global count
        
        
    if count%2 == 0:
        color = black
            
        #if my_board.is_move_valid([y_board,x_board],color): #행렬과 그림의 좌표 체계가 달라서 바뀜
        player1.move(y_board,x_board)
                
                
            #count += 1
    else:
        color = white
        #if my_board.is_move_valid([y_board,x_board],color):
        player2.move(y_board,x_board)
                
            #count += 1
        
def update_screen():
    for i in range(len(my_board.get_board())):
            for j in range(len(my_board.get_board())):
                
                #행렬과 그림의 좌표 체계 차이
                pos_pixel = (area_add/2.0 + edge_size[0] + j * square_size  - stone_width/2.0,
                             area_add/2.0 + edge_size[1] + i * square_size - stone_height/2.0)
                         
                if my_board.get_board()[i][j] == black:
                    screen.blit(black_stone_img, pos_pixel)
                elif my_board.get_board()[i][j] == white:
                    screen.blit(white_stone_img, pos_pixel)
                    
                           
                           
                    
                
        
    
while True:
    
    
    
            
    for event in pygame.event.get():
        #이벤트 처리부분 --> 키보드. 마우스 등의 이벤트


        #if not hasattr(event, 'key'):
        #    continue



        LEFT = 1
        RIGHT = 3
        
        if event.type == MOUSEBUTTONDOWN and event.button == 1:
            
            stone_pos = decide_position(list(event.pos))
            click_handler( stone_pos)
            
            




        
        if event.type == QUIT:
            pygame.quit()
            sys.exit()
            

        
    #게임의 상태를 업데이트

    screen.blit(board_img, (area_add/2.0,area_add/2.0))
    update_screen()
    


    
    pygame.display.flip() #update the full display SUrface to the screen
    clock.tick(TARGET_FPS)


    #게임의 상태를 화면에 그려주는 부분(지우고, 그리고)


    
