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

def draw_game_over():
    pass

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

    ## 如果「現在前進的方向(變數now_dir)」為「向上」時，身體會從(headx, heady)移動到(headx, heady - 1)這個位置
    ## 再將(headx, heady - 1)當作參數傳給body_move1()函式，即能得到身體移動到新位置的效果
    if now_dir == 'Up':
        body_move1((headx, heady - 1))

    ## 如果「現在前進的方向(變數now_dir)」為「向下」時，身體會從(headx, heady)移動到(headx, heady + 1)這個位置
    ## 再將(headx, heady + 1)當作參數傳給body_move1()函式，即能得到身體移動到新位置的效果
    if now_dir == 'Down':
        body_move1((headx, ??))

    ## 如果「現在前進的方向(變數now_dir)」為「向左」時，身體會從(headx, heady)移動到(headx - 1, heady)這個位置
    ## 再將(headx - 1, heady)當作參數傳給body_move1()函式，即能得到身體移動到新位置的效果
    if now_dir == 'Left':
        body_move1((??, heady))

    ## 如果「現在前進的方向(變數now_dir)」為「向右」時，身體會從(headx, heady)移動到(headx + 1, heady)這個位置
    ## 再將(headx + 1, heady)當作參數傳給body_move1()函式，即能得到身體移動到新位置的效果
    if now_dir == 'Right':
        body_move1((??, heady))

    return

if __name__ == "__main__":
    gen_win(18, 36, 24)
    draw_walls()
    gen_init_snake((0, 2))
    gen_food()
    root_event_handler_bind()

    test_case = ['Right', 'Up', 'Up', 'Left', 'Down', 'Right', 'Down', 'Left', 'Down', 'Right', 'Down', 'Left', 'Down', 'Right', 'Down', 'Left', 'Down', 'Right', 'Down', 'Left', 'Down', 'Right', 'Down', 'Left', 'Down', 'Right', 'Down', 'Left', 'Down', 'Right', 'Down', 'Left', 'Down', 'Right', 'Down', 'Left', 'Down', 'Right', 'Down', 'Left', 'Down', 'Right', 'Down', 'Left', 'Down', 'Right', 'Down', 'Left', 'Down', 'Right', 'Right', 'Up', 'Right', 'Down', 'Left', 'Up', 'Right', 'Up', 'Left', 'Up', 'Right', 'Up', 'Left', 'Up', 'Right', 'Up', 'Left', 'Up', 'Right', 'Up', 'Left', 'Up', 'Right', 'Up', 'Left', 'Up', 'Right', 'Up', 'Left', 'Up', 'Right', 'Up', 'Left', 'Up', 'Right', 'Up', 'Left', 'Up', 'Right', 'Up', 'Left', 'Up', 'Right', 'Up', 'Left', 'Up', 'Right', 'Up', 'Left', 'Up', 'Right', 'Right', 'Down', 'Right', 'Up', 'Left', 'Down', 'Right', 'Down', 'Left', 'Down', 'Right', 'Down', 'Left', 'Down', 'Right', 'Down', 'Left', 'Down', 'Right', 'Down', 'Left', 'Down', 'Right', 'Down', 'Left', 'Down', 'Right', 'Down', 'Left', 'Down', 'Right', 'Down', 'Left', 'Down', 'Right', 'Down', 'Left', 'Down', 'Right', 'Down', 'Left', 'Down', 'Right', 'Down', 'Left', 'Down', 'Right', 'Down', 'Left', 'Down', 'Right', 'Right', 'Up', 'Right', 'Down', 'Left', 'Up', 'Right', 'Up', 'Left', 'Up', 'Right', 'Up', 'Left', 'Up', 'Right', 'Up', 'Left', 'Up', 'Right', 'Up', 'Left', 'Up', 'Right', 'Up', 'Left', 'Up', 'Right', 'Up', 'Left', 'Up', 'Right', 'Up', 'Left', 'Up', 'Right', 'Up', 'Left', 'Up', 'Right', 'Up', 'Left', 'Up', 'Right', 'Up', 'Left', 'Up', 'Right', 'Up', 'Left', 'Up', 'Right', 'Right', 'Down', 'Right', 'Up', 'Left', 'Down', 'Right', 'Down', 'Left', 'Down', 'Right', 'Down', 'Left', 'Down', 'Right', 'Down', 'Left', 'Down', 'Right', 'Down', 'Left', 'Down', 'Right', 'Down', 'Left', 'Down', 'Right', 'Down', 'Left', 'Down', 'Right', 'Down', 'Left', 'Down', 'Right', 'Down', 'Left', 'Down', 'Right', 'Down', 'Left', 'Down', 'Right', 'Down', 'Left', 'Down', 'Right', 'Down', 'Left', 'Down', 'Right', 'Right', 'Up', 'Right', 'Down', 'Left', 'Up', 'Right', 'Up', 'Left', 'Up', 'Right', 'Up', 'Left', 'Up', 'Right', 'Up', 'Left', 'Up', 'Right', 'Up', 'Left', 'Up', 'Right', 'Up', 'Left', 'Up', 'Right', 'Up', 'Left', 'Up', 'Right', 'Up', 'Left', 'Up', 'Right', 'Up', 'Left', 'Up', 'Right', 'Up', 'Left', 'Up', 'Right', 'Up', 'Left', 'Up', 'Right', 'Up', 'Left', 'Up', 'Right', 'Right', 'Down', 'Right', 'Up', 'Left', 'Down', 'Right', 'Down', 'Left', 'Down', 'Right', 'Down', 'Left', 'Down', 'Right', 'Down', 'Left', 'Down', 'Right', 'Down', 'Left', 'Down', 'Right', 'Down', 'Left', 'Down', 'Right', 'Down', 'Left', 'Down', 'Right', 'Down', 'Left', 'Down', 'Right', 'Down', 'Left', 'Down', 'Right', 'Down', 'Left', 'Down', 'Right', 'Down', 'Left', 'Down', 'Right', 'Down', 'Left', 'Down', 'Right', 'Right', 'Up', 'Right', 'Down', 'Left', 'Up', 'Right', 'Up', 'Left', 'Up', 'Right', 'Up', 'Left', 'Up', 'Right', 'Up', 'Left', 'Up', 'Right', 'Up', 'Left', 'Up', 'Right', 'Up', 'Left', 'Up', 'Right', 'Up', 'Left', 'Up', 'Right', 'Up', 'Left', 'Up', 'Right', 'Up', 'Left', 'Up', 'Right', 'Up', 'Left', 'Up', 'Right', 'Up', 'Left', 'Up', 'Right', 'Up', 'Left', 'Up', 'Right', 'Right', 'Down', 'Right', 'Up', 'Left', 'Down', 'Right', 'Down', 'Left', 'Down', 'Right', 'Down', 'Left', 'Down', 'Right', 'Down', 'Left', 'Down', 'Right', 'Down', 'Left', 'Down', 'Right', 'Down', 'Left', 'Down', 'Right', 'Down', 'Left', 'Down', 'Right', 'Down', 'Left', 'Down', 'Right', 'Down', 'Left', 'Down', 'Right', 'Down', 'Left', 'Down', 'Right', 'Down', 'Left', 'Down', 'Right', 'Down', 'Left', 'Down', 'Right', 'Right', 'Up', 'Right', 'Down', 'Left', 'Up', 'Right', 'Up', 'Left', 'Up', 'Right', 'Up', 'Left', 'Up', 'Right', 'Up', 'Left', 'Up', 'Right', 'Up', 'Left', 'Up', 'Right', 'Up', 'Left', 'Up', 'Right', 'Up', 'Left', 'Up', 'Right', 'Up', 'Left', 'Up', 'Right', 'Up', 'Left', 'Up', 'Right', 'Up', 'Left', 'Up', 'Right', 'Up', 'Left', 'Up', 'Right', 'Up', 'Left', 'Up', 'Right', 'Right', 'Down', 'Right', 'Up', 'Left', 'Down', 'Right', 'Down', 'Left', 'Down', 'Right', 'Down', 'Left', 'Down', 'Right', 'Down', 'Left', 'Down', 'Right', 'Down', 'Left', 'Down', 'Right', 'Down', 'Left', 'Down', 'Right', 'Down', 'Left', 'Down', 'Right', 'Down', 'Left', 'Down', 'Right', 'Down', 'Left', 'Down', 'Right', 'Down', 'Left', 'Down', 'Right', 'Down', 'Left', 'Down', 'Right', 'Down', 'Left', 'Down', 'Right', 'Right', 'Up', 'Right', 'Down', 'Left', 'Up', 'Right', 'Up', 'Left', 'Up', 'Right', 'Up', 'Left', 'Up', 'Right', 'Up', 'Left', 'Up', 'Right', 'Up', 'Left', 'Up', 'Right', 'Up', 'Left', 'Up', 'Right', 'Up', 'Left', 'Up', 'Right', 'Up', 'Left', 'Up', 'Right', 'Up', 'Left', 'Up', 'Right', 'Up', 'Left', 'Up', 'Right', 'Up', 'Left', 'Up', 'Right', 'Up', 'Left', 'Up', 'Right', 'Right', 'Down', 'Right', 'Up', 'Left', 'Down', 'Right', 'Down', 'Left', 'Down', 'Right', 'Down', 'Left', 'Down', 'Right', 'Down', 'Left', 'Down', 'Right', 'Down', 'Left', 'Down', 'Right', 'Down', 'Left', 'Down', 'Right', 'Down', 'Left', 'Down', 'Right', 'Down', 'Left', 'Down', 'Right', 'Down', 'Left', 'Down', 'Right', 'Down', 'Left', 'Down', 'Right', 'Down', 'Left', 'Down', 'Right', 'Down', 'Left', 'Down', 'Right', 'Right', 'Up', 'Right', 'Down', 'Left', 'Up', 'Right', 'Up', 'Left', 'Up', 'Right', 'Up', 'Left', 'Up', 'Right', 'Up', 'Left', 'Up', 'Right', 'Up', 'Left', 'Up', 'Right', 'Up', 'Left', 'Up', 'Right', 'Up', 'Left', 'Up', 'Right', 'Up', 'Left', 'Up', 'Right', 'Up', 'Left', 'Up', 'Right', 'Up', 'Left', 'Up', 'Right', 'Up', 'Left', 'Up', 'Right', 'Up', 'Left', 'Up', 'Right', 'Right', 'Down', 'Right', 'Up', 'Left', 'Down', 'Right', 'Down', 'Left', 'Down', 'Right', 'Down', 'Left', 'Down', 'Right', 'Down', 'Left', 'Down', 'Right', 'Down', 'Left', 'Down', 'Right', 'Down', 'Left', 'Down', 'Right', 'Down', 'Left', 'Down', 'Right', 'Down', 'Left', 'Down', 'Right', 'Down', 'Left', 'Down', 'Right', 'Down', 'Left', 'Down', 'Right', 'Down', 'Left', 'Down', 'Right', 'Down', 'Left', 'Down', 'Right', 'Right', 'Up', 'Right', 'Down', 'Left', 'Up', 'Right', 'Up', 'Left', 'Up', 'Right', 'Up', 'Left', 'Up', 'Right', 'Up', 'Left', 'Up', 'Right', 'Up', 'Left', 'Up', 'Right', 'Up', 'Left', 'Up', 'Right', 'Up', 'Left', 'Up', 'Right', 'Up', 'Left', 'Up', 'Right', 'Up', 'Left', 'Up', 'Right', 'Up', 'Left', 'Up', 'Right', 'Up', 'Left', 'Up', 'Right', 'Up', 'Left', 'Up', 'Right', 'Right', 'Down', 'Right', 'Up', 'Left', 'Down', 'Right', 'Down', 'Left', 'Down', 'Right', 'Down', 'Left', 'Down', 'Right', 'Down', 'Left', 'Down', 'Right', 'Down', 'Left', 'Down', 'Right', 'Down', 'Left', 'Down', 'Right', 'Down', 'Left', 'Down', 'Right', 'Down', 'Left', 'Down', 'Right', 'Down', 'Left', 'Down', 'Right', 'Down', 'Left', 'Down', 'Right', 'Down', 'Left', 'Down', 'Right', 'Down', 'Left', 'Down', 'Right', 'Right', 'Up', 'Right', 'Down', 'Left', 'Up', 'Right', 'Up', 'Left', 'Up', 'Right', 'Up', 'Left', 'Up', 'Right', 'Up', 'Left', 'Up', 'Right', 'Up', 'Left', 'Up', 'Right', 'Up', 'Left', 'Up', 'Right', 'Up', 'Left', 'Up', 'Right', 'Up', 'Left', 'Up', 'Right', 'Up', 'Left', 'Up', 'Right', 'Up', 'Left', 'Up', 'Right', 'Up', 'Left', 'Up', 'Right', 'Up', 'Left', 'Up', 'Right']
    answer_case = [((0, 0), [(1, 2), (0, 2), (0, 1)], [9, 5, 6]), ((0, 1), [(1, 1), (1, 2), (0, 2)], [10, 9, 5]), ((0, 2), [(1, 0), (1, 1), (1, 2)], [11, 10, 9]), ((1, 2), [(0, 0), (1, 0), (1, 1)], [12, 11, 10]), ((1, 1), [(0, 1), (0, 0), (1, 0)], [13, 12, 11]), ((1, 0), [(1, 1), (0, 1), (0, 0)], [14, 13, 12]), ((0, 0), [(1, 2), (1, 1), (0, 1)], [15, 14, 13]), ((0, 1), [(0, 2), (1, 2), (1, 1)], [16, 15, 14]), ((1, 1), [(0, 3), (0, 2), (1, 2)], [17, 16, 15]), ((1, 2), [(1, 3), (0, 3), (0, 2)], [18, 17, 16]), ((0, 2), [(1, 4), (1, 3), (0, 3)], [19, 18, 17]), ((0, 3), [(0, 4), (1, 4), (1, 3)], [20, 19, 18]), ((1, 3), [(0, 5), (0, 4), (1, 4)], [21, 20, 19]), ((1, 4), [(1, 5), (0, 5), (0, 4)], [22, 21, 20]), ((0, 4), [(1, 6), (1, 5), (0, 5)], [23, 22, 21]), ((0, 5), [(0, 6), (1, 6), (1, 5)], [24, 23, 22]), ((1, 5), [(0, 7), (0, 6), (1, 6)], [25, 24, 23]), ((1, 6), [(1, 7), (0, 7), (0, 6)], [26, 25, 24]), ((0, 6), [(1, 8), (1, 7), (0, 7)], [27, 26, 25]), ((0, 7), [(0, 8), (1, 8), (1, 7)], [28, 27, 26]), ((1, 7), [(0, 9), (0, 8), (1, 8)], [29, 28, 27]), ((1, 8), [(1, 9), (0, 9), (0, 8)], [30, 29, 28]), ((0, 8), [(1, 10), (1, 9), (0, 9)], [31, 30, 29]), ((0, 9), [(0, 10), (1, 10), (1, 9)], [32, 31, 30]), ((1, 9), [(0, 11), (0, 10), (1, 10)], [33, 32, 31]), ((1, 10), [(1, 11), (0, 11), (0, 10)], [34, 33, 32]), ((0, 10), [(1, 12), (1, 11), (0, 11)], [35, 34, 33]), ((0, 11), [(0, 12), (1, 12), (1, 11)], [36, 35, 34]), ((1, 11), [(0, 13), (0, 12), (1, 12)], [37, 36, 35]), ((1, 12), [(1, 13), (0, 13), (0, 12)], [38, 37, 36]), ((0, 12), [(1, 14), (1, 13), (0, 13)], [39, 38, 37]), ((0, 13), [(0, 14), (1, 14), (1, 13)], [40, 39, 38]), ((1, 13), [(0, 15), (0, 14), (1, 14)], [41, 40, 39]), ((1, 14), [(1, 15), (0, 15), (0, 14)], [42, 41, 40]), ((0, 14), [(1, 16), (1, 15), (0, 15)], [43, 42, 41]), ((0, 15), [(0, 16), (1, 16), (1, 15)], [44, 43, 42]), ((1, 15), [(0, 17), (0, 16), (1, 16)], [45, 44, 43]), ((1, 16), [(1, 17), (0, 17), (0, 16)], [46, 45, 44]), ((0, 16), [(1, 18), (1, 17), (0, 17)], [47, 46, 45]), ((0, 17), [(0, 18), (1, 18), (1, 17)], [48, 47, 46]), ((1, 17), [(0, 19), (0, 18), (1, 18)], [49, 48, 47]), ((1, 18), [(1, 19), (0, 19), (0, 18)], [50, 49, 48]), ((0, 18), [(1, 20), (1, 19), (0, 19)], [51, 50, 49]), ((0, 19), [(0, 20), (1, 20), (1, 19)], [52, 51, 50]), ((1, 19), [(0, 21), (0, 20), (1, 20)], [53, 52, 51]), ((1, 20), [(1, 21), (0, 21), (0, 20)], [54, 53, 52]), ((0, 20), [(1, 22), (1, 21), (0, 21)], [55, 54, 53]), ((0, 21), [(0, 22), (1, 22), (1, 21)], [56, 55, 54]), ((1, 21), [(0, 23), (0, 22), (1, 22)], [57, 56, 55]), ((1, 22), [(1, 23), (0, 23), (0, 22)], [58, 57, 56]), ((0, 22), [(2, 23), (1, 23), (0, 23)], [59, 58, 57]), ((0, 23), [(2, 22), (2, 23), (1, 23)], [60, 59, 58]), ((1, 23), [(3, 22), (2, 22), (2, 23)], [61, 60, 59]), ((2, 23), [(3, 23), (3, 22), (2, 22)], [62, 61, 60]), ((2, 22), [(2, 23), (3, 23), (3, 22)], [63, 62, 61]), ((3, 22), [(2, 22), (2, 23), (3, 23)], [64, 63, 62]), ((3, 23), [(3, 22), (2, 22), (2, 23)], [65, 64, 63]), ((2, 23), [(3, 21), (3, 22), (2, 22)], [66, 65, 64]), ((2, 22), [(2, 21), (3, 21), (3, 22)], [67, 66, 65]), ((3, 22), [(2, 20), (2, 21), (3, 21)], [68, 67, 66]), ((3, 21), [(3, 20), (2, 20), (2, 21)], [69, 68, 67]), ((2, 21), [(3, 19), (3, 20), (2, 20)], [70, 69, 68]), ((2, 20), [(2, 19), (3, 19), (3, 20)], [71, 70, 69]), ((3, 20), [(2, 18), (2, 19), (3, 19)], [72, 71, 70]), ((3, 19), [(3, 18), (2, 18), (2, 19)], [73, 72, 71]), ((2, 19), [(3, 17), (3, 18), (2, 18)], [74, 73, 72]), ((2, 18), [(2, 17), (3, 17), (3, 18)], [75, 74, 73]), ((3, 18), [(2, 16), (2, 17), (3, 17)], [76, 75, 74]), ((3, 17), [(3, 16), (2, 16), (2, 17)], [77, 76, 75]), ((2, 17), [(3, 15), (3, 16), (2, 16)], [78, 77, 76]), ((2, 16), [(2, 15), (3, 15), (3, 16)], [79, 78, 77]), ((3, 16), [(2, 14), (2, 15), (3, 15)], [80, 79, 78]), ((3, 15), [(3, 14), (2, 14), (2, 15)], [81, 80, 79]), ((2, 15), [(3, 13), (3, 14), (2, 14)], [82, 81, 80]), ((2, 14), [(2, 13), (3, 13), (3, 14)], [83, 82, 81]), ((3, 14), [(2, 12), (2, 13), (3, 13)], [84, 83, 82]), ((3, 13), [(3, 12), (2, 12), (2, 13)], [85, 84, 83]), ((2, 13), [(3, 11), (3, 12), (2, 12)], [86, 85, 84]), ((2, 12), [(2, 11), (3, 11), (3, 12)], [87, 86, 85]), ((3, 12), [(2, 10), (2, 11), (3, 11)], [88, 87, 86]), ((3, 11), [(3, 10), (2, 10), (2, 11)], [89, 88, 87]), ((2, 11), [(3, 9), (3, 10), (2, 10)], [90, 89, 88]), ((2, 10), [(2, 9), (3, 9), (3, 10)], [91, 90, 89]), ((3, 10), [(2, 8), (2, 9), (3, 9)], [92, 91, 90]), ((3, 9), [(3, 8), (2, 8), (2, 9)], [93, 92, 91]), ((2, 9), [(3, 7), (3, 8), (2, 8)], [94, 93, 92]), ((2, 8), [(2, 7), (3, 7), (3, 8)], [95, 94, 93]), ((3, 8), [(2, 6), (2, 7), (3, 7)], [96, 95, 94]), ((3, 7), [(3, 6), (2, 6), (2, 7)], [97, 96, 95]), ((2, 7), [(3, 5), (3, 6), (2, 6)], [98, 97, 96]), ((2, 6), [(2, 5), (3, 5), (3, 6)], [99, 98, 97]), ((3, 6), [(2, 4), (2, 5), (3, 5)], [100, 99, 98]), ((3, 5), [(3, 4), (2, 4), (2, 5)], [101, 100, 99]), ((2, 5), [(3, 3), (3, 4), (2, 4)], [102, 101, 100]), ((2, 4), [(2, 3), (3, 3), (3, 4)], [103, 102, 101]), ((3, 4), [(2, 2), (2, 3), (3, 3)], [104, 103, 102]), ((3, 3), [(3, 2), (2, 2), (2, 3)], [105, 104, 103]), ((2, 3), [(3, 1), (3, 2), (2, 2)], [106, 105, 104]), ((2, 2), [(2, 1), (3, 1), (3, 2)], [107, 106, 105]), ((3, 2), [(2, 0), (2, 1), (3, 1)], [108, 107, 106]), ((3, 1), [(3, 0), (2, 0), (2, 1)], [109, 108, 107]), ((2, 1), [(4, 0), (3, 0), (2, 0)], [110, 109, 108]), ((2, 0), [(4, 1), (4, 0), (3, 0)], [111, 110, 109]), ((3, 0), [(5, 1), (4, 1), (4, 0)], [112, 111, 110]), ((4, 0), [(5, 0), (5, 1), (4, 1)], [113, 112, 111]), ((4, 1), [(4, 0), (5, 0), (5, 1)], [114, 113, 112]), ((5, 1), [(4, 1), (4, 0), (5, 0)], [115, 114, 113]), ((5, 0), [(5, 1), (4, 1), (4, 0)], [116, 115, 114]), ((4, 0), [(5, 2), (5, 1), (4, 1)], [117, 116, 115]), ((4, 1), [(4, 2), (5, 2), (5, 1)], [118, 117, 116]), ((5, 1), [(4, 3), (4, 2), (5, 2)], [119, 118, 117]), ((5, 2), [(5, 3), (4, 3), (4, 2)], [120, 119, 118]), ((4, 2), [(5, 4), (5, 3), (4, 3)], [121, 120, 119]), ((4, 3), [(4, 4), (5, 4), (5, 3)], [122, 121, 120]), ((5, 3), [(4, 5), (4, 4), (5, 4)], [123, 122, 121]), ((5, 4), [(5, 5), (4, 5), (4, 4)], [124, 123, 122]), ((4, 4), [(5, 6), (5, 5), (4, 5)], [125, 124, 123]), ((4, 5), [(4, 6), (5, 6), (5, 5)], [126, 125, 124]), ((5, 5), [(4, 7), (4, 6), (5, 6)], [127, 126, 125]), ((5, 6), [(5, 7), (4, 7), (4, 6)], [128, 127, 126]), ((4, 6), [(5, 8), (5, 7), (4, 7)], [129, 128, 127]), ((4, 7), [(4, 8), (5, 8), (5, 7)], [130, 129, 128]), ((5, 7), [(4, 9), (4, 8), (5, 8)], [131, 130, 129]), ((5, 8), [(5, 9), (4, 9), (4, 8)], [132, 131, 130]), ((4, 8), [(5, 10), (5, 9), (4, 9)], [133, 132, 131]), ((4, 9), [(4, 10), (5, 10), (5, 9)], [134, 133, 132]), ((5, 9), [(4, 11), (4, 10), (5, 10)], [135, 134, 133]), ((5, 10), [(5, 11), (4, 11), (4, 10)], [136, 135, 134]), ((4, 10), [(5, 12), (5, 11), (4, 11)], [137, 136, 135]), ((4, 11), [(4, 12), (5, 12), (5, 11)], [138, 137, 136]), ((5, 11), [(4, 13), (4, 12), (5, 12)], [139, 138, 137]), ((5, 12), [(5, 13), (4, 13), (4, 12)], [140, 139, 138]), ((4, 12), [(5, 14), (5, 13), (4, 13)], [141, 140, 139]), ((4, 13), [(4, 14), (5, 14), (5, 13)], [142, 141, 140]), ((5, 13), [(4, 15), (4, 14), (5, 14)], [143, 142, 141]), ((5, 14), [(5, 15), (4, 15), (4, 14)], [144, 143, 142]), ((4, 14), [(5, 16), (5, 15), (4, 15)], [145, 144, 143]), ((4, 15), [(4, 16), (5, 16), (5, 15)], [146, 145, 144]), ((5, 15), [(4, 17), (4, 16), (5, 16)], [147, 146, 145]), ((5, 16), [(5, 17), (4, 17), (4, 16)], [148, 147, 146]), ((4, 16), [(5, 18), (5, 17), (4, 17)], [149, 148, 147]), ((4, 17), [(4, 18), (5, 18), (5, 17)], [150, 149, 148]), ((5, 17), [(4, 19), (4, 18), (5, 18)], [151, 150, 149]), ((5, 18), [(5, 19), (4, 19), (4, 18)], [152, 151, 150]), ((4, 18), [(5, 20), (5, 19), (4, 19)], [153, 152, 151]), ((4, 19), [(4, 20), (5, 20), (5, 19)], [154, 153, 152]), ((5, 19), [(4, 21), (4, 20), (5, 20)], [155, 154, 153]), ((5, 20), [(5, 21), (4, 21), (4, 20)], [156, 155, 154]), ((4, 20), [(5, 22), (5, 21), (4, 21)], [157, 156, 155]), ((4, 21), [(4, 22), (5, 22), (5, 21)], [158, 157, 156]), ((5, 21), [(4, 23), (4, 22), (5, 22)], [159, 158, 157]), ((5, 22), [(5, 23), (4, 23), (4, 22)], [160, 159, 158]), ((4, 22), [(6, 23), (5, 23), (4, 23)], [161, 160, 159]), ((4, 23), [(6, 22), (6, 23), (5, 23)], [162, 161, 160]), ((5, 23), [(7, 22), (6, 22), (6, 23)], [163, 162, 161]), ((6, 23), [(7, 23), (7, 22), (6, 22)], [164, 163, 162]), ((6, 22), [(6, 23), (7, 23), (7, 22)], [165, 164, 163]), ((7, 22), [(6, 22), (6, 23), (7, 23)], [166, 165, 164]), ((7, 23), [(7, 22), (6, 22), (6, 23)], [167, 166, 165]), ((6, 23), [(7, 21), (7, 22), (6, 22)], [168, 167, 166]), ((6, 22), [(6, 21), (7, 21), (7, 22)], [169, 168, 167]), ((7, 22), [(6, 20), (6, 21), (7, 21)], [170, 169, 168]), ((7, 21), [(7, 20), (6, 20), (6, 21)], [171, 170, 169]), ((6, 21), [(7, 19), (7, 20), (6, 20)], [172, 171, 170]), ((6, 20), [(6, 19), (7, 19), (7, 20)], [173, 172, 171]), ((7, 20), [(6, 18), (6, 19), (7, 19)], [174, 173, 172]), ((7, 19), [(7, 18), (6, 18), (6, 19)], [175, 174, 173]), ((6, 19), [(7, 17), (7, 18), (6, 18)], [176, 175, 174]), ((6, 18), [(6, 17), (7, 17), (7, 18)], [177, 176, 175]), ((7, 18), [(6, 16), (6, 17), (7, 17)], [178, 177, 176]), ((7, 17), [(7, 16), (6, 16), (6, 17)], [179, 178, 177]), ((6, 17), [(7, 15), (7, 16), (6, 16)], [180, 179, 178]), ((6, 16), [(6, 15), (7, 15), (7, 16)], [181, 180, 179]), ((7, 16), [(6, 14), (6, 15), (7, 15)], [182, 181, 180]), ((7, 15), [(7, 14), (6, 14), (6, 15)], [183, 182, 181]), ((6, 15), [(7, 13), (7, 14), (6, 14)], [184, 183, 182]), ((6, 14), [(6, 13), (7, 13), (7, 14)], [185, 184, 183]), ((7, 14), [(6, 12), (6, 13), (7, 13)], [186, 185, 184]), ((7, 13), [(7, 12), (6, 12), (6, 13)], [187, 186, 185]), ((6, 13), [(7, 11), (7, 12), (6, 12)], [188, 187, 186]), ((6, 12), [(6, 11), (7, 11), (7, 12)], [189, 188, 187]), ((7, 12), [(6, 10), (6, 11), (7, 11)], [190, 189, 188]), ((7, 11), [(7, 10), (6, 10), (6, 11)], [191, 190, 189]), ((6, 11), [(7, 9), (7, 10), (6, 10)], [192, 191, 190]), ((6, 10), [(6, 9), (7, 9), (7, 10)], [193, 192, 191]), ((7, 10), [(6, 8), (6, 9), (7, 9)], [194, 193, 192]), ((7, 9), [(7, 8), (6, 8), (6, 9)], [195, 194, 193]), ((6, 9), [(7, 7), (7, 8), (6, 8)], [196, 195, 194]), ((6, 8), [(6, 7), (7, 7), (7, 8)], [197, 196, 195]), ((7, 8), [(6, 6), (6, 7), (7, 7)], [198, 197, 196]), ((7, 7), [(7, 6), (6, 6), (6, 7)], [199, 198, 197]), ((6, 7), [(7, 5), (7, 6), (6, 6)], [200, 199, 198]), ((6, 6), [(6, 5), (7, 5), (7, 6)], [201, 200, 199]), ((7, 6), [(6, 4), (6, 5), (7, 5)], [202, 201, 200]), ((7, 5), [(7, 4), (6, 4), (6, 5)], [203, 202, 201]), ((6, 5), [(7, 3), (7, 4), (6, 4)], [204, 203, 202]), ((6, 4), [(6, 3), (7, 3), (7, 4)], [205, 204, 203]), ((7, 4), [(6, 2), (6, 3), (7, 3)], [206, 205, 204]), ((7, 3), [(7, 2), (6, 2), (6, 3)], [207, 206, 205]), ((6, 3), [(7, 1), (7, 2), (6, 2)], [208, 207, 206]), ((6, 2), [(6, 1), (7, 1), (7, 2)], [209, 208, 207]), ((7, 2), [(6, 0), (6, 1), (7, 1)], [210, 209, 208]), ((7, 1), [(7, 0), (6, 0), (6, 1)], [211, 210, 209]), ((6, 1), [(8, 0), (7, 0), (6, 0)], [212, 211, 210]), ((6, 0), [(8, 1), (8, 0), (7, 0)], [213, 212, 211]), ((7, 0), [(9, 1), (8, 1), (8, 0)], [214, 213, 212]), ((8, 0), [(9, 0), (9, 1), (8, 1)], [215, 214, 213]), ((8, 1), [(8, 0), (9, 0), (9, 1)], [216, 215, 214]), ((9, 1), [(8, 1), (8, 0), (9, 0)], [217, 216, 215]), ((9, 0), [(9, 1), (8, 1), (8, 0)], [218, 217, 216]), ((8, 0), [(9, 2), (9, 1), (8, 1)], [219, 218, 217]), ((8, 1), [(8, 2), (9, 2), (9, 1)], [220, 219, 218]), ((9, 1), [(8, 3), (8, 2), (9, 2)], [221, 220, 219]), ((9, 2), [(9, 3), (8, 3), (8, 2)], [222, 221, 220]), ((8, 2), [(9, 4), (9, 3), (8, 3)], [223, 222, 221]), ((8, 3), [(8, 4), (9, 4), (9, 3)], [224, 223, 222]), ((9, 3), [(8, 5), (8, 4), (9, 4)], [225, 224, 223]), ((9, 4), [(9, 5), (8, 5), (8, 4)], [226, 225, 224]), ((8, 4), [(9, 6), (9, 5), (8, 5)], [227, 226, 225]), ((8, 5), [(8, 6), (9, 6), (9, 5)], [228, 227, 226]), ((9, 5), [(8, 7), (8, 6), (9, 6)], [229, 228, 227]), ((9, 6), [(9, 7), (8, 7), (8, 6)], [230, 229, 228]), ((8, 6), [(9, 8), (9, 7), (8, 7)], [231, 230, 229]), ((8, 7), [(8, 8), (9, 8), (9, 7)], [232, 231, 230]), ((9, 7), [(8, 9), (8, 8), (9, 8)], [233, 232, 231]), ((9, 8), [(9, 9), (8, 9), (8, 8)], [234, 233, 232]), ((8, 8), [(9, 10), (9, 9), (8, 9)], [235, 234, 233]), ((8, 9), [(8, 10), (9, 10), (9, 9)], [236, 235, 234]), ((9, 9), [(8, 11), (8, 10), (9, 10)], [237, 236, 235]), ((9, 10), [(9, 11), (8, 11), (8, 10)], [238, 237, 236]), ((8, 10), [(9, 12), (9, 11), (8, 11)], [239, 238, 237]), ((8, 11), [(8, 12), (9, 12), (9, 11)], [240, 239, 238]), ((9, 11), [(8, 13), (8, 12), (9, 12)], [241, 240, 239]), ((9, 12), [(9, 13), (8, 13), (8, 12)], [242, 241, 240]), ((8, 12), [(9, 14), (9, 13), (8, 13)], [243, 242, 241]), ((8, 13), [(8, 14), (9, 14), (9, 13)], [244, 243, 242]), ((9, 13), [(8, 15), (8, 14), (9, 14)], [245, 244, 243]), ((9, 14), [(9, 15), (8, 15), (8, 14)], [246, 245, 244]), ((8, 14), [(9, 16), (9, 15), (8, 15)], [247, 246, 245]), ((8, 15), [(8, 16), (9, 16), (9, 15)], [248, 247, 246]), ((9, 15), [(8, 17), (8, 16), (9, 16)], [249, 248, 247]), ((9, 16), [(9, 17), (8, 17), (8, 16)], [250, 249, 248]), ((8, 16), [(9, 18), (9, 17), (8, 17)], [251, 250, 249]), ((8, 17), [(8, 18), (9, 18), (9, 17)], [252, 251, 250]), ((9, 17), [(8, 19), (8, 18), (9, 18)], [253, 252, 251]), ((9, 18), [(9, 19), (8, 19), (8, 18)], [254, 253, 252]), ((8, 18), [(9, 20), (9, 19), (8, 19)], [255, 254, 253]), ((8, 19), [(8, 20), (9, 20), (9, 19)], [256, 255, 254]), ((9, 19), [(8, 21), (8, 20), (9, 20)], [257, 256, 255]), ((9, 20), [(9, 21), (8, 21), (8, 20)], [258, 257, 256]), ((8, 20), [(9, 22), (9, 21), (8, 21)], [259, 258, 257]), ((8, 21), [(8, 22), (9, 22), (9, 21)], [260, 259, 258]), ((9, 21), [(8, 23), (8, 22), (9, 22)], [261, 260, 259]), ((9, 22), [(9, 23), (8, 23), (8, 22)], [262, 261, 260]), ((8, 22), [(10, 23), (9, 23), (8, 23)], [263, 262, 261]), ((8, 23), [(10, 22), (10, 23), (9, 23)], [264, 263, 262]), ((9, 23), [(11, 22), (10, 22), (10, 23)], [265, 264, 263]), ((10, 23), [(11, 23), (11, 22), (10, 22)], [266, 265, 264]), ((10, 22), [(10, 23), (11, 23), (11, 22)], [267, 266, 265]), ((11, 22), [(10, 22), (10, 23), (11, 23)], [268, 267, 266]), ((11, 23), [(11, 22), (10, 22), (10, 23)], [269, 268, 267]), ((10, 23), [(11, 21), (11, 22), (10, 22)], [270, 269, 268]), ((10, 22), [(10, 21), (11, 21), (11, 22)], [271, 270, 269]), ((11, 22), [(10, 20), (10, 21), (11, 21)], [272, 271, 270]), ((11, 21), [(11, 20), (10, 20), (10, 21)], [273, 272, 271]), ((10, 21), [(11, 19), (11, 20), (10, 20)], [274, 273, 272]), ((10, 20), [(10, 19), (11, 19), (11, 20)], [275, 274, 273]), ((11, 20), [(10, 18), (10, 19), (11, 19)], [276, 275, 274]), ((11, 19), [(11, 18), (10, 18), (10, 19)], [277, 276, 275]), ((10, 19), [(11, 17), (11, 18), (10, 18)], [278, 277, 276]), ((10, 18), [(10, 17), (11, 17), (11, 18)], [279, 278, 277]), ((11, 18), [(10, 16), (10, 17), (11, 17)], [280, 279, 278]), ((11, 17), [(11, 16), (10, 16), (10, 17)], [281, 280, 279]), ((10, 17), [(11, 15), (11, 16), (10, 16)], [282, 281, 280]), ((10, 16), [(10, 15), (11, 15), (11, 16)], [283, 282, 281]), ((11, 16), [(10, 14), (10, 15), (11, 15)], [284, 283, 282]), ((11, 15), [(11, 14), (10, 14), (10, 15)], [285, 284, 283]), ((10, 15), [(11, 13), (11, 14), (10, 14)], [286, 285, 284]), ((10, 14), [(10, 13), (11, 13), (11, 14)], [287, 286, 285]), ((11, 14), [(10, 12), (10, 13), (11, 13)], [288, 287, 286]), ((11, 13), [(11, 12), (10, 12), (10, 13)], [289, 288, 287]), ((10, 13), [(11, 11), (11, 12), (10, 12)], [290, 289, 288]), ((10, 12), [(10, 11), (11, 11), (11, 12)], [291, 290, 289]), ((11, 12), [(10, 10), (10, 11), (11, 11)], [292, 291, 290]), ((11, 11), [(11, 10), (10, 10), (10, 11)], [293, 292, 291]), ((10, 11), [(11, 9), (11, 10), (10, 10)], [294, 293, 292]), ((10, 10), [(10, 9), (11, 9), (11, 10)], [295, 294, 293]), ((11, 10), [(10, 8), (10, 9), (11, 9)], [296, 295, 294]), ((11, 9), [(11, 8), (10, 8), (10, 9)], [297, 296, 295]), ((10, 9), [(11, 7), (11, 8), (10, 8)], [298, 297, 296]), ((10, 8), [(10, 7), (11, 7), (11, 8)], [299, 298, 297]), ((11, 8), [(10, 6), (10, 7), (11, 7)], [300, 299, 298]), ((11, 7), [(11, 6), (10, 6), (10, 7)], [301, 300, 299]), ((10, 7), [(11, 5), (11, 6), (10, 6)], [302, 301, 300]), ((10, 6), [(10, 5), (11, 5), (11, 6)], [303, 302, 301]), ((11, 6), [(10, 4), (10, 5), (11, 5)], [304, 303, 302]), ((11, 5), [(11, 4), (10, 4), (10, 5)], [305, 304, 303]), ((10, 5), [(11, 3), (11, 4), (10, 4)], [306, 305, 304]), ((10, 4), [(10, 3), (11, 3), (11, 4)], [307, 306, 305]), ((11, 4), [(10, 2), (10, 3), (11, 3)], [308, 307, 306]), ((11, 3), [(11, 2), (10, 2), (10, 3)], [309, 308, 307]), ((10, 3), [(11, 1), (11, 2), (10, 2)], [310, 309, 308]), ((10, 2), [(10, 1), (11, 1), (11, 2)], [311, 310, 309]), ((11, 2), [(10, 0), (10, 1), (11, 1)], [312, 311, 310]), ((11, 1), [(11, 0), (10, 0), (10, 1)], [313, 312, 311]), ((10, 1), [(12, 0), (11, 0), (10, 0)], [314, 313, 312]), ((10, 0), [(12, 1), (12, 0), (11, 0)], [315, 314, 313]), ((11, 0), [(13, 1), (12, 1), (12, 0)], [316, 315, 314]), ((12, 0), [(13, 0), (13, 1), (12, 1)], [317, 316, 315]), ((12, 1), [(12, 0), (13, 0), (13, 1)], [318, 317, 316]), ((13, 1), [(12, 1), (12, 0), (13, 0)], [319, 318, 317]), ((13, 0), [(13, 1), (12, 1), (12, 0)], [320, 319, 318]), ((12, 0), [(13, 2), (13, 1), (12, 1)], [321, 320, 319]), ((12, 1), [(12, 2), (13, 2), (13, 1)], [322, 321, 320]), ((13, 1), [(12, 3), (12, 2), (13, 2)], [323, 322, 321]), ((13, 2), [(13, 3), (12, 3), (12, 2)], [324, 323, 322]), ((12, 2), [(13, 4), (13, 3), (12, 3)], [325, 324, 323]), ((12, 3), [(12, 4), (13, 4), (13, 3)], [326, 325, 324]), ((13, 3), [(12, 5), (12, 4), (13, 4)], [327, 326, 325]), ((13, 4), [(13, 5), (12, 5), (12, 4)], [328, 327, 326]), ((12, 4), [(13, 6), (13, 5), (12, 5)], [329, 328, 327]), ((12, 5), [(12, 6), (13, 6), (13, 5)], [330, 329, 328]), ((13, 5), [(12, 7), (12, 6), (13, 6)], [331, 330, 329]), ((13, 6), [(13, 7), (12, 7), (12, 6)], [332, 331, 330]), ((12, 6), [(13, 8), (13, 7), (12, 7)], [333, 332, 331]), ((12, 7), [(12, 8), (13, 8), (13, 7)], [334, 333, 332]), ((13, 7), [(12, 9), (12, 8), (13, 8)], [335, 334, 333]), ((13, 8), [(13, 9), (12, 9), (12, 8)], [336, 335, 334]), ((12, 8), [(13, 10), (13, 9), (12, 9)], [337, 336, 335]), ((12, 9), [(12, 10), (13, 10), (13, 9)], [338, 337, 336]), ((13, 9), [(12, 11), (12, 10), (13, 10)], [339, 338, 337]), ((13, 10), [(13, 11), (12, 11), (12, 10)], [340, 339, 338]), ((12, 10), [(13, 12), (13, 11), (12, 11)], [341, 340, 339]), ((12, 11), [(12, 12), (13, 12), (13, 11)], [342, 341, 340]), ((13, 11), [(12, 13), (12, 12), (13, 12)], [343, 342, 341]), ((13, 12), [(13, 13), (12, 13), (12, 12)], [344, 343, 342]), ((12, 12), [(13, 14), (13, 13), (12, 13)], [345, 344, 343]), ((12, 13), [(12, 14), (13, 14), (13, 13)], [346, 345, 344]), ((13, 13), [(12, 15), (12, 14), (13, 14)], [347, 346, 345]), ((13, 14), [(13, 15), (12, 15), (12, 14)], [348, 347, 346]), ((12, 14), [(13, 16), (13, 15), (12, 15)], [349, 348, 347]), ((12, 15), [(12, 16), (13, 16), (13, 15)], [350, 349, 348]), ((13, 15), [(12, 17), (12, 16), (13, 16)], [351, 350, 349]), ((13, 16), [(13, 17), (12, 17), (12, 16)], [352, 351, 350]), ((12, 16), [(13, 18), (13, 17), (12, 17)], [353, 352, 351]), ((12, 17), [(12, 18), (13, 18), (13, 17)], [354, 353, 352]), ((13, 17), [(12, 19), (12, 18), (13, 18)], [355, 354, 353]), ((13, 18), [(13, 19), (12, 19), (12, 18)], [356, 355, 354]), ((12, 18), [(13, 20), (13, 19), (12, 19)], [357, 356, 355]), ((12, 19), [(12, 20), (13, 20), (13, 19)], [358, 357, 356]), ((13, 19), [(12, 21), (12, 20), (13, 20)], [359, 358, 357]), ((13, 20), [(13, 21), (12, 21), (12, 20)], [360, 359, 358]), ((12, 20), [(13, 22), (13, 21), (12, 21)], [361, 360, 359]), ((12, 21), [(12, 22), (13, 22), (13, 21)], [362, 361, 360]), ((13, 21), [(12, 23), (12, 22), (13, 22)], [363, 362, 361]), ((13, 22), [(13, 23), (12, 23), (12, 22)], [364, 363, 362]), ((12, 22), [(14, 23), (13, 23), (12, 23)], [365, 364, 363]), ((12, 23), [(14, 22), (14, 23), (13, 23)], [366, 365, 364]), ((13, 23), [(15, 22), (14, 22), (14, 23)], [367, 366, 365]), ((14, 23), [(15, 23), (15, 22), (14, 22)], [368, 367, 366]), ((14, 22), [(14, 23), (15, 23), (15, 22)], [369, 368, 367]), ((15, 22), [(14, 22), (14, 23), (15, 23)], [370, 369, 368]), ((15, 23), [(15, 22), (14, 22), (14, 23)], [371, 370, 369]), ((14, 23), [(15, 21), (15, 22), (14, 22)], [372, 371, 370]), ((14, 22), [(14, 21), (15, 21), (15, 22)], [373, 372, 371]), ((15, 22), [(14, 20), (14, 21), (15, 21)], [374, 373, 372]), ((15, 21), [(15, 20), (14, 20), (14, 21)], [375, 374, 373]), ((14, 21), [(15, 19), (15, 20), (14, 20)], [376, 375, 374]), ((14, 20), [(14, 19), (15, 19), (15, 20)], [377, 376, 375]), ((15, 20), [(14, 18), (14, 19), (15, 19)], [378, 377, 376]), ((15, 19), [(15, 18), (14, 18), (14, 19)], [379, 378, 377]), ((14, 19), [(15, 17), (15, 18), (14, 18)], [380, 379, 378]), ((14, 18), [(14, 17), (15, 17), (15, 18)], [381, 380, 379]), ((15, 18), [(14, 16), (14, 17), (15, 17)], [382, 381, 380]), ((15, 17), [(15, 16), (14, 16), (14, 17)], [383, 382, 381]), ((14, 17), [(15, 15), (15, 16), (14, 16)], [384, 383, 382]), ((14, 16), [(14, 15), (15, 15), (15, 16)], [385, 384, 383]), ((15, 16), [(14, 14), (14, 15), (15, 15)], [386, 385, 384]), ((15, 15), [(15, 14), (14, 14), (14, 15)], [387, 386, 385]), ((14, 15), [(15, 13), (15, 14), (14, 14)], [388, 387, 386]), ((14, 14), [(14, 13), (15, 13), (15, 14)], [389, 388, 387]), ((15, 14), [(14, 12), (14, 13), (15, 13)], [390, 389, 388]), ((15, 13), [(15, 12), (14, 12), (14, 13)], [391, 390, 389]), ((14, 13), [(15, 11), (15, 12), (14, 12)], [392, 391, 390]), ((14, 12), [(14, 11), (15, 11), (15, 12)], [393, 392, 391]), ((15, 12), [(14, 10), (14, 11), (15, 11)], [394, 393, 392]), ((15, 11), [(15, 10), (14, 10), (14, 11)], [395, 394, 393]), ((14, 11), [(15, 9), (15, 10), (14, 10)], [396, 395, 394]), ((14, 10), [(14, 9), (15, 9), (15, 10)], [397, 396, 395]), ((15, 10), [(14, 8), (14, 9), (15, 9)], [398, 397, 396]), ((15, 9), [(15, 8), (14, 8), (14, 9)], [399, 398, 397]), ((14, 9), [(15, 7), (15, 8), (14, 8)], [400, 399, 398]), ((14, 8), [(14, 7), (15, 7), (15, 8)], [401, 400, 399]), ((15, 8), [(14, 6), (14, 7), (15, 7)], [402, 401, 400]), ((15, 7), [(15, 6), (14, 6), (14, 7)], [403, 402, 401]), ((14, 7), [(15, 5), (15, 6), (14, 6)], [404, 403, 402]), ((14, 6), [(14, 5), (15, 5), (15, 6)], [405, 404, 403]), ((15, 6), [(14, 4), (14, 5), (15, 5)], [406, 405, 404]), ((15, 5), [(15, 4), (14, 4), (14, 5)], [407, 406, 405]), ((14, 5), [(15, 3), (15, 4), (14, 4)], [408, 407, 406]), ((14, 4), [(14, 3), (15, 3), (15, 4)], [409, 408, 407]), ((15, 4), [(14, 2), (14, 3), (15, 3)], [410, 409, 408]), ((15, 3), [(15, 2), (14, 2), (14, 3)], [411, 410, 409]), ((14, 3), [(15, 1), (15, 2), (14, 2)], [412, 411, 410]), ((14, 2), [(14, 1), (15, 1), (15, 2)], [413, 412, 411]), ((15, 2), [(14, 0), (14, 1), (15, 1)], [414, 413, 412]), ((15, 1), [(15, 0), (14, 0), (14, 1)], [415, 414, 413]), ((14, 1), [(16, 0), (15, 0), (14, 0)], [416, 415, 414]), ((14, 0), [(16, 1), (16, 0), (15, 0)], [417, 416, 415]), ((15, 0), [(17, 1), (16, 1), (16, 0)], [418, 417, 416]), ((16, 0), [(17, 0), (17, 1), (16, 1)], [419, 418, 417]), ((16, 1), [(16, 0), (17, 0), (17, 1)], [420, 419, 418]), ((17, 1), [(16, 1), (16, 0), (17, 0)], [421, 420, 419]), ((17, 0), [(17, 1), (16, 1), (16, 0)], [422, 421, 420]), ((16, 0), [(17, 2), (17, 1), (16, 1)], [423, 422, 421]), ((16, 1), [(16, 2), (17, 2), (17, 1)], [424, 423, 422]), ((17, 1), [(16, 3), (16, 2), (17, 2)], [425, 424, 423]), ((17, 2), [(17, 3), (16, 3), (16, 2)], [426, 425, 424]), ((16, 2), [(17, 4), (17, 3), (16, 3)], [427, 426, 425]), ((16, 3), [(16, 4), (17, 4), (17, 3)], [428, 427, 426]), ((17, 3), [(16, 5), (16, 4), (17, 4)], [429, 428, 427]), ((17, 4), [(17, 5), (16, 5), (16, 4)], [430, 429, 428]), ((16, 4), [(17, 6), (17, 5), (16, 5)], [431, 430, 429]), ((16, 5), [(16, 6), (17, 6), (17, 5)], [432, 431, 430]), ((17, 5), [(16, 7), (16, 6), (17, 6)], [433, 432, 431]), ((17, 6), [(17, 7), (16, 7), (16, 6)], [434, 433, 432]), ((16, 6), [(17, 8), (17, 7), (16, 7)], [435, 434, 433]), ((16, 7), [(16, 8), (17, 8), (17, 7)], [436, 435, 434]), ((17, 7), [(16, 9), (16, 8), (17, 8)], [437, 436, 435]), ((17, 8), [(17, 9), (16, 9), (16, 8)], [438, 437, 436]), ((16, 8), [(17, 10), (17, 9), (16, 9)], [439, 438, 437]), ((16, 9), [(16, 10), (17, 10), (17, 9)], [440, 439, 438]), ((17, 9), [(16, 11), (16, 10), (17, 10)], [441, 440, 439]), ((17, 10), [(17, 11), (16, 11), (16, 10)], [442, 441, 440]), ((16, 10), [(17, 12), (17, 11), (16, 11)], [443, 442, 441]), ((16, 11), [(16, 12), (17, 12), (17, 11)], [444, 443, 442]), ((17, 11), [(16, 13), (16, 12), (17, 12)], [445, 444, 443]), ((17, 12), [(17, 13), (16, 13), (16, 12)], [446, 445, 444]), ((16, 12), [(17, 14), (17, 13), (16, 13)], [447, 446, 445]), ((16, 13), [(16, 14), (17, 14), (17, 13)], [448, 447, 446]), ((17, 13), [(16, 15), (16, 14), (17, 14)], [449, 448, 447]), ((17, 14), [(17, 15), (16, 15), (16, 14)], [450, 449, 448]), ((16, 14), [(17, 16), (17, 15), (16, 15)], [451, 450, 449]), ((16, 15), [(16, 16), (17, 16), (17, 15)], [452, 451, 450]), ((17, 15), [(16, 17), (16, 16), (17, 16)], [453, 452, 451]), ((17, 16), [(17, 17), (16, 17), (16, 16)], [454, 453, 452]), ((16, 16), [(17, 18), (17, 17), (16, 17)], [455, 454, 453]), ((16, 17), [(16, 18), (17, 18), (17, 17)], [456, 455, 454]), ((17, 17), [(16, 19), (16, 18), (17, 18)], [457, 456, 455]), ((17, 18), [(17, 19), (16, 19), (16, 18)], [458, 457, 456]), ((16, 18), [(17, 20), (17, 19), (16, 19)], [459, 458, 457]), ((16, 19), [(16, 20), (17, 20), (17, 19)], [460, 459, 458]), ((17, 19), [(16, 21), (16, 20), (17, 20)], [461, 460, 459]), ((17, 20), [(17, 21), (16, 21), (16, 20)], [462, 461, 460]), ((16, 20), [(17, 22), (17, 21), (16, 21)], [463, 462, 461]), ((16, 21), [(16, 22), (17, 22), (17, 21)], [464, 463, 462]), ((17, 21), [(16, 23), (16, 22), (17, 22)], [465, 464, 463]), ((17, 22), [(17, 23), (16, 23), (16, 22)], [466, 465, 464]), ((16, 22), [(18, 23), (17, 23), (16, 23)], [467, 466, 465]), ((16, 23), [(18, 22), (18, 23), (17, 23)], [468, 467, 466]), ((17, 23), [(19, 22), (18, 22), (18, 23)], [469, 468, 467]), ((18, 23), [(19, 23), (19, 22), (18, 22)], [470, 469, 468]), ((18, 22), [(18, 23), (19, 23), (19, 22)], [471, 470, 469]), ((19, 22), [(18, 22), (18, 23), (19, 23)], [472, 471, 470]), ((19, 23), [(19, 22), (18, 22), (18, 23)], [473, 472, 471]), ((18, 23), [(19, 21), (19, 22), (18, 22)], [474, 473, 472]), ((18, 22), [(18, 21), (19, 21), (19, 22)], [475, 474, 473]), ((19, 22), [(18, 20), (18, 21), (19, 21)], [476, 475, 474]), ((19, 21), [(19, 20), (18, 20), (18, 21)], [477, 476, 475]), ((18, 21), [(19, 19), (19, 20), (18, 20)], [478, 477, 476]), ((18, 20), [(18, 19), (19, 19), (19, 20)], [479, 478, 477]), ((19, 20), [(18, 18), (18, 19), (19, 19)], [480, 479, 478]), ((19, 19), [(19, 18), (18, 18), (18, 19)], [481, 480, 479]), ((18, 19), [(19, 17), (19, 18), (18, 18)], [482, 481, 480]), ((18, 18), [(18, 17), (19, 17), (19, 18)], [483, 482, 481]), ((19, 18), [(18, 16), (18, 17), (19, 17)], [484, 483, 482]), ((19, 17), [(19, 16), (18, 16), (18, 17)], [485, 484, 483]), ((18, 17), [(19, 15), (19, 16), (18, 16)], [486, 485, 484]), ((18, 16), [(18, 15), (19, 15), (19, 16)], [487, 486, 485]), ((19, 16), [(18, 14), (18, 15), (19, 15)], [488, 487, 486]), ((19, 15), [(19, 14), (18, 14), (18, 15)], [489, 488, 487]), ((18, 15), [(19, 13), (19, 14), (18, 14)], [490, 489, 488]), ((18, 14), [(18, 13), (19, 13), (19, 14)], [491, 490, 489]), ((19, 14), [(18, 12), (18, 13), (19, 13)], [492, 491, 490]), ((19, 13), [(19, 12), (18, 12), (18, 13)], [493, 492, 491]), ((18, 13), [(19, 11), (19, 12), (18, 12)], [494, 493, 492]), ((18, 12), [(18, 11), (19, 11), (19, 12)], [495, 494, 493]), ((19, 12), [(18, 10), (18, 11), (19, 11)], [496, 495, 494]), ((19, 11), [(19, 10), (18, 10), (18, 11)], [497, 496, 495]), ((18, 11), [(19, 9), (19, 10), (18, 10)], [498, 497, 496]), ((18, 10), [(18, 9), (19, 9), (19, 10)], [499, 498, 497]), ((19, 10), [(18, 8), (18, 9), (19, 9)], [500, 499, 498]), ((19, 9), [(19, 8), (18, 8), (18, 9)], [501, 500, 499]), ((18, 9), [(19, 7), (19, 8), (18, 8)], [502, 501, 500]), ((18, 8), [(18, 7), (19, 7), (19, 8)], [503, 502, 501]), ((19, 8), [(18, 6), (18, 7), (19, 7)], [504, 503, 502]), ((19, 7), [(19, 6), (18, 6), (18, 7)], [505, 504, 503]), ((18, 7), [(19, 5), (19, 6), (18, 6)], [506, 505, 504]), ((18, 6), [(18, 5), (19, 5), (19, 6)], [507, 506, 505]), ((19, 6), [(18, 4), (18, 5), (19, 5)], [508, 507, 506]), ((19, 5), [(19, 4), (18, 4), (18, 5)], [509, 508, 507]), ((18, 5), [(19, 3), (19, 4), (18, 4)], [510, 509, 508]), ((18, 4), [(18, 3), (19, 3), (19, 4)], [511, 510, 509]), ((19, 4), [(18, 2), (18, 3), (19, 3)], [512, 511, 510]), ((19, 3), [(19, 2), (18, 2), (18, 3)], [513, 512, 511]), ((18, 3), [(19, 1), (19, 2), (18, 2)], [514, 513, 512]), ((18, 2), [(18, 1), (19, 1), (19, 2)], [515, 514, 513]), ((19, 2), [(18, 0), (18, 1), (19, 1)], [516, 515, 514]), ((19, 1), [(19, 0), (18, 0), (18, 1)], [517, 516, 515]), ((18, 1), [(20, 0), (19, 0), (18, 0)], [518, 517, 516]), ((18, 0), [(20, 1), (20, 0), (19, 0)], [519, 518, 517]), ((19, 0), [(21, 1), (20, 1), (20, 0)], [520, 519, 518]), ((20, 0), [(21, 0), (21, 1), (20, 1)], [521, 520, 519]), ((20, 1), [(20, 0), (21, 0), (21, 1)], [522, 521, 520]), ((21, 1), [(20, 1), (20, 0), (21, 0)], [523, 522, 521]), ((21, 0), [(21, 1), (20, 1), (20, 0)], [524, 523, 522]), ((20, 0), [(21, 2), (21, 1), (20, 1)], [525, 524, 523]), ((20, 1), [(20, 2), (21, 2), (21, 1)], [526, 525, 524]), ((21, 1), [(20, 3), (20, 2), (21, 2)], [527, 526, 525]), ((21, 2), [(21, 3), (20, 3), (20, 2)], [528, 527, 526]), ((20, 2), [(21, 4), (21, 3), (20, 3)], [529, 528, 527]), ((20, 3), [(20, 4), (21, 4), (21, 3)], [530, 529, 528]), ((21, 3), [(20, 5), (20, 4), (21, 4)], [531, 530, 529]), ((21, 4), [(21, 5), (20, 5), (20, 4)], [532, 531, 530]), ((20, 4), [(21, 6), (21, 5), (20, 5)], [533, 532, 531]), ((20, 5), [(20, 6), (21, 6), (21, 5)], [534, 533, 532]), ((21, 5), [(20, 7), (20, 6), (21, 6)], [535, 534, 533]), ((21, 6), [(21, 7), (20, 7), (20, 6)], [536, 535, 534]), ((20, 6), [(21, 8), (21, 7), (20, 7)], [537, 536, 535]), ((20, 7), [(20, 8), (21, 8), (21, 7)], [538, 537, 536]), ((21, 7), [(20, 9), (20, 8), (21, 8)], [539, 538, 537]), ((21, 8), [(21, 9), (20, 9), (20, 8)], [540, 539, 538]), ((20, 8), [(21, 10), (21, 9), (20, 9)], [541, 540, 539]), ((20, 9), [(20, 10), (21, 10), (21, 9)], [542, 541, 540]), ((21, 9), [(20, 11), (20, 10), (21, 10)], [543, 542, 541]), ((21, 10), [(21, 11), (20, 11), (20, 10)], [544, 543, 542]), ((20, 10), [(21, 12), (21, 11), (20, 11)], [545, 544, 543]), ((20, 11), [(20, 12), (21, 12), (21, 11)], [546, 545, 544]), ((21, 11), [(20, 13), (20, 12), (21, 12)], [547, 546, 545]), ((21, 12), [(21, 13), (20, 13), (20, 12)], [548, 547, 546]), ((20, 12), [(21, 14), (21, 13), (20, 13)], [549, 548, 547]), ((20, 13), [(20, 14), (21, 14), (21, 13)], [550, 549, 548]), ((21, 13), [(20, 15), (20, 14), (21, 14)], [551, 550, 549]), ((21, 14), [(21, 15), (20, 15), (20, 14)], [552, 551, 550]), ((20, 14), [(21, 16), (21, 15), (20, 15)], [553, 552, 551]), ((20, 15), [(20, 16), (21, 16), (21, 15)], [554, 553, 552]), ((21, 15), [(20, 17), (20, 16), (21, 16)], [555, 554, 553]), ((21, 16), [(21, 17), (20, 17), (20, 16)], [556, 555, 554]), ((20, 16), [(21, 18), (21, 17), (20, 17)], [557, 556, 555]), ((20, 17), [(20, 18), (21, 18), (21, 17)], [558, 557, 556]), ((21, 17), [(20, 19), (20, 18), (21, 18)], [559, 558, 557]), ((21, 18), [(21, 19), (20, 19), (20, 18)], [560, 559, 558]), ((20, 18), [(21, 20), (21, 19), (20, 19)], [561, 560, 559]), ((20, 19), [(20, 20), (21, 20), (21, 19)], [562, 561, 560]), ((21, 19), [(20, 21), (20, 20), (21, 20)], [563, 562, 561]), ((21, 20), [(21, 21), (20, 21), (20, 20)], [564, 563, 562]), ((20, 20), [(21, 22), (21, 21), (20, 21)], [565, 564, 563]), ((20, 21), [(20, 22), (21, 22), (21, 21)], [566, 565, 564]), ((21, 21), [(20, 23), (20, 22), (21, 22)], [567, 566, 565]), ((21, 22), [(21, 23), (20, 23), (20, 22)], [568, 567, 566]), ((20, 22), [(22, 23), (21, 23), (20, 23)], [569, 568, 567]), ((20, 23), [(22, 22), (22, 23), (21, 23)], [570, 569, 568]), ((21, 23), [(23, 22), (22, 22), (22, 23)], [571, 570, 569]), ((22, 23), [(23, 23), (23, 22), (22, 22)], [572, 571, 570]), ((22, 22), [(22, 23), (23, 23), (23, 22)], [573, 572, 571]), ((23, 22), [(22, 22), (22, 23), (23, 23)], [574, 573, 572]), ((23, 23), [(23, 22), (22, 22), (22, 23)], [575, 574, 573]), ((22, 23), [(23, 21), (23, 22), (22, 22)], [576, 575, 574]), ((22, 22), [(22, 21), (23, 21), (23, 22)], [577, 576, 575]), ((23, 22), [(22, 20), (22, 21), (23, 21)], [578, 577, 576]), ((23, 21), [(23, 20), (22, 20), (22, 21)], [579, 578, 577]), ((22, 21), [(23, 19), (23, 20), (22, 20)], [580, 579, 578]), ((22, 20), [(22, 19), (23, 19), (23, 20)], [581, 580, 579]), ((23, 20), [(22, 18), (22, 19), (23, 19)], [582, 581, 580]), ((23, 19), [(23, 18), (22, 18), (22, 19)], [583, 582, 581]), ((22, 19), [(23, 17), (23, 18), (22, 18)], [584, 583, 582]), ((22, 18), [(22, 17), (23, 17), (23, 18)], [585, 584, 583]), ((23, 18), [(22, 16), (22, 17), (23, 17)], [586, 585, 584]), ((23, 17), [(23, 16), (22, 16), (22, 17)], [587, 586, 585]), ((22, 17), [(23, 15), (23, 16), (22, 16)], [588, 587, 586]), ((22, 16), [(22, 15), (23, 15), (23, 16)], [589, 588, 587]), ((23, 16), [(22, 14), (22, 15), (23, 15)], [590, 589, 588]), ((23, 15), [(23, 14), (22, 14), (22, 15)], [591, 590, 589]), ((22, 15), [(23, 13), (23, 14), (22, 14)], [592, 591, 590]), ((22, 14), [(22, 13), (23, 13), (23, 14)], [593, 592, 591]), ((23, 14), [(22, 12), (22, 13), (23, 13)], [594, 593, 592]), ((23, 13), [(23, 12), (22, 12), (22, 13)], [595, 594, 593]), ((22, 13), [(23, 11), (23, 12), (22, 12)], [596, 595, 594]), ((22, 12), [(22, 11), (23, 11), (23, 12)], [597, 596, 595]), ((23, 12), [(22, 10), (22, 11), (23, 11)], [598, 597, 596]), ((23, 11), [(23, 10), (22, 10), (22, 11)], [599, 598, 597]), ((22, 11), [(23, 9), (23, 10), (22, 10)], [600, 599, 598]), ((22, 10), [(22, 9), (23, 9), (23, 10)], [601, 600, 599]), ((23, 10), [(22, 8), (22, 9), (23, 9)], [602, 601, 600]), ((23, 9), [(23, 8), (22, 8), (22, 9)], [603, 602, 601]), ((22, 9), [(23, 7), (23, 8), (22, 8)], [604, 603, 602]), ((22, 8), [(22, 7), (23, 7), (23, 8)], [605, 604, 603]), ((23, 8), [(22, 6), (22, 7), (23, 7)], [606, 605, 604]), ((23, 7), [(23, 6), (22, 6), (22, 7)], [607, 606, 605]), ((22, 7), [(23, 5), (23, 6), (22, 6)], [608, 607, 606]), ((22, 6), [(22, 5), (23, 5), (23, 6)], [609, 608, 607]), ((23, 6), [(22, 4), (22, 5), (23, 5)], [610, 609, 608]), ((23, 5), [(23, 4), (22, 4), (22, 5)], [611, 610, 609]), ((22, 5), [(23, 3), (23, 4), (22, 4)], [612, 611, 610]), ((22, 4), [(22, 3), (23, 3), (23, 4)], [613, 612, 611]), ((23, 4), [(22, 2), (22, 3), (23, 3)], [614, 613, 612]), ((23, 3), [(23, 2), (22, 2), (22, 3)], [615, 614, 613]), ((22, 3), [(23, 1), (23, 2), (22, 2)], [616, 615, 614]), ((22, 2), [(22, 1), (23, 1), (23, 2)], [617, 616, 615]), ((23, 2), [(22, 0), (22, 1), (23, 1)], [618, 617, 616]), ((23, 1), [(23, 0), (22, 0), (22, 1)], [619, 618, 617]), ((22, 1), [(24, 0), (23, 0), (22, 0)], [620, 619, 618]), ((22, 0), [(24, 1), (24, 0), (23, 0)], [621, 620, 619]), ((23, 0), [(25, 1), (24, 1), (24, 0)], [622, 621, 620]), ((24, 0), [(25, 0), (25, 1), (24, 1)], [623, 622, 621]), ((24, 1), [(24, 0), (25, 0), (25, 1)], [624, 623, 622]), ((25, 1), [(24, 1), (24, 0), (25, 0)], [625, 624, 623]), ((25, 0), [(25, 1), (24, 1), (24, 0)], [626, 625, 624]), ((24, 0), [(25, 2), (25, 1), (24, 1)], [627, 626, 625]), ((24, 1), [(24, 2), (25, 2), (25, 1)], [628, 627, 626]), ((25, 1), [(24, 3), (24, 2), (25, 2)], [629, 628, 627]), ((25, 2), [(25, 3), (24, 3), (24, 2)], [630, 629, 628]), ((24, 2), [(25, 4), (25, 3), (24, 3)], [631, 630, 629]), ((24, 3), [(24, 4), (25, 4), (25, 3)], [632, 631, 630]), ((25, 3), [(24, 5), (24, 4), (25, 4)], [633, 632, 631]), ((25, 4), [(25, 5), (24, 5), (24, 4)], [634, 633, 632]), ((24, 4), [(25, 6), (25, 5), (24, 5)], [635, 634, 633]), ((24, 5), [(24, 6), (25, 6), (25, 5)], [636, 635, 634]), ((25, 5), [(24, 7), (24, 6), (25, 6)], [637, 636, 635]), ((25, 6), [(25, 7), (24, 7), (24, 6)], [638, 637, 636]), ((24, 6), [(25, 8), (25, 7), (24, 7)], [639, 638, 637]), ((24, 7), [(24, 8), (25, 8), (25, 7)], [640, 639, 638]), ((25, 7), [(24, 9), (24, 8), (25, 8)], [641, 640, 639]), ((25, 8), [(25, 9), (24, 9), (24, 8)], [642, 641, 640]), ((24, 8), [(25, 10), (25, 9), (24, 9)], [643, 642, 641]), ((24, 9), [(24, 10), (25, 10), (25, 9)], [644, 643, 642]), ((25, 9), [(24, 11), (24, 10), (25, 10)], [645, 644, 643]), ((25, 10), [(25, 11), (24, 11), (24, 10)], [646, 645, 644]), ((24, 10), [(25, 12), (25, 11), (24, 11)], [647, 646, 645]), ((24, 11), [(24, 12), (25, 12), (25, 11)], [648, 647, 646]), ((25, 11), [(24, 13), (24, 12), (25, 12)], [649, 648, 647]), ((25, 12), [(25, 13), (24, 13), (24, 12)], [650, 649, 648]), ((24, 12), [(25, 14), (25, 13), (24, 13)], [651, 650, 649]), ((24, 13), [(24, 14), (25, 14), (25, 13)], [652, 651, 650]), ((25, 13), [(24, 15), (24, 14), (25, 14)], [653, 652, 651]), ((25, 14), [(25, 15), (24, 15), (24, 14)], [654, 653, 652]), ((24, 14), [(25, 16), (25, 15), (24, 15)], [655, 654, 653]), ((24, 15), [(24, 16), (25, 16), (25, 15)], [656, 655, 654]), ((25, 15), [(24, 17), (24, 16), (25, 16)], [657, 656, 655]), ((25, 16), [(25, 17), (24, 17), (24, 16)], [658, 657, 656]), ((24, 16), [(25, 18), (25, 17), (24, 17)], [659, 658, 657]), ((24, 17), [(24, 18), (25, 18), (25, 17)], [660, 659, 658]), ((25, 17), [(24, 19), (24, 18), (25, 18)], [661, 660, 659]), ((25, 18), [(25, 19), (24, 19), (24, 18)], [662, 661, 660]), ((24, 18), [(25, 20), (25, 19), (24, 19)], [663, 662, 661]), ((24, 19), [(24, 20), (25, 20), (25, 19)], [664, 663, 662]), ((25, 19), [(24, 21), (24, 20), (25, 20)], [665, 664, 663]), ((25, 20), [(25, 21), (24, 21), (24, 20)], [666, 665, 664]), ((24, 20), [(25, 22), (25, 21), (24, 21)], [667, 666, 665]), ((24, 21), [(24, 22), (25, 22), (25, 21)], [668, 667, 666]), ((25, 21), [(24, 23), (24, 22), (25, 22)], [669, 668, 667]), ((25, 22), [(25, 23), (24, 23), (24, 22)], [670, 669, 668]), ((24, 22), [(26, 23), (25, 23), (24, 23)], [671, 670, 669]), ((24, 23), [(26, 22), (26, 23), (25, 23)], [672, 671, 670]), ((25, 23), [(27, 22), (26, 22), (26, 23)], [673, 672, 671]), ((26, 23), [(27, 23), (27, 22), (26, 22)], [674, 673, 672]), ((26, 22), [(26, 23), (27, 23), (27, 22)], [675, 674, 673]), ((27, 22), [(26, 22), (26, 23), (27, 23)], [676, 675, 674]), ((27, 23), [(27, 22), (26, 22), (26, 23)], [677, 676, 675]), ((26, 23), [(27, 21), (27, 22), (26, 22)], [678, 677, 676]), ((26, 22), [(26, 21), (27, 21), (27, 22)], [679, 678, 677]), ((27, 22), [(26, 20), (26, 21), (27, 21)], [680, 679, 678]), ((27, 21), [(27, 20), (26, 20), (26, 21)], [681, 680, 679]), ((26, 21), [(27, 19), (27, 20), (26, 20)], [682, 681, 680]), ((26, 20), [(26, 19), (27, 19), (27, 20)], [683, 682, 681]), ((27, 20), [(26, 18), (26, 19), (27, 19)], [684, 683, 682]), ((27, 19), [(27, 18), (26, 18), (26, 19)], [685, 684, 683]), ((26, 19), [(27, 17), (27, 18), (26, 18)], [686, 685, 684]), ((26, 18), [(26, 17), (27, 17), (27, 18)], [687, 686, 685]), ((27, 18), [(26, 16), (26, 17), (27, 17)], [688, 687, 686]), ((27, 17), [(27, 16), (26, 16), (26, 17)], [689, 688, 687]), ((26, 17), [(27, 15), (27, 16), (26, 16)], [690, 689, 688]), ((26, 16), [(26, 15), (27, 15), (27, 16)], [691, 690, 689]), ((27, 16), [(26, 14), (26, 15), (27, 15)], [692, 691, 690]), ((27, 15), [(27, 14), (26, 14), (26, 15)], [693, 692, 691]), ((26, 15), [(27, 13), (27, 14), (26, 14)], [694, 693, 692]), ((26, 14), [(26, 13), (27, 13), (27, 14)], [695, 694, 693]), ((27, 14), [(26, 12), (26, 13), (27, 13)], [696, 695, 694]), ((27, 13), [(27, 12), (26, 12), (26, 13)], [697, 696, 695]), ((26, 13), [(27, 11), (27, 12), (26, 12)], [698, 697, 696]), ((26, 12), [(26, 11), (27, 11), (27, 12)], [699, 698, 697]), ((27, 12), [(26, 10), (26, 11), (27, 11)], [700, 699, 698]), ((27, 11), [(27, 10), (26, 10), (26, 11)], [701, 700, 699]), ((26, 11), [(27, 9), (27, 10), (26, 10)], [702, 701, 700]), ((26, 10), [(26, 9), (27, 9), (27, 10)], [703, 702, 701]), ((27, 10), [(26, 8), (26, 9), (27, 9)], [704, 703, 702]), ((27, 9), [(27, 8), (26, 8), (26, 9)], [705, 704, 703]), ((26, 9), [(27, 7), (27, 8), (26, 8)], [706, 705, 704]), ((26, 8), [(26, 7), (27, 7), (27, 8)], [707, 706, 705]), ((27, 8), [(26, 6), (26, 7), (27, 7)], [708, 707, 706]), ((27, 7), [(27, 6), (26, 6), (26, 7)], [709, 708, 707]), ((26, 7), [(27, 5), (27, 6), (26, 6)], [710, 709, 708]), ((26, 6), [(26, 5), (27, 5), (27, 6)], [711, 710, 709]), ((27, 6), [(26, 4), (26, 5), (27, 5)], [712, 711, 710]), ((27, 5), [(27, 4), (26, 4), (26, 5)], [713, 712, 711]), ((26, 5), [(27, 3), (27, 4), (26, 4)], [714, 713, 712]), ((26, 4), [(26, 3), (27, 3), (27, 4)], [715, 714, 713]), ((27, 4), [(26, 2), (26, 3), (27, 3)], [716, 715, 714]), ((27, 3), [(27, 2), (26, 2), (26, 3)], [717, 716, 715]), ((26, 3), [(27, 1), (27, 2), (26, 2)], [718, 717, 716]), ((26, 2), [(26, 1), (27, 1), (27, 2)], [719, 718, 717]), ((27, 2), [(26, 0), (26, 1), (27, 1)], [720, 719, 718]), ((27, 1), [(27, 0), (26, 0), (26, 1)], [721, 720, 719]), ((26, 1), [(28, 0), (27, 0), (26, 0)], [722, 721, 720]), ((26, 0), [(28, 1), (28, 0), (27, 0)], [723, 722, 721]), ((27, 0), [(29, 1), (28, 1), (28, 0)], [724, 723, 722]), ((28, 0), [(29, 0), (29, 1), (28, 1)], [725, 724, 723]), ((28, 1), [(28, 0), (29, 0), (29, 1)], [726, 725, 724]), ((29, 1), [(28, 1), (28, 0), (29, 0)], [727, 726, 725]), ((29, 0), [(29, 1), (28, 1), (28, 0)], [728, 727, 726]), ((28, 0), [(29, 2), (29, 1), (28, 1)], [729, 728, 727]), ((28, 1), [(28, 2), (29, 2), (29, 1)], [730, 729, 728]), ((29, 1), [(28, 3), (28, 2), (29, 2)], [731, 730, 729]), ((29, 2), [(29, 3), (28, 3), (28, 2)], [732, 731, 730]), ((28, 2), [(29, 4), (29, 3), (28, 3)], [733, 732, 731]), ((28, 3), [(28, 4), (29, 4), (29, 3)], [734, 733, 732]), ((29, 3), [(28, 5), (28, 4), (29, 4)], [735, 734, 733]), ((29, 4), [(29, 5), (28, 5), (28, 4)], [736, 735, 734]), ((28, 4), [(29, 6), (29, 5), (28, 5)], [737, 736, 735]), ((28, 5), [(28, 6), (29, 6), (29, 5)], [738, 737, 736]), ((29, 5), [(28, 7), (28, 6), (29, 6)], [739, 738, 737]), ((29, 6), [(29, 7), (28, 7), (28, 6)], [740, 739, 738]), ((28, 6), [(29, 8), (29, 7), (28, 7)], [741, 740, 739]), ((28, 7), [(28, 8), (29, 8), (29, 7)], [742, 741, 740]), ((29, 7), [(28, 9), (28, 8), (29, 8)], [743, 742, 741]), ((29, 8), [(29, 9), (28, 9), (28, 8)], [744, 743, 742]), ((28, 8), [(29, 10), (29, 9), (28, 9)], [745, 744, 743]), ((28, 9), [(28, 10), (29, 10), (29, 9)], [746, 745, 744]), ((29, 9), [(28, 11), (28, 10), (29, 10)], [747, 746, 745]), ((29, 10), [(29, 11), (28, 11), (28, 10)], [748, 747, 746]), ((28, 10), [(29, 12), (29, 11), (28, 11)], [749, 748, 747]), ((28, 11), [(28, 12), (29, 12), (29, 11)], [750, 749, 748]), ((29, 11), [(28, 13), (28, 12), (29, 12)], [751, 750, 749]), ((29, 12), [(29, 13), (28, 13), (28, 12)], [752, 751, 750]), ((28, 12), [(29, 14), (29, 13), (28, 13)], [753, 752, 751]), ((28, 13), [(28, 14), (29, 14), (29, 13)], [754, 753, 752]), ((29, 13), [(28, 15), (28, 14), (29, 14)], [755, 754, 753]), ((29, 14), [(29, 15), (28, 15), (28, 14)], [756, 755, 754]), ((28, 14), [(29, 16), (29, 15), (28, 15)], [757, 756, 755]), ((28, 15), [(28, 16), (29, 16), (29, 15)], [758, 757, 756]), ((29, 15), [(28, 17), (28, 16), (29, 16)], [759, 758, 757]), ((29, 16), [(29, 17), (28, 17), (28, 16)], [760, 759, 758]), ((28, 16), [(29, 18), (29, 17), (28, 17)], [761, 760, 759]), ((28, 17), [(28, 18), (29, 18), (29, 17)], [762, 761, 760]), ((29, 17), [(28, 19), (28, 18), (29, 18)], [763, 762, 761]), ((29, 18), [(29, 19), (28, 19), (28, 18)], [764, 763, 762]), ((28, 18), [(29, 20), (29, 19), (28, 19)], [765, 764, 763]), ((28, 19), [(28, 20), (29, 20), (29, 19)], [766, 765, 764]), ((29, 19), [(28, 21), (28, 20), (29, 20)], [767, 766, 765]), ((29, 20), [(29, 21), (28, 21), (28, 20)], [768, 767, 766]), ((28, 20), [(29, 22), (29, 21), (28, 21)], [769, 768, 767]), ((28, 21), [(28, 22), (29, 22), (29, 21)], [770, 769, 768]), ((29, 21), [(28, 23), (28, 22), (29, 22)], [771, 770, 769]), ((29, 22), [(29, 23), (28, 23), (28, 22)], [772, 771, 770]), ((28, 22), [(30, 23), (29, 23), (28, 23)], [773, 772, 771]), ((28, 23), [(30, 22), (30, 23), (29, 23)], [774, 773, 772]), ((29, 23), [(31, 22), (30, 22), (30, 23)], [775, 774, 773]), ((30, 23), [(31, 23), (31, 22), (30, 22)], [776, 775, 774]), ((30, 22), [(30, 23), (31, 23), (31, 22)], [777, 776, 775]), ((31, 22), [(30, 22), (30, 23), (31, 23)], [778, 777, 776]), ((31, 23), [(31, 22), (30, 22), (30, 23)], [779, 778, 777]), ((30, 23), [(31, 21), (31, 22), (30, 22)], [780, 779, 778]), ((30, 22), [(30, 21), (31, 21), (31, 22)], [781, 780, 779]), ((31, 22), [(30, 20), (30, 21), (31, 21)], [782, 781, 780]), ((31, 21), [(31, 20), (30, 20), (30, 21)], [783, 782, 781]), ((30, 21), [(31, 19), (31, 20), (30, 20)], [784, 783, 782]), ((30, 20), [(30, 19), (31, 19), (31, 20)], [785, 784, 783]), ((31, 20), [(30, 18), (30, 19), (31, 19)], [786, 785, 784]), ((31, 19), [(31, 18), (30, 18), (30, 19)], [787, 786, 785]), ((30, 19), [(31, 17), (31, 18), (30, 18)], [788, 787, 786]), ((30, 18), [(30, 17), (31, 17), (31, 18)], [789, 788, 787]), ((31, 18), [(30, 16), (30, 17), (31, 17)], [790, 789, 788]), ((31, 17), [(31, 16), (30, 16), (30, 17)], [791, 790, 789]), ((30, 17), [(31, 15), (31, 16), (30, 16)], [792, 791, 790]), ((30, 16), [(30, 15), (31, 15), (31, 16)], [793, 792, 791]), ((31, 16), [(30, 14), (30, 15), (31, 15)], [794, 793, 792]), ((31, 15), [(31, 14), (30, 14), (30, 15)], [795, 794, 793]), ((30, 15), [(31, 13), (31, 14), (30, 14)], [796, 795, 794]), ((30, 14), [(30, 13), (31, 13), (31, 14)], [797, 796, 795]), ((31, 14), [(30, 12), (30, 13), (31, 13)], [798, 797, 796]), ((31, 13), [(31, 12), (30, 12), (30, 13)], [799, 798, 797]), ((30, 13), [(31, 11), (31, 12), (30, 12)], [800, 799, 798]), ((30, 12), [(30, 11), (31, 11), (31, 12)], [801, 800, 799]), ((31, 12), [(30, 10), (30, 11), (31, 11)], [802, 801, 800]), ((31, 11), [(31, 10), (30, 10), (30, 11)], [803, 802, 801]), ((30, 11), [(31, 9), (31, 10), (30, 10)], [804, 803, 802]), ((30, 10), [(30, 9), (31, 9), (31, 10)], [805, 804, 803]), ((31, 10), [(30, 8), (30, 9), (31, 9)], [806, 805, 804]), ((31, 9), [(31, 8), (30, 8), (30, 9)], [807, 806, 805]), ((30, 9), [(31, 7), (31, 8), (30, 8)], [808, 807, 806]), ((30, 8), [(30, 7), (31, 7), (31, 8)], [809, 808, 807]), ((31, 8), [(30, 6), (30, 7), (31, 7)], [810, 809, 808]), ((31, 7), [(31, 6), (30, 6), (30, 7)], [811, 810, 809]), ((30, 7), [(31, 5), (31, 6), (30, 6)], [812, 811, 810]), ((30, 6), [(30, 5), (31, 5), (31, 6)], [813, 812, 811]), ((31, 6), [(30, 4), (30, 5), (31, 5)], [814, 813, 812]), ((31, 5), [(31, 4), (30, 4), (30, 5)], [815, 814, 813]), ((30, 5), [(31, 3), (31, 4), (30, 4)], [816, 815, 814]), ((30, 4), [(30, 3), (31, 3), (31, 4)], [817, 816, 815]), ((31, 4), [(30, 2), (30, 3), (31, 3)], [818, 817, 816]), ((31, 3), [(31, 2), (30, 2), (30, 3)], [819, 818, 817]), ((30, 3), [(31, 1), (31, 2), (30, 2)], [820, 819, 818]), ((30, 2), [(30, 1), (31, 1), (31, 2)], [821, 820, 819]), ((31, 2), [(30, 0), (30, 1), (31, 1)], [822, 821, 820]), ((31, 1), [(31, 0), (30, 0), (30, 1)], [823, 822, 821]), ((30, 1), [(32, 0), (31, 0), (30, 0)], [824, 823, 822]), ((30, 0), [(32, 1), (32, 0), (31, 0)], [825, 824, 823]), ((31, 0), [(33, 1), (32, 1), (32, 0)], [826, 825, 824]), ((32, 0), [(33, 0), (33, 1), (32, 1)], [827, 826, 825]), ((32, 1), [(32, 0), (33, 0), (33, 1)], [828, 827, 826]), ((33, 1), [(32, 1), (32, 0), (33, 0)], [829, 828, 827]), ((33, 0), [(33, 1), (32, 1), (32, 0)], [830, 829, 828]), ((32, 0), [(33, 2), (33, 1), (32, 1)], [831, 830, 829]), ((32, 1), [(32, 2), (33, 2), (33, 1)], [832, 831, 830]), ((33, 1), [(32, 3), (32, 2), (33, 2)], [833, 832, 831]), ((33, 2), [(33, 3), (32, 3), (32, 2)], [834, 833, 832]), ((32, 2), [(33, 4), (33, 3), (32, 3)], [835, 834, 833]), ((32, 3), [(32, 4), (33, 4), (33, 3)], [836, 835, 834]), ((33, 3), [(32, 5), (32, 4), (33, 4)], [837, 836, 835]), ((33, 4), [(33, 5), (32, 5), (32, 4)], [838, 837, 836]), ((32, 4), [(33, 6), (33, 5), (32, 5)], [839, 838, 837]), ((32, 5), [(32, 6), (33, 6), (33, 5)], [840, 839, 838]), ((33, 5), [(32, 7), (32, 6), (33, 6)], [841, 840, 839]), ((33, 6), [(33, 7), (32, 7), (32, 6)], [842, 841, 840]), ((32, 6), [(33, 8), (33, 7), (32, 7)], [843, 842, 841]), ((32, 7), [(32, 8), (33, 8), (33, 7)], [844, 843, 842]), ((33, 7), [(32, 9), (32, 8), (33, 8)], [845, 844, 843]), ((33, 8), [(33, 9), (32, 9), (32, 8)], [846, 845, 844]), ((32, 8), [(33, 10), (33, 9), (32, 9)], [847, 846, 845]), ((32, 9), [(32, 10), (33, 10), (33, 9)], [848, 847, 846]), ((33, 9), [(32, 11), (32, 10), (33, 10)], [849, 848, 847]), ((33, 10), [(33, 11), (32, 11), (32, 10)], [850, 849, 848]), ((32, 10), [(33, 12), (33, 11), (32, 11)], [851, 850, 849]), ((32, 11), [(32, 12), (33, 12), (33, 11)], [852, 851, 850]), ((33, 11), [(32, 13), (32, 12), (33, 12)], [853, 852, 851]), ((33, 12), [(33, 13), (32, 13), (32, 12)], [854, 853, 852]), ((32, 12), [(33, 14), (33, 13), (32, 13)], [855, 854, 853]), ((32, 13), [(32, 14), (33, 14), (33, 13)], [856, 855, 854]), ((33, 13), [(32, 15), (32, 14), (33, 14)], [857, 856, 855]), ((33, 14), [(33, 15), (32, 15), (32, 14)], [858, 857, 856]), ((32, 14), [(33, 16), (33, 15), (32, 15)], [859, 858, 857]), ((32, 15), [(32, 16), (33, 16), (33, 15)], [860, 859, 858]), ((33, 15), [(32, 17), (32, 16), (33, 16)], [861, 860, 859]), ((33, 16), [(33, 17), (32, 17), (32, 16)], [862, 861, 860]), ((32, 16), [(33, 18), (33, 17), (32, 17)], [863, 862, 861]), ((32, 17), [(32, 18), (33, 18), (33, 17)], [864, 863, 862]), ((33, 17), [(32, 19), (32, 18), (33, 18)], [865, 864, 863]), ((33, 18), [(33, 19), (32, 19), (32, 18)], [866, 865, 864]), ((32, 18), [(33, 20), (33, 19), (32, 19)], [867, 866, 865]), ((32, 19), [(32, 20), (33, 20), (33, 19)], [868, 867, 866]), ((33, 19), [(32, 21), (32, 20), (33, 20)], [869, 868, 867]), ((33, 20), [(33, 21), (32, 21), (32, 20)], [870, 869, 868]), ((32, 20), [(33, 22), (33, 21), (32, 21)], [871, 870, 869]), ((32, 21), [(32, 22), (33, 22), (33, 21)], [872, 871, 870]), ((33, 21), [(32, 23), (32, 22), (33, 22)], [873, 872, 871]), ((33, 22), [(33, 23), (32, 23), (32, 22)], [874, 873, 872]), ((32, 22), [(34, 23), (33, 23), (32, 23)], [875, 874, 873]), ((32, 23), [(34, 22), (34, 23), (33, 23)], [876, 875, 874]), ((33, 23), [(35, 22), (34, 22), (34, 23)], [877, 876, 875]), ((34, 23), [(35, 23), (35, 22), (34, 22)], [878, 877, 876]), ((34, 22), [(34, 23), (35, 23), (35, 22)], [879, 878, 877]), ((35, 22), [(34, 22), (34, 23), (35, 23)], [880, 879, 878]), ((35, 23), [(35, 22), (34, 22), (34, 23)], [881, 880, 879]), ((34, 23), [(35, 21), (35, 22), (34, 22)], [882, 881, 880]), ((34, 22), [(34, 21), (35, 21), (35, 22)], [883, 882, 881]), ((35, 22), [(34, 20), (34, 21), (35, 21)], [884, 883, 882]), ((35, 21), [(35, 20), (34, 20), (34, 21)], [885, 884, 883]), ((34, 21), [(35, 19), (35, 20), (34, 20)], [886, 885, 884]), ((34, 20), [(34, 19), (35, 19), (35, 20)], [887, 886, 885]), ((35, 20), [(34, 18), (34, 19), (35, 19)], [888, 887, 886]), ((35, 19), [(35, 18), (34, 18), (34, 19)], [889, 888, 887]), ((34, 19), [(35, 17), (35, 18), (34, 18)], [890, 889, 888]), ((34, 18), [(34, 17), (35, 17), (35, 18)], [891, 890, 889]), ((35, 18), [(34, 16), (34, 17), (35, 17)], [892, 891, 890]), ((35, 17), [(35, 16), (34, 16), (34, 17)], [893, 892, 891]), ((34, 17), [(35, 15), (35, 16), (34, 16)], [894, 893, 892]), ((34, 16), [(34, 15), (35, 15), (35, 16)], [895, 894, 893]), ((35, 16), [(34, 14), (34, 15), (35, 15)], [896, 895, 894]), ((35, 15), [(35, 14), (34, 14), (34, 15)], [897, 896, 895]), ((34, 15), [(35, 13), (35, 14), (34, 14)], [898, 897, 896]), ((34, 14), [(34, 13), (35, 13), (35, 14)], [899, 898, 897]), ((35, 14), [(34, 12), (34, 13), (35, 13)], [900, 899, 898]), ((35, 13), [(35, 12), (34, 12), (34, 13)], [901, 900, 899]), ((34, 13), [(35, 11), (35, 12), (34, 12)], [902, 901, 900]), ((34, 12), [(34, 11), (35, 11), (35, 12)], [903, 902, 901]), ((35, 12), [(34, 10), (34, 11), (35, 11)], [904, 903, 902]), ((35, 11), [(35, 10), (34, 10), (34, 11)], [905, 904, 903]), ((34, 11), [(35, 9), (35, 10), (34, 10)], [906, 905, 904]), ((34, 10), [(34, 9), (35, 9), (35, 10)], [907, 906, 905]), ((35, 10), [(34, 8), (34, 9), (35, 9)], [908, 907, 906]), ((35, 9), [(35, 8), (34, 8), (34, 9)], [909, 908, 907]), ((34, 9), [(35, 7), (35, 8), (34, 8)], [910, 909, 908]), ((34, 8), [(34, 7), (35, 7), (35, 8)], [911, 910, 909]), ((35, 8), [(34, 6), (34, 7), (35, 7)], [912, 911, 910]), ((35, 7), [(35, 6), (34, 6), (34, 7)], [913, 912, 911]), ((34, 7), [(35, 5), (35, 6), (34, 6)], [914, 913, 912]), ((34, 6), [(34, 5), (35, 5), (35, 6)], [915, 914, 913]), ((35, 6), [(34, 4), (34, 5), (35, 5)], [916, 915, 914]), ((35, 5), [(35, 4), (34, 4), (34, 5)], [917, 916, 915]), ((34, 5), [(35, 3), (35, 4), (34, 4)], [918, 917, 916]), ((34, 4), [(34, 3), (35, 3), (35, 4)], [919, 918, 917]), ((35, 4), [(34, 2), (34, 3), (35, 3)], [920, 919, 918]), ((35, 3), [(35, 2), (34, 2), (34, 3)], [921, 920, 919]), ((34, 3), [(35, 1), (35, 2), (34, 2)], [922, 921, 920]), ((34, 2), [(34, 1), (35, 1), (35, 2)], [923, 922, 921]), ((35, 2), [(34, 0), (34, 1), (35, 1)], [924, 923, 922]), ((35, 1), [(35, 0), (34, 0), (34, 1)], [925, 924, 923])]
    def test_move(key):
        check_change_dir(key)
        t = 0
        while t < 500000:
            t += 1
        move()
        canvas.update()
        return (tail_to_grow, snake_coor, snake_rect)

    unit_test(test_move, test_case, answer_case)
