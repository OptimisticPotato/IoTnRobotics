import pygame
import sys
import random
import modi
import time

bundle = modi.MODI(conn_type="ser")
button = bundle.buttons[0]
gyro = bundle.gyros[0]
mic = bundle.mics[0]
dial = bundle.dials[0]
speaker = bundle.speakers[0]

ScreenWidth = 720
ScreenHeight = 960

instruction = ['배경\instruction1.png', '배경\instruction2.png']
cut = [100, 70, 50, 30]
sound = ["finalA", "finalB", "finalC", "finalD"]

pygame.init()

pop = pygame.mixer.Sound("소리\pop.wav")
pygame.mixer.music.load('소리\축제.mp3')


score_up_name = ['attend', 'homework', 'quiz', 'exam']
score_up_score = [1.5, 3, 8, 11]
score_up_speed_x = [1.2, 1, 0.7, 0.5]
score_up_speed_y_max = [60, 40, 30, 35]
score_up_speed_y_min = [30, 30, 20, 25]
score_up_list = []
score_up_delay = [2, 5, 10, 15]
score_up_stress = [5, 7, 10, 20]
score_up_life = [0, 0, 1, 5]

score_down_speed_x = [2, 1.5, 1, 0.4]
score_down_speed_y_max = [35, 25, 15, 11]
score_down_speed_y_min = [30, 15, 8, 5]
score_down_delay = [6, 7, 10, 13]
score_down_score = [4, 6, 8, 10]
score_down_list = []
score_down_stress = [7, 7, 13, 15]


class score_down():
    def __init__(self, type):
        self.type_no = int(type - 1)
        self.image = pygame.image.load(f'그림\down{type}.png')
        self.size = self.image.get_rect().size
        self.width = self.size[0]
        self.height = self.size[1]
        self.speed_x = score_down_speed_x[self.type_no]
        self.speed_y = random.randint(score_down_speed_y_min[self.type_no], score_down_speed_y_max[self.type_no]) / 10
        self.delay = score_down_delay[self.type_no]
        self.score = score_down_score[self.type_no]
        self.x = random.randint(1, ScreenWidth - self.width)
        self.start = - self.delay * 60 * self.speed_y
        self.y = self.start
        score_down_list.append(self)
        self.count = 0
        self.stress = score_down_stress[self.type_no]

drink = score_down(1)
drink2 = score_down(2)
football = score_down(3)
game = score_down(4)


class score_up():
    def __init__(self, type):
        self.type_no = int(type - 1)
        self.image = pygame.image.load(f'그림\{type}.png')
        self.size = self.image.get_rect().size
        self.width = self.size[0]
        self.height = self.size[1]
        self.speed_x = score_up_speed_x[self.type_no]
        self.speed_y = random.randint(score_up_speed_y_min[self.type_no], score_up_speed_y_max[self.type_no]) / 10
        self.delay = score_up_delay[self.type_no]
        self.score = score_up_score[self.type_no]
        self.x = random.randint(1, ScreenWidth - self.width)
        self.start = - self.delay * 60 * self.speed_y
        self.y = self.start
        score_up_list.append(self)
        self.count = 0
        self.stress = score_up_stress[self.type_no]
        self.life = score_up_life[self.type_no]

attend = score_up(1)
attend2 = score_up(1)
homework = score_up(2)
quiz = score_up(3)
exam = score_up(4)


flake_list = []

red_flake = ["red1", "red2", "red3", "red4", "red5"]
green_flake = ["green1", "green2", "green3", "green4", "green5"]
blue_flake = ["blue1", "blue2", "blue3", "blue4", "blue5"]

class flake():
	def __init__(self, r, g, b):
		self.RGB = (r, g, b)
		self.width = 10
		self.height = 10
		self.speed = random.randint(3, 8)
		self.x = random.randint(0, ScreenWidth - self.width)
		self.y = - self.height
		flake_list.append(self)
		
	def flake_draw(self):
		pygame.draw.rect(Screen, self.RGB, (self.x, self.y, self.width, self.height))

for r in red_flake:
    r = flake(255, 0, 0)
for g in green_flake:
    g = flake(0, 255, 0)
for b in blue_flake:
    b = flake(0, 0, 255)


def initGame():
    global Screen, clock, background, player, start, missile
    pygame.init()
    Screen = pygame.display.set_mode((ScreenWidth, ScreenHeight))
    pygame.display.set_caption("Test Game")
    background = pygame.image.load('배경\ckground.png')
    player = pygame.transform.scale(pygame.image.load('그림\student_right.png'), (85, 78))
    start = pygame.image.load('배경\시작.png')
    missile = pygame.transform.scale(pygame.image.load('그림\pencil.png'), (10, 20))
    clock = pygame.time.Clock()
        

def draw(obj, x, y):
    global Screen
    Screen.blit(obj, (x, y))


def write(thing, size, x, y):
       font = pygame.font.Font("neo.ttf", size)
       text = font.render(str(thing), True, (0, 0, 0))
       Screen.blit(text, (x, y))
       

def runGame():
    global Screen, clock, background, player, start, missile, limit
    
    missileXY = []
    missileSize = missile.get_rect().size
    missileWidth = missileSize[0]
    missileHeight = missileSize[1]
    missileSpeed = 5
    limit = 5
    
    playerSize = player.get_rect().size
    playerWidth = playerSize[0]
    playerHeight = playerSize[1]
    
    x = (ScreenWidth - playerWidth) * 0.5
    y = (ScreenHeight - playerHeight) * 0.95
    playerX = 0
    playerY = 0
    
    game_instruction = -1
    game_stage = 0
    score = 0
    stress = 0
    missile_gauge = 0
    flake_count = 0
    start_y = 0
    stress_factor = 1
    sound = 0
    music = 0
    
    while True:
    
        playerX = - round(0.05 * gyro.pitch, 2)
        playerY = round(0.05 * gyro.roll, 2)
        nul = 0 
        
        
        if 35 < stress <= 65:
            stress_factor = round(0.01 * random.randrange(round(100 - stress * 0.7), round(100 - stress * 0.2)), 2)
        elif 65 < stress <= 90:
            stress_factor = round(0.01 * random.randrange(round(80 - stress * 0.5), round(80 - stress * 0.2)), 2)
        elif 90 < stress <= 100:
            stress_factor = round(0.01 * random.randrange(round(20 - stress * 0.1), round(40 + stress * 0.1)), 2)
        elif stress > 100:
            stress = 100
        elif stress < 0:
            stress = 0
        else:
            stress_factor = 1
        
        if dial.degree > 87.5:
            game_instruction = 3
        elif dial.degree > 62.5:
            game_instruction = 2
        elif dial.degree > 37.5:
            game_instruction = 1
        elif dial.degree > 12.5:
            game_instruction = 0
        else:
            game_instruction = -1
        
                
        for event in pygame.event.get():
            if event.type in [pygame.QUIT]:
                pygame.quit()
                sys.exit()

        if game_instruction == -1:
            draw(pygame.image.load('배경\시작.png'), 0, 0)
            draw(pygame.image.load('그림\시작.png'), 215, start_y)
            
            if start_y < 400:
                start_y += 8
            else:
                start_y = 400
            
            if start_y == 400:
                write('탕탕 연뚜리', 70, 180, 150)
                write('TURN THE DIAL TO CONTINUE', 30, 200, 800)
                                
                    
        elif game_instruction == 0 or game_instruction == 1:
            draw(pygame.image.load(instruction[game_instruction]), 0, 0)
            score = 0
            stress = 0
            start_y = 0
            game_stage = 0
            sound = 0
            music = 0
            
            for m in score_down_list:
                m.count = 0
                m.y = m.start
                m.count = 0
            
            for m in score_up_list:
                m.count = 0
                m.y = m.start
                m.count = 0
            
            x = (ScreenWidth - playerWidth) * 0.5
            y = (ScreenHeight - playerHeight) * 0.95
#####################################################        

        elif game_instruction == 2:
            if game_stage == 0:
                draw(background, 0, 0)
                
                if button.pressed is True:  #버튼 미사일 발사
                    missile_gauge += 2
                    if missile_gauge >= 30:
                        missile_gauge = 0
                        if len(missileXY) < limit:
                            missileX = x + playerWidth / 2 - missileWidth / 2
                            missileY = y - 10
                            missileXY.append([missileX, missileY])
                            speaker.tune = 700, 10
                                   
                    elif missile_gauge > 20:
                        speaker.turn_off()
                
                    pygame.draw.rect(Screen, (255, 255, 255), (x, y - 25, playerWidth, 10))
                    
                    if len(missileXY) < limit:
                        pygame.draw.rect(Screen, (0, 0, 255), (x, y - 25, missile_gauge * playerWidth / 30, 10))
                    else:
                        pygame.draw.rect(Screen, (150, 150, 150), (x, y - 25, missile_gauge * playerWidth / 30, 10))
                    
                else:
                    missile_gauge = 0
                    speaker.turn_off()


                for m in score_up_list:
                    m.y += m.speed_y
                    m.x += m.speed_x
                    if m.x > ScreenWidth - m.width:
                        m.x = ScreenWidth - m.width
                        m.speed_x = - m.speed_x
                    elif m.x <= 0:
                        m.x = 0
                        m.speed_x = - m.speed_x
                    elif m.y > ScreenHeight:
                        m.y = m.start
                        m.x = random.randint(1, ScreenWidth - m.width)
                        score -= m.score * 0.5
                        m.count += 1
                    
                    draw(m.image, m.x, m.y)
                
                for m in score_down_list:
                    m.y += m.speed_y
                    m.x += m.speed_x
                    if m.x > ScreenWidth - m.width:
                        m.x = ScreenWidth - m.width
                        m.speed_x = - m.speed_x
                    elif m.x <= 0:
                        m.x = 0
                        m.speed_x = - m.speed_x
                    elif m.y > ScreenHeight:
                        m.y = m.start
                        m.x = random.randint(1, ScreenWidth - m.width)
                        m.count += 1
                    
                    draw(m.image, m.x, m.y)

                x += playerX
                if x < 0:
                    x = 0
                elif x > ScreenWidth - playerWidth:
                    x = ScreenWidth - playerWidth
                
                y += playerY
                if y < 0:
                    y = 0
                elif y > ScreenHeight - playerHeight:
                    y = ScreenHeight - playerHeight
                
                #stress_gauge (x, y, dx, dy)
                pygame.draw.rect(Screen, (255, 255, 255), (200, 30, 300, 10))
                stress_gauge_length = stress * 3

                if 35 < stress <= 65:
                    pygame.draw.rect(Screen, (255, 150, 0), (200, 30, stress_gauge_length, 10))
                    draw(pygame.transform.scale(pygame.image.load('그림\stress2.png'), (30, 30)), 160, 15)
                elif 65 < stress <= 90:
                    pygame.draw.rect(Screen, (255, 0, 0), (200, 30, stress_gauge_length, 10))
                    draw(pygame.transform.scale(pygame.image.load('그림\stress3.png'), (30, 30)), 160, 15)
                elif stress > 90:
                    pygame.draw.rect(Screen, (0, 0, 0), (200, 30, stress_gauge_length, 10))
                    draw(pygame.transform.scale(pygame.image.load('그림\stress4.png'), (30, 30)), 160, 15)
                else:
                    pygame.draw.rect(Screen, (0, 0, 255), (200, 30, stress_gauge_length, 10))
                    draw(pygame.transform.scale(pygame.image.load('그림\stress1.png'), (30, 30)), 160, 15)
                
                
                if len(missileXY) != 0:
                    for i, bxy in enumerate(missileXY):
                        bxy[1] -= missileSpeed
                        missileXY[i][1] = bxy[1]
                        if bxy[1] <= -missileHeight:
                            missileXY.remove(bxy)
                            score -= 0.1
                                                
                        for n in score_up_list: #충돌판정
                            if n.y + n.height > bxy[1]  > n.y - missileHeight:
                                if n.x - missileWidth < bxy[0] < n.x + n.width:
                                    missileXY.remove(bxy)
                                    score += n.score * stress_factor
                                    n.life -= 1
                                    stress += n.stress * 0.3
                                    if n.life < 0:
                                        n.y = n.start
                                        n.x = random.randint(0, ScreenWidth - n.width)
                                        n.speed_x = random.randint(n.speed_x * 10 - 5, n.speed_x * 10 + 5) / 10
                                        stress += n.stress
                                        n.count += 1
                                        n.life = score_up_life[n.type_no]
                                        pop.play()
                        
                        for n in score_down_list: #충돌판정
                            if n.y + n.height > bxy[1]  > n.y - missileHeight:
                                if n.x - missileWidth < bxy[0] < n.x + n.width:
                                    missileXY.remove(bxy)
                                    n.y = n.start
                                    n.x = random.randint(0, ScreenWidth - n.width)
                                    n.speed_x = random.randint(n.speed_x * 10 - 15, n.speed_x * 10 + 15) / 10
                                    stress -= n.stress
                                    score -= n.score
                                    n.count += 1
                                    pop.play()
                                    
                    for mx, my in missileXY:
                        draw(missile, mx, my)                
                
                real_score = round(score, 1)
                write(f'SCORE : {real_score}', 20, 10, 10)
                                
                                    
                if playerX < 0:
                    draw(pygame.transform.scale(pygame.image.load('그림\student.png'), (85, 78)), x, y)
                else:
                    draw(player, x, y)

                if exam.count == 1:
                    missileXY = []
                    x = (ScreenWidth - playerWidth) * 0.5
                    y = (ScreenHeight - playerHeight) * 0.95
                    for i in score_up_list:
                        i.y = -i.height
                    game_stage = 1

                if exam.count == 3:
                    game_stage = 2

                for m in range(limit - len(missileXY)):
                    draw(missile, x + nul + 10 , y + 50)
                    nul += 15
##########################################################

            elif game_stage == 1:
                speaker.turn_off()
                if music == 0:
                    pygame.mixer.music.play()
                    music = 1
                draw(pygame.image.load('배경\축제.png'), 0, 0)
                pygame.draw.rect(Screen, (255, 255, 255), (200, 30, 300, 10))
                stress_gauge_length = stress * 3
        
                if 35 < stress <= 65:
                    pygame.draw.rect(Screen, (255, 150, 0), (200, 30, stress_gauge_length, 10))
                    draw(pygame.transform.scale(pygame.image.load('그림\stress2.png'), (30, 30)), 160, 15)
                elif 65 < stress <= 90:
                    pygame.draw.rect(Screen, (255, 0, 0), (200, 30, stress_gauge_length, 10))
                    draw(pygame.transform.scale(pygame.image.load('그림\stress3.png'), (30, 30)), 160, 15)
                elif stress > 90:
                    pygame.draw.rect(Screen, (0, 0, 0), (200, 30, stress_gauge_length, 10))
                    draw(pygame.transform.scale(pygame.image.load('그림\stress4.png'), (30, 30)), 160, 15)
                else:
                    pygame.draw.rect(Screen, (0, 0, 255), (200, 30, stress_gauge_length, 10))
                    draw(pygame.transform.scale(pygame.image.load('그림\stress1.png'), (30, 30)), 160, 15)


                if mic.volume > 20:
                    if stress > 0:
                        stress -= 0.05 * mic.volume / 20
                
                
                for i in flake_list:
                    i.y += i.speed
                    if i.y >= ScreenHeight:
                        i.y = -i.height * random.randint(1, 10)
                        i.x = random.randint(0, ScreenWidth - i.width)
                        flake_count += 1
                        i.speed = random.randint(3, 8)
                                    
                    i.flake_draw()
                    
                if flake_count > 40:
                    for a in score_up_list:
                        a.y = a.start
                    for a in score_down_list:
                        a.y = a.start
                    
                    game_stage = 0
                    exam.count = 2
                    pygame.mixer.music.stop()
                    time.sleep(1)                    
                    
            elif game_stage == 2: #RESULT
                draw(pygame.image.load(f'배경\시작.png'), 0, 0)
                time.sleep(1)
                if score <= 10:
                    draw(pygame.image.load(f'결과\망.png'), 0, 0)
                    if sound == 0:
                        pygame.mixer.Sound("소리\망.wav").play()
                        sound = 1
                else:
                    for m in cut:
                        if score >= m:
                            draw(pygame.image.load(f'결과\{m}.png'), 0, 0)
                            if sound == 0:
                                pygame.mixer.Sound(f'소리\{m}.wav').play()
                                sound = 1
                            break
                        
                    
                
        elif game_instruction == 3: #pause menu
            write("PAUSE", 100, ScreenWidth * 0.35, ScreenHeight * 0.45)


        pygame.display.update()
        
        clock.tick(60)
    
    pygame.quit()

       
initGame()
runGame()