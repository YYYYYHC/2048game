import pygame
import numpy as np

SquareSize = 4


#
#
# class numSquare:
#     def __init__(self, image, value, posx, posy):
#         self.value = value
#         self.image = image
#         self.pos = image.get_rect().move(posx, posy)
#         self.moveStepLength = 10
#
#     def error(self):
#         print("Got an error!")
#
#     def moveLeft(self):
#         self.pos = self.pos.move(-1 * self.moveStepLength, 0)
#
#     def moveRight(self):
#         self.pos = self.pos.move(self.moveStepLength, 0)
#
#     def moveUp(self):
#         self.pos = self.pos.move(0, -1 * self.moveStepLength)
#
#     def moveDown(self):
#         self.pos = self.pos.move(0, 1 * self.moveStepLength)
#
#     def move(self, direction):
#         switch = {'left': self.moveLeft,
#                   'right': self.moveRight,
#                   'up': self.moveRight,
#                   'down': self.moveDown,
#                   }
#         switch.get(direction, self.error)()
#

class NumSquareMap:
    def __init__(self, element_img_lt, base_pos, init_state=np.zeros([SquareSize, SquareSize])):
        self.state = init_state
        self.element_image_lt = element_img_lt
        self.base_pos = element_img_lt[0].get_rect().move(base_pos[0], base_pos[1])


    @staticmethod
    def no_space_error():
        print("no more space")

    @staticmethod
    def wrong_dire_error():
        print("Got an wrong direction !")

    def push_to_left(self):
        for i in range(SquareSize):
            k = 0
            new_row = np.zeros(SquareSize)
            for j in range(SquareSize):
                if self.state[i][j] != 0:
                    new_row[k] = self.state[i][j]
                    k = k + 1
            self.state[i] = new_row

    def merge_iteration(self):
        for i in range(SquareSize):
            for j in range(SquareSize - 1):
                if self.state[i][j] == self.state[i][j + 1]:
                    self.state[i][j] *= 2
                    for k in range(j + 1, SquareSize - 1):
                        self.state[i][k] = self.state[i][k + 1]
                    self.state[i][SquareSize - 1] = 0

    def move_left(self):
        self.push_to_left()
        self.merge_iteration()

    def move_right(self):
        self.state = self.state[:, ::-1]
        self.move_left()
        self.state = self.state[:, ::-1]

    def move_up(self):
        self.state = self.state.T
        self.move_left()
        self.state = self.state.T

    def move_down(self):
        self.state = self.state[::-1, :]
        self.move_up()
        self.state = self.state[::-1, :]

    def move_and_put(self, direction):
        self.move(direction)
        self.put_new_num()

    def move(self, direction):
        switch = {'left': self.move_left,
                  'right': self.move_right,
                  'up': self.move_up,
                  'down': self.move_down,
                  }
        switch.get(direction, self.wrong_dire_error)()

    def find_space(self):
        index = np.where(self.state == 0)
        return len(index[0]) != 0

    def put_new_num(self):
        if self.find_space():
            index = np.where(self.state == 0)
            new_pos_index = np.random.randint(len(index[0]))
            new_pos_index = (index[0][new_pos_index], index[1][new_pos_index])
            new_pos_num = 2
            self.state[new_pos_index] = new_pos_num
        else:
            self.no_space_error()

    def get_element_img(self, row_num, column_num): # start from 0
        switch = {'case0': 0,
                  'case2': 1,
                  'case4': 2,
                  'case8': 3,
                  'case16': 4,
                  'case32': 5,
                  'case64': 6,
                  'case128': 7,
                  'case256': 8,
                  'case512': 9,
                  'case1024': 10,
                  'case2048': 11,
                  }
        case_str = 'case' + str(int(self.state[row_num, column_num]))
        element_img = self.element_image_lt[switch[case_str]]
        return element_img

    def init_game(self):
        if self.state.max() == 0:
            init_state = np.random.randint(0,3,size=[4,4])
            init_state[init_state == 2] = 4
            init_state[init_state == 1] = 2
            self.state = init_state

    def game_over(self):
        state = self.state
        if state_have_zero(state):
            return False
        else:
            row_zero = np.zeros(SquareSize, dtype=int)

            state_up = state - np.insert(state[1:SquareSize, :], SquareSize - 1, values=row_zero, axis=0)
            if state_have_zero(state_up):
                return False

            state_down = state - np.insert(state[0:SquareSize-1, :], 0, values=row_zero, axis=0)
            if state_have_zero(state_down):
                return False

            state_left = state - np.insert(state[:, 1:SquareSize], SquareSize - 1, values=row_zero, axis=1)
            if state_have_zero(state_left):
                return False

            state_right = state - np.insert(state[:, 0:SquareSize - 1], 0, values=row_zero, axis=1)
            if state_have_zero(state_right):
                return False

        return True

    def game_win(self):
        if self.state.max() == 2048:
            return True
        return False


def state_have_zero(state):
    return len(np.where(state == 0)[0]) != 0

def paint_state(screen, nsm):
    for i in range(SquareSize):  # row
        for j in range(SquareSize):  # column
            pass
            screen.blit(nsm.get_element_img(i, j), nsm.base_pos.move(100*j, 100*i))
#
# s = np.array([[0, 1, 1, 1],
#               [0, 1, 1, 0],
#               [4, 0, 2, 1],
#               [1, 2, 2, 8]])
#
# nsm = NumSquareMap(s)
# print(nsm.state)
# nsm.move_and_put('down')
# print(nsm.state)
