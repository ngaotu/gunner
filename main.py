import random
import pygame,sys
import os
import csv
pygame.init()
SCREEN_WIDTH = 800
SCREEN_HEIGHT = int(SCREEN_WIDTH * 0.8)
GRAVITY = 0.5
# so hang so cot cua map
ROWS = 16
COLS = 150
# kich thuoc cua 1 o
TILE_SIZE = SCREEN_HEIGHT//ROWS
TILE_TYPE = 20
levels =1
# Font 
font = pygame.font.SysFont('Futura',25)
# khoi tao cua so tro choi
screen = pygame.display.set_mode((SCREEN_WIDTH,SCREEN_HEIGHT))
pygame.display.set_caption(" Super Shooter")
clock = pygame.time.Clock() 
run = True
move_left = False
move_right = False
shoot = False
screen_scroll = 0
bg_scroll = 0
#bullet

# map _ img
img_list = []
for x in range(TILE_TYPE):
    img = pygame.image.load(f"D:/Workspace/game/img/tile/{x}.png").convert_alpha()
    img = pygame.transform.scale(img,(TILE_SIZE,TILE_SIZE))
    img_list.append(img)


# bullet_img = pygame.transform.scale(bullet_img,(bullet_img.get_width()*2.5,bullet_img.get_height()*0.5))
bullet_img = pygame.image.load('img/icons/bullet.png').convert_alpha()


#pick up item
health_box_img = pygame.image.load("D:/Workspace/game/img/icons/health_box.png").convert_alpha()
ammo_box_img = pygame.image.load("D:/Workspace/game/img/icons/ammo_box.png").convert_alpha()

items_box = {
    'Health' : health_box_img,
    'Ammo'  : ammo_box_img
}
# background 
heart_img = pygame.image.load('D:/Workspace/game/img/icons/heart.png').convert_alpha()
pine1_img = pygame.image.load('D:/Workspace/game/img/Background/pine1.png').convert_alpha()
pine2_img = pygame.image.load('D:/Workspace/game/img/Background/pine2.png').convert_alpha()
mountain_img = pygame.image.load('D:/Workspace/game/img/Background/mountain.png').convert_alpha()
sky_img = pygame.image.load('D:/Workspace/game/img/Background/sky_cloud.png').convert_alpha()
BG = (144, 201, 120)
RED = (255,0,0)
BLACK = (252,252,255)
def draw_bg():
	screen.fill(BG)
	width = sky_img.get_width()
	for x in range(5):
		screen.blit(sky_img, ((x * width) - bg_scroll * 0.5, 0))
		screen.blit(mountain_img, ((x * width) - bg_scroll * 0.6, SCREEN_HEIGHT - mountain_img.get_height() - 300))
		screen.blit(pine1_img, ((x * width) - bg_scroll * 0.7, SCREEN_HEIGHT - pine1_img.get_height() - 150))
		screen.blit(pine2_img, ((x * width) - bg_scroll * 0.8, SCREEN_HEIGHT - pine2_img.get_height()))

def draw_charecter(text,font,text_col,x,y):
    img = font.render(text,True,text_col)
    screen.blit(heart_img,(0,0))
    screen.blit(img,(x+heart_img.get_width(),y))
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
        #  list chua cac hinh anh cua doi tuong 
        self.animation_list = []
        self.update_time = pygame.time.get_ticks()
        # them list hanh dong  vao trong list hoat anh
        animation_types = ['Idle', 'Run', 'Jump','Death']
        for animation in animation_types:
			#reset temporary list of images
            temp_list = []
			#count number of files in the folder
            num_of_frames = len(os.listdir(f'D:/Workspace/game/img/{self.type}/{animation}'))
            for i in range(0,num_of_frames):
                img = pygame.image.load(f'D:/Workspace/game/img/{self.type}/{animation}/{i}.png').convert_alpha()
                img = pygame.transform.scale(img, (int(img.get_width() * scale), int(img.get_height() * scale)))
                temp_list.append(img)
            self.animation_list.append(temp_list)
        self.image = self.animation_list[self.action][self.index]
        self.rect = self.image.get_rect()
        self.rect.center = (pos_x,pos_y)
    def display(self):
        screen.blit(pygame.transform.flip(self.image,self.flip,False),self.rect)
        pygame.draw.rect(screen,(155,155,155),self,1)
    def moving(self,move_left,move_right):
        dx = 0
        dy = 0
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
            self.v = -8
            self.jump = False
            self.jump_limit = True
        # them trong luc va gioi han van toc toi da
        self.v += GRAVITY
        if self.v>7 :
            self.v =7
        dy +=self.v   
        # kiem tra va cham 
        if self.rect.bottom + dy > 400:
            dy = 400-self.rect.bottom 
            self.jump_limit = False
        # cap nhat vi tri moi cua soldier
        self.rect.x += dx
        self.rect.y += dy
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
            bullets = Bullet(self.rect.centerx+(30*self.direction),self.rect.centery,self.direction,10)
            bullet_group.add(bullets)
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
                player1.health-=5
class ItemBox(pygame.sprite.Sprite):
    def __init__(self,x,y,it_type):
        pygame.sprite.Sprite.__init__(self)
        self.it_type = it_type
        self.image = items_box[self.it_type]
        self.rect = self.image.get_rect()
        self.rect.midtop = (x + TILE_SIZE//2,y + (TILE_SIZE- self.image.get_height()))
    def update(self):
        if pygame.sprite.collide_rect(self,player1):
            if self.it_type =='Health':
                player1.health =min(player1.health+50,player1.max_health)
            if self.it_type =='Ammo':
                pass
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
    def automatic(self,player1):
        if self.alive and player1.alive:
            if random.randint(1,300) ==1:
                self.idle =True
                self.update_action(0)
                self.idle_counter = 100
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
        else:
            self.update_action(3)
class Decoration(pygame.sprite.Sprite):
    def __init__(self,x,y,img):
        pygame.sprite.Sprite.__init__(self)
        self.image = img
        self.rect = self.image.get_rect()
        self.rect.midtop = (x + TILE_SIZE//2,y + (TILE_SIZE- self.image.get_height()))
class Water(pygame.sprite.Sprite):
    def __init__(self,x,y,img):
        pygame.sprite.Sprite.__init__(self)
        self.image = img
        self.rect = self.image.get_rect()
        self.rect.midtop = (x + TILE_SIZE//2,y + (TILE_SIZE- self.image.get_height()))
class Exit_level(pygame.sprite.Sprite):
    def __init__(self,x,y,img):
        pygame.sprite.Sprite.__init__(self)
        self.image = img
        self.rect = self.image.get_rect()
        self.rect.midtop = (x + TILE_SIZE//2,y + (TILE_SIZE- self.image.get_height()))
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
                elif 11<=tile<=14:
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
                elif tile ==17:
                    item_box = ItemBox(x*TILE_SIZE,y*TILE_SIZE,'Ammo')
                    items_box_group.add(item_box)
                elif tile ==18:
                    item_box = ItemBox(x*TILE_SIZE,y*TILE_SIZE,'Health')
                    items_box_group.add(item_box)
                elif tile ==19:
                    exit_level = Exit_level(x*TILE_SIZE,y*TILE_SIZE,img)
                    exit_group.add(exit_level)
        return player1
    def draw(self):
        for tile in self.obstacle_lits:
            screen.blit(tile[0],tile[1])
        

bullet_group = pygame.sprite.Group()
enemy_group = pygame.sprite.Group()
items_box_group = pygame.sprite.Group()
decoration_group = pygame.sprite.Group()
water_group = pygame.sprite.Group()
exit_group = pygame.sprite.Group()
item_box = ItemBox(200,300,'Health')
items_box_group.add(item_box)


# bg =pygame.image.load('D:/Workspace/game/img/background/mountain.png')
# rect_bg =  bg.get_rect()
# rect_bg.center =((0,0))

# TAO BAN DO
# khoi tao ban do rong
map_data = []
for row in range(ROWS):
    r =[-1]*COLS
    map_data.append(r)
# them du lieu vao ban do
with open(f"D:/Workspace/game/level{levels}_data.csv",newline='') as f:
    reader = csv.reader(f,delimiter=',')
    for x,row in enumerate(reader):
        for y,tile in enumerate(row):
            map_data[x][y] = int(tile)
new_map = Map()
player1 =new_map.load_data(map_data)
print(map_data)
while run:
    draw_bg()
    new_map.draw()
    draw_charecter(f': {player1.health}',font,BLACK,4,4)
    player1.update()
    player1.display()
    for enemy in enemy_group:
        enemy.automatic(player1)
        enemy.update()
        if enemy.disappear>0:
            enemy.display()
    #hien thi tat ca dan
    bullet_group.update()
    items_box_group.update() 
    decoration_group.update() 
    water_group.update() 
    exit_group.update() 
    bullet_group.draw(screen)
    items_box_group.draw(screen)
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
        player1.moving(move_left,move_right)
    else:
        pass
    
    for event in pygame.event.get():
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
            if event.key == pygame.K_SPACE:
                player1.jump = True
            if event.key == pygame.K_ESCAPE:
                run = False
        if event.type ==pygame.KEYUP:
            if event.key == pygame.K_a:
                move_left = False
            if event.key == pygame.K_d:
                move_right = False
            if event.key ==pygame.K_SPACE:
                player1.jump = False
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button ==1:
                shoot = True
        if event.type == pygame.MOUSEBUTTONUP:
            if event.button ==1:
                shoot = False
    clock.tick(60)
    pygame.display.update()      
pygame.quit()

