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
    

# snake_coor: 一個global list，用來紀錄每格蛇身的grid座標
# snake_rect: 一個global list，用來紀錄蛇身在canvas上的每個rectangle的流水號
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

# food_coor: 一個global tuple，用來紀錄食物的grid座標
# food_rect: 一個global int，用來紀錄食物在canvas上的rectangle流水號
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
    change_dir_up = key == 'Up' and (now_dir == 'Left' or now_dir == 'Right')
    change_dir_down = key == 'Down' and (now_dir == 'Left' or now_dir == 'Right')
    change_dir_left = key == 'Left' and (now_dir == 'Up' or now_dir == 'Down')
    change_dir_right = key == 'Right' and (now_dir == 'Up' or now_dir == 'Down')

    ## 當 a. 跟 b. 同時發生(and)，就表示要改變行進的方向
    if key != now_dir and (change_dir_up or change_dir_down or change_dir_left or change_dir_right):
        ## 由於方向改變，因此新的now_dir即為鍵盤所按的方向(所代表的字串)，也就是參數key
        ## 因為前進方向改變，所以dir_changed要設為True        
        now_dir = key
        dir_changed = True
    else:
        ## 否則，dir_changed就設為False代表前進方向不變
        dir_changed = False

    return

## tail_to_grow：用來紀錄移動前蛇的尾巴grid座標，當蛇前進後吃到食物，會在這個位置長出身體
##               因為tail_to_grow會在body_move1()被呼叫時給設定，但卻在step9_1.py的
##               check_hit_things()被呼叫時才拿來用，因此是個global變數
tail_to_grow = None
def body_move1(coor):
    '''
    step 8-1:
        讓蛇身前進一個grid的函式，會做a、b、c、d四個動作
        參數coor：蛇頭的新座標（是個grid座標）

        註：「舊蛇」指移動前的蛇，「新蛇」指移動後的蛇
        a. 舊蛇頭將移動到新座標，並且要畫出新的矩形，因此要在新座標畫出新蛇頭的grid
        b. 紀錄舊蛇的尾巴座標，當舊蛇前進且撞到食物時，新蛇的身體會成長一格，
           長出來的地方就是剛剛記錄的舊尾巴座標
        c. 刪掉舊蛇的尾巴
        d. 舊蛇除蛇頭、尾巴之外，其他蛇身都保持不變.
    '''

    ## 要改寫global變數tail_to_grow因此使用「global」關鍵字
    global tail_to_grow

    ## 當蛇移動時，新蛇頭如同舊蛇在coor的位置長出一個grid，此外，舊蛇尾消失了

    ## 蛇頭將移動到coor，所以要在coor這個位置畫出新蛇頭，我們可以透過add_body1()添加新蛇頭
    ## 當蛇移動時，新的蛇頭是在舊蛇的前面，因此from_tail參數要設為False
    add_body1(coor, from_tail = False)
    ## 記錄舊的蛇尾座標，如果新蛇頭跟食物重疊，表示撞到食物，吃到食物時會在舊蛇尾的位置長出grid
    tail_to_grow = snake_coor[-1] 

    ## 既然紀錄完舊蛇尾座標，就可以將舊蛇尾座標從snake_coor的尾端去除
    ## 接著從canvas裡面將舊蛇尾巴的矩形從畫面中刪掉，因此透過canvas.delete(「舊蛇尾矩形流水號」)
    ## 來刪除「舊蛇尾矩形流水號」所代表的矩形
    ## 最後再將「舊蛇尾矩形流水號」從snake_rect中去除

    del snake_coor[-1]
    canvas.delete(snake_rect[-1])
    del snake_rect[-1]

    return
    
def move():
    '''
    step 8-2:
        當蛇移動一個grid時，根據現在前進的方向now_dir計算出移動後的座標
        並且在畫面上跟著移動到新座標
    '''

    ## 因為要使用到global變數now_dir，所以用global關鍵字
    ## 將蛇頭的x座標、y座標分別assign給headx、heady
    global now_dir
    (headx, heady) = snake_coor[0]

    ## 如果按照「現在前進的方向(變數now_dir)」，算出移動後蛇頭的新位置
    ## 再將蛇頭的新位置當作參數傳給body_move1()函式，即能得到身體移動到新位置的效果
    if now_dir == 'Up':
        body_move1((headx, heady - 1))

    if now_dir == 'Down':
        body_move1((headx, heady + 1))

    if now_dir == 'Left':
        body_move1((headx - 1, heady))

    if now_dir == 'Right':
        body_move1((headx + 1, heady))

    return

def check_hit_things():
    '''
    step 9-1:
        檢查蛇移動之後，有無撞到東西，基本上就是檢查蛇頭有無撞到東西
        a. 當蛇撞到牆、自己、顯示game over畫面 
        b. 當蛇撞到食物，身體要長長一個grid，並產生新的食物
    '''

    ## 當game over的情況發生時，要設定gobal變數game_over，好讓控制流程的loop()能夠根據這個變數
    ## 切換到對應的執行動作
    global game_over

    ## 我們用hit_walls()、hit_boyd()函式來當作判斷是否有撞到牆的依據
    ## 是否有「撞牆」可用hit_walls()來表示
    ## 是否有「撞自己」可用hit_walls()來表示
    ##
    ## 還要用hit_food()函式來當作是否有撞到食物的依據
    ## 是否有「撞食物」可用hit_food()來表示


    ## 當「撞牆」或「撞自己」：將game_over變數設為True(表示要進入game_over狀態了)
    ## 不然如果「撞到食物」：要使用body_grow()長出尾巴，接著用gen_food()產生新的食物
    ## 否則：就維持原狀，不需做任何事情

    if hit_walls() or hit_body():
        game_over = True
    elif hit_food():
        body_grow()
        gen_food()
    else:
        pass

    return

def hit_walls():
    '''
    step 9-2-1:
        判斷蛇頭有無撞到牆
    '''
    ## 蛇頭座標為snake_coor[0]，分別將蛇頭的x座標、y座標assign給headx, heady 以方便計算
    (headx, heady) = snake_coor[0]

    ## 當headx < 0            代表撞到左牆
    ## 當headx >= grid_witdh  代表撞到右牆
    ## 當heady < 0            代表撞到上牆
    ## 當heady >= grid_height 代表撞到下牆
    ##
    ## 當上述4個條件有「任何一個」成立，就表示蛇有撞到牆
    return headx < 0  or headx >= grid_witdh or heady < 0 or heady >= grid_height

def hit_body():
    '''
    step 9-2-2:
        判斷蛇頭有無撞到頭部以外的身體 
    '''
    ## 蛇頭座標為snake_coor[0]
    ## 蛇頭以外的身體為snake_coor[1 : ]可以透過 in 關鍵字來查詢
    ## snake_coor[0]是否有在snake_coor[1 : ]當中，如果有，表示頭有撞到身體
    return snake_coor[0] in snake_coor[1 : ]

def hit_food():
    '''
    step 9-2-3:
        判斷蛇頭有無撞到食物
    '''
    ## 直接判斷蛇頭座標(snake_coor[0])跟食物座標(food_coor)是否相等
    return snake_coor[0] == food_coor

def body_grow():
    '''
    step 9-3-1:
        當蛇頭撞到食物，在tail_to_grow變數所記錄的座標長尾巴
    '''

    ## 透過add_body1(coor, from_tail)可以幫我們長出一個身體
    ## 新長出來的身體就是global 變數tail_to_grow所記錄的座標
    ## 因此只要將tail_to_grow傳入add_body1()即可
    add_body1(tail_to_grow)
    return

def draw_game_over():
    '''
    step 9-3-2:
        畫出game over畫面
    '''
    ## 先透過canvas.delete(標籤)將畫面上標籤為'snake'、'food'的蛇身與食物刪掉
    canvas.delete('snake')
    canvas.delete('food')

    ## 接著要透過canvas.create_text()來產生'Game Over!'等文字
    ## 由於遊戲畫面的大小可隨使用者去調整，因此文字出現的座標，以及文字的大小都要是可以隨著視窗調整的
    ## 並且文字出現的座標是以px為單位的
    ##
    ## 我們先設定文字出現的位置都是視窗的正中間，因此創造half_width變數
    ## 還記得width變數嗎？它代表整個視窗有多少個px寬，因此
    ## half_width變數應該要是width的一半
    ##
    ## 另外我們也將整個視窗的高度切成6等分，用來調整文字出現的高度
    ## 還記得height變數嗎？它代表整個視窗有多少個px寬，因此
    ## one_sixth_height變數代表height的 1/6
    half_width = int(width / 2)
    one_sixth_height = int(height / 6)

    ## 由於create_text()透過「'自型 字體大小 粗體'」這樣的字串來設定字型
    ## 例如'Consolas 20 bold'就代表要用「Consolas字型、字體大小20、粗體」來表示文字
    ## 我們設定所有文字都要用「Consolas字型、粗體」來顯示，只是有不同大小
    ##
    ## 第一行的文字為'Game Over!'，我們希望他的大小是unit的2倍，因此是unit * 2
    ## 舉例來說若unit為18，字型大小就為36
    ## 別忘了要將unit * 2轉型成str
    ## 接著我們透過字串的「加」，將'Consolas ' 、'36' 、 ' bold'串接起來變成 
    ## 'Consolas 36 bold'，接著將'Consolas 36 bold'存到font_set1這個變數中
    ##
    ## 第二行的文字為'Author: ???? (ɔ)NTUEE'，字型大小為unit的2/3
    ## 舉例來說若unit為18，字型大小就為12，第二行文字最後的設定為'Consolas 12 bold'
    font_set1 = 'Consolas ' + str(unit * 2) + ' bold'
    font_set4 = 'Consolas ' + str(int(unit * 0.67)) + ' bold'

    ## 最後透過canvas.create_text()來擺放文字，
    ## 第一行的設定為：
    ## 擺放位置：(half_width, 2 * one_sixth_height)，也就是水平方向在視窗中央、垂直方向在視窗2/6之處，
    ## 文字：透過text參數設定文字為'Game Over!'
    ## 字型設定：將font參數設為font_set1，也就是'Consolas 36 bold'(當unit為18時)
    ##
    ## 第二行的設定為：
    ## 擺放位置：(half_width, 5 * one_sixth_height)，也就是水平方向在視窗中央、垂直方向在視窗5/6之處，
    ## 文字：透過text參數設定文字為'Author: ???? (ɔ)NTUEE'，請將????改成自己的名字吧
    ## 字型設定：將font參數設為font_set4，也就是'Consolas 12 bold'(當unit為18時)
    canvas.create_text(half_width, 2 * one_sixth_height, text = 'Game Over!', font = font_set1, tag = 'gameover')
    canvas.create_text(half_width, 5 * one_sixth_height, text = 'Author: ???? (ɔ)NTUEE', font = font_set4, tag = 'gameover')
    return 


if __name__ == "__main__":
    gen_win(18, 36, 24)
    draw_walls()
    gen_init_snake((18, 12))
    gen_food()
    root_event_handler_bind()
    loop()




