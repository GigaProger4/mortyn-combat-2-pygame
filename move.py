import pygame
from pygame import mixer
from player import Player
mixer.init()

IDLE = ['Idle0.png','Idle1.png','Idle2.png','Idle3.png','Idle4.png','Idle5.png','Idle6.png','Idle7.png','Idle8.png','Idle9.png']
RUN = ['Run0.png', 'Run1.png', 'Run2.png', 'Run3.png', 'Run4.png', 'Run5.png', 'Run6.png', 'Run7.png']
JUMP = ['Jump0.png', 'Jump1.png', 'Jump2.png']
FALL = ['Fall_0.png', 'Fall_1.png', 'Fall_2.png']
ATTACK = ['Attack0.png', 'Attack1.png', 'Attack2.png', 'Attack3.png', 'Attack4.png', 'Attack5.png', 'Attack6.png']
STUN = ['Stun0.png', 'Stun1.png', 'Stun2.png']
DEATH = ['Death0.png', 'Death1.png', 'Death2.png', 'Death3.png', 'Death4.png', 'Death5.png', 'Death6.png']

ATTACK_SOUND = pygame.mixer.Sound("assets/audio/sword.wav")
ATTACK_SOUND.set_volume(0.1)

def annimation(Go, Jump, OnGround, Attack, Stun, Death, Frame_Idle, Frame_Run, Frame_Jump, Frame_Attack, Frame_Stun, Frame_Death):
    if(Death == False):
        if(Stun == False):

            if(Go == False and Jump == False and OnGround == True and Attack == False):
                image = ('assets/images/fighter_1/idle/'+IDLE[int(Frame_Idle)])
                return(image)

            elif(Go == True and Jump == False and OnGround == True and Attack == False):
                image = ('assets/images/fighter_1/run/'+RUN[int(Frame_Run)])
                return(image)

            if(Jump == True and OnGround == False and Attack == False):
                image = ('assets/images/fighter_1/jump/' + JUMP[int(Frame_Jump)])
                # ATTACK_SOUND.play()
                return (image)

            elif (Jump == False and OnGround == False and Attack == False):
                image = ('assets/images/fighter_1/falls/' + FALL[int(Frame_Jump)])
                return (image)

            if(Attack == True):
                image = ('assets/images/fighter_1/attack_1/' + ATTACK[int(Frame_Attack)])
                return(image)

        else:
            image = ('assets/images/fighter_1/stun/' + STUN[int(Frame_Stun)])
            return (image)
    else:
        image = ('assets/images/fighter_1/death/' + DEATH[int(Frame_Death)])
        return (image)







