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
    ## 請記得用int()轉型，或是直接用1//3來做整數除法
    wall_width = ??

    ## width為視窗的寬度，單位為px
    ## 寬度應為 offset(白邊) + wall_width(黃邊框) + wall_width(藍牆) + unit * grid_width(遊戲區水平寬度) + 
    ##        wall_width(藍牆) + wall_width(黃邊框) + offset(白邊)
    ## height為視窗的高度，單位為px
    ## 寬度應為 offset(白邊) + wall_width(黃邊框) + wall_width(藍牆) + unit * grid_width(遊戲區垂直高度) + 
    ##        wall_width(藍牆) + wall_width(黃邊框) + offset(白邊)
    width = unit * grid_width + 4 * wall_width + 2 * offset
    height = ??

    ## 配置root的長寬跟左上角座標
    ## 舉例來說，透過root.geometry('300x200+30+30')
    ## 可以將root設為300px寬，200px高，左上腳座標(30, 30)
    ## 請將geo_setting設為類似'300x200+30+30'的字串
    ## 300的部分應該為上面算出來的width，200的部分應該為上面算出來的height
    ## 由於width、height為int，並不支援str的加法(串接)，請將width、height轉型為str
    ## 後續可以透過root.geometry(geo_setting)來配置主視窗的長寬
    geo_setting = ?? + "x" + ?? + "+30+30" 

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
    canvas = Canvas(master = ??, bg = 'yellow', width = ??, height = ??)
        

    ## 放置frame跟canvas
    frame.pack()
    canvas.pack()
    return


if __name__ == "__main__":
    gen_win(18, 36, 24)
