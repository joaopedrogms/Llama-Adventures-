import os
import pygame as pg
from pygame.locals import *

if not pg.font:
    print("Warning, fonts disabled")
if not pg.mixer:
    print("Warning, sound disabled")

main_dir = os.path.split(os.path.abspath(__file__))[0]
data_dir = os.path.join(main_dir, "media")

gravity = 0.3

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


class HUD(pg.sprite.Sprite):
    def __init__(self, character):
        pg.sprite.Sprite.__init__(self)
        self.character = character
        self.heart_image = load_image('coracao.png', scale=0.06)
        self.chave_dourada_image = load_image('chave_dourada.png', scale=0.065)
        self.chave_azul_image = load_image('chave_azul.png', scale=0.065)
        self.morango_image = load_image('morango.png', scale=0.16)
        self.rect = self.heart_image.get_rect()
        self.rect.topleft = (10, 10)
        self.key_font = pg.font.Font(None, 30)

    def update(self):
        self.image = pg.Surface((1900, 1900), pg.SRCALPHA)
        self.image.fill((0, 0, 0, 0))

        # corações
        heart_x = 10
        for _ in range(self.character.hp):
            self.image.blit(self.heart_image, (heart_x, 10))
            heart_x += 40

        # morangos
        morango_rect = self.morango_image.get_rect()
        morango_rect.topleft = (self.image.get_width() - 920, 10)
        self.image.blit(self.morango_image, morango_rect)
        morango_count = self.key_font.render(str(self.character.morangos_coletados), True, (255, 0, 0))
        self.image.blit(morango_count, (morango_rect.right + 10, morango_rect.centery))

        # chaves amarelas
        chave_dourada_rect = self.chave_dourada_image.get_rect()
        chave_dourada_rect.topleft = (self.image.get_width() - 930, 50)
        self.image.blit(self.chave_dourada_image, chave_dourada_rect)
        chave_dourada_count = self.key_font.render(str(self.character.chaves_coletadas), True, (255, 255, 50))
        self.image.blit(chave_dourada_count, (
        chave_dourada_rect.right + 10, chave_dourada_rect.centery - chave_dourada_count.get_height() // 2))

        # chaves azuis
        chave_azul_rect = self.chave_azul_image.get_rect()
        chave_azul_rect.topleft = (self.image.get_width() - 930, 90)
        self.image.blit(self.chave_azul_image, chave_azul_rect)
        chave_azul_count = self.key_font.render(str(self.character.chaves_azuis_coletadas), True, (60, 135, 210))
        self.image.blit(chave_azul_count,
                        (chave_azul_rect.right + 10, chave_azul_rect.centery - chave_azul_count.get_height() // 2))


class Character(pg.sprite.Sprite):

    def __init__(self):
        pg.sprite.Sprite.__init__(self)
        self.image = load_image('sprite_llama.png')
        self.rect = load_image('sprite_llama.png').get_rect()
        self.image_upper = self.rect.copy()
        self.looking = True
        self.jump = False
        self.hp = 3
        self.attack = 1
        self.speed = 2
        self.chaves_coletadas = 0
        self.chaves_azuis_coletadas = 0
        self.jaula_coletada = 0
        self.morangos_coletados = 0
        self.velocity_y = 0

    def update(self, width, height, ground_group):
        top_value = self.rect[1]
        if top_value == 0:
            self.rect = self.rect.move(
                0, pg.display.get_surface().get_size()[1] - self.rect[3])
            self.image_upper = self.rect.copy()

        if self.morangos_coletados >= 10:
            self.hp += 1
            self.morangos_coletados -= 10

        self._walk(width)
        # verifica a colisão com o chão
        colisao_chao = pg.sprite.spritecollide(self, ground_group, False)
        self._jump(height, colisao_chao)

        if not colisao_chao:
            self.velocity_y += gravity  # aplica a gravidade
        else:
            self.velocity_y = 0  # Reset da velocidade vertical quando estiver no chão

        self.rect.y += self.velocity_y  # Atualiza a posição vertical com base na velocidade vertical

        self._walk(width)

    def _jump(self, height, colisao):
        up_pressed = pg.key.get_pressed()[pg.K_UP]
        w_pressed = pg.key.get_pressed()[pg.K_w]
        jump_height = 12
        gravity = 0.3

        if colisao:
            self.rect.y = colisao[0].rect.top - self.rect.height
            self.jump = False
        else:
            if (w_pressed or up_pressed) and not self.jump:
                self.jump = True
                self.jump_height = -jump_height

            if self.jump:
                if self.rect.bottom >= height:
                    self.rect.y = (height - 1) - self.rect.height
                    self.jump = False
                else:
                    self.rect.y += self.jump_height
                    self.jump_height += gravity

    def _walk(self, width):
        d_pressed = pg.key.get_pressed()[pg.K_d]
        right_pressed = pg.key.get_pressed()[pg.K_RIGHT]
        left_pressed = pg.key.get_pressed()[pg.K_LEFT]
        a_pressed = pg.key.get_pressed()[pg.K_a]

        if d_pressed or right_pressed:
            self.looking = True
            if self.rect.right < width:
                self.rect = self.rect.move(self.speed, 0)
        elif left_pressed or a_pressed:
            self.looking = False
            if self.rect.left > 0:
                self.rect = self.rect.move(-self.speed, 0)

        if self.jump:
            if self.looking:
                self.image = pg.transform.flip(load_image('sprite_llama_pulo.png'), True, False)
            else:
                self.image = load_image('sprite_llama_pulo.png')
        else:
            if self.looking:
                self.image = pg.transform.flip(load_image('sprite_llama.png'), True, False)
            else:
                self.image = load_image('sprite_llama.png')


class Morango(pg.sprite.Sprite):
    def __init__(self, x, y):
        pg.sprite.Sprite.__init__(self)
        self.image = load_image('morango.png', scale=0.15)
        self.rect = self.image.get_rect()
        self.rect.topleft = (x, y)


class Key(pg.sprite.Sprite):
    def __init__(self, x, y, imagem, tamanho):
        pg.sprite.Sprite.__init__(self)
        self.imagem = imagem
        self.image = load_image(self.imagem, scale=tamanho)
        self.rect = self.image.get_rect()
        # self.original_image = load_image(self.figura, scale=0.25)
        # self.image = pg.transform.scale(self.original_image, (int(self.original_image.get_width() * scale), int(self.original_image.get_height() * scale)))  # Aplica a escala à imagem
        self.rect.topleft = (x, y)

        # self.rect.center = (x, y)
        self.collected = False

    def update(self, character):
        if not self.collected and self.imagem == "chave_dourada.png":
            if self.rect.colliderect(character.rect):
                self.collected = True
                character.chaves_coletadas += 1

        if not self.collected and self.imagem == "chave_azul.png":
            if self.rect.colliderect(character.rect):
                self.collected = True
                character.chaves_azuis_coletadas += 1

        if not self.collected:
            if character.chaves_coletadas == 1 and character.chaves_azuis_coletadas == 1 and self.rect.colliderect(
                    character.rect):
                self.collected = True
                character.jaula_coletada += 1

    def draw(self, screen):
        if not self.collected:
            screen.blit(self.image, self.rect)


class Ground(pg.sprite.Sprite):
    def __init__(self, x, y, width, height, tranparencia):
        super().__init__()
        self.image = pg.Surface((width, height), pg.SRCALPHA)
        self.image.fill((0, 100, 0, tranparencia))
        self.rect = self.image.get_rect()
        self.rect.topleft = (x, y)


def main():
    pg.init()
    screen = pg.display.set_mode((1080, 760), pg.SCALED)
    pg.display.set_caption("Llama simulator")

    width = screen.get_size()[0]
    height = screen.get_size()[1]

    background = pg.Surface(screen.get_size())
    background = load_image('background.png', scale=1)
    background = pg.transform.scale(background, (width, height))

    keys_group = pg.sprite.Group()
    key_gold1 = Key(900, 500, "chave_dourada.png", 0.08)
    Key_blue1 = Key(450, 250, "chave_azul.png", 0.08)
    jaula = Key(900, 50, 'jaula.png', 0.2)
    keys_group.add(key_gold1, Key_blue1, jaula)

    # criação morangos
    morangos = pg.sprite.Group()
    morango1 = Morango(850, 500)
    morango2 = Morango(410, 500)
    morango3 = Morango(480, 500)
    morango4 = Morango(550, 500)
    morango5 = Morango(35, 420)
    morango6 = Morango(250, 250)
    morango7 = Morango(400, 250)
    morango8 = Morango(35, 100)
    morango9 = Morango(105, 100)
    morango10 = Morango(175, 100)
    morango11 = Morango(700, 150)

    morangos.add(morango1, morango2, morango3, morango4, morango5, morango6, morango7, morango8, morango9, morango10,
                 morango11)

    # criação do chão
    grounds = pg.sprite.Group()
    ground = Ground(0, 687, 1080, 70, 0)
    plataforma1 = Ground(800, 550, 200, 10, 255)
    plataforma2 = Ground(400, 550, 200, 10, 255)
    plataforma3 = Ground(30, 470, 150, 10, 255)
    plataforma4 = Ground(200, 300, 300, 10, 255)
    plataforma7 = Ground(600, 200, 180, 10, 255)
    plataforma8 = Ground(30, 150, 180, 10, 255)
    plataforma5 = Ground(800, 150, 200, 10, 255)

    # plataforma1 = Ground(500, 400, 50, 50)
    grounds.add(ground, plataforma1, plataforma5, plataforma2, plataforma3, plataforma4, plataforma7, plataforma8)

    screen.blit(background, (0, 0))
    print(pg.display.get_surface().get_size())
    pg.display.flip()

    pocoyo = Character()
    allsprites = pg.sprite.RenderPlain((pocoyo))
    clock = pg.time.Clock()

    hud = HUD(pocoyo)
    huds = pg.sprite.Group(hud)

    going = True
    while going:
        clock.tick(60)

        for event in pg.event.get():
            if event.type == pg.QUIT:
                going = False
        if pg.key.get_pressed()[pg.K_ESCAPE]:
            going = False
        elif going:
            pocoyo.update(screen.get_size()[0], screen.get_size()[1], grounds)

        keys_group.update(pocoyo)

        screen.blit(background, (0, 0))

        for key in keys_group:
            key.draw(screen)

        allsprites.update(screen.get_size()[0], screen.get_size()[1], grounds)
        allsprites.draw(screen)

        huds.update()
        huds.draw(screen)

        grounds.draw(screen)

        colisoes_morangos = pg.sprite.spritecollide(pocoyo, morangos, True)
        for morango in colisoes_morangos:
            pocoyo.morangos_coletados += 1

        morangos.draw(screen)

        pg.display.flip()

    pg.quit()

if __name__ == "__main__":
    main()