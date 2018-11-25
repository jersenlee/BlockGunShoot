import pygame, sys, random, time, os, math
import pygame.font
from pygame.locals import *

mainClock = pygame.time.Clock()
pygame.mixer.pre_init(44100, 16, 2, 4096)
pygame.init()

font1 = pygame.font.SysFont('arial', 24)
font2 = pygame.font.SysFont('arial', 60)

class enemy_object(object):
    def __init__(self, xenemy_position, enemy_direction, enemy_speed, enemy_type, enemy_index):
        self.enemy_position = [xenemy_position[0], xenemy_position[1]]
        self.enemy_type=enemy_type
        self.enemy_direction = enemy_direction
        self.enemy_speed = enemy_speed
        self.enemy_index = enemy_index

    def update_enemy(self, enemy_direction):
        self.enemy_position[0] = self.enemy_position[0] + self.enemy_speed * math.cos(enemy_direction)
        self.enemy_position[1] = self.enemy_position[1] + self.enemy_speed * math.sin(enemy_direction)     

    def show(self, enemy, screen, enemy_position):
        screen.blit(enemy, enemy_position)

class bullet_object(object):
    def __init__(self, bullet_position, direction, bullet_speed, bullet_type, bullet_range, host):
        start_time = time.time()
        self.bullet_position = [bullet_position[0], bullet_position[1]]
        self.current_position = [bullet_position[0], bullet_position[1]]
        self.direction = direction
        self.bullet_speed = bullet_speed
        self.bullet_type = bullet_type
        self.bullet_range = bullet_range
        self.host = host
        self.start_time = start_time

    def update_bullet(self):
        current_time = time.time()
        self.current_position[0] = self.bullet_position[0] + self.bullet_speed * math.cos(self.direction) * (current_time - self.start_time)
        self.current_position[1] = self.bullet_position[1] + self.bullet_speed * math.sin(self.direction) * (current_time - self.start_time)

    def show(self, screen):
        if self.bullet_type == 1:
            screen.blit(b, self.current_position)
        else :
            if self.bullet_type == 2:
                screen.blit(b_e, self.current_position)

bullets = []
enemys = []
capture_sound = pygame.mixer.Sound("Sounds\capture.ogg")
explosion_sound = pygame.mixer.Sound("Sounds\explosion.ogg")
laser_sound = pygame.mixer.Sound("Sounds\laser.ogg")
#pygame.mixer.music.load("Sounds\\titlesound.ogg")
#pygame.mixer.music.play(5000)

#capture_sound.play(-1)

#explosion_sound.play(-1)
size = width, height = 500, 350
 
screen = pygame.display.set_mode(size)

h = pygame.image.load("hero1.gif")
b = pygame.image.load("bullet.gif")
b_e = pygame.image.load("bullet_enemy.gif")
G = pygame.image.load("gun.gif")
HG = pygame.image.load("herowithgun.gif")
e = pygame.image.load("enemy.gif")


black = 0, 0, 0
herorect = h.get_rect()
gunrect = G.get_rect()
erect = e.get_rect()
right = False
left = False
up = False
down = False
shoot = False
speed = [0, 0]
randomspeed = [0, 0]
position = [0,0]
genemy_position = [0,0]
heropickedgun = False
e_deadflag = False
e_deadsoundflag = False
erect_updatetime = time.time()
bullet_updatetime =  time.time()
enemy_addtime = time.time()
bullet_removeflag = False
enemy_index = 0
enemybullet_updatetime = time.time()
enemybullet_updatetime_flag = False
hero_deadflag = False
hero_life = 3
kill_enemy = 0
while 1:
    screen.fill(black)  
    screen.blit(font1.render(u'hero_life : %d' % hero_life, True, [255, 255, 0]), [20, 20])
    screen.blit(font1.render(u'kill_enemy : %d' % kill_enemy, True, [255, 255, 0]), [300, 20])
    # Buttons ------------------------------------ #
    for event in pygame.event.get():
        if event.type == pygame.QUIT: 
            pygame.quit()
            sys.exit()
        if event.type == KEYDOWN:
            if event.key == K_RIGHT:
                right = True
            if event.key == K_LEFT:
                left = True
            if event.key == K_UP:
                up = True
            if event.key == K_DOWN:
                down = True
            if event.key == K_s:
                shoot = True
            if event.key == K_r:
                hero_life = 10
                hero_deadflag = False
                herorect.top = 20
                herorect.left = 20

        if event.type == KEYUP:
            if event.key == K_RIGHT:
                right = False
            if event.key == K_LEFT:
                left = False
            if event.key == K_UP:
                up = False
            if event.key == K_DOWN:
                down = False
            if event.key == K_s:
                shoot = False

    # Rect update ------------------------------------ #
    if right == True and herorect.right < width:
        speed[0] = 5
    if left == True and herorect.left > 5:
        speed[0] = -5
    if up == True and herorect.top > 5:
        speed[1] = -5
    if down == True and herorect.bottom < width:
        speed[1] = 5

    if right == False and left == False:
        speed[0] = 0
    if up == False and down == False:
        speed[1] = 0

    if time.time() - enemy_addtime > 2 :
        genemy_position[0] = width - 30
        genemy_position[1] = height / random.randint(1, 5)
        #print('{0:2d} {1:3d} {2:4d} {3:5d}'.format(herorect.left,herorect.right,enemy_position[0], enemy_position[1]))
        enemys.append(enemy_object(genemy_position, math.pi, 3, 1, enemy_index))
#        for enemy in enemys:
#            print("%5d ", enemy.enemy_index, enemy.enemy_position[0], enemy.enemy_position[1])
        enemy_addtime = time.time()
        enemy_index = enemy_index + 1


    if time.time() - erect_updatetime > 1 :
        for enemy in enemys: 
            enemy.enemy_direction = math.pi * random.randint(90,270)/180.0

        
        erect_updatetime = time.time()
    
    for enemy in enemys:       
        if time.time() - enemybullet_updatetime > random.randint(10, 30)/30 :
            if enemy.enemy_position[0] - (herorect.left+10) == 0 :
                bullets.append(bullet_object(enemy.enemy_position, math.pi, 800, 2, 100, 1))
            else :
                if enemy.enemy_position[0] - (herorect.left+10) > 0 :
                    bullets.append(bullet_object(enemy.enemy_position,  math.pi + math.atan((herorect.top+10-enemy.enemy_position[1]) / (herorect.left+10 - enemy.enemy_position[0])), 800, 2, 100, 1))
                else :
                    bullets.append(bullet_object(enemy.enemy_position,  math.atan((herorect.top+10-enemy.enemy_position[1]) / (herorect.left+10 - enemy.enemy_position[0])), 800, 2, 100, 1))
            enemybullet_updatetime_flag = True

        enemy.update_enemy(enemy.enemy_direction)
        enemy.show(e, screen, enemy.enemy_position)
        if enemy.enemy_position[0] < 0 :
            enemys.remove(enemy)
    if enemybullet_updatetime_flag == True :
        enemybullet_updatetime = time.time()
        enemybullet_updatetime_flag = False

    herorect = herorect.move(speed)

    
        
    if heropickedgun :

        if shoot == True :
            position[0] = herorect.right
            position[1] = herorect.top + 10
            if time.time() - bullet_updatetime > 0.1 :
                bullets.append(bullet_object(position, 0/180, 400, 1, 100, 1))
                bullet_updatetime = time.time()
            


        for bullet in bullets: 
            bullet.update_bullet()
            if bullet.current_position[0] > width or bullet.current_position[0] < 0 or bullet.current_position[1] > height or bullet.current_position[1] < 0 :
                bullets.remove(bullet)
            else:
#               print('{0:2d} {1:3d} {2:4d} {3:5d}'.format(herorect.left,herorect.right, herorect.top, herorect.bottom))
                bullet.show(screen)
                bullet_removeflag = False
                for enemy in enemys:
                    if bullet.bullet_type == 1 and bullet.current_position[0] > enemy.enemy_position[0] and bullet.current_position[0] < enemy.enemy_position[0] + 30 and bullet.current_position[1] > enemy.enemy_position[1] and bullet.current_position[1] < enemy.enemy_position[1] + 50:
                        enemys.remove(enemy)
                        kill_enemy = kill_enemy + 1
                        explosion_sound.play(-1,500)   
                        bullet_removeflag = True

                if bullet.bullet_type == 2 and bullet.current_position[0] > herorect.left and bullet.current_position[0] < herorect.right and bullet.current_position[1] > herorect.top and bullet.current_position[1] < herorect.bottom :
                    hero_deadflag = True
                    explosion_sound.play(-1, 500)
                    bullet_removeflag = True

                if bullet_removeflag == True :
                    bullets.remove(bullet)

        if hero_deadflag != True or hero_life != 0:
            screen.blit(HG, herorect)
        
        if hero_deadflag == True :
            if hero_life == 1 :
                herorect.top = -100
                herorect.left = -100
                hero_life = 0         


            else :
                if hero_life > 1 :
                    hero_life = hero_life - 1
                    hero_deadflag = False
                else :
                    screen.blit(font2.render(u'Game Over', True, [255, 255, 0]), [90, 150])



    else :
        if herorect.left > 90 and herorect.left < 120 and herorect.top > 90 and herorect.top < 120  :
            heropickedgun = True

        screen.blit(G,(100,100))

        screen.blit(h, herorect)


    pygame.display.flip()
    mainClock.tick(60)
