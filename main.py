import sys
import os
import pygame as pg
from pygame.locals import *
from hud import *
from character import *
from princess import *
from collectables import *
from platforms import *
from holes import *
from clouds import *

main_dir = os.path.split(os.path.abspath(__file__))[0]
data_dir = os.path.join(main_dir, 'media')

def load_image(name, colorkey=None, scale=0.3):
    fullpath = os.path.join(data_dir, 'img')
    fullname = os.path.join(fullpath, name)
    image = pg.image.load(fullname)

    size = image.get_size()
    size = (size[0] * scale, size[1] * scale)
    image = pg.transform.scale(image, size)

    image = image.convert_alpha()
    if colorkey is not None:
        if colorkey == -1:
            colorkey = image.get_at((0, 0))
        image.set_colorkey(colorkey, pg.RLEACCEL)

    return image

def load_strawberries():
    strawberry1 = Collectable(250, 370, 'strawberry')
    strawberry2 = Collectable(300, 370, 'strawberry')
    strawberry3 = Collectable(350, 370, 'strawberry')
    strawberry4 = Collectable(400, 370, 'strawberry')
    strawberry5 = Collectable(250, 320, 'strawberry')
    strawberry6 = Collectable(300, 320, 'strawberry')
    strawberry7 = Collectable(350, 320, 'strawberry')
    strawberry8 = Collectable(400, 320, 'strawberry')

    strawberry9 = Collectable(650, 450, 'strawberry')
    strawberry10 = Collectable(700, 450, 'strawberry')
    strawberry11 = Collectable(750, 450, 'strawberry')
    strawberry12 = Collectable(800, 450, 'strawberry')
    strawberry13 = Collectable(650, 400, 'strawberry')
    strawberry14 = Collectable(700, 400, 'strawberry')
    strawberry15 = Collectable(750, 400, 'strawberry')
    strawberry16 = Collectable(800, 400, 'strawberry')

    strawberry17 = Collectable(200, 630, 'strawberry')
    strawberry18 = Collectable(250, 630, 'strawberry')
    strawberry19 = Collectable(300, 630, 'strawberry')
    strawberry20 = Collectable(350, 630, 'strawberry')
    strawberry21 = Collectable(200, 580, 'strawberry')
    strawberry22 = Collectable(250, 580, 'strawberry')
    strawberry23 = Collectable(300, 580, 'strawberry')
    strawberry24 = Collectable(350, 580, 'strawberry')
    strawberry25 = Collectable(200, 530, 'strawberry')
    strawberry26 = Collectable(250, 530, 'strawberry')
    strawberry27 = Collectable(300, 530, 'strawberry')
    strawberry28 = Collectable(350, 530, 'strawberry')

    strawberry29 = Collectable(550, 180, 'strawberry')
    strawberry30 = Collectable(600, 180, 'strawberry')
    strawberry31 = Collectable(550, 130, 'strawberry')
    strawberry32 = Collectable(600, 130, 'strawberry')

    return strawberry1, strawberry2, strawberry3, strawberry4, strawberry5, strawberry6, strawberry7, strawberry8,\
        strawberry9, strawberry10, strawberry11, strawberry12, strawberry13, strawberry14, strawberry15, strawberry16,\
        strawberry17, strawberry18, strawberry19, strawberry20, strawberry21, strawberry22, strawberry23, strawberry24,\
        strawberry25, strawberry26, strawberry27, strawberry28, strawberry29, strawberry30, strawberry31, strawberry32

def load_keys_and_cage():
    yellow_key_1 = Collectable(900, 600, 'yellow_key')
    yellow_key_2 = Collectable(310, 210, 'yellow_key')

    blue_key_1 = Collectable(450, 150, 'blue_key')
    blue_key_2 = Collectable(190, 350, 'blue_key')

    cage = Collectable(1000, 604, 'cage')

    return yellow_key_1, yellow_key_2, blue_key_1, blue_key_2, cage

def load_platforms():
    #obs: o 10 é a largura da cauda do sprite, o que faz o personagem voar se nao for retirada da colisao
    ground_platform_1 = Platform(0, 687, 590 - 10, 90)
    ground_platform_2 = Platform(780 + 10, 687, 590, 90)

    platform_1 = Platform(600, 500, sprite=1)
    platform_2 = Platform(150, 420, sprite=2)
    platform_3 = Platform(400, 230, sprite=3)

    return ground_platform_1, ground_platform_2, platform_1, platform_2, platform_3

def load_holes():
    hole1 = Hole(590, 630, 190, 140)

    return hole1

def load_clouds():
    cloud_1 = Cloud(-700, 60, 'sprite_platform_1.png')
    cloud_2 = Cloud(1300, 530, 'sprite_platform_2.png')
    cloud_3 = Cloud(180, 370, 'sprite_platform_3.png')

    return cloud_1, cloud_2, cloud_3
def menu():
    pg.init()
    screen = pg.display.set_mode((1080, 760), pg.SCALED)
    pg.display.set_caption('Llama Adventures')
    pg.display.set_icon(load_image('icon.png', scale=1))
    background = load_image('menu.png', scale=1)

    title_button = load_image('llama_adventures.png', scale=1.09)
    title_button_rect = title_button.get_rect(center=(screen.get_width() // 2, 250))
    play_button = load_image('menu_play.png', scale=1)
    play_button_rect = play_button.get_rect(center=(screen.get_width() // 2, 500))

    cloud_group = pg.sprite.Group()
    cloud_group.add(load_clouds())
    clock = pg.time.Clock()
    fullscreen_timer = 0

    going = True
    while going:
        clock.tick(60)

        for event in pg.event.get():
            if event.type == pg.QUIT or pg.key.get_pressed()[pg.K_ESCAPE]:
                sys.exit()
            elif event.type == pg.MOUSEMOTION:
                if play_button_rect.collidepoint(event.pos):
                    play_button = load_image('mouse_on_menu_play.png', scale=1)
                else:
                    play_button = load_image('menu_play.png', scale=1)
            elif event.type == pg.MOUSEBUTTONDOWN:
                if play_button_rect.collidepoint(event.pos):
                    main(screen)

        if pg.key.get_pressed()[pg.K_f]:
            if pg.time.get_ticks() - fullscreen_timer > 300:
                pg.display.toggle_fullscreen()
                fullscreen_timer = pg.time.get_ticks()

        #background
        screen.blit(background, (0, 0))

        #desenho das nuvens
        cloud_group.update()
        cloud_group.draw(screen)

        #desenho do botao:
        screen.blit(title_button, title_button_rect.topleft)
        screen.blit(play_button, play_button_rect.topleft)

        pg.display.flip()

    pg.quit()

def main(screen):

    # carragamento da iamgem de fundo, coeltáveis e plataformas
    background = load_image('background.png', scale=1)
    background = pg.transform.scale(background, (screen.get_size()[0], screen.get_size()[1]))

    # grupos de sprites
    collectables_group = pg.sprite.Group()
    platforms_group = pg.sprite.Group()
    sprites_behind_player = pg.sprite.Group()

    collectables_group.add(load_keys_and_cage(), load_strawberries())
    platforms_group.add(load_platforms())
    sprites_behind_player.add(load_holes())

    # Inicialização de variáveis
    princess = None
    wait_jump_count = 0
    fullscreen_timer = 0
    llama = Character()
    hud = HUD(llama)
    clock = pg.time.Clock()

    going = True
    while going:
        clock.tick(60)

        #saida do jogo
        for event in pg.event.get():
            if event.type == pg.QUIT or pg.key.get_pressed()[pg.K_ESCAPE]:
                sys.exit()

        #update elementos da tela
        collectables_group.update(llama)
        pg.sprite.Group(hud).update()
        llama.update(screen.get_size()[0], platforms_group)

        #desenho de lementos da tela
        screen.blit(background, (0, 0))
        sprites_behind_player.draw(screen)
        collectables_group.draw(screen)
        pg.sprite.Group(hud).draw(screen)
        pg.sprite.RenderPlain(llama).draw(screen)
        platforms_group.draw(screen)

        # inicialização da princesa e fim da fase
        if llama.cage_collected:
            if princess is not None:
                if wait_jump_count < 90:
                    wait_jump_count += 1
                else:
                    llama.can_jump = True
                    princess.update(platforms_group)
            else:
                princess = Princess(965, 600)
                sprites_behind_player.add(princess)
                llama.looking_right = True

        # tela cheia com um contador
        if pg.key.get_pressed()[pg.K_f]:
            if pg.time.get_ticks() - fullscreen_timer > 300:
                pg.display.toggle_fullscreen()
                fullscreen_timer = pg.time.get_ticks()

        '''for platform in platforms_group:
            pg.draw.rect(screen, (255, 0, 0), platform.rect)'''

        pg.display.flip()

    pg.quit()

if __name__ == "__main__":
    menu()