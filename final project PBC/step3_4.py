from tkinter import *
import random
from unit_test import *

# 將會被許多涵式用到的變數設為global變數

# tkinter 部分
# root: Tk的instance, 整個視窗程式的root
# frame: 視窗中的一塊佈局 
# canvas: 畫圖區域，用來畫貪吃蛇
root = None
frame = None
canvas = None


# 遊戲區的grid數量
# grid_width: 遊戲區有多少grid寬，本例為36
# grid_height: 遊戲區有多少gird高，本例為24
grid_width = 0
grid_height = 0

# canvas 畫圖區部分，單位都為pixel
# unit: 一個grid有多少px，本例為18
# wall_width: 牆壁寬，本例為unit / 3，為6px
# width: 遊戲區的寬度有多少px
# height: 遊戲區的高度有多少px
# offset: canvas鑲嵌在frame中造成3px的白邊框
unit = 0
wall_width = 0
width = 0
height = 0
offset = 3


def gen_win(u, w, h):
    '''
    step 1: 
        這個函式會做a、b、c、d四個動作
        參數u：讓使用者自訂一個grid有幾個px
        參數w：整個視窗有多少px寬
        參數h：整個視窗有多少px高

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
    ## 寬度應為 offset + wall_width + wall_width + unit * grid_width + wall_width + wall_width + offset
    ## height為視窗的高度，單位為px
    ## 高度應為 offset + wall_width + wall_width + unit * grid_height + wall_width + wall_width + offset
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
        wall1: 左方牆
        wall2: 下方牆
        wall3: 右方牆
        wall4: 上方牆
    '''
    ## 由於要用create_rectangle來畫牆，所以要定義好wall1 ~ wall4的左上角跟右下角座標
    ## 左上都用 _x1、_y1，右下都用 _x2、_y2命名
    ## wall_margin: 牆之前的空間，即offset(白邊) + wall_width(黃邊框)
    ## 舉例來說，offset若為3px，wall_width若為6px，則wall_margin為9px
    wall_margin = offset + wall_width

    ## 分別計算wall1 ~ wall4的左上、右下座標
    wall1_x1 = wall_margin
    wall1_y1 = wall_margin
    wall1_x2 = wall1_x1 + (wall_width - 1)
    wall1_y2 = ((height - 1)) - wall_margin

    wall3_x1 = ((width - 1)) - (wall_margin + wall_width - 1)
    wall3_y1 = wall1_y1
    wall3_x2 = ((width - 1)) - wall_margin
    wall3_y2 = wall1_y2
    
    wall2_x1 = wall1_x2 + 1
    wall2_y1 = wall1_y2 - (wall_width - 1)
    wall2_x2 = wall3_x1 - 1
    wall2_y2 = wall1_y2

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
    canvas.create_rectangle(*wall1, outline = 'blue', fill = 'blue')
    canvas.create_rectangle(*wall2, outline = 'blue', fill = 'blue')
    canvas.create_rectangle(*wall3, outline = 'blue', fill = 'blue')
    canvas.create_rectangle(*wall4, outline = 'blue', fill = 'blue')
    return

def grid_to_pixel(coor):
    '''
    step 3-1: 
        定義一個grid座標與px座標轉換的涵式，將grid的左上角對應到正確的px座標

        參數coor：代表grid座標的(x座標, y座標)，型別為tuple
        return：grid座標轉換後的左上角px座標，型別為tuple
    '''

    ## 將coor[0], coor[1]分別assign給xgrid, ygrid 以方便計算
    (xgrid, ygrid) = coor

    ## xpx代表x方向的px座標
    ## xgrid = 0 時對應到的xpx為offset(白邊) + 2 * wall_width(黃邊框 + 藍牆)
    ## 當xgrid = 1, 2, 3...時，應該還要加上1*unit, 2*unit, 3*unit，也就是unit * xgrid
    ## ypx以此類推
    xpx = offset + 2 * wall_width + unit * xgrid
    ypx = offset + 2 * wall_width + unit * ygrid
    return (xpx, ypx)

def grid_br_corner(coor_px):
    '''
    step 3-2:
        canvas總是需要2個px座標(分別是左上角、右下角)才能創造了一個rectangle(矩形)。
        我們已經在step 3-1的grid_to_pixel()將grid座標轉換成rectangle的左上角px座標，
        右下角px座標就透過grid_br_corner(coor_px)來完成。

        參數coor_px：grid左上角的px座標，型別為tuple
        return：grid右下角的px座標，型別為tuple
    '''

    ## 將coor_px[0], coor_px[1]分別assign給x1px, y1px以方便計算
    (x1px, y1px) = coor_px
    ## 以(x1px, y1px)為grid左上角px座標，若grid右下角px座標為(x2px, y2px)
    ## 若一個grid有unit個px寬，
    ## x2px應為x1px + unit - 1，y2px以此類推
    x2px = x1px + unit - 1
    y2px = y1px + unit - 1
    return (x2px, y2px)
    
# snake_coor：一個global list，用來紀錄每格蛇身的grid座標
# snake_rect：一個global list，用來紀錄蛇身在canvas上的每個rectangle的流水號
snake_coor = list()
snake_rect = list()
def add_body1(coor, from_tail = True):
    '''
    step 3-3:
        當增加一個蛇身grid時，動作如下
        a. 將新的蛇身grid座標轉換成左上角、右下角的pixel座標
        b. 透過canvas.create_rectangle()畫出新蛇身grid
        c. 若新蛇身要加在尾巴，則將grid座標append到snake_coor這個list
        d. 若新蛇身要加在尾巴，則將canvas上新造出來的rectangle流水號append到snake_rect這個list

        e. 若新蛇身要加在頭部，則將grid座標insert到snake_coor最前面
        f. 若新蛇身要加在頭部，則將grid座標insert到snake_coor最前面
        
        參數coor：新蛇身的grid座標，型別為tuple
        參數from_tail：當from_tail為True時，代表要將新蛇身加入頭部
                      當from_tail為True時，代表要將新蛇身加在尾巴
    '''

    ## 由於會改到snake_coor、snake_rect這兩個global的list 因此要加「global」關鍵字    
    global snake_coor
    global snake_rect

    ## 因為要新增蛇身，所以要先準備好新蛇身的左上角、右下角px座標
    ## 好讓canvans可以create_rectangle，因此創造grid_sta、grid_end這兩個變數
    ## 分別代表新蛇身的左上角、右下角px座標
    grid_sta = grid_to_pixel(coor)
    grid_end = grid_br_corner(grid_sta)

    ## 透過fill參數設定蛇身為'orange'，並透過tag參數將所有蛇身都標記為'snake'
    ## 再用grid_rect變數紀錄canvas.create_rectangle()的流水號
    grid_rect = canvas.create_rectangle(*grid_sta, *grid_end, fill = 'orange', tag = 'snake')

    ## 當from_tail為True時，表示要將coor/grid_rect放在snake_coor/snake_rect的最尾端
    ## 否則表示要將coor/grid_rect放在snake_coor/snake_rect的頭部
    if from_tail:
        snake_coor.append(coor)
        snake_rect.append(grid_rect)        
    else:
        snake_coor.insert(0, coor)
        snake_rect.insert(0, grid_rect)
    return

def gen_init_snake(coor):
    '''
    step 3-4: 
        畫出開機狀態的蛇
        參數coor：開機狀態的蛇頭grid座標
    '''

    ## 將coor[0], coor[1]分別assign給xgrid, ygrid 以方便計算
    (xgrid, ygrid) = coor

    ## 假設開機狀態蛇身為3個grid，蛇預設前進方向為「向下」
    ## 則先造出(並畫出)出蛇頭，座標為coor或者(xgrid, ygrid)
    ## 接著再造出(並畫出)第二個蛇身，即蛇頭「上方一格」
    ## 接著再造出(並畫出)第三個蛇身，即第二個蛇身的「上方一格」
    ## 示意圖如下，「☒」為蛇頭
    ## ☐ (xgrid, ygrid的上方兩格)
    ## ☐ (xgrid, ygrid的上方一格)
    ## ☒ (xgrid, ygrid)
    add_body1(??)
    add_body1(??)
    add_body1(??)
    return


if __name__ == "__main__":
    gen_win(18, 36, 24)
    draw_walls()

    test_case = [(0, 2), (1, 3), (2, 4), (3, 5), (4, 6), (5, 7), (6, 8), (7, 9), (8, 10), (9, 11), (10, 12), (11, 13), (12, 14), (13, 15), (14, 16), (15, 17), (16, 18), (17, 19), (18, 20), (19, 21), (20, 22), (21, 23), (22, 2), (23, 3), (24, 4), (25, 5), (26, 6), (27, 7), (28, 8), (29, 9), (30, 10), (31, 11), (32, 12), (33, 13), (34, 14), (35, 15)]
    answer_case = [[15.0, 51.0, 32.0, 68.0], [15.0, 33.0, 32.0, 50.0], [15.0, 15.0, 32.0, 32.0], [33.0, 69.0, 50.0, 86.0], [33.0, 51.0, 50.0, 68.0], [33.0, 33.0, 50.0, 50.0], [51.0, 87.0, 68.0, 104.0], [51.0, 69.0, 68.0, 86.0], [51.0, 51.0, 68.0, 68.0], [69.0, 105.0, 86.0, 122.0], [69.0, 87.0, 86.0, 104.0], [69.0, 69.0, 86.0, 86.0], [87.0, 123.0, 104.0, 140.0], [87.0, 105.0, 104.0, 122.0], [87.0, 87.0, 104.0, 104.0], [105.0, 141.0, 122.0, 158.0], [105.0, 123.0, 122.0, 140.0], [105.0, 105.0, 122.0, 122.0], [123.0, 159.0, 140.0, 176.0], [123.0, 141.0, 140.0, 158.0], [123.0, 123.0, 140.0, 140.0], [141.0, 177.0, 158.0, 194.0], [141.0, 159.0, 158.0, 176.0], [141.0, 141.0, 158.0, 158.0], [159.0, 195.0, 176.0, 212.0], [159.0, 177.0, 176.0, 194.0], [159.0, 159.0, 176.0, 176.0], [177.0, 213.0, 194.0, 230.0], [177.0, 195.0, 194.0, 212.0], [177.0, 177.0, 194.0, 194.0], [195.0, 231.0, 212.0, 248.0], [195.0, 213.0, 212.0, 230.0], [195.0, 195.0, 212.0, 212.0], [213.0, 249.0, 230.0, 266.0], [213.0, 231.0, 230.0, 248.0], [213.0, 213.0, 230.0, 230.0], [231.0, 267.0, 248.0, 284.0], [231.0, 249.0, 248.0, 266.0], [231.0, 231.0, 248.0, 248.0], [249.0, 285.0, 266.0, 302.0], [249.0, 267.0, 266.0, 284.0], [249.0, 249.0, 266.0, 266.0], [267.0, 303.0, 284.0, 320.0], [267.0, 285.0, 284.0, 302.0], [267.0, 267.0, 284.0, 284.0], [285.0, 321.0, 302.0, 338.0], [285.0, 303.0, 302.0, 320.0], [285.0, 285.0, 302.0, 302.0], [303.0, 339.0, 320.0, 356.0], [303.0, 321.0, 320.0, 338.0], [303.0, 303.0, 320.0, 320.0], [321.0, 357.0, 338.0, 374.0], [321.0, 339.0, 338.0, 356.0], [321.0, 321.0, 338.0, 338.0], [339.0, 375.0, 356.0, 392.0], [339.0, 357.0, 356.0, 374.0], [339.0, 339.0, 356.0, 356.0], [357.0, 393.0, 374.0, 410.0], [357.0, 375.0, 374.0, 392.0], [357.0, 357.0, 374.0, 374.0], [375.0, 411.0, 392.0, 428.0], [375.0, 393.0, 392.0, 410.0], [375.0, 375.0, 392.0, 392.0], [393.0, 429.0, 410.0, 446.0], [393.0, 411.0, 410.0, 428.0], [393.0, 393.0, 410.0, 410.0], [411.0, 51.0, 428.0, 68.0], [411.0, 33.0, 428.0, 50.0], [411.0, 15.0, 428.0, 32.0], [429.0, 69.0, 446.0, 86.0], [429.0, 51.0, 446.0, 68.0], [429.0, 33.0, 446.0, 50.0], [447.0, 87.0, 464.0, 104.0], [447.0, 69.0, 464.0, 86.0], [447.0, 51.0, 464.0, 68.0], [465.0, 105.0, 482.0, 122.0], [465.0, 87.0, 482.0, 104.0], [465.0, 69.0, 482.0, 86.0], [483.0, 123.0, 500.0, 140.0], [483.0, 105.0, 500.0, 122.0], [483.0, 87.0, 500.0, 104.0], [501.0, 141.0, 518.0, 158.0], [501.0, 123.0, 518.0, 140.0], [501.0, 105.0, 518.0, 122.0], [519.0, 159.0, 536.0, 176.0], [519.0, 141.0, 536.0, 158.0], [519.0, 123.0, 536.0, 140.0], [537.0, 177.0, 554.0, 194.0], [537.0, 159.0, 554.0, 176.0], [537.0, 141.0, 554.0, 158.0], [555.0, 195.0, 572.0, 212.0], [555.0, 177.0, 572.0, 194.0], [555.0, 159.0, 572.0, 176.0], [573.0, 213.0, 590.0, 230.0], [573.0, 195.0, 590.0, 212.0], [573.0, 177.0, 590.0, 194.0], [591.0, 231.0, 608.0, 248.0], [591.0, 213.0, 608.0, 230.0], [591.0, 195.0, 608.0, 212.0], [609.0, 249.0, 626.0, 266.0], [609.0, 231.0, 626.0, 248.0], [609.0, 213.0, 626.0, 230.0], [627.0, 267.0, 644.0, 284.0], [627.0, 249.0, 644.0, 266.0], [627.0, 231.0, 644.0, 248.0], [645.0, 285.0, 662.0, 302.0], [645.0, 267.0, 662.0, 284.0], [645.0, 249.0, 662.0, 266.0]]
    batch_call_function(gen_init_snake, test_case)
    unit_test(canvas.coords, snake_rect, answer_case)
