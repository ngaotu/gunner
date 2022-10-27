import random
from pygame import mixer
import pygame,sys
import os
import csv
mixer.init()
pygame.init()
SCREEN_WIDTH = 800
SCREEN_HEIGHT = int(SCREEN_WIDTH * 0.8)
GRAVITY = 0.5
SCROLL = 200
# so hang so cot cua map
ROWS = 16
COLS = 150
# kich thuoc cua 1 o
TILE_SIZE = SCREEN_HEIGHT//ROWS
TILE_TYPE = 23
MAX_LEVEL =1
win_game = False
levels =1
total_diamon = 0
music = 0
# music_play = True
# Font 
font = pygame.font.SysFont('Futura',25)
# khoi tao cua so tro choi
screen = pygame.display.set_mode((SCREEN_WIDTH,SCREEN_HEIGHT))
pygame.display.set_caption(" Super Shooter")
clock = pygame.time.Clock() 
run = True
start_game =False
setting = False
general_setting = True
control_setting = False
set_up = False
# music_ = True
move_left = False   
move_right = False
shoot = False
screen_scroll = 0
bg_scroll = 0

# music
pygame.mixer.music.load('audio/Pubg.mp3')
pygame.mixer.music.set_volume(0.3)
pygame.mixer.music.play(-1,0.0,1000)
jump_fx = pygame.mixer.Sound('audio/jump.wav')
jump_fx.set_volume(0.5)
shoot_fx = pygame.mixer.Sound('audio/ak.wav')
shoot_fx.set_volume(0.2)
collect_fx = pygame.mixer.Sound('audio/collect.wav')
death_fx = pygame.mixer.Sound('audio/die.wav')
low_health_fx = pygame.mixer.Sound('audio/heart_injure.wav')
low_health_fx.set_volume(0.2)

# map _ img
img_list = []
for x in range(TILE_TYPE):
    img = pygame.image.load(f"img/tile/{x}.png").convert_alpha()
    img = pygame.transform.scale(img,(TILE_SIZE,TILE_SIZE))
    img_list.append(img)

player_img = pygame.image.load('img/tile/15.png')
player_img = pygame.transform.scale(player_img,(5*player_img.get_width(),5*player_img.get_height()))
# bullet_img = pygame.transform.scale(bullet_img,(bullet_img.get_width()*2.5,bullet_img.get_height()*0.5))
bullet_img = pygame.image.load('img/icons/bullet.png').convert_alpha()


#pick up item
health_box_img = pygame.image.load("img/icons/health_box.png").convert_alpha()
items_box = {
    'Health' : health_box_img
}
you_win_img = pygame.image.load('img/win.png').convert_alpha()
# you_win_img = pygame.transform.scale(you_win_img,(you_win_img.get_width(),you_win_img.get_height()))
game_over_img = pygame.image.load('img/gameover.png').convert_alpha()
game_over_img = pygame.transform.scale(game_over_img,(game_over_img.get_width()*2,game_over_img.get_height()*2))
# background 
background_settings = pygame.image.load('img/Background/1.jpg').convert_alpha()
background_settings = pygame.transform.scale(background_settings, (SCREEN_WIDTH,SCREEN_HEIGHT))
control_setting_img = pygame.image.load("img/background/control_setting.jpg").convert_alpha()
control_setting_img = pygame.transform.scale(control_setting_img, (SCREEN_WIDTH,SCREEN_HEIGHT))
set_up_img = pygame.image.load("img/background/setting.jpg").convert_alpha()
set_up_img = pygame.transform.scale(set_up_img, (SCREEN_WIDTH,SCREEN_HEIGHT))
background_setup = pygame.image.load('img/Background/2.jpg').convert_alpha()
background_setup = pygame.transform.scale(background_setup, (SCREEN_WIDTH,SCREEN_HEIGHT))
diamon_display_img = pygame.image.load('img/diamon.png').convert_alpha()
heart_img = pygame.image.load('img/icons/heart.png').convert_alpha()
pine1_img = pygame.image.load('img/Background/pine1.png').convert_alpha()
pine2_img = pygame.image.load('img/Background/pine2.png').convert_alpha()
mountain_img = pygame.image.load('img/Background/mountain.png').convert_alpha()
sky_img = pygame.image.load('img/Background/sky_cloud.png').convert_alpha() 

#button_img

start_img = pygame.image.load("img//start_btn.png").convert_alpha()
restart_img = pygame.image.load("img/restart.jpg").convert_alpha()
resume_img = pygame.image.load("img/resume.jpg").convert_alpha()
setting_img = pygame.image.load("img/setting.png").convert_alpha()
menu_img = pygame.image.load("img/menu.jpg").convert_alpha()
general_img = pygame.image.load("img/icons/general.png").convert_alpha()
control_img = pygame.image.load("img/icons/control.png").convert_alpha()

close_img = pygame.image.load("img/icons/close.png")
# start_img = pygame.transform.scale(start_img,(300,100))
# resume_img = pygame.transform.scale(resume_img,(182,79))
# setting_img = pygame.transform.scale(setting_img,(182,79))
# game_over_img = pygame.image.load("img/game_over.png").convert_alpha()
exit_img = pygame.image.load("img/exit.png").convert_alpha()
# exit_img = pygame.transform.scale(exit_img,(300,100))
# hinh map
trungbui = pygame.image.load('img/background/map.jpg')
trungbui = pygame.transform.scale(trungbui,(start_img.get_width(),trungbui.get_height()))

BG = (144, 201, 120)
RED = (255,0,0)
WHITE = (252,252,255)

# create snow fall animation
snow = []
for i in range(200):
    x = random.randrange(0,int(SCREEN_WIDTH*7.5))
    y = random.randrange(0,SCREEN_HEIGHT)
    snow.append([x,y])
def snow_animation():
    for ice in range(len(snow)): 
        pygame.draw.circle(screen, 'white',(snow[ice][0]-bg_scroll*0.6,snow[ice][1]),2)
        #we are increasing the y coordinate by one as we want the fall effect 
        snow[ice][1]+=1 
        if snow[ice][1]>SCREEN_HEIGHT:  
            #y is negative as we wanna start from top again and increase y
            snow[ice][1] = random.randrange(-60,-10)
            snow[ice][0] = random.randrange(0,int(7.5*SCREEN_WIDTH))


def draw_bg():
    if set_up == True:
        screen.blit(background_setup,(0,0))
    else:
        screen.fill(BG)
        width = sky_img.get_width()
        for x in range(5):
            # snow_animation()
            screen.blit(sky_img, ((x * width) - bg_scroll * 0.5, 0))
            screen.blit(mountain_img, ((x * width) - bg_scroll * 0.6, SCREEN_HEIGHT - mountain_img.get_height() - 300))
            screen.blit(pine1_img, ((x * width) - bg_scroll * 0.7, SCREEN_HEIGHT - pine1_img.get_height() - 150))
            screen.blit(pine2_img, ((x * width) - bg_scroll * 0.8, SCREEN_HEIGHT - pine2_img.get_height())) 
def draw_charecter(text,font,text_col,x,y):
    diamon = font.render(text,True,text_col)
    screen.blit(heart_img,(0,0))
    screen.blit(diamon_display_img,(0,heart_img.get_height()))
    screen.blit(diamon,(diamon_display_img.get_width()+x,heart_img.get_height()+y))
def reset_level():
    enemy_group.empty()
    bullet_group.empty()
    items_box_group.empty()
    water_group.empty()
    decoration_group.empty()
    exit_group.empty()
    diamon_group.empty()
    map_data = []
    for row in range(ROWS):
        r =[-1]*COLS
        map_data.append(r)
    return map_data
def start_screen():
    screen.blit(background_settings,(0,0))
    screen.blit(diamon_display_img,(0,0))
    screen.blit(trungbui,(start_btn.rect.x,start_btn.rect.y-trungbui.get_height()))
    screen.blit(player_img,(SCREEN_WIDTH//2 +150,SCREEN_HEIGHT//2))
    screen.blit(player_img,(SCREEN_WIDTH//2,SCREEN_HEIGHT//2+50))
    screen.blit(pygame.transform.flip(player_img,True,False),(SCREEN_WIDTH//2-150,SCREEN_HEIGHT//2))
    all_diamon = font.render(f': {total_diamon}',True,WHITE)
    screen.blit(all_diamon,(diamon_display_img.get_width()+4,4))
# khoi tao lop chien binh
class Soldier(pygame.sprite.Sprite):
    def __init__(self, pos_x , pos_y,typeOf ,scale,speed):
        # ke thua 1 so chuc nang tu sprite
        pygame.sprite.Sprite.__init__(self)
        self.alive = True
        # toc do di chuyen cua nhan vat
        self.speed = speed
        self.shoot_cooldown = 0
        self.disappear = 100
        # suc khoe cua nhan vat
        self.health = 100
        self.max_health = self.health
        self.direction = 1
        self.flip = False
        self.jump = False
        self.jump_limit = False
        # van toc nhay ( van toc theo truc Oy)
        self.v =  0 
        # kieu doi tuong ( player - enemy)
        self.type = typeOf
        self.index = 0 
        self.action = 0
        self.diamon = 0
        #  list chua cac hinh anh cua doi tuong 
        self.animation_list = []
        self.update_time = pygame.time.get_ticks()
        # them list hanh dong  vao trong list hoat anh
        animation_types = ['Idle', 'Run', 'Jump','Death']
        for animation in animation_types:
			#reset temporary list of images
            temp_list = []
			#count number of files in the folder
            num_of_frames = len(os.listdir(f'img/{self.type}/{animation}'))
            for i in range(0,num_of_frames):
                img = pygame.image.load(f'img/{self.type}/{animation}/{i}.png').convert_alpha()
                img = pygame.transform.scale(img, (int(img.get_width() * scale), int(img.get_height() * scale)))
                temp_list.append(img)
            self.animation_list.append(temp_list)
        self.image = self.animation_list[self.action][self.index]
        self.rect = self.image.get_rect()
        self.rect.center = (pos_x,pos_y)
        self.width = self.image.get_width()
        self.height = self.image.get_height()
    def display(self):
        screen.blit(pygame.transform.flip(self.image,self.flip,False),self.rect)
    def moving(self,move_left,move_right):
        dx = 0
        dy = 0
        screen_scroll =0
        level_complete = False
        global total_diamon
        #move left
        if move_left:
            dx = -self.speed
            self.flip = True
            self.direction = -1
        #move-right
        if move_right:
            dx = self.speed
            self.flip = False
            self.direction = 1
        #jump
        if self.jump ==True and self.jump_limit ==False:
            self.v = -10
            self.jump = False
            self.jump_limit = True
        # them trong luc va gioi han van toc toi da
        self.v += GRAVITY
        if self.v>8 :
            self.v =8
        dy +=self.v   
        # kiem tra va cham 
        for tile in  new_map.obstacle_lits:
            #kiem tra va cham theo chieu ngang
            if tile[1].colliderect(self.rect.x+dx,self.rect.y,self.width,self.height):
                dx = 0
                # if tile[0] == img_list[12]:
                #     tile[1].x -=dx
            if tile[1].colliderect(self.rect.x,self.rect.y+dy,self.width,self.height):
                if self.v >= 0:
                    self.v = 0
                    self.jump_limit = False
                    dy = tile[1].top-self.rect.bottom
                else:
                    self.v = 0
                    dy = tile[1].bottom - self.rect.top

        if self.rect.top > SCREEN_HEIGHT:
            self.health = 0
        self.rect.x += dx
        self.rect.y += dy
        if self.type =='player':
            if (self.rect.right > SCREEN_WIDTH-SCROLL and bg_scroll<= COLS*TILE_SIZE-SCREEN_WIDTH) or (self.rect.left <SCROLL and bg_scroll>abs(dx)):
                self.rect.x -=dx
                screen_scroll =-dx
            if self.rect.left+dx<=0 or self.rect.right+dx>=SCREEN_WIDTH:
                dx = 0
            if pygame.sprite.spritecollide(self,exit_group,False):
                # if enemy_group.has()==False:
                level_complete = True
                total_diamon += self.diamon
        return screen_scroll,level_complete
 # cap nhat hoat anh cho nhan vat       
    def update_animation(self):
        COUNTDOWN = 100
        self.image = self.animation_list[self.action][self.index]
        if pygame.time.get_ticks()-self.update_time >COUNTDOWN:
            self.update_time = pygame.time.get_ticks()
            self.index +=1
            if self.index >=len(self.animation_list[self.action]):
                if self.action !=3:
                    self.index = 0
                else:
                    self.index = len(self.animation_list[3])-1
# cap nhat hanh dong cua nhan vat
    def update_action(self,new_action):
        if new_action!=self.action:
            self.action = new_action
            self.index = 0
            self.update_time = pygame.time.get_ticks()
    def check_alive(self):
        if self.type =='player':
            if 0<self.health <=50:
                low_health_fx.play()
            else:
                low_health_fx.stop()
        if self.health <=0:
            self.health =0
            self.disappear-=1
            self.speed = 0
            self.alive =False
            self.update_action(3)
                
    def update(self):
        self.update_animation()
        self.check_alive()
        #update cooldown
        if self.shoot_cooldown >0:
            self.shoot_cooldown-=1
    def shoot(self):
        if self.shoot_cooldown ==0:
            self.shoot_cooldown=15
            bullets = Bullet(self.rect.centerx+(29*self.direction),self.rect.centery,self.direction,10)
            bullet_group.add(bullets)
            shoot_fx.play()
class Bullet(pygame.sprite.Sprite):
    def __init__(self,x,y,direction,speed):
        pygame.sprite.Sprite.__init__(self)
        self.speed = speed
        self.image = bullet_img
        self.rect = self.image.get_rect()
        self.rect.center = (x,y)
        self.direction = direction
    def update(self):
        self.rect.x += (self.direction*self.speed)
        if self.rect.right<0 or self.rect.right >SCREEN_WIDTH:
            self.kill()
        # xoa dan khi xay ra va cham
        for enemy in enemy_group:
            if pygame.sprite.spritecollide(enemy,bullet_group,False):
                if enemy.alive:
                    self.kill()
                    enemy.health-=20
        if pygame.sprite.spritecollide(player1,bullet_group,False):
            if player1.alive:
                self.kill()
                player1.health-=10
        for tile in  new_map.obstacle_lits:
            #kiem tra va cham theo chieu ngang
            if tile[1].colliderect(self.rect):
                self.kill()
class ItemBox(pygame.sprite.Sprite):
    def __init__(self,x,y,it_type):
        pygame.sprite.Sprite.__init__(self)
        self.it_type = it_type
        self.image = items_box[self.it_type]
        self.rect = self.image.get_rect()
        self.rect.midtop = (x + TILE_SIZE//2,y + (TILE_SIZE- self.image.get_height()))
    def update(self):
        self.rect.x +=screen_scroll
        if pygame.sprite.collide_rect(self,player1):
            if self.it_type =='Health':
                player1.health =min(player1.health+50,player1.max_health)
            collect_fx.play()
            self.kill()
class Enemy(Soldier):
    def __init__(self, pos_x, pos_y):
        super().__init__(pos_x, pos_y, typeOf = "enemy", scale = 1.5, speed =2)
        self.move_counter = 0
        self.idle = False
        self.idle_counter  = 0
        self.vision = pygame.Rect(0,0,200,20)
    def shoot(self):
        if self.shoot_cooldown ==0:
            self.shoot_cooldown=50
            bullets = Bullet(self.rect.centerx+(0.75 * self.rect.size[0] * self.direction),self.rect.centery,self.direction,5)
            bullet_group.add(bullets)
        # cai dat phuong thuc di chuyen cua ai
    def moving(self, move_left, move_right):
        dx = 0
        dy = 0
        for tile in  new_map.obstacle_lits:
            #kiem tra va cham theo chieu ngang
            if tile[1].colliderect(self.rect.x+dx,self.rect.y,self.width,self.height):
                self.direction*=-1
        return super().moving(move_left, move_right)
    def automatic(self):
        if self.alive and player1.alive:
            if self.idle == False and random.randint(1,300) ==1:
                self.idle =True
                self.update_action(0)
                self.idle_counter = 100
                # dung yen ban
            if self.vision.colliderect(player1.rect):
                self.idle =True
                self.update_action(0)
                self.shoot()
            if self.idle ==False:
                if self.direction==1:
                    ai_move_right = True
                else:
                    ai_move_right = False
                ai_move_left = not ai_move_right
                self.moving(ai_move_left,ai_move_right)
                self.update_action(1)
                self.move_counter+=1
                self.vision.center = (self.rect.centerx+75*self.direction ,self.rect.centery)
                # pygame.draw.rect(screen,RED,self.vision)
                if self.move_counter > TILE_SIZE:
                    self.direction*=-1
                    self.move_counter *=-1
            else:
                self.idle_counter -=1
                if self.idle_counter <=0:
                    self.idle =False
        elif player1.alive ==False:
            self.update_action(0)
        self.rect.x +=screen_scroll

class Decoration(pygame.sprite.Sprite):
    def __init__(self,x,y,img):
        pygame.sprite.Sprite.__init__(self)
        self.image = img
        self.rect = self.image.get_rect()
        self.rect.midtop = (x + TILE_SIZE//2,y + (TILE_SIZE- self.image.get_height()))
    def update(self):
        self.rect.x +=screen_scroll
class Water(pygame.sprite.Sprite):
    def __init__(self,x,y,img):
        pygame.sprite.Sprite.__init__(self)
        self.image = img
        self.rect = self.image.get_rect()
        self.rect.midtop = (x + TILE_SIZE//2,y + (TILE_SIZE- self.image.get_height()))
    def update(self):
        self.rect.x +=screen_scroll
        if self.rect.colliderect(player1.rect.x,player1.rect.y -player1.width//2,player1.width,player1.height):
            # music = 0
            # if music ==0:
            #     jump_water_fx.play()
            #     music +=1
            player1.health = 0
            
class Exit_level(pygame.sprite.Sprite):
    def __init__(self,x,y,img):
        pygame.sprite.Sprite.__init__(self)
        self.image = img
        self.rect = self.image.get_rect()
        self.rect.midtop = (x + TILE_SIZE//2,y + (TILE_SIZE- self.image.get_height()))
    def update(self):
        self.rect.x +=screen_scroll
class Map():
    def __init__(self):
        self.obstacle_lits = []
    def load_data(self,data):
        for y,row in enumerate(data):
            for x,tile in enumerate(row):
                if tile>=0:
                    img = img_list[tile]
                    img_rect = img.get_rect()
                    img_rect.x = x*TILE_SIZE
                    img_rect.y = y*TILE_SIZE
                    tile_data = (img,img_rect)
                    #ground
                if 0<= tile <=8:
                    self.obstacle_lits.append(tile_data)
                    #water
                elif 9<=tile<=10:
                    water = Water(x*TILE_SIZE,y*TILE_SIZE,img)
                    water_group.add(water)
                    #decorate
                elif 11<=tile<=14 or tile ==22:
                    if tile ==11 or tile ==12 or tile ==22:
                        img = pygame.transform.scale(img,(img.get_width()*2,img.get_height()*2))
                    if tile ==21:
                        img = pygame.transform.scale(img,(img.get_width()*2,img.get_height()*3))
                    decorate = Decoration(x*TILE_SIZE,y*TILE_SIZE,img)
                    decoration_group.add(decorate)
                #player
                elif tile ==15:
                    player1 = Soldier(x*TILE_SIZE,y*TILE_SIZE,'player',1.5,3)
                #enemy
                elif tile ==16:
                    enemy = Enemy(x*TILE_SIZE,y*TILE_SIZE)
                    enemy_group.add(enemy)
                #item box
                elif tile ==18:
                    item_box = ItemBox(x*TILE_SIZE,y*TILE_SIZE,'Health')
                    items_box_group.add(item_box)
                elif tile ==19 or tile ==17:
                    exit_level = Exit_level(x*TILE_SIZE,y*TILE_SIZE,img)
                    exit_group.add(exit_level)
                elif tile ==20:
                    diamon = Diamons(x*TILE_SIZE,y*TILE_SIZE,img)
                    diamon_group.add(diamon)
        return player1
    def draw(self):
        for tile in self.obstacle_lits:
            tile[1][0] +=screen_scroll
            screen.blit(tile[0],tile[1])
class hearth_bar():
    def __init__ (self,pos_x,pos_y):
        self.pos_x = pos_x
        self.pos_y = pos_y
    def update(self):
        pygame.draw.rect(screen, RED, pygame.Rect(self.pos_x, self.pos_y, 100,10))
        pygame.draw.rect(screen, (0,255,0), pygame.Rect(self.pos_x,self.pos_y,100*(player1.health/player1.max_health),10))
class Diamons(pygame.sprite.Sprite):
    def __init__(self,x,y,img):
        pygame.sprite.Sprite.__init__(self)
        self.image = img
        self.rect = self.image.get_rect()
        self.rect.midtop = (x + TILE_SIZE//2,y + (TILE_SIZE- self.image.get_height()))
    def update(self):
        self.rect.x +=screen_scroll 
        if self.rect.colliderect(player1.rect):
            player1.diamon+=1
            collect_fx.play()
            self.kill()

class Button():
    def __init__(self,img,x,y,scale):
        self.image = pygame.transform.scale(img,(img.get_width()*scale,img.get_height()*scale))
        self.rect = self.image.get_rect()
        self.rect.topleft =(x,y)
        self.clicked = False
    def draw(self,surface):
        action = False
        pos = pygame.mouse.get_pos()
        if self.rect.collidepoint(pos):
            if pygame.mouse.get_pressed()[0] == 1 and self.clicked ==False:
                self.clicked =True
                action = True
            elif pygame.mouse.get_pressed()[0] ==0:
                self.clicked = False
        surface.blit(self.image,(self.rect.x,self.rect.y))
        return action
class OptionBox():
    def __init__(self, x, y, w, h, color, highlight_color, font, option_list, selected = 0):
        self.color = color
        self.highlight_color = highlight_color
        self.rect = pygame.Rect(x, y, w, h)
        self.font = font
        self.option_list = option_list
        self.selected = selected
        self.draw_menu = False
        self.menu_active = False
        self.active_option = -1

    def draw(self, surf):
        pygame.draw.rect(surf, self.highlight_color if self.menu_active else self.color, self.rect)
        pygame.draw.rect(surf, (0, 0, 0), self.rect, 2)
        msg = self.font.render(self.option_list[self.selected], 1, (0, 0, 0))
        surf.blit(msg, msg.get_rect(center = self.rect.center))

        if self.draw_menu:
            for i, text in enumerate(self.option_list):
                rect = self.rect.copy()
                rect.y += (i+1) * self.rect.height
                pygame.draw.rect(surf, self.highlight_color if i == self.active_option else self.color, rect)
                msg = self.font.render(text, 1, (0, 0, 0))
                surf.blit(msg, msg.get_rect(center = rect.center))
            outer_rect = (self.rect.x, self.rect.y + self.rect.height, self.rect.width, self.rect.height * len(self.option_list))
            pygame.draw.rect(surf, (0, 0, 0), outer_rect, 2)

    def update(self, event_list):
        mpos = pygame.mouse.get_pos()
        self.menu_active = self.rect.collidepoint(mpos)
        
        self.active_option = -1
        for i in range(len(self.option_list)):
            rect = self.rect.copy()
            rect.y += (i+1) * self.rect.height
            if rect.collidepoint(mpos):
                self.active_option = i
                break

        if not self.menu_active and self.active_option == -1:
            self.draw_menu = False

        for event in event_list:
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                if self.menu_active:
                    self.draw_menu = not self.draw_menu
                elif self.draw_menu and self.active_option >= 0:
                    self.selected = self.active_option
                    self.draw_menu = False
                    return self.active_option
bullet_group = pygame.sprite.Group()
enemy_group = pygame.sprite.Group()
items_box_group = pygame.sprite.Group()
decoration_group = pygame.sprite.Group()
water_group = pygame.sprite.Group()
exit_group = pygame.sprite.Group()
diamon_group = pygame.sprite.Group()

#create button
start_btn = Button(start_img,20,SCREEN_HEIGHT-80,1)
restart_btn = Button(restart_img,SCREEN_WIDTH//2-menu_img.get_width()//2,SCREEN_HEIGHT-300,1)
exit_btn = Button(exit_img,SCREEN_WIDTH//2-88,SCREEN_HEIGHT//2,1)
resume_btn = Button(resume_img,SCREEN_WIDTH//2-88,SCREEN_HEIGHT//2-160,1)
setting_btn = Button(setting_img,SCREEN_WIDTH//2-88,SCREEN_HEIGHT//2-80,1)
menu_btn = Button(menu_img,SCREEN_WIDTH//2-menu_img.get_width()//2,SCREEN_HEIGHT-150,1)
close_btn = Button(close_img,SCREEN_WIDTH//2-106,SCREEN_HEIGHT-100,1)
general_btn = Button(general_img,200,6,1)
control_btn = Button (control_img,204+general_img.get_width(),6,1)
# TAO BAN DO
map_data = reset_level()
with open(f"level{levels}_data.csv",newline='') as f:
                    reader = csv.reader(f,delimiter=',')
                    for x,row in enumerate(reader):
                        for y,tile in enumerate(row):
                            map_data[x][y] = int(tile)
new_map = Map()
player1 =new_map.load_data(map_data)
img_down = 0
img_up = 150
hearth = hearth_bar(30,8)
list1 = OptionBox(
    400, 270, 160, 40, (150, 150, 150), (100, 200, 255), pygame.font.SysFont(None, 30), 
    ["100%", "75%", "50%","25%","0%"])
list2 = OptionBox(
    400, 130, 160, 40, (150, 150, 150), (100, 200, 255), pygame.font.SysFont(None, 30), 
    ["800x640","1280x720", "1920x1280"])
while run:
    event_list = pygame.event.get()
    if win_game==True:
        # screen.fill('sky blue')
        screen.fill((0,0,0))
        snow_animation()
        if menu_btn.draw(screen):
            start_game=False
            win_game = False
        screen.blit(you_win_img,(SCREEN_WIDTH//2-you_win_img.get_width()//2,min(img_down,img_up)))
        if img_down <150:
            img_down+=1
        else:
            img_up-=1
        if img_up==0:
            img_down=0
            img_up=150
    else:
        if set_up == True:
                pygame.mixer.music.set_volume(0)
                draw_bg()
                selected_option = list1.update(event_list)
                selected_option = list2.update(event_list)
                if exit_btn.draw(screen):
                    run = False
                if resume_btn.draw(screen):
                    set_up = False
                if setting_btn.draw(screen):
                    setting = True
                if setting == True:
                    screen.blit(set_up_img, (0,0))
                    list2.draw(screen)
                    list1.draw(screen)
                    if close_btn.draw(screen):
                        setting = False
                    if general_btn.draw(screen):
                        general_setting = True
                        control_setting = False
                    if control_btn.draw(screen):
                        control_setting = True  
                        general_setting = False
                    if control_setting == True:
                        screen.blit(control_setting_img,(0,0))
                        if close_btn.draw(screen):
                            setting = False
        else:
            if list1.selected == 4:
                pygame.mixer.music.set_volume(0)
            if list1.selected == 3:
                pygame.mixer.music.set_volume(0.3*0.25)
            if list1.selected == 2:
                pygame.mixer.music.set_volume(0.3*0.5)
            if list1.selected == 1:
                pygame.mixer.music.set_volume(0.3*0.75)
            if list1.selected == 0:
                pygame.mixer.music.set_volume(0.3)
            if start_game==False:
                start_screen()
                if start_btn.draw(screen):
                    start_game =True
                # if exit_btn.draw(screen):
                #     run = False
            else:
                draw_bg()
                hearth.update()
                snow_animation()
                new_map.draw()
                draw_charecter(f': {player1.diamon}',font,WHITE,4,4)
                player1.update()
                player1.display()
                for enemy in enemy_group:
                    enemy.automatic()
                    enemy.update()
                    if enemy.disappear>0:
                        enemy.display()
                #hien thi tat ca dan
                bullet_group.update()
                items_box_group.update()
                diamon_group.update()
                decoration_group.update() 
                water_group.update() 
                exit_group.update() 
                bullet_group.draw(screen)
                items_box_group.draw(screen)
                diamon_group.draw(screen)
                decoration_group.draw(screen) 
                water_group.draw(screen)
                exit_group.draw(screen)  
                if player1.alive:
                    if shoot:
                        player1.shoot()
                    if player1.jump_limit:
                        player1.update_action(2)
                    elif move_left or move_right:
                        player1.update_action(1)
                    else:
                        player1.update_action(0)
                    screen_scroll,level_complete=player1.moving(move_left,move_right)
                    bg_scroll -=screen_scroll
                    if level_complete:
                        screen_scroll = 0
                        levels+=1
                        if levels<=MAX_LEVEL:
                            bg_scroll =0
                            map_data = reset_level()
                            with open(f"level{levels}_data.csv",newline='') as f:
                                reader = csv.reader(f,delimiter=',')
                                for x,row in enumerate(reader):
                                    for y,tile in enumerate(row):
                                        map_data[x][y] = int(tile)
                            new_map = Map()
                            player1 =new_map.load_data(map_data)
                        if levels > MAX_LEVEL:
                            win_game = True
                            # start_game =False
                            levels = 1
                            bg_scroll =0
                            map_data = reset_level()
                            with open(f"level{levels}_data.csv",newline='') as f:
                                reader = csv.reader(f,delimiter=',')
                                for x,row in enumerate(reader):
                                    for y,tile in enumerate(row):
                                        map_data[x][y] = int(tile)
                            new_map = Map()
                            player1 =new_map.load_data(map_data)
                else:
                    # âm thanh người chơi chết chỉ phát 1 lần
                    if music ==0:
                        death_fx.play()
                    music+=1
                    screen_scroll =0
                    if music >=100:
                        music =100
                        screen.fill((0,0,0))
                        snow_animation()
                        screen.blit(game_over_img,(SCREEN_WIDTH//2-game_over_img.get_width()//2,min(img_down,img_up)))
                        if img_down <150:
                            img_down+=1
                        else:
                            img_up-=1
                        if img_up==0:
                            img_down=0
                            img_up=150
                        if restart_btn.draw(screen):
                            music = 0
                            bg_scroll =0
                            map_data = reset_level()
                            with open(f"level{levels}_data.csv",newline='') as f:
                                reader = csv.reader(f,delimiter=',')
                                for x,row in enumerate(reader):
                                    for y,tile in enumerate(row):
                                        map_data[x][y] = int(tile)
                            new_map = Map()
                            player1 =new_map.load_data(map_data)
                        if menu_btn.draw(screen):
                            music = 0
                            start_game=False
                            bg_scroll =0
                            map_data = reset_level()
                            with open(f"level{levels}_data.csv",newline='') as f:
                                reader = csv.reader(f,delimiter=',')
                                for x,row in enumerate(reader):
                                    for y,tile in enumerate(row):
                                        map_data[x][y] = int(tile)
                            new_map = Map()
                            player1 =new_map.load_data(map_data)
    for event in event_list:
        #quit game
        if event.type == pygame.QUIT:
            run = False
            # sys.exit()
        # keyboard_event
        if event.type ==pygame.KEYDOWN:
            # di sang trai
            if event.key == pygame.K_a:
                move_left = True
                # di sang phai
            if event.key == pygame.K_d:
                move_right = True
            if event.key == pygame.K_w:
                player1.jump = True
                jump_fx.play()
            if event.key == pygame.K_ESCAPE:
                # run = False
                set_up = True
            if event.key ==pygame.K_SPACE:
                shoot = True
        if event.type ==pygame.KEYUP:
            if event.key == pygame.K_a:
                move_left = False
            if event.key == pygame.K_d:
                move_right = False
            if event.key ==pygame.K_w:
                player1.jump = False
            if event.key ==pygame.K_SPACE:
                shoot = False
        # if event.type == pygame.MOUSEBUTTONDOWN:
        #     if event.button ==1:
        #         shoot = True
        # if event.type == pygame.MOUSEBUTTONUP:
        #     if event.button ==1:
        #         shoot = False
    clock.tick(60)
    pygame.display.update()      
pygame.quit()

