from Tkinter import *
import random   #for food 
from PIL import ImageTk
import time
class snake_window:
    def __init__(self, unit = 18, offset = 3, height = 24, width = 36, pos = 20, slable_height = 30, init_length = 4, title = "Snake game"):
        self.ofs = offset
        self.wall_wid = 0
        self.grid_width = width
        self.grid_height = height
        self.wid = 0
        self.hei = 0
        self.shei = slable_height
        self.unit = unit
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
        self.start = 0
        self.timer_init = 15000#60000
        self.timer_count = self.timer_init
        self.slabel_dict = {'Score': self.score, 'Level': self.level, 'Speed': self.speed}
        self.gen_frame()
        self.snake = snake(canvas_master = self.canvas, unit = unit, draw_body_origin = (self.ofs + 2* self.wall_wid, self.ofs + 2* self.wall_wid), height = height, width = width, init_length = init_length)
        self.now_dir = 'Down'
        self.dir_changed = False
        self.ctrl_key_pressed = False
        self.game_over = False
        self.draw_gam_over_done = False
        self.exit = False

        #self.dirkeys = ['Up', 'Down', 'Left', 'Right']
        #self.ctrlkeys = ['Escape', 'space']


    def init_size(self, pos):
        self.wall_wid = int(self.unit/3)
        self.wid = self.unit * self.grid_width + 4 * self.wall_wid + 2 * self.ofs
        self.hei = self.unit * self.grid_height + self.shei + 4 * self.wall_wid
        return str(self.wid) + "x" + str(self.hei) + ("+" + str(pos)) * 2


    def gen_frame(self):
        self.image = ImageTk.PhotoImage(file = "D:\document\join.jpg")
        self.frame1 = Frame(master = self.root, width = self.wid, height = self.hei - self.shei)
        self.frame2 = Frame(master = self.root, width = self.wid, height = self.shei)
        self.canvas = Canvas(master = self.frame1, bg = 'black', width = self.wid, height = self.hei - self.shei)
        self.slabel = Label(master = self.frame2, text = self.slable_str())
        self.canvas.create_image(420,360,image = self.image)
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
        half_wall_wid = int(0.5 * self.wall_wid)
        wall1x = self.ofs + self.wall_wid + half_wall_wid
        wall1y_up = self.ofs + self.wall_wid
        wall1y_down = self.hei - self.shei + self.ofs - self.wall_wid
        
        wall3x = self.wid  - wall1x
        wall3y_up = wall1y_up
        wall3y_down = wall1y_down
        
        wall2x_left = self.ofs + 2 * self.wall_wid
        wall2x_right = self.wid  - wall2x_left
        wall4y = self.ofs + self.wall_wid + half_wall_wid
        wall2y = self.hei - self.shei + self.ofs - self.wall_wid - half_wall_wid

        wall1 = [(wall1x, wall1y_up), (wall1x, wall1y_down)]
        wall2 = [(wall2x_left, wall2y), (wall2x_right, wall2y)]
        wall3 = [(wall3x, wall1y_down), (wall3x, wall1y_up)]
        wall4 = [(wall2x_right, wall4y), (wall2x_left, wall4y)]
        
        self.canvas.create_line(*wall1, width = self.wall_wid, fill = 'yellow')
        self.canvas.create_line(*wall2, width = self.wall_wid, fill = 'yellow')
        self.canvas.create_line(*wall3, width = self.wall_wid, fill = 'yellow')
        self.canvas.create_line(*wall4, width = self.wall_wid, fill = 'yellow')
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

    def add_super_score(self):
        self.score += self.score_step*3
        return

    def delete_score(self):
        self.score -= self.score_step
        return
		
    def add_level(self):
        self.level += 1
        return

    def delete_level(self):
        self.level -= 1
        return
		
    def add_speed(self):
        self.speed += self.speed_step
        self.timer_count -= int(self.timer_init * self.speed_step / 50)
        return
		
    def delete_speed(self):
        self.speed -= self.speed_step
        self.timer_count -= int(self.timer_init * self.speed_step / 10)
        return
		
    def add_super_speed(self):
        self.speed += self.speed_step*10
        self.timer_count -= int(self.timer_init * self.speed_step*5 / 10)
        return

    def draw_score_level(self):
        self.slabel.config(text = self.slable_str())
        return

    def keyboard_handler(self, event):
        if self.game_over:
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
            self.re_init()
            self.snake.re_init()
            self.snake.gen_food()
            self.snake.gen_strange()
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
        elif self.snake.hit_strange():
            self.start = time.time()
            x = random.randint(0,4 ) 
            if x == 0:
                self.add_super_score()
                self.add_level()
                self.add_speed()
                self.snake.body_add3()
            elif x == 1:
                self.add_score()
                self.add_super_speed()
                self.add_level()
            elif x == 2:
                self.delete_speed()
                self.add_score()
                self.delete_level()
            elif x >= 3:
                self.snake.body_delete()
                self.delete_score()
            y = random.randint(4,10)
            self.snake.canvas.delete(self.snake.strange_rect)
            self.root.after(y*1000,self.snake.gen_strange)
            #self.snake.gen_strange()
        else:
            pass

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

        self.canvas.create_text(wid_1_2, hei_1_6, text = 'Game Over!',fill = 'yellow', font = font_set1, tag = 'gameover_text')
        self.canvas.create_text(wid_1_2, hei_2_6, text = 'Your score is : ' + str(self.score), fill ='yellow',font = font_set2, tag = 'gameover_text')
        self.canvas.create_text(wid_1_2, hei_3_6, text = 'Press SPACE to retry and press ESC to exit',fill = 'yellow', font = font_set3, tag = 'gameover_text')

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
        self.snake.gen_strange()
        #self.draw_score()
        self.loop()
        return


class snake:
    def __init__(self, canvas_master, unit = 12, draw_body_origin = (0, 0), height = 24, width = 36, init_length = 3, color = 'yellow'):
        self.canvas = canvas_master
        self.unit = unit
        self.draw_body_ox = draw_body_origin[0]
        self.draw_body_oy = draw_body_origin[1]
        self.height = height
        self.width = width
        self.init_length = init_length
        self.color = color

        self.cstack = list() # coorinate stack
        self.rstack = list() # rectangle stack
        self.head = tuple()
        self.tail_to_grow = tuple()

        self.init_snake_body()
        self.food_rect = None
        self.strange_rect = None
        self.food = tuple()
        self.strange = tuple()

    def init_snake_body(self):
        y_amount = self.init_length
        x_amount = 1
        start = (int(self.width/2) - 1, 0)
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
    def body_add3(self):
        self.body_add1(self.tail_to_grow)
        self.body_add1(self.tail_to_grow)
        self.body_add1(self.tail_to_grow)
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

    def body_delete(self):
	
        del self.cstack[-1]
        self.canvas.delete(self.rstack[-1])
        del self.rstack[-1]
        return
        
    def body_move1(self, coor):
        self.body_add1(coor, from_tail = False)
        self.tail_to_grow = self.cstack[-1] 

        del self.cstack[-1]
        self.canvas.delete(self.rstack[-1])
        del self.rstack[-1]

        return

    def gen_food(self):           
        x = random.randint(0, self.width - 1)
        y = random.randint(0, self.height - 1)
        self.food = (x, y)

        while self.food in self.cstack:
            x = random.randint(0, self.width - 1)
            y = random.randint(0, self.height - 1)
            self.food = (x, y)
        else:
            if self.food_rect:
                self.canvas.delete(self.food_rect)

            self.food_rect = self.create_a_rect(self.food, color = 'red', tag = 'food')
            return
			
			
    def gen_strange(self):           

        x = random.randint(0, self.width - 1)
        y = random.randint(0, self.height - 1)
        self.strange = (x, y)

        while self.strange in self.cstack:
            x = random.randint(0, self.width - 1)
            y = random.randint(0, self.height - 1)
            self.strange = (x, y)
        if self.strange == self.food:
            x = random.randint(0, self.width - 1)
            y = random.randint(0, self.height - 1)
            self.strange = (x, y)      
        else:
            if self.strange_rect:
                self.canvas.delete(self.strange_rect)

            self.strange_rect = self.create_a_rect(self.strange, color = 'blue', tag = 'food')
            return
			
			
    def hit_food(self):
        return self.head == self.food
		
    def hit_strange(self):
        return self.head == self.strange

    def hit_walls(self):
        (x, y) = self.head
        return x < 0 or x >= self.width or y < 0 or y >= self.height

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
        self.strange_rect = None
        self.food = tuple()
        self.strange = tuple()
 
        self.init_snake_body()
        return




  

if __name__ == "__main__":
    w = snake_window(unit = 24, offset = 3, height = 24, width = 36, pos = 20, slable_height = 30,  init_length = 10, title = "Snake game")
    w.main()
    

