# 再帰呼び出しの事例
import tkinter

#枝分かれする四角形を描く
def drawbox(x, y, scale, count, depth):
    count += 1
    scaleh = int(scale * 0.5)
    
    xa = x - scaleh
    ya = y - 40
    xb = x + scaleh
    yb = y + 40
    canvas.create_rectangle(xa, ya, xb, yb, fill='Yellow')
    
    #実行回数を表示
    msg = str(count)
    canvas.create_text(x, y, text=msg, font=("", 16))
    
    if depth == 0: return count
    
    count = drawbox(x-scaleh, y+85, scaleh, count, depth-1)
    
    count = drawbox(x+scaleh, y+85, scaleh, count, depth-1)
    
    return count

root = tkinter.Tk()

root.geometry("640x480")

canvas = tkinter.Canvas(root, width=640, height=480)

canvas.pack()

drawbox(320, 80, 300, 0, 3)

root.mainloop()