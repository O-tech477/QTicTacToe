import tkinter
from tkinter import messagebox
import QL 

#The board keeps track of the current state of the entire game. 0 -> Empty, 1 -> OpponentPlayed(Human), 2 -> CompPlayed.

board = [0]*9
numBoard = [0]*9
gameOver = False
wins = ((0,1,2), (3,4,5), (6,7,8),
        (0,3,6), (1,4,7), (2,5,8),
        (0,4,8), (2,4,6))
qla = QL.QLearning("qTable.npy", numBoard)


def checkGameOver():
    for a,b,c in wins:
        if board[a]['text'] == board[b]['text'] == board[c]['text'] != "":
            return True
    if all(cell['text'] != "" for cell in board):
        return None
    return False



def resetBoard():
    for cells in board:
        cells['text'] = ""
    for i in range(len(numBoard)):
        numBoard[i] = 0
    status_label['text'] = "Computer is Ready !!"
    

def generateNumBoard(buttonBoard):
    
    for i in range(9):
        if(buttonBoard[i]['text'] == ""):
            numBoard[i] = 0
        elif(buttonBoard[i]['text'] == "X"):
            numBoard[i] = 1
        else:
            numBoard[i] = 2


def updateStatusLabel(qla):
    status_label['text'] = f"The Q-Value of that move was: {float(qla.qValue):.2f} \n The reward given was: {qla.reward}"



def generateButtonBoard(numBoard):
    for i in range(9):
        if(numBoard[i] == 0):
            board[i]['text'] = ""
        elif(numBoard[i] == 1):
            board[i]['text'] = "X"
        else:
            board[i]['text'] = "O"
            board[i]['fg'] = "#3498db"

def onButtonClick(button_id):
    #The code assumes user is always X and computer is O. 
    #Also that the user plays first and the user is always valid.
    button_row = int(button_id.split("x")[0])
    button_col = int(button_id.split("x")[1])

    if(numBoard[button_row*3 +button_col] == 0):
        board[button_row*3 + button_col].config(text = "X", fg = "#e74c3c")
    else:
        messagebox.showwarning("BeValid", "Please Click Proper Button")
        
        return
    generateNumBoard(buttonBoard=board)


    if(checkGameOver()):
        qla.reward = -50
        qla.writeToQTableLost(action=qla.action)
        updateStatusLabel(qla)
        messagebox.showinfo("You Won", message="You have won !!. Congrats ")
        resetBoard()
    elif(checkGameOver() == None):
        qla.reward = 25
        qla.writeToQTableLost(action=qla.action)
        updateStatusLabel(qla)
        messagebox.showinfo("Its A Draw", message = "The game is a draw")
        resetBoard()
    else:
        qla.prev_state = qla.getState()
        qla.action = qla.chooseAction()
        qla.reward = qla.getReward(qla.action)
        qla.performAction(action=qla.action)
        qla.writeToQTable(action=qla.action)
        updateStatusLabel(qla)

        generateButtonBoard(numBoard=numBoard)

        if(qla.reward == 50):
            messagebox.showinfo("You have lost", message = "You Lost")
            resetBoard()
        elif(qla.reward == 25):
            messagebox.showinfo("Draw", message= "The game is a draw")
            resetBoard()



def main():
    root = tkinter.Tk()
    root.title("Q-Learning TicTacToe")
    root.geometry("500x600")
    root.minsize(width  =500, height = 600)
    root.maxsize(width=500, height=600)

    heading = tkinter.Label(text="Tic-Tac-Toe with Q-Learning",
                            font=("Helvetica", 22, "bold"),
                            fg="#2c3e50",
                            bg="#f4f6f8")
    heading.place(x=70, y=30)

    frame = tkinter.Frame(root, height=500, width=400, borderwidth=2, relief="sunken")
    frame.place(x = 50, y = 80)
    frame.config(background="#f4f6f8")
    frame.grid_propagate(False)

    tic_tac_toe_frame = tkinter.Frame(frame, background="#2c3e50", width = 300, height=300)
    tic_tac_toe_frame.grid(row=0, column=0, padx = 50, pady =30)
    tic_tac_toe_frame.grid_propagate(False)

    for row in range(3):
        for col in range(3):
            button = tkinter.Button(tic_tac_toe_frame, text = "", background="white", activebackground="white", relief="flat", font=("Helvetica", 9, "bold"), command=lambda button_id = f"{row}x{col}" :onButtonClick(button_id), width=10, height=4)
            button.grid(row=row, column=col, padx = 10, pady = 14)
            board[row*3 +col] = button

    global status_label
    status_label = tkinter.Label(frame, text="Computer is Ready !!", font=("Helvetica", 12), bg="#f4f6f8", fg="#34495e")
    status_label.grid(row=1, column=0, padx=80, pady=20)

    root.mainloop()

if __name__ == "__main__":
    main()