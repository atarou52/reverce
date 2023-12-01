# AIを実装したリバーシのプログラム
import tkinter
import threading

CELLSIZE = 48       # 1マスのピクセル数
FONTSIZE = ("", 24) # フォントサイズを設定
BOARDW = 8          # 盤の幅高さ
OFSX = 2 * CELLSIZE # 盤のオフセットX座標
OFSY = 1 * CELLSIZE # 盤のオフセットY座標
TYPE_BLACK = 0      # 右の種類：黒
TYPE_WHITE = 1      # 石の種類：白
TYPE_NONE = 255     # 石の種類：なし
DEPTHMAX = 4        # AIの深さ(必ず偶数にする)
turn = TYPE_BLACK   # 現在のターン
myturn = TYPE_BLACK # あなたの手番
passcnt = 0         # パスの連続回数
endflag = True      # ゲーム終了フラグ

# 番を管理する配列
board = bytearray(BOARDW * BOARDW)

playtbl = ["黒", "白"] # プレイヤーの表示名
colortbl = ["Black", "White"]   # カラーテーブル
vectable = [    # ベクトルテーブル
    (0, -1),    # 上
    (1, -1),    # 右上
    (1, 0),     # 右
    (1, 1),     # 右下
    (0, 1),     # 下
    (-1, 1),    # 左下
    (-1, 0),    # 左
    (-1, -1)    # 左上
]

# 手版の表示名
whotbl = ["(あなた)", "(AI)"]

# タイマー処理(約1秒)
def timerctrl():
    if turn != myturn:      # AIの番場合
        AI(turn)            # AIの思考ルーチン
        # プレイヤー切り替え&ゲームの判定   
        nextturn()
        redraw()            # 画面全体を再描画
        
    timer = threading.Timer(1, timerctrl)
    timer.start()
# 盤の得点テーブル
maptable = [
    [120, -20, 20,  5,  5, 20, -20, 120],
    [-20, -40, -5, -5, -5, -5, -40, -20],
    [ 20,  -5, 15,  3,  3, 15,  -5,  20],
    [  5,  -5,  3,  3,  3,  3,  -5,   5],
    [  5,  -5,  3,  3,  3,  3,  -5,   5],
    [ 20,  -5, 15,  3,  3, 15,  -5,  20],
    [-20, -40, -5, -5, -5, -5, -40, -20],
    [120, -20, 20,  5,  5, 20, -20, 120]
]

# 評価関数
def evaluation(board, mynum):
    score = 0 #評価値の合計
    for y in range (BOARDW):
        for x in range(BOARDW):
            num = getpiece(board, (x, y))
            s = maptable[y][x] # 1マスあたりの点数
            if num == mynum : score += s #加点
            if num == mynum ^ 1: score -= s # 減点
    return score

# AIの思考ルーチン(AI側の石の種類)
def AI(num):
    # パス発生中 or ゲーム終了の場合、終了
    if passcnt > 0 or endflag == True:
        return
    
    # 最良の手を探索する
    bestscore = -9999
    for y in range(BOARDW):
        for x in range(BOARDW):
            # 石が置けるか判定する
            if turnablepiece(board, (x,y), num) == 0:
                continue
            # 仮の盤に石を億
            newboard = bytearray(BOARDW * BOARDW)
            copyboard(board, newboard)
            confirmpiece(newboard, (x,y), num)
            # 相手の石をおいて、評価値を得る
            score = minimax(newboard, num^1, DEPTHMAX-1)
            # 最大の評価値を発見
            if bestscore < score:
                bestscore = score # 評価値
                bestpos = (x, y)  # 石の座標
    # 石を確定する
    confirmpiece(board, bestpos, num)
    
# ミニマックス法
# 盤、石の種類、深さ
def minimax (board, num, depth):
    if depth == 0:
        return evaluation(board, num) # 評価値
    
    branch = 0 # 枝分かれの数
    # 偶数ならMAX,奇数ならMIN
    if depth % 2 == 0:
        score = -9999
        for y in range(BOARDW):
            for x in range(BOARDW):
                # 石がおけるか判定する
                if turnablepiece(board, (x,y), num) == 0:
                    continue
                branch += 1 # 枝分かれの数 + 1
                # 仮の盤に石を置く
                newboard = bytearray(BOARDW * BOARDW)
                copyboard(board, newboard)
                confirmpiece(newboard, (x,y), num)
                # 相手の石をおいて、評価値をいる
                s = minimax(newboard, num^1, depth-1)
                score = max(score, s)
                
    if branch == 0: #石を全く置けない場合
        # 探索打ち切り
        return evaluation(board, num)
    else:
        score = 9999
        for Y in range(BOARDW):
            for x in range(BOARDW):
                #石が置けるか判定する
                if turnablepiece(board, (x,y), num) == 0:
                    continue
                branch += 1 #枝分かれの数 + 1
                # 仮の番に石を置く
                newboard = bytearray(BOARDW * BOARDW)
                copyboard(board, newboard)
                confirmpiece(newboard, (x,y), num)
                # 相手の意思をおいて、評価を得る
                s = minimax(newboard, num^1, depth-1)
                score = min(score, s)
                
        if branch == 0:  # 石が全くおけない場合
            # 探索打ち切り
            return evaluation(board, num^1)
    
    return score # 評価値を返す

# 先手ボタンのクリック時に実行する関数
def buttona_click(event):
    global myturn
    myturn= TYPE_WHITE # あなたの石の種類
    initboard()        # 盤の初期化
    
# 後手ボタンのクリック時に実行する関数
def buttonb_click(event):
    global myturn
    myturn = TYPE_WHITE # あなたの石の種類
    initboard()         # 盤の初期化
    
# 盤に書き込み(盤、座標、石の種類)
def setpiece(board, pos, num):
    index = (pos[1] * BOARDW) + pos[0]
    board[index] = num
    
# 盤の読み込み(盤、座標)
def getpiece(board,pos):
    index = (pos[1] * BOARDW) + pos[0]
    return board[index]

# スタート画面を表示
def startscreen():
    canvas.place_forget() # 非表示
    btna.place(x=140, y=120, width=300, height=100)
    btnb.place(x=140, y=260, width=300, height=100)
    
# 盤の初期化
def initboard():
    global turn, passcnt, endflag
    btna.place_forget() # 先手ボタンを非表示
    btnb.place_forget() # 後手ボタンを非表示
    canvas.place(x=0, y=0) #キャンパスを表示
    
    for y in range(BOARDW):
        for x in range (BOARDW):
            setpiece(board, (x,y), TYPE_NONE)
            

    # 最初に4この石を置く
    setpiece(board, (3,3), TYPE_BLACK)  # 黒石
    setpiece(board, (4,3), TYPE_WHITE)  # 白石
    setpiece(board, (3,4), TYPE_WHITE)  # 白石
    setpiece(board, (4,4), TYPE_BLACK)  # 黒石

    turn = TYPE_BLACK # 現在のターン
    passcnt = 0       # パスの連続回数
    endflag = False   # ゲームの終了フラグ
    drawboard()       # 盤を描画
    redraw()          # 画面全体を再描画
    
# 盤の内容をコピー(コピー元, コピー先)
def copyboard(board1, board2):
    for i in range(BOARDW*BOARDW):
        board2[i] = board1[i]
        
# キャンバスのクリック時に実行する関数
def canvas_click(event):
    if endflag == True: # ゲーム終了
        startscreen()   # 接続画面を表示
        return 
    
    if turn != myturn:
        return # 自分の番ではない場合、入力は無効
    
    if passcnt > 0:  # パス発生中
        # プレイヤー切り替え＆ゲームの判定
        nextturn()
        redraw()    # 画面全体を再描画
        return 
    
    x = int ((event.x -OFSX) / CELLSIZE)
    y = int ((event.y - OFSY) / CELLSIZE)
    pos = (x,y)
    if isinside(pos) == False:
        return # 盤の外をクリックした場合は無効
    if turnablepiece(board, pos, turn ) == 0:
        return # 反転できる医師がない場合は無効
    
    confirmpiece(board, pos, turn) # 石を確定
    nextturn() # プレイヤー切り替え＆ゲームの判定
    redraw()    # 画面全体を再描画
    
# 石を確定(盤、座標、石の種類)
def confirmpiece(workboard, pos, num):
    for vectol in range(8):     # 石を反転
        # 石のサーチ
        loopcount = search(workboard, pos, vectol, num)
        temppos = pos
        for i in range(loopcount):
            temppos = moveposition(temppos, vectol)
            # 石を置き換える
            setpiece(workboard, temppos, num)
            setpiece(workboard, pos, num) # 石を置く
            
# プレイヤー切り替え＆ゲームの判定
def nextturn():
    global passcnt, endflag, turn
    turn ^= 1 # プレイヤーの切り替え
    empty = 0 # 空いたマスの数
    for y in range(BOARDW):
        for x in range(BOARDW):
            if getpiece(board, (x,y)) == TYPE_NONE:
                empty += 1
            if turnablepiece(board, (x,y), turn) > 0:
                passcnt = 0 # パスは不要
                return
            
    if empty == 0:  # 空いたマスがない場合
        # 石が置けないので、ゲーム終了
        endflag = True
        return
    
    passcnt += 1 # パスが発生
    # 連続してパスが発生した場合
    if passcnt >= 2:
        # 無限ループ回避のためゲーム終了
        endflag = True
    
# 座標の移動(座標、ベクトル番号)
def moveposition(pos, vectol):
    x = pos[0] + vectable[vectol][0]
    y = pos[1] + vectable[vectol][1]
    return(x, y)

# 反転できる石の数を取得(盤、座標、石の種類)
def turnablepiece(board, pos, num):
    if getpiece(board, pos) != TYPE_NONE:
        return 0 #　石が置けない場合は無効
    
    total = 0 # 石の総数
    for vectol in range(8): # 8方向をサーチする
        total += search(board, pos, vectol, num)
    return total

# 石のサーチ(盤、座標、ベクトル番号、石の種類)
def search (board, pos , vectol, num):
    piece = 0  # 石の数
    while True:
        pos = moveposition(pos, vectol)
        if isinside(pos) == False:
            return 0 # 盤の外へ出た場合は無効
        if getpiece(board, pos ) == TYPE_NONE:
            return 0 # 数えられない場合は無効
        if getpiece(board, pos) == num:
            break    # 目的の石を検出した場合は終了
        piece += 1
    return piece

# 指定座標の範囲☑(座標)
def isinside(pos):
    if pos[0]<0 or pos[0]>=8: return False # 範囲外
    if pos[1]<0 or pos[1]>=8: return False # 範囲外
    return True  # 範囲内

# 盤だけを表示
def drawboard():
    canvas.create_rectangle(0,0,576, 480, fill="khaki1")
    
    for y in range(BOARDW):
        for x in range(BOARDW):
            xa = x * CELLSIZE + OFSX
            ya = y * CELLSIZE + OFSY
            xb = xa + CELLSIZE
            yb = ya + CELLSIZE
            canvas.create_rectangle(xa, ya, xb, yb, fill='Green', width=2)


# 画面全体を再描画
def redraw():
    d = int(CELLSIZE / 10)
    black = 0   # 黒石の数
    white = 0   # 白石の数
    
    # 石を表示
    for y in range(BOARDW):
        for x in range(BOARDW):
            num = getpiece(board, (x, y))
            if num == TYPE_NONE: continue
            if num == TYPE_BLACK: black += 1
            if num == TYPE_WHITE: white += 1
            xa = x * CELLSIZE + OFSX + d
            ya = y * CELLSIZE + OFSY + d
            xb = xa + CELLSIZE - (2*d)
            yb = ya + CELLSIZE - (2*d)
            canvas.create_oval(xa, ya, xb, yb, fill=colortbl[num], width=2)
            
    canvas.create_rectangle(0, 433, 576, 480, fill="khaki1", width=0)
    msg = "黒" + str(black) + " 対  白" + str(white)
    canvas.create_text(288, 456, text = msg, font=FONTSIZE)
    msg = playtbl[turn]
    msg += whotbl[abs(turn-myturn)] + 'の番です'
    if passcnt > 0: # パスが発生中
        msg += "(パス)"
    if endflag == True:     # ゲーム終了
        msg = "終了です"
        
    canvas.create_rectangle(0,0, 576, 46, fill="khaki1", width=0)
    canvas.create_text(288, 24, text=msg, font=FONTSIZE)
    

root = tkinter.Tk()     # ウインドウを作成
root.title("Reversi")   # タイトルを設定
root.geometry("576x480")# サイズを設定

# Buttonウィジェットを作成
# 先手ボタン
btna = tkinter.Button(root, text = '先手(黒)')
btna.bind("<Button-1>", buttona_click)
# 後手ボタン
btnb = tkinter.Button(root, text = '後手(白)')
btnb.bind("<Button-1>", buttonb_click)

# Canvasウィジェット(キャンバス)を作成
canvas = tkinter.Canvas(root, width=576, height=480)

# キャンパスのクリック時に実行する関数を登録
canvas.bind("<Button-1>", canvas_click)

startscreen()   # スタート画面を表示

# スレッドを作成
thread = threading.Thread(target=timerctrl)
thread.deamon = True
thread.start() # スレッド開始

root.mainloop()
    