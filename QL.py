import numpy as np
import random


class QLearning():
    def __init__(self, filename, board):
        self.filename = filename
        
        self.gamma =0.9
        self.episilon = 0.2
        self.lr = 0.8

        self.nosActions = 9
        self.nosStates = 19683 #Need to fill this later

        self.actions = [i for i in range(9)] 
        self.q_table = self.loadQTable()

        self.board = board #Array of 9 elements representing the board 
        self.prev_state = None
        self.reward = 0

        self.action = None

        self.qValue = 0


    def getState(self):
        state = 0
        for i in range(len(self.board)):
            cell = self.board[i]
            if(cell == 0):
                d = 0
            elif(cell == 1):
                d = 1
            else:
                d = 2

            state += d*(3**i)
        return state


    def chooseAction(self):
        if random.random() <= self.episilon:
            valid_actions = [i for i in range(9) if self.board[i] == 0]
            action = random.choice(valid_actions)
        else:
            q_vals = self.q_table[self.prev_state].copy()
            for i in range(9):
                if self.board[i] != 0:
                    q_vals[i] = -np.inf
            action = np.argmax(q_vals)


        return action
        



    def statusAfterAction(self, action):
        wins = ((0,1,2), (3,4,5), (6,7,8),
        (0,3,6), (1,4,7), (2,5,8),
        (0,4,8), (2,4,6))
        self.board[action] = 2
        for a,b,c in wins:
            if self.board[a] == self.board[b]== self.board[c] != 0:
                self.board[action] = 0
                return True
        if all(cell != 0 for cell in self.board):
            self.board[action] = 0
            return None
        self.board[action] = 0
        return False


    def getReward(self, action):
        """If the computer wins after this action return 5
        If the computer loses after this action return -5
        If the game is a draw retuen 3
        Else return 1"""


        result = self.statusAfterAction(action)

        if(result == True):
            return 50
        elif(result == None):
            return 25
        else:
            return 1

    def performAction(self, action):
        self.board[action] = 2


    def loadQTable(self):
        try:
            self.q_table = np.load(self.filename)
        except:
            self.q_table = np.zeros((self.nosStates, self.nosActions))
        return self.q_table
    

    def writeToQTable(self, action):
        #Here the state is the current state and getState() will give us the next state
        self.q_table[self.prev_state][action] = self.q_table[self.prev_state][action] + self.lr*(self.reward + self.gamma*np.max(self.q_table[self.getState()]) - self.q_table[self.prev_state][action])
        self.qValue = self.q_table[self.prev_state][action]
        np.save(self.filename, self.q_table)
        print("The reward given", self.reward)


    def writeToQTableLost(self, action):
        self.q_table[self.prev_state][action] = self.q_table[self.prev_state][action] + self.lr*(self.reward - self.q_table[self.prev_state][action])
        self.qValue = self.q_table[self.prev_state][action]
        np.save(self.filename, self.q_table)
        print("The reward given:", self.reward)