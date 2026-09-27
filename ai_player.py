import pygame
import os
import random
import neat

from bird import Bird
from pipe import Pipe
from base import Base

WIN_WIDTH = 500
WIN_HEIGHT = 800
GEN = 0
BG_IMG = pygame.transform.scale2x(pygame.image.load(os.path.join("imgs", "bg.png")))
STAT_FONT = pygame.font.SysFont("comicsans", 50)

pygame.font.init()

def draw_window(win, birds, pipes, base, score, gen):
    win.blit(BG_IMG, (0,0))
    
    for pipe in pipes:
        pipe.draw(win)
        
    base.draw(win)
    
    text = STAT_FONT.render("Score: " + str(score), 1, (255,255,255))
    win.blit(text, (WIN_WIDTH - 10 - text.get_width(), 10))
    
    gen_text = STAT_FONT.render("Gen: " + str(gen), 1, (255,255,255))
    win.blit(gen_text, (10, 10))
    
    for bird in birds: 
        bird.draw(win)
    pygame.display.update()

def run(config_path):
    config = neat.config.Config(neat.DefaultGenome, neat.DefaultReproduction, 
                                neat.DefaultSpeciesSet, neat.DefaultStagnation, 
                                config_path)
    
    p = neat.Population(config)
    p.add_reporter(neat.StdOutReporter(True))
    stats = neat.StatisticsReporter()
    p.add_reporter(stats)
    
    p.run(mainAI, 50)

def mainAI(genomes, config):
    global GEN
    
    nets = []
    ge = []
    birds = []
    
    for _, g in genomes:
        net = neat.nn.FeedForwardNetwork.create(g, config)
        nets.append(net)
        g.fitness = 0
        ge.append(g)
        birds.append(Bird(230, 350))
        
    gap = random.randrange(500, 800, 100)
    pipes = [Pipe(gap)]
    base = Base(730)
    
    win = pygame.display.set_mode((WIN_WIDTH, WIN_HEIGHT))
    clock = pygame.time.Clock()
    score = 0
    run = True
    
    while run:
        clock.tick(60)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
        
        #Change the pipe to the second one on screen if the bird has passed it
        pipe_ind = 0
        if len(birds) > 0:
            if len(pipes) > 1 and birds[0].x > pipes[0].x + pipes[0].PIPE_TOP.get_width():
                pipe_ind = 1
        else: 
            GEN += 1
            run = False
            break
        
        for bird in list(birds):
            index = birds.index(bird)
            bird.move()
            ge[index].fitness += 0.1
            
            output = nets[index].activate((bird.y, abs(bird.y - pipes[pipe_ind].height), abs(bird.y - pipes[pipe_ind].bottom)))

            if output[0] > 0.5:
                bird.jump()
        
        rem = []
        add_pipe = False
        for pipe in pipes:
            for bird in list(birds):
                if pipe.collide(bird):
                    index = birds.index(bird)
                    ge[index].fitness -= 1
                    nets.pop(index)
                    ge.pop(index)
                    birds.remove(bird)
            
                #creates booleans to check whether the pipe has been passed and if program should add pipe
                if not pipe.passed and pipe.x < bird.x:
                    pipe.passed = True
                    add_pipe = True
            
            # adds pipe to a list to remove if it goes offscreen
            if pipe.x + pipe.PIPE_TOP.get_width() < 0:
                rem.append(pipe)
            
            pipe.move()
        
        if add_pipe:
            score += 1
            for g in ge:
                g.fitness += 5
            gap = random.randrange(500, 800, 100)
            pipes.append(Pipe(gap))
        
        for r in rem:
            pipes.remove(r)
        
        for bird in list(birds):
            #if the bird hits the bottom or top
            if bird.y + bird.img.get_height() >= WIN_HEIGHT or bird.y < 0:
                index = birds.index(bird)
                nets.pop(index)
                ge.pop(index)
                birds.pop(index)
        
        base.move()
        draw_window(win, birds, pipes, base, score, GEN)