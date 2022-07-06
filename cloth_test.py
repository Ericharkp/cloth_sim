import pygame, sys

# import cloth2 as cloth
import cloth


mainClock = pygame.time.Clock()

from pygame.locals import *

pygame.init()
pygame.display.set_caption('cloth?')
screen = pygame.display.set_mode((1000,1000),0,32)

points_data = cloth.load_model('test_mesh_2.mesh')

test_cloth = cloth.ClothObj(points_data)


font = pygame.font.SysFont("Arial" , 18 , bold = True)

def fps_counter(clock, window):
    fps = str(int(clock.get_fps()))
    fps_t = font.render(fps , 1, pygame.Color("RED"))
    window.blit(fps_t,(0,0))

render_mode = 0
mouse_pressed = 0


while True:

    # Background --------------------------------------------- #
    screen.fill((0,0,0))

    mouse = pygame.mouse.get_pos()

    test_cloth.update_pos()

    if mouse_pressed:
        test_cloth.cut(mouse)


    if render_mode:
        test_cloth.render_point(screen, radius = 1)
    else:
        test_cloth.render_line(screen)


    fps_counter(mainClock, screen)

    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()
        if event.type == KEYDOWN:
            if event.key == K_ESCAPE:
                pygame.quit()
                sys.exit()
            if event.key == K_l:
                render_mode = not render_mode
            if event.key == K_r:
                test_cloth.set_pos((10,10))
         

        if event.type == MOUSEBUTTONDOWN:
            if event.button == 1:
                mouse_pressed = 1

        if event.type == MOUSEBUTTONUP:
            if event.button == 1:
                mouse_pressed = 0


    pygame.display.update()
    mainClock.tick(60)


