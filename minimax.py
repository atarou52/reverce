# ミニマックス法の実験
import tkinter 
import random 

def minimax(x, y, scale, depth):
    scaleh = int(scale * 0.5)
    
    xa = x - scaleh
    ya = y - 40
    xb = x + scaleh
    yb = y + 40
    canvas.create_rectangle(xa, ya, xb, yb, fill='Yellow')
    
    if depth == 0:
        score = random.randint(0,9)
        
        msg = str(score)
        canvas.create_text(x, y, text=msg, font=("", 16))
        
        return score
    
    if depth % 2 == 0:
        mode = 'MAX'
        score = -9999
        for i in range(2):
            s = minimax(x-scaleh+(i*scale), y+85, scaleh, depth-1)
            score = max(score, s)
    else:
        mode = 'MIN'
        score = 9999
        for i in range(2):
            s=minimax(x-scaleh+(i*scale), y+85, scaleh, depth-1)
            score = min(score,s)
                
    canvas.create_text(x, y-20, text=mode, font=("",16))
    
    msg= str(score)
    canvas.create_text(x, y+20,text=msg, font=("",16))
    
    return score

root = tkinter.Tk()
root.geometry("640x480")

canvas = tkinter.Canvas(root, width=640, height=480)

canvas.pack()

minimax(320, 80, 300, 4)

root.mainloop()