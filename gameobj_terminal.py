import copy

import pygame
import numpy as np
import os
import time
# from testPygame_ransac import  ransacsolve

SquareSize = 4
def map_dir(i):
    if i == 0:
        return 'right'
    if i == 1:
        return 'down'
    if i == 2:
        return 'left'
    if i == 3:
        return 'up'

def getlist(num, snum):
    re_lt = []
    for i in range(snum):
        re_lt.append(num%snum)
        num = num//snum
    return re_lt

def ransacsolve(nsm, flag):
    print("solve a time")
    time.sleep(0.01)
    #random step
    # ini_score = nsm.judge_score()
    ini_state = nsm.state.copy()
    iteration_count = 0
    thread = 0
    nsm_state_lt_return = []
    step_lt__return = []

    if flag == 0:
        for step_num in range(pow(4,3)):
            # print(nsm.state)
            nsm.change_state(ini_state)
            cur_score = 0
            nsm_state_lt = []
            random_step_4 = getlist(step_num, 3)
            print(random_step_4)
            for i in random_step_4:
                dir = map_dir(i)
                nsm.move_and_put(dir)
                nsm_state_lt.append(nsm.state.copy())
                if nsm.game_over():
                    cur_score = -1
                    break
            iteration_count += 1
            #judge score
            if np.sum(nsm.judge_score()) > thread:
                thread = np.sum(nsm.judge_score())
                nsm_state_lt_return = nsm_state_lt
                step_lt__return = random_step_4
        if(thread > 0):
            return step_lt__return
        else:
            return -1


    else:
        dir = map_dir(np.random.randint(0,4))
        nsm.move_and_put(dir)
        return



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
        self.score = np.sum(self.state)

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
        state_past = self.state.copy()
        self.move(direction)
        if not (self.state == state_past).all() :
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
            new_pos_num = 2 * np.random.randint(low=1,high=2)
            self.state[new_pos_index] = new_pos_num
        else:
            self.no_space_error()

    def get_element_img(self, row_num, column_num):  # start from 0
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
            init_pos = np.random.randint(0,3,size=[2,2])
            init_state = self.state
            init_state[init_pos[0][0], init_pos[0][1]] = 4
            init_state[init_pos[1][0], init_pos[1][1]] = 2
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

            state_down = state - np.insert(state[0:SquareSize - 1, :], 0, values=row_zero, axis=0)
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

    def game_score(self):
        num_score = np.sum(self.state)

        total_score = num_score
        return total_score

    def change_state(self, new_state):
        self.state = new_state

    def judge_score(self):
        max_num_pos_score = 0
        max_num_pos = np.where(self.state == np.max(self.state))
        # print(max_num_pos)
        # print("")
        for i in range(len(max_num_pos[0])):
            pos = np.array([max_num_pos[0][i], max_num_pos[1][i]])
            # print(pos)
            if (pos == np.array([0,0])).all() or (pos == np.array([0,3])).all() or (pos == np.array([3,0])).all() or (pos == np.array([3,3])).all():
                max_num_pos_score += np.max(self.state)
            elif (pos == np.array([0,1])).all() or (pos == np.array([0,2])).all() \
                or (pos == np.array([1,0])).all() or(pos == np.array([2,0])).all() \
                or (pos == np.array([1,3])).all() or (pos == np.array([2,3])).all() \
                or (pos == np.array([3,1])).all() or (pos == np.array([3,2])).all():
                max_num_pos_score -= np.max(self.state)/10
            else:
                max_num_pos_score -= np.max(self.state)

        step_score = 0
        r_up_score = 0
        l_up_score = 0
        u_up_score = 0
        d_up_score = 0
        for i in range(4):
            for j in range(4):
                if j != 3:
                    r_up_score += self.state[i][j+1] - self.state[i][j]
                    d_up_score += self.state[j+1][i] - self.state[j][i]
                if j != 0:
                    l_up_score += self.state[i][j-1] - self.state[i][j]
                    u_up_score += self.state[j-1][i] - self.state[j][i]
            step_score += max([l_up_score, r_up_score]) + max([u_up_score, d_up_score])

        clear_score = np.count_nonzero(self.state) * -10

        total_score = step_score + max_num_pos_score
        return np.array([step_score, max_num_pos_score*100, clear_score])

    def ransacsolve(self, flag):
        ini_state = self.state.copy()
        iteration_count = 0
        thread = 0
        nsm_state_lt_return = []
        step_lt__return = []

        if flag == 0:
            for step_num in range(pow(4, 3)):
                # print(nsm.state)
                # print(step_num, ini_state)
                self.change_state(ini_state)
                # print(ini_state)
                cur_score = 0
                nsm_state_lt = []
                random_step_4 = getlist(step_num, 3)
                #print(random_step_4)
                for i in random_step_4:
                    dir = map_dir(i)
                    ini_state = copy.deepcopy(ini_state)
                    self.move_and_put(dir)
                    nsm_state_lt.append(self.state.copy())
                    if self.game_over():
                        cur_score = -1
                        break
                iteration_count += 1
                # judge score
                if np.sum(self.judge_score()) > thread:
                    thread = np.sum(self.judge_score())
                    nsm_state_lt_return = nsm_state_lt
                    step_lt__return = random_step_4
            if (thread > 0):
                self.change_state(ini_state)
                return step_lt__return
            else:
                self.change_state(ini_state)
                return -1


        else:
            dir = map_dir(np.random.randint(0, 4))
            self.move_and_put(dir)
            return

def state_have_zero(state):
    return len(np.where(state == 0)[0]) != 0


def paint_state(screen, nsm):
    game_font = pygame.font.SysFont('arial', 15, True)
    state = nsm.state

    pygame.init()
    for i in range(SquareSize):  # row
        for j in range(SquareSize):  # column
            pass
            screen.blit(nsm.get_element_img(i, j), nsm.base_pos.move(100 * j, 100 * i))
    # step_lt = nsm.ransacsolve(0)
    # AI_suggestion = "none"
    # if step_lt!=-1:
    #     AI_suggestion = map_dir(step_lt[0])
    # screen.blit(game_font.render(u'AI suggestion: %s' %AI_suggestion, True, (255, 255 ,255)), (0,200))

# s = np.array([[0, 1, 1, 1],
#               [0, 1, 1, 0],
#               [4, 0, 2, 1],
#               [1, 2, 2, 8]])
#
# nsm = NumSquareMap(s)
# print(nsm.state)
# nsm.move_and_put('down')
# print(nsm.state)
