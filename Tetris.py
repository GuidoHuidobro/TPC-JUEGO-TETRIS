
import pygame 
from pygame.locals import * 
from random import randint
pygame.init()
ventana = pygame.display.set_mode((600,600))
forma = [] # forma actual mostrada en la pantalla
formas = [[[3,-1],[4,-1],[5,-1],[6,-1]],# las siete formas de tetris
          [[3,0],[4,0],[4,-1],[5,0]],
          [[3,-1],[4,0],[4,-1],[5,0]],
          [[3,0],[4,0],[4,-1],[5,-1]],
          [[3,-1],[3,0],[4,0],[5,0]],
          [[3,0],[5,0],[4,0],[5,-1]],
          [[3,-1],[3,0],[4,-1],[4,0]]]
llaves = [0,0,0] # los 3 movimientos básicos de una forma hacia abajo, izquierda y derecha
base = [] # las piezas asentadas
omen = [] # la siguiente pieza que se va a generar
colores = [(247,19,247),(247,187,19),(19,240,247),(239,119,163),(175,119,239),(32,169,78)] # color de las piezas
carrera = (128,0,0) # color actual de la pieza en la pantalla
game = 0 #  0 -> jugando el game, 1 -> perdido el game
new_game_image = pygame.image.load("nuevo_juego.png") # logo para iniciar un game nuevo

clickear = 0 # si el usuario hizo clic para iniciar un nuevo game 
button = [(200,200,200),(255,0,0)] 
puntos = 0 # 10 por cada línea completada 
mifuente = pygame.font.SysFont('Comic Sans MS', 20) 
miotrafuente = pygame.font.SysFont('Comic Sans MS', 15) 
proxima_pieza = [] # la forma que se va a generar a continuación 
proxima_carrera = [] # el color de la forma que se va a generar a continuación 
nivel = 1 # el nivel, para cada nivel la velocidad aumenta en 50 milisegundos 
up_button = 0 # Si el usuario hace clic en el botón de nivel superior 
down_button = 0 # Si el usuario hace clic en el botón de nivel menor
pausa = 0 # Si el usuario hace clic en el botón de pausa #pausa
bnivel = 0 # el nivel antes de que el usuario hiciera clic en pausa 
highscore = 0 #highscore
pygame.display.set_icon(pygame.image.load("tetris.png"))
pygame.display.set_caption("Unla Tetris")
sad_cara = 0
sad_forma = [[2,3],[2,4],[2,10],[2,11],[3,3],[3,4],[3,10],[3,11],[5,6],[5,7],[5,8],[6,6],[6,7],[6,8],[9,5],[9,6],[9,7],[9,8],[9,9]]
start = 0
def dibujar_cara():
    global sad_forma
    global ventana
    global sad_cara
    for i in sad_forma:
        if sad_cara == 1:
            pygame.draw.rect(ventana,(0,255,0),[30*i[1]+2,30*i[0]+2,26,26])
        else:
            pygame.draw.rect(ventana,(255,255,255),[30*i[1]+2,30*i[0]+2,26,26])
def menufy(forma): # función para transformar la siguiente forma para que aparezca en una forma en el menú
    menufied = []
    for i in forma:
        menufied.append([i[0]-3,i[1]+2])
    return menufied

def menu(): # función para mostrar el menú de la derecha
    global clickear 
    global puntos
    global proxima_pieza
    global proxima_carrera
    global nivel
    global up_button
    global down_button
    global pausa
    global highscore
    next_forma = [] # variable de la siguiente forma que se va a generar
    pygame.draw.rect(ventana, (128,128,128), [450,0,150,600]) # el rectángulo gris del menu
    textsurcara = mifuente.render("Nuevo", False, (0,0,0)) 
    ventana.blit(textsurcara, (490, 8))
    textsurcara = mifuente.render("Juego", False, (0,0,0))
    ventana.blit(textsurcara, (480, 24))
    textsurcara = mifuente.render(":", False, (0,0,0))
    ventana.blit(textsurcara, (480, 24))
    pygame.draw.circle(ventana, (200,200,200), [570,30], 20) # Botón para hacer clic en Nuevo juevo
    if clickear == 1:
        pygame.draw.circle(ventana, (255,0,0), [570,30], 20) # si se hace clic en el botón Nuevo juego, se vuelve rojo
    ventana.blit(new_game_image, (560,18)) # Nuevo juego logo
    textsurcara = mifuente.render("Puntos : "+str(puntos), False, (0,0,0))# Puntos mostrados
    ventana.blit(textsurcara, (480, 55)) 
    textsurcara = mifuente.render("Proxima Pieza", False, (0,0,0)) 
    ventana.blit(textsurcara, (475, 87))
    pygame.draw.lines(ventana, (255,0,0), False, [(460,125),(580,125),(580,245),(460,245),(460,125)],2) # Las siguientes 7 líneas son para mostrar la cuadrícula
    pygame.draw.line(ventana, (255,0,0),[490,125],[490,245],2)
    pygame.draw.line(ventana, (255,0,0),[520,125],[520,245],2)
    pygame.draw.line(ventana, (255,0,0),[550,125],[550,245],2)
    pygame.draw.line(ventana, (255,0,0),[460,155],[580,155],2)
    pygame.draw.line(ventana, (255,0,0),[460,185],[580,185],2)
    pygame.draw.line(ventana, (255,0,0),[460,215],[580,215],2)
    next_forma = menufy(proxima_pieza) # gire las posiciones de la forma en la lista de formas (línea 11) en posición en la cuadrícula dibujada arriba
    for i in next_forma:
        pygame.draw.rect(ventana,proxima_carrera,[462+30*i[0],127+i[1]*30,28,28])
    textsurcara = mifuente.render("Nivel : "+str(nivel), False, (0,0,0))# nivel de visualización
    ventana.blit(textsurcara, (460, 280))
    pygame.draw.circle(ventana, (200,200,200), [570,280], 20) # dibujar botón
    if up_button == 1:
        pygame.draw.circle(ventana, (255,0,0), [570,280], 20) # si se hace clic en el botón arriba, girar el botón rojo
    pygame.draw.circle(ventana, (200,200,200), [570,375], 20) # dibujar botón de pausa-continuar
    if pausa == 0:
        textsurcara = mifuente.render("Pausa ", False, (0,0,0)) # si el juego está activado, escribe "pausa:"
        ventana.blit(textsurcara, (460, 360))
        pygame.draw.polygon(ventana, (0,0,0), [[563,360],[563,390],[583,375]]) # dibujar símbolo de pausa (triángulo)
    else:
        textsurcara = mifuente.render("Continuar : ", False, (0,0,0)) # si el juego está en pausa, escribe "continuar:"
        ventana.blit(textsurcara, (453, 360))
        pygame.draw.rect(ventana, (0,0,0), [557,360,10,30]) # esta línea y la siguiente son para dibujar el símbolo de continuación (dos rectas paralelas)
        pygame.draw.rect(ventana, (0,0,0), [573,360,10,30])
    pygame.draw.circle(ventana, (200,200,200), [570,325], 20) # botón de bajar
    textsurcara = mifuente.render("MayorPuntaje : ", False, (0,0,0)) # las siguientes 4 líneas son para mostrar la puntuación más alta durante la sesión
    ventana.blit(textsurcara, (455, 420))
    textsurcara = mifuente.render(str(highscore), False, (0,0,0))
    ventana.blit(textsurcara, (475, 445))
    if down_button: 
        pygame.draw.circle(ventana, (255,0,0), [570,325], 20) # si se hace clic en el botón abajo, se vuelve rojo
    pygame.draw.lines(ventana, (0,0,0), False, [[560,290],[570,265],[580,290]],2) # dibujar símbolo
    pygame.draw.lines(ventana, (0,0,0), False, [[560,315],[570,340],[580,315]],2) # dibujar símbolo
    pygame.draw.rect(ventana, (255,0,0), [450,535,150,80]) # Las siguientes 7 líneas son para dibujar el banner en la parte inferior del menú.
    
    

def fuera_obligado(hape):# Esta función se utiliza durante las rotaciones, comprueba si la forma rotada no está en la pantalla
    for i in hape:
        if (i[0]<0) or (i[0]>14):
            return True
    return False

def traducir(hape, moverse):
    new_moverse = []
    for i in hape:
        if i[0]<15 and i[0]>-1:
            new_moverse.append([i[0]+moverse,i[1]])
        else:
            return hape
    return new_moverse

def dentro(hape, basis):
    for i in hape:
        if i in basis:
            return True
    return False

def hacer(): # generar la forma actual y siguiente y sus colores
    global forma
    global formas
    global colores
    global carrera
    global base
    global clickear
    global proxima_pieza
    global proxima_carrera
    global puntos
    global highscore
    for i in base:
        if i[1] == 0:
            if highscore < puntos:
                highscore = puntos
            animacion()
            return True
    forma = proxima_pieza
    carrera = proxima_carrera
    proxima_pieza = formas[randint(0,len(formas)-1)]
    proxima_carrera = colores[randint(0,len(colores)-1)]
    clickear = 0
    return False
    
def checkit(): # si se completa la línea en la base, se vuelve verde durante 0.1 segundos y se elimina
    global base
    global puntos
    global nivel
    checker = 0
    bases = []
    for i in range(0,20):
        for j in range(0,15):
            if [j,i] not in base:
                checker = 1
                break
        if checker == 0:
            bases.append(i)
            puntos = puntos + 10
            if puntos%100 == 0:
                if nivel<8:
                    nivel = nivel +1
        checker = 0
    return bases

def predecir():
    global base
    global forma
    global omen
    if forma == []:
        return []
    omen = []
    for i in forma:
        omen.append([i[0],i[1]])
    old_omen = []
    llegado = False
    while not llegado:
        old_omen = omen
        for i in omen:
            i[1] = i[1] + 1
            if i[1] >= 19 or [i[0],i[1]+1] in base:
                llegado = 1
    if omen == forma:
        omen = []
    return omen 
    
def removerseit(lines): # eliminar líneas, ver función checkit
    global base
    new_base = []
    for i in base:
        if i[1] not in lines:
            new_base.append(i)
    for j in new_base:
        for k in lines:
            if j[1]<k:
                j[1] = j[1] + 1
    return new_base

def in_base(hape):  # función utilizada durante la rotación, si la forma rotada está en la base
    global base
    for i in hape:
        if i in base:
            return True
    return False

def en_el_piso(hape):  # si la forma en movimiento golpea la parte inferior de la pantalla
    for i in hape:
        if i[1] == 19:
            return True
    return False

def obtener_limite_superior_izquierdo(): 
    global forma
    l = 14
    t = 19
    for i in forma:
        if i[0] < l:
            l = i[0]
        if i[1] < t:
            t = i[1]
    return [l,t]

def mas_izquierda_arriba(hape):
    l = hape[0][0]
    t = hape[0][1]
    for i in hape:
        if i[0] < l:
            l = i[0]
        if i[1] < t:
            t = i[1]
    return [l,t]

def arriba_izquierda():
    global forma 
    l = forma[0][0]
    t = 19
    for i in forma:
        if i[0] < l:
            l = i[0]
    for i in forma:
        if i[0] == l:
            if i[1] < t:
                t = i[1]
    return [l,t]

def get_diff(lt):
    global forma
    forma_diff = []
    for i in forma:
        forma_diff.append([lt[0]-i[0],lt[1]-i[1]])
    return forma_diff
    
def init_transformar(gd): # transformaración base para rotaciones
    const = 0
    for i in gd:
        i[0] = i[0] * -1
        const = i[0]
        i[0] = i[1]
        i[1] = const
    return gd 

def pantalla_trasera(hape):
        r = 0
        d = 0
        new_hape = hape
        for i in hape:
            if i[0]>r:
                r = i[0]
            if i[1]>d:
                d = i[1]
        if r>14:
            new_hape = []
            for i in hape:
                new_hape.append([i[0]+(14-r),i[1]])
        if d>19:
            new_hape = []
            for i in hape:
                new_hape.append([i[0],i[1]+(19-d)])
        return new_hape
            
    
def transformar(tl, it): # función central para rotación, las 8 funciones anteriores se utilizan todas dentro de esta función
    global forma
    global base
    final_forma = []
    ml = []
    for i in it:
        final_forma.append([tl[0]+i[0],tl[1]+i[1]])
    ml = mas_izquierda_arriba(final_forma)
    lefttop = obtener_limite_superior_izquierdo()
    for j in final_forma:
        j[0] = j[0] + (lefttop[0] - ml[0])
        j[1] = j[1] + (lefttop[1] - ml[1])
    siko = pantalla_trasera(final_forma)
    if dentro(siko,base):
        siko = traducir(siko,1)
        if dentro(siko,base):
            siko = traducir(siko,-1)
            if dentro(siko,base):
                siko = forma        
    return siko

def moverse_d():
    global forma
    global base
    global init
    global game
    global puntos
    new = []
    for i in forma:
        if i[1] == 19:
            for i in forma:
                base.append(i)
            if not hacer():
                draw_wall()
                draw_base()
                draw_forma()
                pygame.display.flip()
                return
            return
    for i in forma:
        new.append([i[0],i[1]+1])
    if in_base(new):
        for i in forma:
            base.append(i)
        if not hacer():
            draw_wall()
            draw_base()
            draw_forma()
            pygame.display.flip()
    else:
        forma = new
    lines = []
    lines = checkit()
    if lines != []:
        draw_forma()
        dibujalo(lines)
        pygame.time.wait(300)
        base = removerseit(lines)
        draw_wall()
        draw_base()
        draw_forma()
        pygame.time.wait(300)
def moverse_r():
    global forma
    new = []
    for i in forma:
        if i[0] == 14:
            return
    for i in forma:
        new.append([i[0] + 1,i[1]])
    if not in_base(new):
        forma = new

def moverse_l():
    global forma
    new = []
    for i in forma:
        if i[0] == 0:
            return
    for i in forma:
        new.append([i[0] - 1,i[1]])
    if not in_base(new):
        forma = new
def draw_forma():
    global forma
    for i in forma:
        pygame.draw.rect(ventana, carrera, [30*i[0]+2,30*i[1]+2, 26, 26])
    pygame.display.flip()
def draw_wall():
    menu()
    futura_base = predecir()
    for i in range(0,15):
        for j in range(0,20):
            pygame.draw.rect(ventana, (128,128,128), [30*i,30*j, 30,30])
            if [i,j] in futura_base:
                pygame.draw.rect(ventana, (0,255,0), [30*i,30*j, 30,30])
            pygame.draw.rect(ventana, (255,255,255), [30*i+2,30*j+2, 26,26])
def dibujalo(lines):
    for i in lines:
        for j in range(0,15):
            pygame.draw.rect(ventana, (0,255,0), [30*j+2,30*i+2, 26,26])
    pygame.display.flip()
def draw_base():
    for i in base:
        pygame.draw.rect(ventana, (0,0,255), [30*i[0]+2,30*i[1]+2, 26, 26])
def animacion():
    global base
    global omen
    global game
    global llaves
    global forma
    llaves = [0,0,0]
    base = []
    omen = []
    game = 1
    draw_wall()
    for j in range(0,20):
        for i in range(0,15):
            pygame.draw.rect(ventana, (128,128,128), [30*i, 30*(19-j), 30, 30])
            pygame.draw.rect(ventana, (255,0,0), [30*i+2, 30*(19-j)+2, 26, 26])
        pygame.display.flip()
        pygame.time.wait(200)
    forma = []
continuer = 0
draw_wall()
draw_forma()
pygame.display.flip()
pygame.time.set_timer(USEREVENT+1, 400)
pygame.time.set_timer(USEREVENT+2, 350)
pygame.time.set_timer(USEREVENT+3, 300)
pygame.time.set_timer(USEREVENT+4, 250)
pygame.time.set_timer(USEREVENT+5, 200)
pygame.time.set_timer(USEREVENT+6, 150)
pygame.time.set_timer(USEREVENT+7, 100)
pygame.time.set_timer(USEREVENT, 50)
proxima_pieza = formas[randint(0,len(formas)-1)]
proxima_carrera = colores[randint(0,len(colores)-1)]
hacer()
while continuer == 0:
    for event in pygame.event.get():
        if event.type == QUIT:
            continuer = 1
        if event.type == KEYDOWN and game == 0 and pausa == 0:
            if event.key == K_RIGHT:
                llaves[0] = 1
            if event.key == K_LEFT:
                llaves[1] = 1
            if event.key == K_DOWN:
                llaves[2] = 1
            if event.key == K_UP:
                forma = transformar(arriba_izquierda(),init_transformar(get_diff(arriba_izquierda())))
                draw_wall()
                draw_base()
                draw_forma()
        if event.type == KEYUP and game == 0:
            llaves = [0,0,0]
        if event.type == MOUSEBUTTONDOWN :
            if (event.pos[0]<590 and event.pos[0]>550) and (event.pos[1]<50 and event.pos[1]>10):
                    if highscore < puntos:
                        highscore = puntos
                    game = 0
                    base = []
                    puntos = 0
                    nivel = 1
                    clickear = 1
            if (event.pos[0]<590 and event.pos[0]>550) and (event.pos[1]<300 and event.pos[1]>260) and pausa == 0:
                up_button = 1
                if nivel < 8:
                    nivel = nivel + 1
            if (event.pos[0]<590 and event.pos[0]>550) and (event.pos[1]<345 and event.pos[1]>305) and pausa == 0:
                down_button = 1
                if nivel > 1:
                    nivel = nivel - 1
            if (event.pos[0]<590 and event.pos[0]>550) and (event.pos[1]<395 and event.pos[1]>355) and game == 0:
                if pausa == 0:
                    pausa = 1
                    bnivel = nivel
                    nivel = 0
                else:
                    pausa = 0
                    nivel = bnivel
                draw_wall()    
                draw_forma()
                draw_base()
                pygame.display.flip()
        if event.type == MOUSEBUTTONUP:
            if clickear == 1:
                clickear = 0
                hacer()
            if up_button == 1:
                up_button = 0
            if down_button == 1:
                down_button = 0
        if game == 1:
            if event.type == USEREVENT+1:
                    sad_cara = (sad_cara+1)%2
                    dibujar_cara()
        if game == 0:
            if event.type == USEREVENT+1 and game == 0 and nivel == 1:
                draw_wall()
                draw_base()
                moverse_d()
                draw_forma()
            if event.type == USEREVENT+2 and game == 0 and nivel == 2:
                draw_wall()
                draw_base()
                moverse_d()
                draw_forma()
            if event.type == USEREVENT+3 and game == 0 and nivel == 3:
                draw_wall()
                draw_base()
                moverse_d()
                draw_forma()
            if event.type == USEREVENT+4 and game == 0 and nivel == 4:
                draw_wall()
                draw_base()
                moverse_d()
                draw_forma()
            if event.type == USEREVENT+5 and game == 0 and nivel == 5:
                draw_wall()
                draw_base()
                moverse_d()
                draw_forma()
            if event.type == USEREVENT+6 and game == 0 and nivel == 6:
                draw_wall()
                draw_base()
                moverse_d()
                draw_forma()
            if event.type == USEREVENT+7 and game == 0 and nivel == 7:
                draw_wall()
                draw_base()
                moverse_d()
                draw_forma()
            if event.type == USEREVENT and game == 0 and nivel == 8:
                draw_wall()
                draw_base()
                moverse_d()
                draw_forma()
    if llaves[0] == 1 and game == 0:
        pygame.time.wait(100)
        draw_wall()
        draw_base()
        moverse_r()
        draw_forma()
    if llaves[1] == 1 and game == 0:
        pygame.time.wait(100)
        draw_wall()
        draw_base()
        moverse_l()
        draw_forma()
    if llaves[2] == 1 and game == 0:
        pygame.time.wait(100)
        draw_wall()
        draw_base()
        moverse_d()
        draw_forma()
    pygame.display.flip()
