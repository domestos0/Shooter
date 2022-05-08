from pygame import *
from random import randint
from time import time as timer

#музыка
mixer.init()
mixer.music.load('space.ogg')
mixer.music.play()
fire_sound = mixer.Sound('fire.ogg')
flight_sound = mixer.Sound('flight.ogg')
laser_shot = mixer.Sound('laser_shot.ogg')
arrow_shot = mixer.Sound('bow_arrow.ogg')

font.init()
font1 = font.SysFont('Verdana', 80)
win = font1.render('YOU WIN', True, (255, 255, 255))
lose = font1.render('YOU LOSE', True, (180, 0, 0))
font2 = font.SysFont('Times New Roman', 36)

#Картинки
img_back = 'galaxy.jpg' #Фон
img_hero = 'rocket.png' #Игрок
img_enemy = 'ufo.png' #Враги
img_bullet = 'bullet.png' #Пуля
img_rocket = 'rocket1.png' #Ракета
img_laser = 'laser.png' #Лазер
img_arrow = 'arrow.png' #Стрела
img_asteroid = 'asteroid.png' #Астероид

score = 0 #Сбитых врагов
goal = 100 #Столько юфошек нужно сбить для победы
lost = 0 #Пропущено врагов
max_lost = 3 #Проигрыш, если пропустил столько юфошек
life = 3 #Жизни

#Класс-родитель для спрайтов
class GameSprite(sprite.Sprite):
    #Конструктор класса
    def __init__(self, player_image, player_x, player_y, size_x, size_y, player_speed):
        super().__init__()
        #Каждый спрайт должен хранить свойство image - изображение
        self.image = transform.scale(image.load(player_image), (65, 65))
        self.speed = player_speed
        #Каждый спрайт должен хранить свойство rect - прямоугольник, в который он вписан
        self.rect = self.image.get_rect()
        self.rect.x = player_x
        self.rect.y = player_y
    #Метод для отрисовки героя на экране
    def reset(self):
        window.blit(self.image, (self.rect.x, self.rect.y))

#Класс самого игрока
class Player(GameSprite):
    def update(self):
        keys = key.get_pressed()
        if keys[K_LEFT] and self.rect.x > 5:
            self.rect.x -= self.speed
        if keys[K_RIGHT] and self.rect.x < win_width - 80:
            self.rect.x += self.speed
    #Метод "Выстрел"
    def fire(self):
        bullet = Bullet(img_bullet, self.rect.centerx, self.rect.top, 15, 20, -15)
        bullets.add(bullet)

    def rocket(self):
        rocket = Bullet(img_rocket, self.rect.centerx, self.rect.top, 15, 20, -15)
        bullets.add(rocket)

    def laser(self):
        laser = Bullet(img_laser, self.rect.centerx, self.rect.top, 15, 20, -15)
        bullets.add(laser)

    def arrow(self):
        arrow = Bullet(img_arrow, self.rect.centerx, self.rect.top, 15, 20, -15)
        bullets.add(arrow)

#Класс врага
class Enemy(GameSprite):
    #Движение
    def update(self):
        self.rect.y += self.speed
        global lost
        #Исчезает, если дойдет до края экрана
        if self.rect.y > win_height:
            self.rect.x = randint(80, win_width - 80)
            self.rect.y = 0
            lost = lost + 1

#Класс пуля
class Bullet(GameSprite):
    #Движение
    def update(self):
        self.rect.y += self.speed
        #Исчезает, если доходит до конца экрана
        if self.rect.y < 0:
            self.kill()

#Создание окна
win_width = 700
win_height = 500
display.set_caption('Шутер')
window = display.set_mode((win_width, win_height))
background = transform.scale(image.load(img_back), (win_width, win_height))

#Создаем спрайты
space_ship = Player(img_hero, 5, win_height - 100, 80, 100, 10)

monsters = sprite.Group()
for i in range(1, 6):
    monster = Enemy(img_enemy, randint(80, win_width - 80), -40, 80, 50, randint(1, 5))
    monsters.add(monster)
    
asteroids = sprite.Group()
for i in range(1, 3):
    asteroid = Enemy(img_asteroid, randint(30, win_width - 30), -40, 80, 50, randint(1, 7))
    asteroids.add(asteroid)

bullets = sprite.Group()
#Переменная "Игра закончилась", как только True - перестают работать спрайты
finish = False
#Основной цикл
run = True #Флаг сбрасывается кнопкой закрытия окна

rel_time = False #Флаг, отвечающий за перезарядку

num_fire = 0 #Переменная для подчета выстрелов

while run:
    #Событие нажатия на кнопку "Закрыть"
    for e in event.get():
        if e.type == QUIT:
            run = False
        #Событие нажатия на пробел - игрок стреляет
        elif e.type == KEYDOWN:
            if e.key == K_1:
                if num_fire < 5 and rel_time == False:
                    num_fire = num_fire + 1
                    fire_sound.play()
                    space_ship.fire()
                    
                if num_fire  >= 5 and rel_time == False : #если игрок сделал 5 выстрелов
                    last_time = timer() #засекаем время, когда это произошло
                    rel_time = True #ставим флаг перезарядки

            elif e.key == K_2:
                if num_fire < 2 and rel_time == False:
                    num_fire = num_fire + 1
                    flight_sound.play()
                    space_ship.rocket()

                if num_fire  >= 2 and rel_time == False : #если игрок сделал 2 выстрелов
                    last_time = timer() #засекаем время, когда это произошло
                    rel_time = True #ставим флаг перезарядки

            elif e.key == K_3:
                if num_fire < 3 and rel_time == False:
                    num_fire = num_fire + 1
                    laser_shot.play()
                    space_ship.laser()

                if num_fire  >= 3 and rel_time == False : #если игрок сделал 3 выстрелов
                    last_time = timer() #засекаем время, когда это произошло
                    rel_time = True #ставим флаг перезарядки

            elif e.key == K_4:
                if num_fire < 5 and rel_time == False:
                    num_fire = num_fire + 1
                    arrow_shot.play()
                    space_ship.arrow()

                if num_fire  >= 5 and rel_time == False : #если игрок сделал 5 выстрелов
                    last_time = timer() #засекаем время, когда это произошло
                    rel_time = True #ставим флаг перезарядки 
       
    #Сама игра - действие спрайтов, проверка правил игры, перерисовка
    if not finish:
        #Обновляем фон
        window.blit(background, (0,0))
        
        #Производим движение спрайтов
        space_ship.update()
        monsters.update()
        asteroids.update()
        bullets.update()
       
        #Обновляем их в новом местоположении при каждой итерации цикла
        space_ship.reset()
        monsters.draw(window)
        asteroids.draw(window)
        bullets.draw(window)

        #Перезарядка
        if rel_time == True:
            now_time = timer() #Считываем время

            if now_time - last_time < 3: #Пока не прошло 3 секунды, выводим информацию о перезарядке
                reload = font2.render('Reloading...', 1, (150, 0, 0))
                window.blit(reload, (260, 460))
            else:
                num_fire = 0 #Обнуляем счетчик
                rel_time = False #Сбрасываем флаг перезарядки

        #Проверка столкновения пули и монстров, при этом и монстр, и пуля при касании исчезают
        collides = sprite.groupcollide(monsters, bullets, True, True)
        for c in collides:
            #Этот цикл повторится столько раз, сколько монстров сбито
            score = score + 1
            monster = Enemy(img_enemy, randint(80, win_width - 80), -40, 80, 50, randint(1, 5))
            monsters.add(monster)

        #Если спрайт коснулся врага, уменьшает жизнь
        if sprite.spritecollide(space_ship, monsters, False) or sprite.spritecollide(space_ship, asteroids, False):
            sprite.spritecollide(space_ship, monsters, True)
            sprite.spritecollide(space_ship, asteroids, True)
            life = life - 1
        
        #Возможный проигрыш - пропустил слишком много или герой столкнулся с врагом
        if life == 0 or lost >= max_lost:
            finish = True #Проиграв, больше не можем управлять спрайтами
            window.blit(lose, (200, 200))

        #Проверка выигрыша - сколько очков набрал?
        if score >= goal:
            finish = True
            window.blit(win, (200, 200))

        #Пишем текст на экране
        text = font2.render('Счет: ' + str(score), 1, (255, 255, 255))
        window.blit(text, (10, 20))

        text_lose = font2.render('Пропущено: ' + str(lost), 1, (255, 255, 255))
        window.blit(text_lose, (10, 50))
        
        #Разный цвет в зависимости от кол-ва жизней
        if life == 3:
            life_color = (0, 150, 0)
        if life == 2:
            life_color = (150, 250, 0)
        if life == 1:
            life_color = (150, 0, 0)

        text_life = font1.render(str(life), 1, life_color)
        window.blit(text_life, (630, 10))

        display.update()
    #Бонусный перезапуск игры, если выиграл или проиграл
    else:
        finish = False
        score = 0
        lost = 0
        num_fire = 0
        life = 3
        for b in bullets:
            b.kill()
        for m in monsters:
            m.kill()
        for a in asteroids:
            a.kill()

        time.delay(3000)
        for i in range(1, 6):
            monster = Enemy(img_enemy, randint(80, win_width - 80), -40, 80, 50, randint(1, 5))
            monsters.add(monster)
        
        for i in range(1, 3):
            asteroid = Enemy(img_asteroid, randint(30, win_width - 30), -40, 80, 50, randint(1, 7))
            asteroids.add(asteroid)

    time.delay(50)