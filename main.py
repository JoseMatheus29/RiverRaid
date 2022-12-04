from pygame.locals import *
from objects2 import place, Colors, ponte, Islands, obj, shot
import pygame
import random

#Variaveis globais
gazlev = 0
gaz_level = 166
eny_box = 96
helice = 0
n_eny = 5
vel_y = 2
speed = 0
vidas = 1
pontos = 0
delay_y = 3
screen_height = 480
sair = False
game = False
intro = False
hitplane = False
width, height = 800,600
s_gaz_alert = "gaz_full"


# Iniciando o jogo
pygame.init()


# Definindo a janela
win = pygame.display.set_mode((width, height))

# Sons
voo0 = pygame.mixer.Sound("sons/voo0.wav")
voo1 = pygame.mixer.Sound("sons/voo1.wav")
voo2 = pygame.mixer.Sound("sons/voo2.wav")
gaz1 = pygame.mixer.Sound("sons/gaz1.wav")
gaz0 = pygame.mixer.Sound("sons/gaz0.wav")
s_tiro = pygame.mixer.Sound("sons/tiro.wav")
gaz_end = pygame.mixer.Sound("sons/gaz_end.wav")
s_explode = pygame.mixer.Sound("sons/explode.wav")
gaz_alert = pygame.mixer.Sound("sons/gaz_alert.wav")
gaz_explode = pygame.mixer.Sound("sons/gaz_explode.wav")

# Objetos
casas = [3]
colors = Colors.cor
plane = obj.Obj(win, 370, 420, 49, 42, 0, 0, 0)
terra = [3]
tiro = shot.Shot(win, 1, 0, 1)
islands = [3]
base = place.Place(win, width, 8, -100)
enemy = [n_eny]
data_casa = [3]
data_enemy = [n_eny]
data_island = [3, 3, 3]
data_terra = [3, 3, 3]
pontes = [3]


for i in range(n_eny):
    enemy.append(i)
    enemy[i] = obj.Obj(win, 0, 0, 0, 0, 0, 0, 0)
    data_enemy.append(i)


for i in range(3):
    terra.append(i)
    islands.append(i)
    pontes.append(i)
    casas.append(i)
    data_casa.append(i)

    casas[i] = obj.Obj(win, -100, 0, 85, 56, 14, 0, 0)
    pontes[i] = ponte.Ponte(win, i * 485, -screen_height, 316, 77, 0, 0, 0)
    islands[i] = Islands.Ilhas(win, width, 1, 0)
    terra[i] = place.Place(win, width, 3, -i * 336)


pontes[2].ty = 1
pontes[2].x = 312
pontes[2].out = 1
pontes[2].h = 68
pontes[2].w = 175




def restart():
    """"Função que começa o jogo novamente"""
    global pontos, vidas, mover, hitplane,data_enemy, data_island, data_terra, eny_box, gaz_level, data_casa,s_gaz_alert

    # Zerando as variaveis
    vidas = 3
    pontos = 0
    base.y = -100
    mover = False
    gaz_level = 166
    plane.out = True
    hitplane = False
    pontes[2].out = True
    s_gaz_alert = "gaz_full"

    #Parando os sons
    voo0.stop()
    voo1.stop()
    voo2.stop()
    gaz_alert.stop()

    # Zerando os objetos
    for i in range(3):
        terra[i].forma = 3
        data_terra[i] = 3
        terra[i].y = -i * 336 - 100
        islands[i].y = -1600
        data_island[i] = 13
        casas[i].x = 80
        data_casa[i] = [80, False]

    data_casa[1][1] = True

    for i in range (n_eny):
        data_enemy[i] = [100, i * eny_box -screen_height, 42, 30, 6, 1, 0]
    data_enemy[4] =  [350, -96, 81, 24, 8, 0]
    data_enemy[3] = [450, -192, 42, 30, 6, 0]
    data_enemy[1] = [500, -384, 37, 77, 11, 0]


def opned():

    global game, intro, vidas, gaz_level, casas, pontos
    #introdução do jogo

    if base.y < 238 and not game:
        intro = True
        base.y+=1
        for i in range (n_eny):
            enemy[i].y +=1
            if i < 3:
                casas[i].y +=1
                islands[i].y += 1
                terra[i].y +=1

    if base.y == -100 and plane.out:
        ler_pos()

    #Iniciando o jogo
    if base.y < 238 and game and intro:
        base.y+=1
        for i in range(n_eny):
            #espaço entre a base e os inimigos
            if enemy[i].y > base.y+4:
                enemy[i].out = True
            enemy[i].y += 1
            if i < 3:
                casas[i].y +=1
                islands[i].y +=1
                terra[i].y +=1

    #controlando se o avião morreu
    if plane.out and not plane.t_expl and game and vidas > 0 and not intro:
        pontos = 0
        intro = True
        gaz_level = 166
        pontes[2].out = True
        plane.x = 370
        plane.ty = 0
        base.y = -100

    if base.y == 238 and game and intro:
        plane.out = False

    #Verifica se saiu
    for e in pygame.event.get():
        if e.type == pygame.QUIT or e.type == pygame.KEYDOWN and e.key == K_RCTRL:
            return True
        if (e.type == KEYDOWN) and e.key == K_F2:
            restart()
            game = True
        if base.y == 238 and game and intro and (e.type == KEYDOWN):
            intro = False
            voo1.play(-1)

    return False


def hitcortest(obj, cor):
    cor = hex(cor)
    cor = cor.lstrip('0x')
    cor = tuple(int(cor[i:i + int(6 / 3)], 16) for i in range(0, 6, int(6 / 3)))

    if obj.x >= 0 and obj.x + obj.w <= width and obj.y >= 0 and obj.y + obj.h <= height:
        for i in range(int(obj.w)):
            for j in range(int(obj.h)):
                if (not i and (not j or j == int(obj.h) - 1)) or not j and i == int(obj.w) - 1:
                    if win.get_at((int(obj.x + i), int(obj.y + j))) == cor:
                        return True
    return False


def colidir(a,b):
    return a.x + a.w > b.x and a.x < b.x + b.w and a.y + a.h > b.y and a.y < b.y + b.h


def salvar_pos():
    global data_enemy, data_casa, data_terra, data_island
    for i in range(n_eny):
        data_enemy[i][0] = enemy[i].x
        data_enemy[i][1] = enemy[i].y
        data_enemy[i][2] = enemy[i].w
        data_enemy[i][3] = enemy[i].h
        data_enemy[i][4] = enemy[i].ty
        data_enemy[i][5] = enemy[i].out
        if i < 3:
            data_terra[i] = terra[i].forma
            data_island[i] = islands[i].forma
            data_casa[i][0] = casas[i].x
            data_casa[i][1] = casas[i].y


def ler_pos():
    global game, data_island, data_terra, data_enemy, eny_box
    if vidas < 0:
        game = False
    for i in range(n_eny):
        enemy[i].x = data_enemy[i][0]
        enemy[i].y = data_enemy[i][1]
        enemy[i].w = data_enemy[i][2]
        enemy[i].h = data_enemy[i][3]
        enemy[i].ty = data_enemy[i][4]
        enemy[i].out = data_enemy[i][5]

    for i in range(3):
        casas[i].x = data_casa[i][0]
        casas[i].out = data_casa[i][1]
        terra[i].forma = data_terra[i]
        islands[i].forma = data_island[i]
        casas[i].x = 80
        casas[i].y = -i * 350

    terra[0].y = 100


def hittest():
    global hitplane, gaz_level, mover, pontos, gaz_alert
    t_expl = 40
    #tiro com paredes
    if hitcortest(tiro, colors[2]):
        tiro.y = -tiro.h

    #avião com a parede
    if hitcortest(plane, colors[2]) or hitplane or not gaz_level and not plane.out:
        voo0.stop()
        voo1.stop()
        voo2.stop()
        mover = False
        hitplane = False
        plane.out = True
        gaz_alert.stop()
        plane.t_expl = 30


    enehit = 0

    for i in range(n_eny):
        if enemy[i].ty == 5 or enemy[i].ty == 6 or enemy[i].ty == 8 or enemy[i].ty == 9:
            enemy[i].dir = -1
        else:
            enemy[i].dir = 1

        hit = enemy[i].w
        enemy[i].w = hit / 2
        if hitcortest(enemy[i], colors[2]):
            if enemy[i].ty == 5 or enemy[i].ty == 6:
                enemy[i].ty = 4
                enemy[i].x += 2
            if enemy[i].ty == 8:
                enemy[i].x += 2
                enemy[i].ty = 7

        enemy[i].x += hit / 2
        if hitcortest(enemy[i], colors[2]):
            if enemy[i].ty == 4 or enemy[i].ty == 3:
                enemy[i].x -= 2
                enemy[i].ty = 6
            if enemy[i].ty == 7:
                enemy[i].x -= 2
                enemy[i].ty = 8
        enemy[i].x -= hit / 2
        enemy[i].w = hit

        # Tiro colide com os objetos
        if colidir(tiro, enemy[i]) and not enemy[i].out and tiro.y >= 0:
            enemy[i].t_expl = t_expl
            enemy[i].out = True
            enehit = enemy[i].ty
            s_tiro.stop()
            s_explode.play()
            tiro.y = -tiro.h

        # Avião colidindo
        if colidir(plane, enemy[i]) and enemy[i].ty != 11 and not enemy[i].out:
            enemy[i].t_expl = t_expl
            enemy[i].out = True
            enehit = enemy[i].ty
            s_tiro.stop()
            hitplane = True

        # Avião com gasoline
        if colidir(plane, enemy[i]) and enemy[i].ty == 11 and not enemy[i].out and not plane.out:
            if gaz_level < 165:
                gaz0.play()
                gaz_level += 0.3
            else:
                gaz1.play()

        # Avião com pontes
        if (colidir(plane, pontes[0]) or colidir(plane, pontes[1])) and not plane.out:
            hitplane = True

        # Avião com ponte base
        if colidir(plane, pontes[2]) and not pontes[2].out:
            salvar_pos()
            hitplane = False
            pontos += 250
            pontes[2].out = True
            pontes[2].t_expl = t_expl

        # Tiro com a ponte da base
        if colidir(pontes[2], tiro) and not pontes[2].out and tiro.y >= 0:
            salvar_pos()
            pontes[2].t_expl = t_expl
            pontes[2].out = True
            pontos += 250
            s_tiro.stop()
            s_explode.play()
            tiro.y = -100



        #Pontos ao atingir um inimigo
        if 2 < enehit < 7:  # helicoptero
            pontos += 80
        elif 6 < enehit < 9:  # navio
            pontos += 40
        elif 8 < enehit < 11:  # avião
            pontos += 120
        elif enehit == 11:  # Posto gaz
            pontos += 30


def inimigos():
    global helice, gaz_level, gazlev, s_gaz_alert
    helice = not helice
    hittest()
    for i in range(n_eny):
        if helice and enemy[i].ty == 3 or enemy[i].ty == 5:
            enemy[i].ty += 1
        elif enemy[i].ty == 4 or enemy[i].ty == 6:
            enemy[i].ty -= 1

        if game and not intro:
            #movimento dos inimigos na vertical
            enemy[i].y += mover * vel_y

            #movimento dos navios e helicopteros
            if 2 < enemy[i].ty < 9 and enemy[i].y > 200 and not enemy[i].out:
                enemy[i].x += enemy[i].dir

            #movimento dos aviões
            if enemy[i].ty == 10 or enemy[i].ty == 9:
                if enemy[i].x > width and enemy[i].ty == 10:
                    enemy[i].x = 0
                if enemy[i].x < 0 and enemy[i].ty == 9:
                    enemy[i].x = width
                if not enemy[i].out and not plane.out:
                    enemy[i].x += enemy[i].dir

            #reposicionando inimigos
            if enemy[i].y == screen_height - eny_box / 3:
                enemy[i].y = 0
                if base.y < enemy[i].y < base.y + 400:
                    enemy[i].out = True
                else:
                    enemy[i].out = False

                #sorteia inimigos
                enemys = [4, 6, 7, 8, 9, 10, 11]
                rnd = random.randint(0, 6)
                enemy[i].ty = enemys[rnd]
                if rnd == 0 or rnd == 1:
                    enemy[i].w = 42
                    enemy[i].h = 30
                elif rnd == 2 or rnd == 3:
                    enemy[i].w = 81
                    enemy[i].h = 24
                elif rnd == 4 or rnd == 5:
                    enemy[i].w = 48
                    enemy[i].h = 18
                elif rnd == 6:
                    enemy[i].w = 37
                    enemy[i].h = 72

                pos = True
                while pos:
                    enemy[i].x = random.randint(0, 8) * 84 + 23
                    pos = hitcortest(enemy[i], colors[2])

                enemy[i].y = -eny_box/3
            if -370 <= base.y < 50 and enemy[i].y == screen_height + eny_box/2:
                enemy[i].out = True

            if enemy[i].y == screen_height + eny_box/2:
                enemy[i].y = -eny_box/2

        enemy[i].show()
    # Retira gasolina
    if not intro and mover:
        gazlev+=1
        if gazlev > 100:
            gazlev = 0
            gaz_level -= 5
        if gaz_level < 0:
            gaz_level = 0

    if gaz_level <= 70 and s_gaz_alert == "gaz_full":
        s_gaz_alert = "gaz_alert"
        gaz_alert.play(-1)
    if gaz_level <= 5 and gazlev > 80 and s_gaz_alert == "gaz_alert":
        s_gaz_alert = "gaz_end"
        gaz_alert.stop()
        gaz_end.play()

    if s_gaz_alert != "gaz_full" and gaz_level > 70:
        s_gaz_alert = "gaz_full"
        gaz_end.stop()
        gaz_alert.stop()


def lands():
    if game and not intro and not plane.t_expl:
        base.y += mover * vel_y

    for i in range(3):
        islands[i].y = base.y - (2000+i*246)
        terra[i].y = base.y - (330+i*300)

        #verificando se a terra lateral chegou no limite da tela e voltando pra origem
        if terra[i].y < screen_height:
            terra[i].show()
        #Verificando se a ilha chegou no limite da tela e voltando para a origem
        if islands[i].y < screen_height:
            islands[i].show()

    for i in range(3):
        #movendo casinhas em y
        casas[i].y+=mover * vel_y

        #criando as pocicoes
        if casas[i].y == screen_height:
            casas[i].y = 0
            rnd_casas = [0,1,2,3,4,5,6,7,8]
            random.shuffle(rnd_casas)
            for j in range(0, 8):
                casas[i].x = rnd_casas[j] * casas[i].w + 25
                if hitcortest(casas[i], colors[3]) or pontes[2].t_expl or colidir(casas[i], pontes[0]) or colidir(casas[i],pontes[1]) or colidir(casas[i], pontes[2]):casas[i].out = True
                else:
                    casas[i].out = False
                    break

        if casas[i].y < screen_height:
            casas[i].show()

        pontes[i].y = base.y + 164
        if -screen_height < base.y < screen_height:
            pontes[i].show()

    pontes[2].y = base.y +169

    if base.y > screen_height and not intro:
        pontes[2].out = False


def paint():
    pygame.display.update()
    #Rio
    if pontes[2].t_expl % 2:
        win.fill(colors[8])
    else:
        win.fill(colors[3])

    if plane.out == False and not intro:
        control()

    tiro.show(plane.x + plane.w/2, plane.y + plane.h/2)

    #Fundo
    win.fill(colors[2], rect=[0, 0, 20, height])
    win.fill(colors[2], rect=[width - 20, 0,20, height])

    if -screen_height < base.y < screen_height:
        base.show()

    lands()
    inimigos()
    plane.show()

    #Painel
    win.fill(colors[7], rect=[0, screen_height, width, 130])
    win.fill(colors[11],rect=[0, height - 117, width, 112])

    #medidor de gasolina
    pygame.draw.rect(win, colors[7], [320, 515, 204, 44],4)
    pygame.draw.rect(win, colors[7], [335, 515, 11, 13])
    pygame.draw.rect(win, colors[7], [422, 515, 11, 13])
    pygame.draw.rect(win, colors[7], [500, 515, 11, 13])

    textos()

    #Reinicia ilha e base
    if islands[2].y > screen_height:
        base.y = -400
        for i in range(3):
            terra[i].forma = random.randint(0, 7)
            islands[i].forma = random.randint(0, 3)


def textos():
    #medidor
    font = pygame.font.SysFont("arial",33)
    txt = font.render("E       " + chr(189) + "       F", 0,(0,0,0))
    win.blit(txt, (334, 524))
    pygame.draw.rect(win, colors[1], [335 + gaz_level, 529, 10, 27])

    #vidas
    if vidas:
        font = pygame.font.SysFont("cooper Black", 34)
        txt = font.render(str(vidas), 0, (232,232,74))
        win.blit(txt, (290, 554))

    #Pontos
    if pontos:
        font = pygame.font.SysFont("cooper Black", 34)
        txt = font.render(str(pontos), 0, (232, 232, 74))
        win.blit(txt, (450, 474))


def control():
    global speed, delay_y, mover
    if game and not intro:
        speed+=1
        if speed > delay_y:
            mover = True
            speed = 0
        else:
            mover = False

    plane.ty = 0
    key = pygame.key.get_pressed()
    if key[K_LEFT] and plane.x > 10:
        plane.x -= 1
        plane.ty = 1
    if key[K_RIGHT] and plane.x < 734:
        plane.x += 1
        plane.ty = 1

    #controlando a velocidade
    if key[K_UP]:
        if delay_y > 0:
            voo0.stop()
            voo1.stop()
            voo2.play(-1)
        delay_y = 0
    elif key[K_DOWN]:
        if delay_y < 2:
            voo1.stop()
            voo2.stop()
            voo0.play(-1)
        delay_y = 2
    else:
        if delay_y != 1:
            voo0.stop()
            voo2.stop()
            voo1.play(-1)
        delay_y = 1

    # Atirando
    if key[K_SPACE]:
        tiro.shoting = True
        if tiro.y == plane.y - 15:
            s_tiro.stop()
            s_tiro.play()


restart()

while not sair:
    paint()
    sair = opned()