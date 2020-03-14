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
    ## 會使用到global變數grid_width跟grid_height，代表遊戲區的範圍
    ## 雖然不會去改寫這兩個變數的值，但仍使用「global」關鍵字，提醒我們這兩個變數是global的
    global grid_width
    global grid_height  
    ## 由於會改到food_coor、food_rect這兩個global的tuple跟int，因此要加「global」關鍵字
    global food_coor
    global food_rect

    ## 食物的水平方向grid座標x應介於0 ~ grid_width - 1之間
    ## 食物的垂直方向grid座標y應介於0 ~ grid_height - 1之間
    ## 將(x, y)組成tuple代表食物座標，並存於global變數food_coor內
    x = random.randint(0, grid_width - 1)
    y = random.randint(0, grid_height - 1)
    food_coor = (x, y)

    ## 當food_coor重疊於snake_coor內的任何一個元素，就要重新產生一次座標，直到food_coor不重疊於snake_coor
    while food_coor in snake_coor:
            x = random.randint(0, grid_width - 1)
            y = random.randint(0, grid_height - 1)
            food_coor = (x, y)
    else:
        ## 既然while迴圈執行結束，表示這時候的food_coor沒有跟蛇身重疊
        ## 那就可以開始來畫新的食物方格了    

        ## 如果canvas上有食物的方格(即food_rect有值，不為0)，則產生新的食物rectangle之前
        ## 應該要把舊的食物方格清除
        if food_rect:
            canvas.delete(food_rect)

        ## 因為要畫出食物方格，所以要先準備好食物方格的左上角、右下角px座標好讓canvans可以create_rectangle
        ## food_grid_sta、food_grid_end這兩個變數，分別代表食物方格的左上角、右下角px座標
        food_grid_sta = grid_to_pixel(food_coor)
        food_grid_end = grid_br_corner(food_grid_sta)
 
        ## 透過fill參數設定食物為'red'，並透過tag參數將食物的方格標記為'food'
        ## 再用food_rect變數紀錄canvas.create_rectangle()的流水號       
        food_rect = canvas.create_rectangle(*food_grid_sta, *food_grid_end, fill = 'red', tag = 'food')
        return    

def root_event_handler_bind():
    '''
    step 5-1:
        將root視窗，的事件處理函式跟外部事件繫結
    '''
    ## 設定按壓鍵盤的焦點為root widget
    ## 將按壓鍵盤的外部事件'<Key>'跟處理函式keyboard_handler()繫結
    ## 將關閉視窗的外部事件'WM_DELETE_WINDOW'跟處理函式root_exit()繫結
    root.focus_set()
    root.bind('<Key>', keyboard_handler)
    root.protocol("WM_DELETE_WINDOW", root_exit)
    return

def check_change_dir(key):
    '''
        傳入按鍵(其實是傳入按鍵所代表的字串)
        檢查看看蛇是否需要改變前進的方向，內容先擱置，後續再補
    '''
    pass
    return

def keyboard_handler(event):
    '''
    step 5-2-1:
        按壓鍵盤的外部事件處理函式
        檢查所按壓的鍵盤並紀錄按鍵的代表字串
        參數event：event會記錄「按鍵盤」這個事件，內含event.keysym跟event.keycode等內容
    '''

    ## event.keysym是鍵盤對應的字串
    ## 當event.keysym是按鍵「上」、「下」、「左」、「右」其中一個，才處理
    key = ''
    if event.keysym in ['Up', 'Down', 'Left', 'Right']:
        ## 將event.keysym所代表的字串，丟入chack_change()函式，來檢查蛇的前進方向是否需要改變
        key = event.keysym
        check_change_dir(key)

    return
## game_exit：用來標記視窗關閉是否觸發了，當game_exit為True代表視窗的x被點擊，初始狀態為True
game_exit = False
def root_exit():
    '''
    step 5-2-2:
        a. 透過root.destroy()來關閉視窗
        b. 將game_exit這個控制流程的變數設為True
    '''
    ## 由於會改變 game_exit的值，因此要用「global」關鍵字
    ## 透過root.destroy()來關閉視窗
    global game_exit
    game_exit = True
    root.destroy()

    return

## game_over：用來紀錄遊戲是否在game over狀態的變數，當蛇撞牆或撞到自己時，應設為True
##            初始狀態還未發生，應設為True
## draw_game_over_done：先擱置
## timer_reset：由於迴圈每一回合約為數百微秒，因此在沒有按入方向鍵的情況下
##              設定每60000回合讓蛇前進一格，約略於每0.3秒蛇移動一步
game_over = False
#draw_game_over_done = False
timer_reset = 60000#1200
def loop():
    '''
    step 6:
        遊戲控制流程迴圈
        使用計時器來決定畫面多久更新一次
        a. 當任何外部事件(按鍵盤、關視窗)都沒發生，蛇應該要往原來的方向前進
           當「上」「下」「左」「右」被按時，要「馬上」改變蛇的前進方向，而不是等計時器數完才改變
        b. 蛇移動了以後，要作碰撞判斷(檢查是否撞到牆、撞到自己，或撞到食物)
        c. 蛇移動後表示是個新畫面，因此要用canvas.update()來畫出新畫面
    '''
    ## 由於要用到下列global變數，因此使用「global」關鍵字，提醒我們這些變數是global的
    global timer_reset
    global dir_changed
    global game_over

    ## draw_game_over_done：先擱置
    #global draw_game_over_done

    ## 計時器，沒有按入方向鍵的情況下，每次計時器數到60000時，就讓蛇照著目前的行進方向前進一格
    ## 蛇移動後(不管是透過方向鍵移動，或是計時器數到60000而移動)，都應該要歸0重數
    timer = 0

    ## 由於root視窗開啟之後，只要視窗沒有被關閉(視窗的X沒有被按)就不斷執行的迴圈
    ## 只有當視窗被關閉，即game_exit發生，迴圈才結束
    while not game_exit:

        ## 當game_over(蛇撞自己或撞牆)發生時，呼叫draw_game_over()函式
        ## draw_game_over()是負責畫game over畫面的
        if game_over:
            draw_game_over()
            #if not draw_game_over_done:
            #   draw_game_over()
            #    draw_game_over_done = True

        ## 若非game_over狀態(即遊戲進行中)
        ## 則判斷是因為按壓方向鍵導致蛇要改變方向而移動(dir_changed)
        ## 或是方向沒改變，所以等計時器倒數結束蛇才前進(timer == timer_reset)
        elif dir_changed or timer == timer_reset:
            ## 呼叫move()來讓讓蛇移動到下一格
            ## 移動後呼叫check_hit_things()判斷有無撞到東西
            ## 蛇移動到下一格後，應該要讓timer歸0，重數
            ## 蛇移動後，dir_changed應該要設回False，讓下一個按壓方向鍵的事件來決定是否有改變方向的情形            
            move()
            check_hit_things()
            timer = 0
            dir_changed = False

        ## 每次迴圈都透過canvas.update()來更新畫面            
        canvas.update()
        ## 每次迴圈計時器都應該要加1
        timer += 1
    
    return

## 畫game over畫面的函式，先擱置
def draw_game_over():
    pass

## 算出蛇移動時的下一個grid座標的函式，先擱置
def move():
    pass

## 檢查蛇是否有撞到牆、自己或食物的函式，先擱置
def check_hit_things():
    pass

## dir_changed：用來判斷蛇行進方向是否改變的變數，當蛇改變方向時，應設為True
##              初始狀態應設為False
## now_dir：用來紀錄現在蛇前進的方向，其內容就是方向鍵的代表字串，由於方向只有「上」、「下」、「左」、「右」
##          因此now_dir的值只有4種，即'Up'、'Down'、'Left'、'Right'分別對應「上」、「下」、「左」、「右」
##          預設開機時蛇向下移動，因此初始值為'Down'
dir_changed = False
now_dir = 'Down'
def check_change_dir(key):
    '''
    step 7:
        檢查方向鍵是否造成蛇改變方向(轉彎)，如果蛇蛇改變方向，就要將dir_changed設為True
        好讓loop()函式的迴圈，可以根據dir_changed的狀態做對應的動作
        key：方向鍵的代表字串，'Up'、'Down'、'Left'、'Right'分別對應「上」、「下」、「左」、「右」
    '''
    ## 使用到global變數now_dir、dir_changed
    global now_dir
    global dir_changed

    ## 方向改變的判斷如下：
    ## a. 方向鍵 != 現在前進的方向
    ## b. 方向鍵跟現在行進方向垂直
    ## 當 a. 跟 b. 同時發生(and)，就表示要改變行進的方向

    ## b.條件判斷式很長，因此用4個bool變數來紀錄這些條件
    ## 當方向鍵為「上」，那麼只要現在的行進方向(now_dir)向左或向右，就表示要轉彎向上走
    change_dir_up = key == 'Up' and (now_dir == 'Left' or now_dir == 'Right')
 
    ## 當方向鍵為「下」，那麼只要現在的行進方向(now_dir)向左或向右，就表示要轉彎向下走
    change_dir_down = key == 'Down' and (now_dir == 'Left' or now_dir == 'Right')
 
    ## 當方向鍵為「左」，那麼只要現在的行進方向(now_dir)向上或向下，就表示要轉彎向左走    
    change_dir_left = key == 'Left' and (now_dir == ?? or now_dir == ??)
 
    ## 當方向鍵為「右」，那麼只要現在的行進方向(now_dir)向上或向下，就表示要轉彎向右走        
    change_dir_right = key == 'Right' and (now_dir == ?? or now_dir == ??)

    ## 當 a. 跟 b. 同時發生(and)，就表示要改變行進的方向
    if key != now_dir and (change_dir_up or change_dir_down or change_dir_left or change_dir_right):
        ## 由於方向改變，因此新的now_dir即為鍵盤所按的方向(所代表的字串)，也就是參數key
        now_dir = key
        ## 因為前進方向改變，所以dir_changed要設為True? False?
        dir_changed = ??
    else:
        ## 否則，dir_changed就設為True? False?代表前進方向不變
        dir_changed = ??

    return

if __name__ == "__main__":
    gen_win(18, 36, 24)
    draw_walls()
    gen_init_snake((18, 12))
    gen_food()
    root_event_handler_bind()

    test_case = [(False, 'Up', 'Up'), (False, 'Up', 'Down'), (False, 'Up', 'Left'), (False, 'Up', 'Right'), (False, 'Down', 'Up'), (False, 'Down', 'Down'), (False, 'Down', 'Left'), (False, 'Down', 'Right'), (False, 'Left', 'Up'), (False, 'Left', 'Down'), (False, 'Left', 'Left'), (False, 'Left', 'Right'), (False, 'Right', 'Up'), (False, 'Right', 'Down'), (False, 'Right', 'Left'), (False, 'Right', 'Right')]
    answer_case = [(False, 'Up'), (False, 'Up'), (True, 'Left'), (True, 'Right'), (False, 'Down'), (False, 'Down'), (True, 'Left'), (True, 'Right'), (True, 'Up'), (True, 'Down'), (False, 'Left'), (False, 'Left'), (True, 'Up'), (True, 'Down'), (False, 'Right'), (False, 'Right')]

    def test_check_change_dir(test):
        (d, n, k) = test
        global dir_changed
        global now_dir

        dir_changed = d
        now_dir = n
        check_change_dir(k)
        return (dir_changed, now_dir)

    unit_test(test_check_change_dir, test_case, answer_case)
