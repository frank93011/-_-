from Tkinter import *
import random   #for food 

class snake_window:
    def __init__(self, unit = 18, offset = 3, height = 24, width = 36, pos = 20, slable_height = 30, init_length = 4, title = "Snake game"):
        self.ofs = offset
        self.wall_wid = 0
        self.grid_width = width #36
        self.grid_height = height #24
        self.wid = 0
        self.hei = 0
        self.shei = slable_height #30
        self.unit = unit #18
        geostr = self.init_size(pos)
        self.root = Tk()
        self.root.geometry(geostr)
        self.root_kb_handler = self.root.bind('<Key>', self.keyboard_handler)
        self.root_close_handler = self.root.protocol('WM_DELETE_WINDOW', self.root_exit)       
        self.root.title(title)
        self.root.focus_set()
        self.frame1 = None
        self.frame2 = None
        self.canvas = None
        self.slabel = None
        self.score = 0
        self.score_step = 100
        self.level = 1
        self.speed = 20
        self.speed_step = 0.5
        self.timer_init = 40000#60000
        self.timer_count = self.timer_init
        self.slabel_dict = {'Score': self.score, 'Level': self.level, 'Speed': self.speed}
        self.gen_frame()
        self.snake = snake(canvas_master = self.canvas, unit = unit, draw_body_origin = (self.ofs + 2* self.wall_wid, self.ofs + 2* self.wall_wid), height = height, width = width, init_length = init_length)
        self.now_dir = 'Down'
        self.dir_changed = False
        self.ctrl_key_pressed = False
        self.game_over = False
        self.draw_gam_over_done = False
        self.mission = False
        self.draw_mission_complete_done = False
        self.exit = False

        #self.dirkeys = ['Up', 'Down', 'Left', 'Right']
        #self.ctrlkeys = ['Escape', 'space']


    def init_size(self, pos):
        self.wall_wid = int(self.unit/3) #6
        self.wid = self.unit * self.grid_width + 4 * self.wall_wid + 2 * self.ofs  #678
        self.hei = self.unit * self.grid_height + self.shei + 4 * self.wall_wid  #486
        return str(self.wid) + "x" + str(self.hei) + ("+" + str(pos)) * 2


    def gen_frame(self):

        self.frame1 = Frame(master = self.root, width = self.wid, height = self.hei - self.shei)
        self.frame2 = Frame(master = self.root, width = self.wid, height = self.shei)
        self.canvas = Canvas(master = self.frame1, bg = 'white', width = self.wid, height = self.hei - self.shei)
        self.slabel = Label(master = self.frame2, text = self.slable_str())
        
        self.frame1.pack()
        self.frame2.pack(side = LEFT)
        self.slabel.pack()
        self.canvas.pack()

    def draw_walls(self):
        '''
        step 2: 
            Draw the wall of game zone.
            wall1: left
            wall2: horizontal down
            wall3: vertical right
            wall4: horizontal up
        '''
        half_wall_wid = int(0.5 * self.wall_wid) #3
        wall1x = self.ofs + self.wall_wid + half_wall_wid #12
        wall1y_up = self.ofs + self.wall_wid #9
        wall1y_down = self.hei - self.shei + self.ofs - self.wall_wid #453
        
        wall3x = self.wid  - wall1x #666
        wall3y_up = wall1y_up #9
        wall3y_down = wall1y_down #453
        
        wall2x_left = self.ofs + 2 * self.wall_wid #15
        wall2x_right = self.wid  - wall2x_left #663
        wall4y = self.ofs + self.wall_wid + half_wall_wid #12
        wall2y = self.hei - self.shei + self.ofs - self.wall_wid - half_wall_wid #450

        wall1 = [(15, 11), (15, 598)] #(15,11),(15,607)
        wall2 = [(11, 598), (891, 598)] #(11,598),(1,598)
        wall3 = [(887, 11), (887, 598)]#(887,11),(887,598)
        wall4 = [(15, 15), (891, 15)]#(15,15),(890,15)
        add1 = [(82, 19), (82, 109)]
        add2 = [(79, 106), (151, 106)]
        add3 = [(147, 105), (147, 128)]
        add4 = [(143, 128), (185, 128)]
        add5 = [(19,151), (107,151)]
        add6 = [(147,54), (197,54)]
        add7 = [(179,52), (214,86)]
        add8 = [(212,84),(224,104)]
        add9 = [(223,103), (223,163)]
        add10 = [(223,103),(237,77)]
        add11 = [(195,174),(225,160)]
        add12 = [(147,173),(200,173)]
        add13 = [(152,173),(152,198)]
        add14 = [(78,198),(157,198)]
        add15 = [(79,193),(79,223)]
        add16 = [(78,216),(107,245)]
        add17 = [(104,240), (104,324)]
        add18 = [(99,319), (370,319)]
        add24 = [(55,268),(55,371)]
        add25 = [(55,366),(400,366)]
        add25 = [(55,366), (321,366)]
        add26 = [(247,366), (247,415)]
        add27 = [(242,415), (321,415)]
        add28 = [(315,418), (330,390)]
        add29 = [(317,366), (333,390)]
        add30 = [(330,390), (467,390)]
        add31 = [(321,415), (344,439)]
        add32 = [(343,437), (343,564)]
        add33 = [(19,415), (107,415)]
        add33 = [(19,415), (107,415)]
        add34 = [(125,473),(160,439)]
        add35 = [(127,470),(127,510)]
        add36 = [(122,510),(174,510)]
        add37 = [(170,510),(221,460)]
        add38 = [(217,463),(295,463)]
        add39 = [(295,458),(295,594)]
        add40 = [(79,482),(79,563)]
        add41 = [(79,558),(212,558)]
        add42 = [(208,559),(222,532)]
        add43 = [(220,535),(251,535)]
		
        
        self.canvas.create_line(*wall1, width = self.wall_wid, fill = 'blue')
        self.canvas.create_line(*wall2, width = self.wall_wid, fill = 'blue')
        self.canvas.create_line(*wall3, width = self.wall_wid, fill = 'blue')
        self.canvas.create_line(*wall4, width = self.wall_wid, fill = 'blue')
        self.canvas.create_line(*add1, width = self.wall_wid, fill = 'red')
        self.canvas.create_line(*add2, width = self.wall_wid, fill = 'red')
        self.canvas.create_line(*add3, width = self.wall_wid, fill = 'red')
        self.canvas.create_line(*add4, width = self.wall_wid, fill = 'red')
        self.canvas.create_line(*add5, width = self.wall_wid, fill = 'red')
        self.canvas.create_line(*add6, width = self.wall_wid, fill = 'red')
        self.canvas.create_line(*add7, width = self.wall_wid, fill = 'red')
        self.canvas.create_line(*add8, width = self.wall_wid, fill = 'red')
        self.canvas.create_line(*add9, width = self.wall_wid, fill = 'red')
        self.canvas.create_line(*add10, width = self.wall_wid, fill = 'red')
        self.canvas.create_line(*add11, width = self.wall_wid, fill = 'red')
        self.canvas.create_line(*add12, width = self.wall_wid, fill = 'red')
        self.canvas.create_line(*add13, width = self.wall_wid, fill = 'red')
        self.canvas.create_line(*add14, width = self.wall_wid, fill = 'red')
        self.canvas.create_line(*add15, width = self.wall_wid, fill = 'red')
        self.canvas.create_line(*add16, width = self.wall_wid, fill = 'red')
        self.canvas.create_line(*add17, width = self.wall_wid, fill = 'red')
        self.canvas.create_line(*add18, width = self.wall_wid, fill = 'red')
        self.canvas.create_line(*add24, width = self.wall_wid, fill = 'red')
        self.canvas.create_line(*add25, width = self.wall_wid, fill = 'red')
        self.canvas.create_line(*add26, width = self.wall_wid, fill = 'red')
        self.canvas.create_line(*add27, width = self.wall_wid, fill = 'red')
        self.canvas.create_line(*add28, width = self.wall_wid, fill = 'red')
        self.canvas.create_line(*add29, width = self.wall_wid, fill = 'red')
        self.canvas.create_line(*add30, width = self.wall_wid, fill = 'red')
        self.canvas.create_line(*add31, width = self.wall_wid, fill = 'red')
        self.canvas.create_line(*add32, width = self.wall_wid, fill = 'red')
        self.canvas.create_line(*add33, width = self.wall_wid, fill = 'red')
        self.canvas.create_line(*add34, width = self.wall_wid, fill = 'red')
        self.canvas.create_line(*add35, width = self.wall_wid, fill = 'red')
        self.canvas.create_line(*add36, width = self.wall_wid, fill = 'red')
        self.canvas.create_line(*add37, width = self.wall_wid, fill = 'red')
        self.canvas.create_line(*add38, width = self.wall_wid, fill = 'red')
        self.canvas.create_line(*add39, width = self.wall_wid, fill = 'red')
        self.canvas.create_line(*add40, width = self.wall_wid, fill = 'red')
        self.canvas.create_line(*add41, width = self.wall_wid, fill = 'red')
        self.canvas.create_line(*add42, width = self.wall_wid, fill = 'red')
        return

    def update_slabel_dict(self):
        self.slabel_dict['Score'] = self.score
        self.slabel_dict['Level'] = self.level
        self.slabel_dict['Speed'] = self.speed

    def slable_str(self):
        self.update_slabel_dict()
        label_str = ''
        for k in self.slabel_dict.keys():
            label_str = label_str + k + ":{}\t"

        return label_str.format(*self.slabel_dict.values())

    def add_score(self):
        self.score += self.score_step
        return

    def add_level(self):
        self.level += 1
        return

    def add_speed(self):
        self.speed += self.speed_step
        self.timer_count -= int(self.timer_init * self.speed_step / 100)
        return

    def draw_score_level(self):
        self.slabel.config(text = self.slable_str())
        return

    def keyboard_handler(self, event):
        if self.game_over:
            if event.keysym in ['Escape', 'space']:
                self.ctrl_keys(event.keysym)
        if self.mission:
            if event.keysym in ['Escape', 'space']:
                self.ctrl_keys(event.keysym)
        else:
            if event.keysym in ['Up', 'Down', 'Left', 'Right']:
                self.dir_keys(event.keysym)
        
        return

    def dir_keys(self, key):
        change_dir_up = key == 'Up' and self.now_dir != 'Down'
        change_dir_down = key == 'Down' and self.now_dir != 'Up'
        change_dir_left = key == 'Left' and self.now_dir != 'Right'
        change_dir_right = key == 'Right' and self.now_dir != 'Left'

        if key != self.now_dir and (change_dir_up or change_dir_down or change_dir_left or change_dir_right):
            self.now_dir = key
            self.dir_changed = True
        else:
            self.dir_changed = False  
                  
        return

    def ctrl_keys(self, key):
        self.ctrl_key_pressed = True
        if key == 'Escape':
            self.root_exit()
        elif key == 'space':
            self.canvas.delete('gameover_text')
            self.canvas.delete('missioncomplete_text')		
            self.re_init()
            self.snake.re_init()
            self.snake.gen_food()
        else:
            pass

        return

    def root_exit(self):
        self.exit = True
        self.root.unbind('<Key>', self.root_kb_handler)
        # self.root.quit()
        # better don't use quit(), it will stop Tcl interpretor
        self.root.destroy()
        return

    def re_init(self):
        self.score = 0
        self.level = 1
        self.speed = 20
        self.timer_count = self.timer_init
        self.slabel_dict = {'Score': self.score, 'Level': self.level, 'Speed': self.speed}
        self.now_dir = 'Down'
        self.dir_changed = False
        self.ctrl_key_pressed = False
        self.game_over = False
        self.draw_gam_over_done = False    		
        self.exit = False 
        self.mission = False
        return


    def move(self):
        self.snake.move_to_next_position(self.now_dir)
        if self.snake.hit_walls() or self.snake.hit_body():
            self.game_over = True
        elif self.snake.hit_food():
            self.add_score()
            self.add_level()
            self.add_speed()
            self.snake.body_add1(self.snake.tail_to_grow)
            self.snake.gen_food()
            self.mission = True
        else:
            pass

    def draw_mission_complete(self, bypass = False):
        self.snake.clear()

        wid_1_2 = int(self.unit * self.grid_width / 2) + 4 * self.wall_wid + 2 * self.ofs
        hei_1_6 = int(self.unit * self.grid_height * 1 / 6) + self.shei + 4 * self.wall_wid
        hei_2_6 = int(self.unit * self.grid_height * 2 / 6) + self.shei + 4 * self.wall_wid
        hei_3_6 = int(self.unit * self.grid_height * 3 / 6) + self.shei + 4 * self.wall_wid
        hei_5_6 = int(self.unit * self.grid_height * 5 / 6) + self.shei + 4 * self.wall_wid

        font = 'Consolas'
        bold = 'bold'
        font_set1 = font + ' ' + str(self.unit * 2) + ' ' + bold
        font_set2 = font + ' ' + str(int(self.unit * 1.33)) + ' ' + bold
        font_set3 = font + ' ' + str(self.unit) + ' ' + bold
        font_set4 = font + ' ' + str(int(self.unit * 0.67)) + ' ' + bold

        self.canvas.create_text(wid_1_2, hei_1_6, text = 'Mission Complete!', font = font_set1, tag = 'missioncomplete_text')
        self.canvas.create_text(wid_1_2, hei_3_6, text = 'Press SPACE to retry and press ESC to exit', font = font_set3, tag = 'missioncomplete_text')

        self.draw_mission_complete_done = True

        return

    def draw_game_over(self, bypass = False):
        self.snake.clear()

        wid_1_2 = int(self.unit * self.grid_width / 2) + 4 * self.wall_wid + 2 * self.ofs
        hei_1_6 = int(self.unit * self.grid_height * 1 / 6) + self.shei + 4 * self.wall_wid
        hei_2_6 = int(self.unit * self.grid_height * 2 / 6) + self.shei + 4 * self.wall_wid
        hei_3_6 = int(self.unit * self.grid_height * 3 / 6) + self.shei + 4 * self.wall_wid
        hei_5_6 = int(self.unit * self.grid_height * 5 / 6) + self.shei + 4 * self.wall_wid

        font = 'Consolas'
        bold = 'bold'
        font_set1 = font + ' ' + str(self.unit * 2) + ' ' + bold
        font_set2 = font + ' ' + str(int(self.unit * 1.33)) + ' ' + bold
        font_set3 = font + ' ' + str(self.unit) + ' ' + bold
        font_set4 = font + ' ' + str(int(self.unit * 0.67)) + ' ' + bold

        self.canvas.create_text(wid_1_2, hei_1_6, text = 'Game Over!', font = font_set1, tag = 'gameover_text')
        self.canvas.create_text(wid_1_2, hei_2_6, text = 'Your score is : ' + str(self.score), font = font_set2, tag = 'gameover_text')
        self.canvas.create_text(wid_1_2, hei_3_6, text = 'Press SPACE to retry and press ESC to exit', font = font_set3, tag = 'gameover_text')

        self.draw_gam_over_done = True

        return 

 

    def loop(self):
        #self.root.focus_set()

        timer = 0
        
        while True:

            if self.game_over:
                if not self.draw_gam_over_done:
                    self.draw_game_over()

                timer = 0
            if self.mission:
                if not self.draw_mission_complete_done:
                    self.draw_mission_complete()

                timer = 0
            elif self.dir_changed or timer == self.timer_count:
                self.move()
                self.draw_score_level()
                self.dir_changed = False
                timer = 0



            if self.exit:
                break

            timer += 1
            self.canvas.update()

        return



    def main(self):
        #self.gen_frame()
        self.draw_walls()
        self.snake.gen_food()
        #self.draw_score()
        self.loop()
        return


class snake:
    def __init__(self, canvas_master, unit = 12, draw_body_origin = (0, 0), height = 24, width = 36, init_length = 3, color = 'blue'):
        self.canvas = canvas_master
        self.unit = unit
        self.draw_body_ox = draw_body_origin[0]
        self.draw_body_oy = draw_body_origin[1]
        self.height = height
        self.width = width
        self.init_length = 3
        self.color = color

        self.cstack = list() # coorinate stack
        self.rstack = list() # rectangle stack
        self.head = tuple()
        self.tail_to_grow = tuple()

        self.init_snake_body()
        self.food_rect = None
        self.food = tuple()

    def init_snake_body(self):
        y_amount = self.init_length
        x_amount = 1
        start = (0, 0)
        if self.height < self.init_length:
            if self.width > self.init_length:
                y_amount = 1
                x_amount = self.init_length
                start = (int(self.width/2) - 1, 0)
            else:
                y_amount = 1
                x_amount = 1
                start = (0, 0)

        for y in range(y_amount - 1, -1, -1):
            for x in range(x_amount -1, -1, -1 ):
                self.body_add1((start[0] + x, start[1] + y))

        return

    def create_a_rect(self, coor, color = None, tag =''):
        x = self.draw_body_ox + coor[0] * self.unit
        y = self.draw_body_oy + coor[1] * self.unit
        return self.canvas.create_rectangle(x, y, x + self.unit - 1, y + self.unit - 1, fill = color, tag = tag)

    def body_add1(self, coor, from_tail = True):
        self.body_coor_add1(coor, from_tail)
        self.body_rect_add1(coor, from_tail)
        self.head = self.cstack[0]
        return

    def body_coor_add1(self, coor, from_tail = True):
        if from_tail:
            self.cstack.append(coor)
        else:
            self.cstack.insert(0, coor)
        return
    
    def body_rect_add1(self, coor, from_tail = True):
        if from_tail:
            self.rstack.append(self.create_a_rect(coor, color = self.color, tag = 'snake'))
        else:
            self.rstack.insert(0, self.create_a_rect(coor, color = self.color, tag = 'snake'))
        return

    def move_to_next_position(self, direction = 'Down', step = 1):
        (x, y) = self.head

        if direction == 'Up':
            self.body_move1((x, y - step))
        
        if direction == 'Down':
            self.body_move1((x, y + step))

        if direction == 'Left':
            self.body_move1((x - step, y))

        if direction == 'Right':
            self.body_move1((x + step, y))

        return     

        
    def body_move1(self, coor):
        self.body_add1(coor, from_tail = False)
        self.tail_to_grow = self.cstack[-1] 

        del self.cstack[-1]
        self.canvas.delete(self.rstack[-1])
        del self.rstack[-1]

        return

    def gen_food(self):           

        
        self.food = (35, 23)


        self.food_rect = self.create_a_rect(self.food, color = 'red', tag = 'food')
        return
			
	    

    def hit_food(self):
       return self.head == self.food 
	
	
	

    """def hit_food(self):
        return """

    def hit_walls(self):
        (x, y) = self.head
        if x < 0 or x >= self.width or y < 0 or y >= self.height:
            return x < 0 or x >= self.width or y < 0 or y >= self.height #row:24,col:36
        '''if x == 2 and (y >= 0 and y<= 3): #1
            return True
        if (x >= 2 and x<= 5) and y == 3: #2
            return True
        if x == 5 and (y >=3 and y<= 4 ): #3
            return True
        if y == 4 and (x >=5 and x<= 6 ): #4
            return True
        if y == 5 and (x >=0 and x<= 3 ): #5
            return True
        if y == 1 and (x >=5 and x<= 6 ): #6
            return True
        if (x == 7 and y == 1) : #7
            return True
        if (x ==7 and y == 2): #8
            return True
        if x == 8 and (y >=3 and y<= 5 ): #9
            return True
        if (x>=8 and x <=9 and y == 2): #10
            return True
        if y == 6 and (x >=6 and x<= 8 ): #11
            return True
        if x == 5 and (y >=6 and y<= 7 ): #12
            return True
        if y == 7 and (x >=2 and x<= 5 ): #14
            return True
        if x == 2 and (y >=7 and y<= 8 ): #15
            return True
        if (x == 3 and y == 9): #16
            return True
        if (x == 3 and y >= 9 and y <= 12): #17
            return True
        if (x>=3 and x <=14 and y == 12): #18
            return True
        if (x == 14 and y >= 12 and y <= 13): #19
            return True
        if (x>=14 and x <= 20 and y == 13): #20
            return True
        if (x == 20 and y >= 13 and y <= 17): #21
            return True
        if (x>=15 and x <= 22 and y == 17): #22
            return True
        if (x == 15 and y >= 17 and y <= 23): #23
            return True
        if (x == 1 and y >= 10 and y <= 14): #24
            return True
        if (x>=1 and x <= 12 and y == 14): #25
            return True
        if (x == 8 and y >= 14 and y <= 16): #26
            return True
        if (x>=8 and x <= 12 and y == 16): #27
            return True
        if (x>= 13 and x <= 17 and y == 15): #30
            return True
        if (x == 13 and y >= 17 and y <= 22): #32
            return True
        if (x>= 0 and x <= 3 and y == 16): #33
            return True
        if x == 5 and y >= 17 and y <= 18: #34
		    return 	True
        if x == 4 and y >= 18 and y <= 20: #35
		    return 	True
        if (x>= 4 and x <= 6 and y == 20): #36
            return True	
        if (x>= 6 and x <= 7 and y == 19): #37
            return True	
        if (x>= 7 and x <= 10 and y == 18): #38
            return True
        if x == 11 and y >= 18 and y <= 23: #39
		    return 	True
        if x == 2 and y >= 19 and y <= 22: #40
		    return 	True
        if (x>= 2 and x <= 7 and y == 22): #41
            return True
        if (x>= 8 and x <= 9 and y == 21): #43
            return True
        if x == 10 and y >= 4 and y <= 8: #44
		    return 	True
        if (x>= 7 and x <= 10 and y == 8): #47
            return True
        if x == 6 and y >= 9 and y <= 10: #49
		    return 	True
        if (x>= 6 and x <= 10 and y == 10): #50
            return True
        if (x>= 11 and x <= 12 and y == 9): #52
            return True
        if (x>= 13 and x <= 15 and y == 8): #54
            return True
        if (x>= 16 and x <= 19 and y == 7): #56
            return True
        if (x>= 20 and x <= 25 and y == 6): #58
            return True
        if x == 21 and y >= 6 and y <= 9: #59
		    return 	True
        if x == 25 and y >= 6 and y <= 13: #60
		    return 	True
        if x == 24 and y >= 14 and y <= 21: #62
		    return 	True
        if (x>= 25 and x <= 27 and y == 22): #63
            return True
        if (x>= 17 and x <= 21 and y == 21): #64
            return True
        if x == 17 and y >= 19 and y <= 20: #67
		    return 	True
        if (x>= 17 and x <= 22 and y == 19): #68
            return True
        if x == 22 and y >= 11 and y <= 19: #69
		    return 	True
        if (x>= 17 and x <= 23 and y == 11): #70
            return True
        if x == 23 and y >= 8 and y <= 11: #71
		    return 	True
        if x == 16 and y == 10: #72
		    return 	True
        if y == 9 and x >= 17 and x <= 18: #73
		    return 	True
        if x == 10 and y == 19: #75
		    return 	True
        if y == 1 and x >= 12 and x <= 13: #77
		    return 	True
        if x == 13 and y >= 1 and y <= 5: #78
		    return 	True
        if x == 14 and y == 5: #79
		    return 	True
        if y == 5 and x >= 15 and x <= 18: #81
		    return 	True
        if y == 4 and x >= 13 and x <= 14: #83
		    return 	True
        if y == 3 and x == 20 : #84
		    return 	True
        if x == 16 and y >= 0 and y <= 2: #85
		    return 	True
        if y == 2 and x >= 16 and x <= 18: #86
		    return 	True
        if y == 1 and x >= 19 and x <= 23: #88
		    return 	True
        if y == 12 and x >= 25 and x <= 29: #89
		    return 	True
        if x == 12 and y >= 4 and y <= 2: #90
		    return 	True
        if y == 11 and x >= 29 and x <= 31: #91
		    return 	True
        if (y == 10 and x == 31) or (x== 30 and y == 9) : #92,93
		    return 	True
        if x == 27 and y >= 12 and y <= 15: #94
		    return 	True
        if x == 16 and y >= 19 and y <= 26: #96
		    return 	True
        if y == 20 and x >= 27 and x <= 29: #98
		    return 	True
        if x == 29 and y >= 16 and y <= 20: #99
		    return 	True
        if y == 16 and x >= 29 and x <= 31: #100
		    return 	True
        if (x == 30 and y >= 22 and y <= 23) or (x == 31 and y>=18 and y == 22): #103
		    return 	True'''
			
    def hit_body(self):
        return self.head in self.cstack[1 : ]

    def clear(self):
        self.canvas.delete('snake')
        self.canvas.delete('food')
        return

    def re_init(self):
        self.cstack = list() # coorinate stack
        self.rstack = list() # rectangle stack
        self.head = tuple()
        self.tail_to_grow = tuple()
        self.food_rect = None
        self.food = tuple()
 
        self.init_snake_body()
        return




  

if __name__ == "__main__":
    w = snake_window(unit = 24, offset = 3, height = 24, width = 36, pos = 20, slable_height = 30,  init_length = 10, title = "Snake game")
    w.main()
    

