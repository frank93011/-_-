from tkinter import *
import random

# 將會被許多涵式用到的變數設為global變數

# tkinter 部分
# root：Tk的instance, 整個視窗程式的root
# frame：視窗中的一塊佈局 
# canvas：畫圖區域，用來畫貪吃蛇
root = None
frame = None
canvas = None


# 遊戲區的grid數量
# grid_width：遊戲區有多少grid寬，本例為36
# grid_height：遊戲區有多少gird高，本例為24
grid_width = 0
grid_height = 0

# canvas 畫圖區部分，單位都為pixel
# unit：一個grid有多少px，本例為18
# wall_width：牆壁寬，本例為unit / 3，為6px
# width：遊戲區的寬度有多少px
# height：遊戲區的高度有多少px
# offset：canvas鑲嵌在frame中造成3px的白邊框
unit = 0
wall_width = 0
width = 0
height = 0
offset = 3


def gen_win(u, w, h):
    '''
    step 1: 
        這個函式會做a、b、c、d四個動作。
        參數u：讓使用者自訂一個grid有幾個px。
        參數w：整個視窗有多少px寬。
        參數h：整個視窗有多少px高。

        a. 創造主視窗
        b. 透過u, w, h計算unit、wall_width、width、height應該有的值，並設進去
        c. 創造一個Frame instance，存入變數frame，綁定在root底下
        d. 創造一個Canvas instance，存入變數canvas，綁定在frame底下
    '''

    ## 因為要在涵式內設定下列global變數，因此要用global關鍵字
    global grid_width
    global grid_height
    global unit
    global wall_width
    global width
    global height

    ## 因為要在涵式內設定下列global變數，因此要用global關鍵字    
    grid_width = w
    grid_height = h
    unit = u

    ## wall_width為牆壁寬，設為unit的1/3，因為單位為px，所以計算的結果不應為float，必須為int
    wall_width = int(unit/3)

    ## width為視窗的寬度，單位為px
    ## 寬度應為 offset(白邊) + wall_width(黃邊框) + wall_width(藍牆) + unit * grid_width(遊戲區水平寬度) + 
    ##        wall_width(藍牆) + wall_width(黃邊框) + offset(白邊)
    ## height為視窗的高度，單位為px
    ## 寬度應為 offset(白邊) + wall_width(黃邊框) + wall_width(藍牆) + unit * grid_width(遊戲區垂直高度) + 
    ##        wall_width(藍牆) + wall_width(黃邊框) + offset(白邊)
    width = unit * grid_width + 4 * wall_width + 2 * offset
    height = unit * grid_height + 4 * wall_width + 2 * offset

    ## 配置root的長寬跟左上角座標
    ## geo_setting為'widthxheight+30+30'的字串
    ## 可將root設為寬度width px，高度為height px的視窗，左上角座標為(30, 30)
    geo_setting = str(width) + "x" + str(height) + "+30+30" 

    global root
    global frame
    global canvas

    ## 創造主視窗，設為root
    root = Tk()

    ## 用geo_setting字串配置主視窗大小
    root.geometry(geo_setting)
    root.title("Snake game")

    ## 創造一個Frame instance，存入變數frame，綁定在root底下
    ## frame寬度設為前面算出來的width，高度設為前面算出來的height
    frame = Frame(master = root, width = width, height = height)

    ## 創造一個Canvas instance，存入變數canvas，綁定在frame底下
    ## canvas的背景色設為'yellow'
    ## frame寬度設為前面算出來的width，高度設為前面算出來的height
    canvas = Canvas(master = frame, bg = 'yellow', width = width - 2 * offset, height = height - 2 * offset)
 
    ## 放置frame跟canvas       
    frame.pack()
    canvas.pack()
    return

def draw_walls():
    '''
    step 2:
        繪製遊戲區的牆壁
        wall1：左方牆
        wall2：下方牆
        wall3：右方牆
        wall4：上方牆
    '''
    ## 由於要用create_rectangle來畫牆，所以要定義好wall1 ~ wall4的左上角跟右下角座標
    ## 左上都用 _x1、_y1，右下都用 _x2、_y2命名
    ## wall_margin: 牆之前的空間，即offset(白邊) + wall_width(黃邊框)
    ## 舉例來說，offset若為3px，wall_width若為6px，則wall_margin為9px
    wall_margin = offset + wall_width

    ## 注意座標是從0開始數，若想要抓水平方向wall_margin(例9px)的範圍，
    ## 則實際上最後一個px的座標為wall_margin - 1(即8px)
    ## 示意圖如下(☐為px，空格只是視覺上讓大家方便區分不同的空間，實際上☐都是緊鄰的, 第三排數字為座標)
    ## 白邊 黃邊框
    ## ☐☐☐ ☐☐☐☐☐☐
    ## 0 2 3    8

    ## 攻略：若你是抓「某區段的終點座標(例黃邊框的最後一個px)」，則為
    ## 區段起點座標 + (區段寬度 - 1)
    ## 以「黃邊框」區段終點而言
    ## 黃邊框起點座標3，區段寬度6，因此「黃邊終點座標」為 3 + (6 - 1) = 8
    ## 白邊 黃邊框
    ## ☐☐☐ ☐☐☐☐☐☒
    ## 0 2 3    8

    ## 攻略：若你是抓「某區段的起點座標(例藍牆的第一個px)」，則為
    ## 「上一區段」終點座標 + 1
    ## 以「藍牆」區段起點而言
    ## 上一區段可視為「白邊+黃邊框」，因此這個區段的終點為
    ## 白邊起點座標0 + (區段寬度9(白邊3 + 黃邊框6) - 1) = 0 + (9 - 1) = 8
    ## 藍牆的起點座標則為 8 + 1
    ## 白邊 黃邊框  藍牆
    ## ☐☐☐ ☐☐☐☐☐☐ ☒☐☐☐☐☐
    ## 0 2 3    8 9

    ## wall1的範圍，從黃邊框之後6px，☒為我們的目標點
    ## wall1_x1: 0 + (wall_margin - 1) + 1
    ## wall1_x2: wall_margin + (wall_width - 1)
    ## 白邊 黃邊框  藍牆(方向↓)
    ## ☐☐☐ ☐☐☐☐☐☐ ☒☐☐☐☐☒
    ## 0 2 3    8 9    14
    ## 
    ## wall1_y1(請將下面畫的☐想成垂直方向):
    ## wall1_y1: 0 + (wall_margin - 1) + 1
    ## wall1_y2: 從終點(height - 1)倒扣回來比較方便，觀念跟「攻略」一樣，只是方向相反
    ## 因此會區段終點的計算會從 
    ## 區段起點座標 + (區段寬度 - 1) 變成
    ## 區段起點座標 - (區段寬度 - 1)
    ##
    ## 區段起點的計算會從
    ## 「上一區段」終點座標 + 1 變成
    ## 「上一區段」終點座標 - 1
    ## 例如，從終點(height - 1)為起點，白邊區段的終點為(方向是從下方往上數)
    ## (height - 1) - (offset - 1) = height -1 - (3 - 1) = height - 3
    ## wall1_y2: (height - 1) - (wall_margin - 1) - 1 = (height - 1) - wall_margin
    ##
    ## (請將下面畫的☐想成垂直方向)
    ## 白邊 黃邊框  藍牆(方向→)          藍牆
    ## ☐☐☐ ☐☐☐☐☐☐ ☒☐☐☐☐☐...........☐☐☐☐☐☒ ☐☐☐☐☐☐ ☐☐☐
    ## 0 2 3    8 9    14                       -3 (height - 1)

    wall1_x1 = wall_margin
    wall1_y1 = wall_margin
    wall1_x2 = wall1_x1 + (wall_width - 1)
    wall1_y2 = ((height - 1)) - wall_margin

    ## 白邊 黃邊框  藍牆(方向↓)    藍牆(方向↓)
    ## ☐☐☐ ☐☐☐☐☐☐ ☐☐☐☐☐☐...........☒☐☐☐☐☒ ☒☐☐☐☐☐ ☐☐☐
    ## 0 2 3    8 9    14                       -3 (width - 1)
    ##
    ## 我們先計算右邊「白邊+黃邊框」區段的終點(上圖最右邊的☒)
    ## 起點為(width - 1)，區段寬度wall_margin
    ## 因此「白邊+黃邊框」區段的終點 = (width - 1) - (wall_margin - 1)
    ## wall3_x2則為「白邊+黃邊框」區段的終點的下一個點
    ## wall3_x2: (width - 1) - (wall_margin - 1) - 1 =  (width - 1) - wall_margin
    ## wall3_x1為以wall3_x2，藍牆(寬度wall_width)的終點
    ## wall3_x1: (width - 1) - wall_margin - (wall_width - 1)
    wall3_x1 = ((width - 1)) - ?? - (?? - 1)
    wall3_y1 = wall1_y1
    wall3_x2 = ((width - 1)) - ??
    wall3_y2 = wall1_y2

    ## (請將下面畫的☐想成垂直方向)
    ## 白邊 黃邊框  藍牆(方向→)    藍牆(方向→)
    ## ☐☐☐ ☐☐☐☐☐☐ ☐☐☐☐☐☐...........☒☐☐☐☐☒ ☐☐☐☐☐☐ ☐☐☐
    ## 0 2 3    8 9    14               wall1_y2   (height - 1)
    ## wall2_x1就在wall1_x2右邊一格，所以應為wall1_x2 + 1
    ## wall2_x2就在wall3_x1左邊一格，所以應為wall3_x1 - 1
    ## wall2_y2跟wall1_y2一樣
    ## wall2_y1以wall1_y2為起點，為藍牆區段的終點
    ## wall2_y1 = wall1_y2 - (wall_width - 1)
    wall2_x1 = ?? + 1
    wall2_y1 = wall1_y2 - (?? - 1)
    wall2_x2 = ?? - 1
    wall2_y2 = wall1_y2

    ## (請將下面畫的☐想成垂直方向)
    ## 白邊 黃邊框  藍牆(方向→)    藍牆(方向→)
    ## ☐☐☐ ☐☐☐☐☐☐ ☒☐☐☐☐☒...........☐☐☐☐☐☐ ☐☐☐☐☐☐ ☐☐☐
    ## 0 2 3    8 9    14                          (height - 1)
    ## wall4_x1跟wall2_x1一樣
    ## wall4_x2跟wall1_y1一樣
    ## wall4_x2跟wall2_x2一樣
    ## wall4_y2以wall1_y1為起點，為藍牆區段的終點
    ## wall2_y1 = wall1_y1 + (wall_width - 1)
    wall4_x1 = wall2_x1
    wall4_y1 = wall1_y1
    wall4_x2 = wall2_x2
    wall4_y2 = wall1_y1 + (wall_width - 1)

    ## 將wall1的左上座標(wall1_x1, wall1_y1)、右下座標(wall1_x2, wall1_y2)包成wall1這個list
    ## wall2 ~ wall4也是類似
    wall1 = [(wall1_x1, wall1_y1), (wall1_x2, wall1_y2)]
    wall2 = [(wall2_x1, wall2_y1), (wall2_x2, wall2_y2)]
    wall3 = [(wall3_x1, wall3_y1), (wall3_x2, wall3_y2)]
    wall4 = [(wall4_x1, wall4_y1), (wall4_x2, wall4_y2)]
 
    ## 將wall1的左上座標(wall1_x1, wall1_y1)、右下座標(wall1_x2, wall1_y2)丟進
    ## canvas.create_rectangle當作參數
    ## *wall1是特殊語法，意思是將wall1裡面所有的東西攤平、展開，所以
    ## canvas.create_rectangle(*wall1, ...) 等價為
    ## canvas.create_rectangle(wall1_x1, wall1_y1, wall1_x2, wall1_y2, ...)
    ## 此外 outline參數指的是長方形的外框，預設是黑色'black'，我們改成藍色'blue'
    ## 為了區隔水平、垂直的牆，因此水平的wall2、wall4都改為紅色'red'
    canvas.create_rectangle(*wall1, outline = 'blue', fill = 'blue')
    canvas.create_rectangle(*wall2, outline = 'red', fill = 'red')
    canvas.create_rectangle(*wall3, outline = 'blue', fill = 'blue')
    canvas.create_rectangle(*wall4, outline = 'red', fill = 'red')
    return


if __name__ == "__main__":
    gen_win(18, 36, 24)
    draw_walls()
