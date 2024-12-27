import pygame
from intersection import Intersection
from intersection import Point

class Player():
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.dy = 0
        self.rect = (x,y)
        self.Vel = 10 # скорость передвижения

        # прыжок
        self.OnGround = False

        # смерть
        self.spawn_x = x
        self.spawn_y = y
        self.Death = False
        self.Resp_Timer = 0
        self.Death_Count = 0

        # атака
        self.attacking = False
        self.attack_cooldown = 0
        self.HP = 100

        # Get_Attack
        self.Get_Attack = False
        self.Stun = False
        self.Stun_Time = 0

        # индикаторы для аннимации
        self.Go = False
        self.Jump = False
        self.Attack = False

        self.Frame_Run = 0
        self.Frame_Idle = 0
        self.Frame_Jump = 0
        self.Frame_Attack = 0
        self.Frame_Stun = 0
        self.Frame_Death = 0


    def reset_death_count(self):
        self.Death_Count = -1
        self.respawn()
        self.update()

    def respawn(self):
        self.x = self.spawn_x
        self.y = self.spawn_y
        self.dy = 0
        self.OnGround = False
        self.Death = False
        self.Death_Count += 1
        self.HP = 100

    def Death_Ivent(self):
        if not self.Death:
            self.Death = True
            self.Resp_Timer = 200   # время респавна

        self.update()


    def Attack_Ivent(self,player1,player2, player_width, player_height):

        x1 = (player_width - player_width*0.2)
        y1 = (player_height/1.5 - player_height/1.5 * 0.2 )


        Body_1_1 = Point(player1[0] - x1, player1[1] - y1)
        Body_1_2 = Point(player1[0] + x1, player1[1] + y1)
        Body_2_1 = Point(player2[0] - x1, player2[1] - y1)
        Body_2_2 = Point(player2[0] + x1, player2[1] + y1)

        intersection = Intersection(Body_1_1, Body_1_2, Body_2_1, Body_2_2)

        if self.Get_Attack == False and intersection == True:
            self.Get_Attack = True
            self.Stun = True
            self.Stun_Time = 30         # время стана


    def Get_Loc(self):
        return (self.x, self.y)

    def move(self):
        keys = pygame.key.get_pressed()

        if self.Death == False and self.Stun == False:

            if keys[pygame.K_a]:
                self.x -= self.Vel
                if self.x <= -30:
                    self.x = 1010
                self.Go = True

            if keys[pygame.K_d]:
                self.x += self.Vel
                if self.x >= 1030:
                    self.x = -10
                self.Go = True

            if not (keys[pygame.K_a] or keys[pygame.K_d]):
                self.Go = False

            if keys[pygame.K_w] and self.OnGround:
                self.dy = -30
                self.OnGround = False
                self.Jump = True

            if keys[pygame.K_SPACE] and self.attack_cooldown == 0 and self.attacking == False:
                self.attacking = True
                self.Attack = True
                self.attack_cooldown = 60  # Добавляем задержку между атаками

            # if keys[pygame.K_p]:
            #     self.Pause = not self.Pause


        self.update()

    def update(self):
        self.rect = (self.x, self.y)

        # прыжок
        if not self.OnGround:
            self.y += self.dy
            self.dy += 1.5

            if self.dy >= 0:
                self.Jump = False       # фрейм прыжка

            if self.y >= 435:
                self.y = 435
                self.dy = 0
                self.OnGround = True

        # respawn
        if self.Death == True:
            self.Resp_Timer -= 1
            if self.Resp_Timer <= 0:  # 3 секунды при 60 FPS
                self.respawn()

        # атака
        if self.attack_cooldown > 0:
            self.attack_cooldown -= 1

        if self.attack_cooldown == 20: # промежуток времени для получения атаки
            self.attacking = False

        #получение урона
        if self.Get_Attack == True:
            self.Stun_Time -= 1

            if self.Stun_Time <= 0:
                self.Stun = False
                self.Get_Attack = False
                self.HP -= 20           # значение урона

                if self.HP <= 0:
                    self.Death_Ivent()


        ##### фреймы ######


        # фрейм бега и idle
        if self.Go:
            self.Frame_Run += 0.2
            if self.Frame_Run > 7:
                self.Frame_Run -= 7
        else:
            self.Frame_Idle += 0.2
            if self.Frame_Idle > 9:
                self.Frame_Idle -= 9

        # фрейм прыжка
        if self.OnGround == False:
            self.Frame_Jump += 0.2
            if self.Frame_Jump > 3:
                self.Frame_Jump -= 3

        # фрейм атаки
        if self.Attack:
            self.Frame_Attack += 0.2
            if self.Frame_Attack > 6:
                self.Frame_Attack -= 6
                self.Attack = False

        # фрейм стана
        if self.Stun:
            self.Frame_Stun += 0.2
            if self.Frame_Stun > 2:
                self.Frame_Stun -= 2

        # фрейм смерти
        if self.Death:
            self.Frame_Death += 0.1
            if self.Frame_Death > 6:
                self.Frame_Death = 6
        else:
            self.Frame_Death = 0

