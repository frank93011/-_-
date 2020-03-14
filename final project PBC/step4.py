from tkinter import *
import random
from unit_test import *

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

    ## 假設開機狀態蛇身為3個grid，蛇預設前進方向為「向下」
    ## 則先造出(並畫出)出蛇頭，座標為coor或者(xgrid, ygrid)
    ## 接著再造出(並畫出)第二個蛇身，即蛇頭「上方一格」
    ## 接著再造出(並畫出)第三個蛇身，即第二個蛇身的「上方一格」
    (xgrid, ygrid) = coor
    add_body1((xgrid, ygrid))
    add_body1((xgrid, ygrid - 1))
    add_body1((xgrid, ygrid - 2))
    return

# food_coor：一個global tuple，用來紀錄食物的grid座標
# food_rect：一個global int，用來紀錄食物在canvas上的rectangle流水號
food_coor = None
food_rect = None
def gen_food():
    '''
    step 4: 
        隨機產生食物grid座標並畫出食物
    '''
    ## 隨機產生的食物座標不能超出遊戲區，而global變數grid_width跟grid_height則代表遊戲區的範圍
    ## 雖然不會去改寫這兩個變數的值，但仍使用「global」關鍵字，提醒我們這兩個變數是global的
    global grid_width
    global grid_height

    ## 由於會改到food_coor、food_rect這兩個global的tuple跟int，因此要加「global」關鍵字
    global food_coor
    global food_rect

    ## 食物的水平方向grid座標x應介於0 ~ grid_width - 1之間
    ## 食物的垂直方向grid座標y應介於0 ~ grid_height - 1之間 
    x = random.randint(??)
    y = random.randint(??)

    ## 將(x, y)組成tuple代表食物座標，並存於global變數food_coor內
    food_coor = (x, y)

    ## 由於food_coor不能重疊於蛇身，因此只要當food_coor跟snake_coor內的任何一個元素一樣
    ## 就要再隨機產生一次座標，直到food_coor不重疊於snake_coor
    ## 提示：對於一個list l，可用e in l 來判斷e是否為l內的一個元素
    ##      例如l = [1, 99, 100]，若e = 99則「e in l」的結果為true，若e為45，則「e in l」為false
    while ??:
        ## 重新隨機產生一次食物座標
        x = random.randint(??)
        y = random.randint(??)
        food_coor = (x, y)
    else:
        ## 既然while迴圈執行結束，表示這時候的food_coor沒有跟蛇身重疊
        ## 那就可以開始來畫新的食物方格了    

        ## 如果canvas上有食物的方格(即food_rect有值，不為0)，則產生新的食物rectangle之前
        ## 應該要把舊的食物方格清除。在canvas上清除已經產生的圖形
        ## 可以用canvas.delete(圖形流水號)，或是canvas.delete(圖形的tag標籤)
        if food_rect:
            canvas.delete(food_rect)

        ## 透過grid_to_pixel(food_grid)可以產生食物grid的左上角px座標，將它存在food_grid_sta變數
        ## 透過grid_br_corner(food_grid_sta)可以產生食物grid右下角座標
        food_grid_sta = ??
        food_grid_end = ??
        
        ## 透過canvas.create_rectangle()畫出食物的方格
        ## 透過fill參數設定食物為'red'，並透過tag參數將食物的方格標記為'food'
        ## 再用food_rect變數紀錄canvas.create_rectangle()的流水號
        food_rect = canvas.create_rectangle(*food_grid_sta, *food_grid_end, fill = 'red', tag = 'food')
        return


if __name__ == "__main__":
    gen_win(18, 36, 24)
    draw_walls()

    test_case = [(0, 0), (0, 1), (0, 2), (0, 3), (0, 4), (0, 5), (0, 6), (0, 7), (0, 8), (0, 9), (0, 10), (0, 11), (0, 12), (0, 13), (0, 14), (0, 15), (0, 16), (0, 17), (0, 18), (0, 19), (0, 20), (0, 21), (0, 22), (0, 23), (1, 0), (1, 1), (1, 2), (1, 3), (1, 4), (1, 5), (1, 6), (1, 7), (1, 8), (1, 9), (1, 10), (1, 11), (1, 12), (1, 13), (1, 14), (1, 15), (1, 16), (1, 17), (1, 18), (1, 19), (1, 20), (1, 21), (1, 22), (1, 23), (2, 0), (2, 1), (2, 2), (2, 3), (2, 4), (2, 5), (2, 6), (2, 7), (2, 8), (2, 9), (2, 10), (2, 11), (2, 12), (2, 13), (2, 14), (2, 15), (2, 16), (2, 17), (2, 18), (2, 19), (2, 20), (2, 21), (2, 22), (2, 23), (3, 0), (3, 1), (3, 2), (3, 3), (3, 4), (3, 5), (3, 6), (3, 7), (3, 8), (3, 9), (3, 10), (3, 11), (3, 12), (3, 13), (3, 14), (3, 15), (3, 16), (3, 17), (3, 18), (3, 19), (3, 20), (3, 21), (3, 22), (3, 23), (4, 0), (4, 1), (4, 2), (4, 3), (4, 4), (4, 5), (4, 6), (4, 7), (4, 8), (4, 9), (4, 10), (4, 11), (4, 12), (4, 13), (4, 14), (4, 15), (4, 16), (4, 17), (4, 18), (4, 19), (4, 20), (4, 21), (4, 22), (4, 23), (5, 0), (5, 1), (5, 2), (5, 3), (5, 4), (5, 5), (5, 6), (5, 7), (5, 8), (5, 9), (5, 10), (5, 11), (5, 12), (5, 13), (5, 14), (5, 15), (5, 16), (5, 17), (5, 18), (5, 19), (5, 20), (5, 21), (5, 22), (5, 23), (6, 0), (6, 1), (6, 2), (6, 3), (6, 4), (6, 5), (6, 6), (6, 7), (6, 8), (6, 9), (6, 10), (6, 11), (6, 12), (6, 13), (6, 14), (6, 15), (6, 16), (6, 17), (6, 18), (6, 19), (6, 20), (6, 21), (6, 22), (6, 23), (7, 0), (7, 1), (7, 2), (7, 3), (7, 4), (7, 5), (7, 6), (7, 7), (7, 8), (7, 9), (7, 10), (7, 11), (7, 12), (7, 13), (7, 14), (7, 15), (7, 16), (7, 17), (7, 18), (7, 19), (7, 20), (7, 21), (7, 22), (7, 23), (8, 0), (8, 1), (8, 2), (8, 3), (8, 4), (8, 5), (8, 6), (8, 7), (8, 8), (8, 9), (8, 10), (8, 11), (8, 12), (8, 13), (8, 14), (8, 15), (8, 16), (8, 17), (8, 18), (8, 19), (8, 20), (8, 21), (8, 22), (8, 23), (9, 0), (9, 1), (9, 2), (9, 3), (9, 4), (9, 5), (9, 6), (9, 7), (9, 8), (9, 9), (9, 10), (9, 11), (9, 12), (9, 13), (9, 14), (9, 15), (9, 16), (9, 17), (9, 18), (9, 19), (9, 20), (9, 21), (9, 22), (9, 23), (10, 0), (10, 1), (10, 2), (10, 3), (10, 4), (10, 5), (10, 6), (10, 7), (10, 8), (10, 9), (10, 10), (10, 11), (10, 12), (10, 13), (10, 14), (10, 15), (10, 16), (10, 17), (10, 18), (10, 19), (10, 20), (10, 21), (10, 22), (10, 23), (11, 0), (11, 1), (11, 2), (11, 3), (11, 4), (11, 5), (11, 6), (11, 7), (11, 8), (11, 9), (11, 10), (11, 11), (11, 12), (11, 13), (11, 14), (11, 15), (11, 16), (11, 17), (11, 18), (11, 19), (11, 20), (11, 21), (11, 22), (11, 23), (12, 0), (12, 1), (12, 2), (12, 3), (12, 4), (12, 5), (12, 6), (12, 7), (12, 8), (12, 9), (12, 10), (12, 11), (12, 12), (12, 13), (12, 14), (12, 15), (12, 16), (12, 17), (12, 18), (12, 19), (12, 20), (12, 21), (12, 22), (12, 23), (13, 0), (13, 1), (13, 2), (13, 3), (13, 4), (13, 5), (13, 6), (13, 7), (13, 8), (13, 9), (13, 10), (13, 11), (13, 12), (13, 13), (13, 14), (13, 15), (13, 16), (13, 17), (13, 18), (13, 19), (13, 20), (13, 21), (13, 22), (13, 23), (14, 0), (14, 1), (14, 2), (14, 3), (14, 4), (14, 5), (14, 6), (14, 7), (14, 8), (14, 9), (14, 10), (14, 11), (14, 12), (14, 13), (14, 14), (14, 15), (14, 16), (14, 17), (14, 18), (14, 19), (14, 20), (14, 21), (14, 22), (14, 23), (15, 0), (15, 1), (15, 2), (15, 3), (15, 4), (15, 5), (15, 6), (15, 7), (15, 8), (15, 9), (15, 10), (15, 11), (15, 12), (15, 13), (15, 14), (15, 15), (15, 16), (15, 17), (15, 18), (15, 19), (15, 20), (15, 21), (15, 22), (15, 23), (16, 0), (16, 1), (16, 2), (16, 3), (16, 4), (16, 5), (16, 6), (16, 7), (16, 8), (16, 9), (16, 10), (16, 11), (16, 12), (16, 13), (16, 14), (16, 15), (16, 16), (16, 17), (16, 18), (16, 19), (16, 20), (16, 21), (16, 22), (16, 23), (17, 0), (17, 1), (17, 2), (17, 3), (17, 4), (17, 5), (17, 6), (17, 7), (17, 8), (17, 9), (17, 10), (17, 11), (17, 12), (17, 13), (17, 14), (17, 15), (17, 16), (17, 17), (17, 18), (17, 19), (17, 20), (17, 21), (17, 22), (17, 23), (18, 0), (18, 1), (18, 2), (18, 3), (18, 4), (18, 5), (18, 6), (18, 7), (18, 8), (18, 9), (18, 10), (18, 11), (18, 12), (18, 13), (18, 14), (18, 15), (18, 16), (18, 17), (18, 18), (18, 19), (18, 20), (18, 21), (18, 22), (18, 23), (19, 0), (19, 1), (19, 2), (19, 3), (19, 4), (19, 5), (19, 6), (19, 7), (19, 8), (19, 9), (19, 10), (19, 11), (19, 12), (19, 13), (19, 14), (19, 15), (19, 16), (19, 17), (19, 18), (19, 19), (19, 20), (19, 21), (19, 22), (19, 23), (20, 0), (20, 1), (20, 2), (20, 3), (20, 4), (20, 5), (20, 6), (20, 7), (20, 8), (20, 9), (20, 10), (20, 11), (20, 12), (20, 13), (20, 14), (20, 15), (20, 16), (20, 17), (20, 18), (20, 19), (20, 20), (20, 21), (20, 22), (20, 23), (21, 0), (21, 1), (21, 2), (21, 3), (21, 4), (21, 5), (21, 6), (21, 7), (21, 8), (21, 9), (21, 10), (21, 11), (21, 12), (21, 13), (21, 14), (21, 15), (21, 16), (21, 17), (21, 18), (21, 19), (21, 20), (21, 21), (21, 22), (21, 23), (22, 0), (22, 1), (22, 2), (22, 3), (22, 4), (22, 5), (22, 6), (22, 7), (22, 8), (22, 9), (22, 10), (22, 11), (22, 12), (22, 13), (22, 14), (22, 15), (22, 16), (22, 17), (22, 18), (22, 19), (22, 20), (22, 21), (22, 22), (22, 23), (23, 0), (23, 1), (23, 2), (23, 3), (23, 4), (23, 5), (23, 6), (23, 7), (23, 8), (23, 9), (23, 10), (23, 11), (23, 12), (23, 13), (23, 14), (23, 15), (23, 16), (23, 17), (23, 18), (23, 19), (23, 20), (23, 21), (23, 22), (23, 23), (24, 0), (24, 1), (24, 2), (24, 3), (24, 4), (24, 5), (24, 6), (24, 7), (24, 8), (24, 9), (24, 10), (24, 11), (24, 12), (24, 13), (24, 14), (24, 15), (24, 16), (24, 17), (24, 18), (24, 19), (24, 20), (24, 21), (24, 22), (24, 23), (25, 0), (25, 1), (25, 2), (25, 3), (25, 4), (25, 5), (25, 6), (25, 7), (25, 8), (25, 9), (25, 10), (25, 11), (25, 12), (25, 13), (25, 14), (25, 15), (25, 16), (25, 17), (25, 18), (25, 19), (25, 20), (25, 21), (25, 22), (25, 23), (26, 0), (26, 1), (26, 2), (26, 3), (26, 4), (26, 5), (26, 6), (26, 7), (26, 8), (26, 9), (26, 10), (26, 11), (26, 12), (26, 13), (26, 14), (26, 15), (26, 16), (26, 17), (26, 18), (26, 19), (26, 20), (26, 21), (26, 22), (26, 23), (27, 0), (27, 1), (27, 2), (27, 3), (27, 4), (27, 5), (27, 6), (27, 7), (27, 8), (27, 9), (27, 10), (27, 11), (27, 12), (27, 13), (27, 14), (27, 15), (27, 16), (27, 17), (27, 18), (27, 19), (27, 20), (27, 21), (27, 22), (27, 23), (28, 0), (28, 1), (28, 2), (28, 3), (28, 4), (28, 5), (28, 6), (28, 7), (28, 8), (28, 9), (28, 10), (28, 11), (28, 12), (28, 13), (28, 14), (28, 15), (28, 16), (28, 17), (28, 18), (28, 19), (28, 20), (28, 21), (28, 22), (28, 23), (29, 0), (29, 1), (29, 2), (29, 3), (29, 4), (29, 5), (29, 6), (29, 7), (29, 8), (29, 9), (29, 10), (29, 11), (29, 12), (29, 13), (29, 14), (29, 15), (29, 16), (29, 17), (29, 18), (29, 19), (29, 20), (29, 21), (29, 22), (29, 23), (30, 0), (30, 1), (30, 2), (30, 3), (30, 4), (30, 5), (30, 6), (30, 7), (30, 8), (30, 9), (30, 10), (30, 11), (30, 12), (30, 13), (30, 14), (30, 15), (30, 16), (30, 17), (30, 18), (30, 19), (30, 20), (30, 21), (30, 22), (30, 23), (31, 0), (31, 1), (31, 2), (31, 3), (31, 4), (31, 5), (31, 6), (31, 7), (31, 8), (31, 9), (31, 10), (31, 11), (31, 12), (31, 13), (31, 14), (31, 15), (31, 16), (31, 17), (31, 18), (31, 19), (31, 20), (31, 21), (31, 22), (31, 23), (32, 0), (32, 1), (32, 2), (32, 3), (32, 4), (32, 5), (32, 6), (32, 7), (32, 8), (32, 9), (32, 10), (32, 11), (32, 12), (32, 13), (32, 14), (32, 15), (32, 16), (32, 17), (32, 18), (32, 19), (32, 20), (32, 21), (32, 22), (32, 23), (33, 0), (33, 1), (33, 2), (33, 3), (33, 4), (33, 5), (33, 6), (33, 7), (33, 8), (33, 9), (33, 10), (33, 11), (33, 12), (33, 13), (33, 14), (33, 15), (33, 16), (33, 17), (33, 18), (33, 19), (33, 20), (33, 21), (33, 22), (33, 23), (34, 0), (34, 1), (34, 2), (34, 3), (34, 4), (34, 5), (34, 6), (34, 7), (34, 8), (34, 9), (34, 10), (34, 11), (34, 12), (34, 13), (34, 14), (34, 15), (34, 16), (34, 17), (34, 18), (34, 19), (34, 20), (34, 21), (34, 22), (34, 23), (35, 0), (35, 1), (35, 2), (35, 3), (35, 4), (35, 5), (35, 6), (35, 7), (35, 8), (35, 9), (35, 10), (35, 11), (35, 12), (35, 13), (35, 14), (35, 15), (35, 16), (35, 17), (35, 18), (35, 19), (35, 20), (35, 21), (35, 22), (35, 23)]
    batch_call_function(add_body1, test_case)

    def test_gen_food(to_skip, fill_body_back = True):
        i = snake_coor.index(to_skip)
        del snake_coor[i]
        canvas.delete(snake_rect[i])
        del snake_rect[i]

        canvas.delete(food_rect)
        gen_food()

        if fill_body_back:
            add_body1(to_skip)
        return food_coor

    unit_test(test_gen_food, test_case, test_case)

    test_gen_food((0, 0), False)


