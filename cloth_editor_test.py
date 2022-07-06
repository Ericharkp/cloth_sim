import pygame
import sys
from pygame.locals import *
import cloth_editor

pygame.init()
pygame.display.set_caption("cloth_editor")
screen = pygame.display.set_mode((500, 600), 0, 32)


screen.fill((0, 0, 0))
p1 = [-1,-1]


cloth_editor = cloth_editor.ClothEditor(screen, grid_size= 10)
while True:

    # Background --------------------------------------------- #
    
    mouse = pygame.mouse.get_pos()

    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()
        if event.type == KEYDOWN:
            if event.key == K_s:
                cloth_editor.save_as_json("test.rag", 10)
            if event.key == K_ESCAPE:           
                pygame.quit()
                sys.exit()

        if event.type == MOUSEBUTTONDOWN:
            if event.button == 1:
                cloth_editor.add_grounded_point(mouse)
                cloth_editor.add_point(mouse)
            if event.button == 2:
                cloth_editor.earse_point(mouse)
            if event.button == 3:
                p1[0] = mouse[0]
                p1[1] = mouse[1]


        if event.type == MOUSEBUTTONUP:
            if event.button == 3:
                cloth_editor.add_line(p1, mouse)            
                p1 = [-1,-1]

    pygame.display.update()
