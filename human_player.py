import pygame
import os
import random

from bird import Bird
from pipe import Pipe
from base import Base

pygame.init()
pygame.font.init()

WIN_WIDTH = 500
WIN_HEIGHT = 800
BG_IMG = pygame.transform.scale2x(pygame.image.load(os.path.join("imgs", "bg.png")))
STAT_FONT = pygame.font.SysFont("comicsans", 50)

def draw_win(win, bird, pipes, base, score):
    win.blit(BG_IMG, (0,0))
    
    for pipe in pipes:
        pipe.draw(win)
    
    base.draw(win)
    
    text = STAT_FONT.render("Score " + str(score), 1, (255, 255, 255))
    win.blit(text, (WIN_WIDTH - 10 - text.get_width(), 10))
    
    bird.draw(win)
    pygame.display.update()

def mainHuman():
    gap = random.randrange(500, 700, 100)
    bird = Bird(230, 350)
    pipes = [Pipe(gap)]
    base = Base(730)
    
    win = pygame.display.set_mode((WIN_WIDTH, WIN_HEIGHT))
    clock = pygame.time.Clock()
    score = 0
    run = True
    
    pygame.key.set_repeat(300, 100)

    while run:
        clock.tick(30)
        for event in pygame.event.get():
            if event == pygame.QUIT:
                pygame.quit()
                quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    bird.jump()
            
        bird.move()
        
        removePipe = []
        add_pipe = False
        for pipe in pipes:
            if pipe.collide(bird):
                pygame.quit()
                quit()
                
            if not pipe.passed and pipe.x < bird.x:
                pipe.passed = True
                add_pipe = True
            
            if pipe.x + pipe.PIPE_TOP.get_width() < 0:
                removePipe.append(pipe)
            
            pipe.move()
        
        if add_pipe:
            score += 1
            gap = random.randrange(500, 800, 100)
            pipes.append(Pipe(gap))
        
        for pipe in removePipe:
            pipes.remove(pipe)
        
        if bird.y < 0 or bird.y + bird.img.get_height() >= WIN_HEIGHT:
            pygame.quit()
            quit()
        
        base.move()
        draw_win(win, bird, pipes, base, score)