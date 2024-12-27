import pygame
from pygame import mixer
from network import Network
from move import annimation
from player import Player
import os

pygame.init()

width = 1000
height = 600
win = pygame.display.set_mode((width, height))
bg_image = pygame.image.load("assets/images/background/background.jpg").convert_alpha()
scaled_bg = pygame.transform.scale(bg_image, (width, height))

pygame.mixer.music.load('assets/audio/mortyn.MP3')
pygame.mixer.music.play()
pygame.mixer.music.set_volume(0.05)

count_font = pygame.font.Font("assets/fonts/turok.ttf", 50)
score_font = pygame.font.Font("assets/fonts/turok.ttf", 25)
win_font = pygame.font.Font("assets/fonts/turok.ttf", 100)
timer_font = pygame.font.Font("assets/fonts/turok.ttf", 35)

pygame.display.set_caption("Client")

scale = 2.5
player_width = 39 * scale
player_height = 45 * scale


def display_high_scores(screen, font):
    if not os.path.exists("assets/high_scores.txt"):
        return

    scores = []
    with open("assets/high_scores.txt", "r") as file:
        scores = [int(line.strip()) for line in file]

    scores = sorted(scores, reverse=True)[:5]  # Берем только топ-5 результатов

    title = font.render("High Scores", True, (255, 255, 255))
    screen.blit(title, (screen.get_width() // 2 - title.get_width() // 2, 110))

    y_offset = 180
    for i, score in enumerate(scores, 1):
        score_text = font.render(f"{i}. {score}", True, (255, 255, 255))
        screen.blit(score_text, (screen.get_width() // 2 - score_text.get_width() // 2, y_offset))
        y_offset += 50


def Draw_Bar(player1, player2):
    # полоска ХП
    pl1_HP = player1.HP
    pl2_HP = player2.HP
    scale_HP = 3                # длина хп
    HP_Draw = 100 * scale_HP

    pygame.draw.rect(win,"red",(100, 50, HP_Draw, 20))
    pygame.draw.rect(win,"green",(100, 50, pl1_HP * scale_HP, 20))

    pygame.draw.rect(win, "red", (600, 50, HP_Draw, 20))
    pygame.draw.rect(win,"green",(900 - pl2_HP * scale_HP, 50, pl2_HP * scale_HP, 20))

    # иконка игрока и счет
    Score2 = player1.Death_Count

    P1 = count_font.render('YOU: ', True, "red")
    win.blit(P1, (15, 25))

    score1 = score_font.render('Score: ' + str(player2.Death_Count), True, "red")
    win.blit(score1, (50, 100))

    score2 = score_font.render('Score: ' + str(player1.Death_Count), True, "red")
    win.blit(score2, (800, 100))

    P1 = count_font.render(':P2 ', True, "red")
    win.blit(P1, (910, 25))

    pygame.display.update()

def Convert_Image(file,flip):
    image = pygame.image.load(file)
    image = pygame.transform.scale(image, (image.get_width() * scale, image.get_height() * scale))

    if(flip == True):
        image = pygame.transform.flip(image,180,0)

    image = image.convert_alpha()
    return (image)

def redrawWindow(win,player1, player2, Game_Over, Round_Timer, pause):
    win.blit(scaled_bg, (0, 0))

    # экран паузы
    if pause == True:
        pygame.draw.rect(win, (125, 125, 125), (400, 100, 200, 400))
        pause_text = timer_font.render("PAUSE", True, "red")
        win.blit(pause_text, (450, 10))
        display_high_scores(win, timer_font)

    # игровой таймер
    time = timer_font.render(str(Round_Timer // 120), True, "red")
    win.blit(time,(480,40))

    player1_loc = player1.Get_Loc()
    player2_loc = player2.Get_Loc()

    if(player1_loc[0] >= player2_loc[0]):
        p1_flip = True
        p2_flip = False
    else:
        p1_flip = False
        p2_flip = True

    file1 = annimation(player1.Go, player1.Jump, player1.OnGround, player1.Attack, player1.Stun, player1.Death, player1.Frame_Idle,
                       player1.Frame_Run, player1.Frame_Jump, player1.Frame_Attack, player1.Frame_Stun, player1.Frame_Death)
    file2 = annimation(player2.Go, player2.Jump, player2.OnGround, player2.Attack, player2.Stun, player2.Death, player2.Frame_Idle,
                       player2.Frame_Run, player2.Frame_Jump, player2.Frame_Attack, player2.Frame_Stun, player2.Frame_Death)

    player_1 = Convert_Image(file1,p1_flip)
    player_2 = Convert_Image(file2,p2_flip)

    player_1_rect = player_1.get_rect(center=(player1.Get_Loc()))
    player_2_rect = player_2.get_rect(center=(player2.Get_Loc()))
    win.blit(player_1, player_1_rect)
    win.blit(player_2, player_2_rect)

    Draw_Bar(player1,player2)

    # экран победы
    if Game_Over:
        if player1.Death_Count > player2.Death_Count:
            winner_text = win_font.render('P2 WINS!', True, "red")
        elif player1.Death_Count < player2.Death_Count:
            winner_text = win_font.render('YOU WIN!', True, "red")
        else:
            winner_text = win_font.render('TIME UP!', True, "red")
        win.blit(winner_text, (300, 200))

    pygame.display.update()


def main():
    run = True
    n = Network()
    p, Time_of_Round, Reset_Timer, pause = n.getP()
    clock = pygame.time.Clock()

    while run:
        clock.tick(60)
        p2, Round_Timer, Game_Over, Reset_Timer, pause = n.send((p, pygame.key.get_pressed()[pygame.K_p]))


        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                pygame.quit()


        if not pause:
            if not Game_Over:
                p.move()

                if p.attacking:
                    p2.Attack_Ivent(p.Get_Loc(),p2.Get_Loc(), player_width, player_height)
                if p2.attacking:
                    p.Attack_Ivent(p.Get_Loc(),p2.Get_Loc(), player_width, player_height)
            else:
                if Reset_Timer == 0 or Reset_Timer == 1 or Reset_Timer == 2:
                    p.reset_death_count()
                    p2.reset_death_count()

        redrawWindow(win, p, p2, Game_Over, Round_Timer, pause)

main()