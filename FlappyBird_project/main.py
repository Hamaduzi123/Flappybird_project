import pygame
from sys import exit
import random
import time
pygame.init()

width,height = 700,600
WIN=pygame.display.set_mode((width,height))
pygame.display.set_caption('Flappy bird')

pipe_gap=150

bg_img=pygame.image.load('images/bg_img.png')
ground_img=pygame.image.load('images/ground_img.png')
ground_rect=ground_img.get_rect(topleft=(0,500))

bird_img=pygame.image.load('images/bird_img.png')
bird_rect=pygame.Rect(100,100,bird_img.get_width(),bird_img.get_height())

pipe_img=pygame.image.load('images/pipe_img.png')
pipe_bottom=pipe_img.get_rect(topleft=(300,height/2+(pipe_gap/2)))

pipe_img_top=pygame.transform.flip(pipe_img,False,True)
pipe_top=pipe_img_top.get_rect(bottomleft=(300,height/2-(pipe_gap/2)))

button_restart=pygame.image.load('images/button_restart.png')
button_restart_rect=button_restart.get_rect(topleft=(170,400))

button_quit=pygame.image.load('images/button_quit.png')
button_quit_rect=button_quit.get_rect(topleft=(400,400))

pipe_make = pygame.USEREVENT + 1
pygame.time.set_timer(pipe_make,2000)

jump=pygame.mixer.Sound('soundtracks/jump.mp3')
score_sound=pygame.mixer.Sound('soundtracks/score.mp3')
death=pygame.mixer.Sound('soundtracks/death.mp3')

game_over=False
falling=False


score=0
font=pygame.font.Font('assets\Pixeltype.ttf',100)




def draw(scroll,gravity,ground_scroll,pipes_b,pipes_t):
    global online,game_over,falling,score
    for i in range(0,2):
        WIN.blit(bg_img,(bg_img.get_width()*i+scroll,0))

    for pipe in pipes_b:
        if online:
            pipe.x-=3
            if bird_rect.colliderect(pipe):
                online=False
                game_over=True  
                falling=True
                gravity=1
                flash()
                death.play()
        WIN.blit(pipe_img,(pipe.x,pipe.y)) 
        
        if pipe.x in [bird_rect.x,bird_rect.x+1,bird_rect.x+2] and online:
            score+=1
            score_sound.play()
        


    for pipe in pipes_t:
        if online:
            pipe.x-=3
            if bird_rect.colliderect(pipe):
                online=False
                game_over=True
                falling=True
                gravity=1
                flash()
                death.play()
        WIN.blit(pipe_img_top,(pipe.x,pipe.y))

    for i in range(0,3):
        WIN.blit(ground_img,(ground_img.get_width()*i+ground_scroll,500))
    if gravity<=0 and not falling:
        bird_img_up=pygame.transform.rotate(bird_img,gravity*-2)
        WIN.blit(bird_img_up,(bird_rect.x,bird_rect.y))
    elif falling:
        bird_img_down=pygame.transform.rotate(bird_img,270)
        WIN.blit(bird_img_down,(bird_rect.x,bird_rect.y))
    else:
        WIN.blit(bird_img,(bird_rect.x,bird_rect.y))


def flash():
    WIN.fill('white')
    pygame.display.update()
    time.sleep(0.1)
def gameover():
    bird_rect.y+=2

def restart_screen():
    WIN.blit(button_restart,(button_restart_rect.x,button_restart_rect.y))
    WIN.blit(button_quit,(button_quit_rect.x,button_quit_rect.y))



def display_score(score):
    score_text=font.render(f'{score}',0,'white')
    WIN.blit(score_text,(width/2-score_text.get_width()/2,70))

def remove(pipes_t,pipes_b):
    for pipe in pipes_t:
        if pipe.x<=-200:
                pipes_t.remove(pipe)
    for pipe in pipes_b:
        if pipe.x<=-200:
                pipes_b.remove(pipe)

def main():
    global online,game_over,falling,score
    online=False
    clock=pygame.time.Clock()
    scroll=0
    ground_scroll=0
    gravity=0
    pipes_t=[]
    pipes_b=[]
    while True:
        
        for event in pygame.event.get():
            if event.type==pygame.QUIT:
                pygame.quit()
                exit()
            if not game_over:
                if event.type==pygame.MOUSEBUTTONDOWN and online and bird_rect.y>=-200:
                    gravity=-10
                    jump.play()
                if event.type==pygame.MOUSEBUTTONDOWN and not online and not game_over:
                    online=True
                if event.type==pipe_make and online:
                    a=random.randint(700,800)
                    b=random.randint(100,400)
                    pipe_top1=pipe_img_top.get_rect(bottomleft=(a,b-(pipe_gap/2)))
                    pipe_bottom1=pipe_img.get_rect(topleft=(a,b+(pipe_gap/2)))
                    pipes_t.append(pipe_top1)
                    pipes_b.append(pipe_bottom1)
            else:

                if event.type==pygame.MOUSEBUTTONDOWN:
                    if button_restart_rect.collidepoint(pygame.mouse.get_pos()):
                        online=False
                        flash()
                        scroll=0
                        ground_scroll=0
                        gravity=0
                        pipes_t=[]
                        pipes_b=[]
                        bird_rect.x=100
                        bird_rect.y=100
                        game_over=False
                        falling=False
                        score=0
                    if button_quit_rect.collidepoint(pygame.mouse.get_pos()):
                        pygame.quit()
                        exit()



        if online:
            remove(pipes_t,pipes_b)
            gravity+=0.6
            clock.tick(60)
            scroll-=2
            ground_scroll-=3
            if abs(scroll)>bg_img.get_width():
                scroll=0
            if abs(ground_scroll)>ground_rect.width:
                ground_scroll=0
            bird_rect.y+=gravity
            if bird_rect.colliderect(ground_rect):
                online=False
                game_over=True
                falling=True
                gravity=1
                flash()
                death.play()
        if bird_rect.y>=471:
            bird_rect.y=471
        

        draw(scroll,gravity,ground_scroll,pipes_b,pipes_t)
        display_score(score)
        if game_over==True:
            gameover()
            restart_screen()
        pygame.display.update()
        

if __name__=='__main__':
    main()
