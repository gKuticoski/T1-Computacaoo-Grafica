# ***********************************************************************************
#   PontosNoTriangulo.py
#       Autor: Márcio Sarroglia Pinho
#       pinho@pucrs.br
#   Este programa exibe um conjunto de Pontos e um triangulo em OpenGL
#   Para construir este programa, foi utilizada a biblioteca PyOpenGL, disponível em
#   http://pyopengl.sourceforge.net/documentation/index.html
#
#   Sugere-se consultar também as páginas listadas
#   a seguir:
#   http://bazaar.launchpad.net/~mcfletch/pyopengl-demo/trunk/view/head:/PyOpenGL-Demo/NeHe/lesson1.py
#   http://pyopengl.sourceforge.net/documentation/manual-3.0/index.html#GLUT
#
#   No caso de usar no MacOS, pode ser necessário alterar o arquivo ctypesloader.py,
#   conforme a descrição que está nestes links:
#   https://stackoverflow.com/questions/63475461/unable-to-import-opengl-gl-in-python-on-macos
#   https://stackoverflow.com/questions/6819661/python-location-on-mac-osx
#   Veja o arquivo Patch.rtf, armazenado na mesma pasta deste fonte.
# ***********************************************************************************

from ctypes.wintypes import POINT
from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *
from Poligonos import * 
from QuadTree import *
from Envelope import *
import random

# ***********************************************************************************
# Variaveis que controlam o triangulo do campo de visao
PontosDoCenario = Polygon()
CampoDeVisao = Polygon()
TrianguloBase = Polygon()
PosicaoDoCampoDeVisao = Ponto

AnguloDoCampoDeVisao=0.0

# Limites da Janela de Seleção
Min = Ponto()
Max = Ponto()
Tamanho = Ponto()
Meio = Ponto()

PontoClicado = Ponto()
TotalPontosNoTriangulo = 0
TotalPontosNoEnvelope = 0
TotalPontosQuadTree = 0

flagDesenhaEixos = True
flagDesenhaPontos = False

modo = 0

# capac = 8
QuadTreeCenario = QuadTree(Envelope(Ponto(0, 0),  Ponto(500,500)), 8)

# **********************************************************************
# GeraPontos(int qtd)
#      Metodo que gera pontos aleatorios no intervalo [Min..Max]
# **********************************************************************
def GeraPontos(qtd, Min: Ponto, Max: Ponto):
    global PontosDoCenario
    Escala = Ponto()
    Escala = (Max - Min) * (1.0/1000.0)
    
    for i in range(qtd):
        x = random.randint(0, 1000)
        y = random.randint(0, 1000)
        x = x * Escala.x + Min.x
        y = y * Escala.y + Min.y
        P = Ponto(x,y)
        PontosDoCenario.insereVertice(P.x, P.y, P.z)
        QuadTreeCenario.insert_point(P)
        #PontosDoCenario.insereVertice(P)

# **********************************************************************
#  CriaTrianguloDoCampoDeVisao()
#  Cria um triangulo a partir do vetor (1,0,0), girando este vetor
#  em 45 e -45 graus.
#  Este vetor fica armazenado nas variáveis "TrianguloBase" e
#  "CampoDeVisao"
# **********************************************************************
def CriaTrianguloDoCampoDeVisao():
    global TrianguloBase, CampoDeVisao

    vetor = Ponto(1,0,0)

    TrianguloBase.insereVertice(0,0,0)
    CampoDeVisao.insereVertice(0,0,0)
    
    vetor.rotacionaZ(45)
    TrianguloBase.insereVertice (vetor.x,vetor.y, vetor.z)
    CampoDeVisao.insereVertice (vetor.x,vetor.y, vetor.z)
    
    vetor.rotacionaZ(-90)
    TrianguloBase.insereVertice (vetor.x,vetor.y, vetor.z)
    CampoDeVisao.insereVertice (vetor.x,vetor.y, vetor.z)

def getEnvelope():
    global CampoDeVisao

    min, max = CampoDeVisao.getLimits()
    return Envelope(min, max)


# ***********************************************************************************
# void PosicionaTrianguloDoCampoDeVisao()
#  Posiciona o campo de visão na posicao PosicaoDoCampoDeVisao,
#  com a orientacao "AnguloDoCampoDeVisao".
#  O tamanho do campo de visão eh de 25% da largura da janela.
# **********************************************************************
def PosicionaTrianguloDoCampoDeVisao():
    global Tamanho, CampoDeVisao, PosicaoDoCampoDeVisao, TrianguloBase
    global AnguloDoCampoDeVisao


    tam = Tamanho.x * 0.25
    temp = Ponto()
    for i in range(TrianguloBase.getNVertices()):
        temp = TrianguloBase.getVertice(i)
        temp.rotacionaZ(AnguloDoCampoDeVisao)
        CampoDeVisao.alteraVertice(i, PosicaoDoCampoDeVisao + temp*tam)


def AvancaCampoDeVisao(distancia):
    global PosicaoDoCampoDeVisao, AnguloDoCampoDeVisao
    vetor = Ponto(1,0,0)
    vetor.rotacionaZ(AnguloDoCampoDeVisao)
    PosicaoDoCampoDeVisao = PosicaoDoCampoDeVisao + vetor * distancia

# ***********************************************************************************
#
# ***********************************************************************************
def init():
    global PosicaoDoCampoDeVisao, AnguloDoCampoDeVisao

    # Define a cor do fundo da tela (AZUL)
    glClearColor(0, 0, 1, 1)
    global Min, Max, Meio, Tamanho

    GeraPontos(500, Ponto(0,0), Ponto(500,500))
    Min, Max = PontosDoCenario.getLimits()  
    #Min, Max = PontosDoCenario.LePontosDeArquivo("PoligonoDeTeste.txt")

    Meio = (Max+Min) * 0.5 # Ponto central da janela
    Tamanho = (Max - Min) # Tamanho da janela em X,Y

    # Ajusta variaveis do triangulo que representa o campo de visao
    PosicaoDoCampoDeVisao = Meio
    AnguloDoCampoDeVisao = 0

    # Cria o triangulo que representa o campo de visao
    CriaTrianguloDoCampoDeVisao()
    PosicionaTrianguloDoCampoDeVisao()


def produtoVetorial(aresta1: Ponto, aresta2: Ponto):
    return (aresta1.x*aresta2.y) - (aresta2.x*aresta1.y)


def lado(pt: Ponto, a: Ponto, b: Ponto):
    aresta1 = pt-a
    aresta2 = b-a

    prodVeto = produtoVetorial(aresta1, aresta2)
    if prodVeto > 0: return 1
    elif prodVeto < 0: return -1
    return 0

def pontoNoTriangulo(ponto: Ponto):
    global CampoDeVisao, TotalPontosNoTriangulo

    a = CampoDeVisao.getVertice(0)
    b = CampoDeVisao.getVertice(1)
    c = CampoDeVisao.getVertice(2)

    l1 = lado(ponto, a, b)
    l2 = lado(ponto, b, c)
    l3 = lado(ponto, c, a)
    
    if (l1 == l2) and (l2 == l3): 
        TotalPontosNoTriangulo += 1
        return True

    return False
    

def contarPontosNoTriangulo():
    global TotalPontosNoTriangulo 
    TotalPontosNoTriangulo = 0
    for n in range(PontosDoCenario.getNVertices()):
        pt: Ponto = PontosDoCenario.getVertice(n)
        glColor(1, 0, 0)
        if pontoNoTriangulo(pt):
            glColor(0, 1, 0)
        
        desenha(pt)

    #print("Pontos no triangulo: ", TotalPontosNoTriangulo)


def desenha(pt: Ponto):
    glBegin(GL_POINTS);
    glVertex3f(pt.x,pt.y,pt.z)
    glEnd();

def desenhaEnvelope(poly: Polygon):
    global TotalPontosNoEnvelope, TotalPontosNoTriangulo

    TotalPontosNoTriangulo = 0
    TotalPontosNoEnvelope = 0
    Envelope_tri = getEnvelope()
    Envelope_tri.desenhaPoligono()

    for n in range(poly.getNVertices()):
        pt: Ponto = poly.getVertice(n)
        glColor(1, 0, 0)
        if Envelope_tri.is_inside(pt):
            TotalPontosNoEnvelope += 1
            if pontoNoTriangulo(pt):
                glColor(0, 1, 0)
            else:
                glColor(1, 1, 0 )

        desenha(pt)

def filtraPontosPelaQuad(poly: Polygon):
    global TotalPontosNaQuad, TotalPontosNoTriangulo, QuadTreeCenario

    TotalPontosNoTriangulo = 0
    TotalPontosNaQuad = 0

    for n in range(poly.getNVertices()):
        pt: Ponto = poly.getVertice(n)
        glColor3f(1,0,0) # R, G, B  [0..1]
        # PontosDoCenario.desenhaVertices()
        if QuadTreeCenario.is_inside_quad(pt):
            TotalPontosNaQuad += 1
            if pontoNoTriangulo(pt):
                glColor(0, 1, 0)
            else:
                glColor(1, 1, 0 )
        # else:
        #     glColor(1, 0, 0 )

        desenha(pt)

# ***********************************************************************************
#
# ***********************************************************************************
def DesenhaLinha (P1, P2):
    glBegin(GL_LINES)
    glVertex3f(P1.x,P1.y,P1.z)
    glVertex3f(P2.x,P2.y,P2.z)
    glEnd()

# ***********************************************************************************
#
# ***********************************************************************************
def DesenhaEixos():
    global Min, Max, Meio

    glBegin(GL_LINES)
    # eixo horizontal
    glVertex2f(Min.x,Meio.y)
    glVertex2f(Max.x,Meio.y)
    # eixo vertical
    glVertex2f(Meio.x,Min.y)
    glVertex2f(Meio.x,Max.y)
    glEnd()

# ***********************************************************************************
def reshape(w,h):
    global Min, Max

    glViewport(0, 0, w, h)
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    # Cria uma folga na Janela de Selecão, com 10% das dimensoes do poligono
    BordaX = abs(Max.x-Min.x)*0.1
    BordaY = abs(Max.y-Min.y)*0.1
    glOrtho(Min.x-BordaX, Max.x+BordaX, Min.y-BordaY, Max.y+BordaY, 0.0, 1.0)
    glMatrixMode (GL_MODELVIEW)
    glLoadIdentity()

# ***********************************************************************************
def display():
    global PontoClicado, flagDesenhaEixos, modo, QuadTreeCenario

    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    glLoadIdentity()
    glColor3f(1.0, 0.0, 0.0)

    if (flagDesenhaEixos):
        glLineWidth(1)
        glColor3f(1,1,1); # R, G, B  [0..1]
        DesenhaEixos()

    glPointSize(3);
    glColor3f(1,0,0) # R, G, B  [0..1]
    PontosDoCenario.desenhaVertices()

    glLineWidth(3)
    glColor3f(1,0,0) # R, G, B  [0..1]
    CampoDeVisao.desenhaPoligono()
    glColor3f(1.0, 1.0, 1.0)

    if modo == 1:
        global TotalPontosNoTriangulo 
        TotalPontosNoTriangulo = 0
        contarPontosNoTriangulo()
        print("Pontos no triangulo: ", TotalPontosNoTriangulo)
    elif modo == 2:
        TotalPontosNoTriangulo = 0
        desenhaEnvelope(PontosDoCenario)
        print("Pontos com o algoritmo do envelope: ", TotalPontosNoTriangulo)
    elif modo == 3:
        TotalPontosNoTriangulo = 0
        QuadTreeCenario.desenha_quad_tree()
    elif modo == 4:
        TotalPontosNoTriangulo = 0
        QuadTreeCenario.intersecao(getEnvelope(), PontosDoCenario)
        filtraPontosPelaQuad(PontosDoCenario)
        print("Pontos com o algoritmo da quadtree: ", TotalPontosNoTriangulo)
        

    glutSwapBuffers()

# ***********************************************************************************
# The function called whenever a key is pressed. Note the use of Python tuples to pass in: (key, x, y)
#ESCAPE = '\033'
ESCAPE = b'\x1b'
def keyboard(*args):
    global flagDesenhaEixos, TrianguloBase, modo

    #print (args)
    # If escape is pressed, kill everything.
    if args[0] == b'q':
        os._exit(0)
    if args[0] == ESCAPE:
        os._exit(0)
    if args[0] == b'p':
        PontosDoCenario.imprimeVertices()
    if args[0] == b'o':
        p: Ponto = TrianguloBase.getVertice(1) * 1.05
        TrianguloBase.alteraVertice(1, p)
        p: Ponto = TrianguloBase.getVertice(2) * 1.05
        TrianguloBase.alteraVertice(2, p)
        PosicionaTrianguloDoCampoDeVisao()
    if args[0] == b'i':
        p: Ponto = TrianguloBase.getVertice(1) * 0.95
        TrianguloBase.alteraVertice(1, p)
        p: Ponto = TrianguloBase.getVertice(2) * 0.95
        TrianguloBase.alteraVertice(2, p)
        PosicionaTrianguloDoCampoDeVisao()
    if args[0] == b'g':
        P1, P2 = PontosDoCenario.getAresta(0)
        P1.imprime()
        P2.imprime()
    if args[0] == b' ':
        flagDesenhaEixos = not flagDesenhaEixos
    if args[0] == b'a':
        # modo = modo + 1 
        if modo < 4:
            modo = modo + 1
        else:
            modo = 1
    if args[0] == b'1':
        #QuadTreeCenario = QuadTree(Envelope(Ponto(0, 0),  Ponto(500,500)), 1)
        #QuadTreeCenario.desenha_quad_tree()
        print("mudou para 1")
            # elif args[0] == b'2':
            #     # capac = 2
            #     QuadTreeCenario.desenha_quad_tree()
            # elif args[0] == b'3':
            #     # capac = 3
            #     QuadTreeCenario.desenha_quad_tree()
            # elif args[0] == b'4':
            #     # capac = 4
            #     QuadTreeCenario.desenha_quad_tree()
        
            # global TotalPontosNoTriangulo 
            # TotalPontosNoTriangulo = 0

    # Forca o redesenho da tela
    glutPostRedisplay()
# **********************************************************************
#  arrow_keys ( a_keys: int, x: int, y: int )   
# **********************************************************************
def arrow_keys(a_keys: int, x: int, y: int):
    global AnguloDoCampoDeVisao, TrianguloBase

    #print ("Tecla:", a_keys)
    if a_keys == GLUT_KEY_UP:         # Se pressionar UP
        AvancaCampoDeVisao(2)
    if a_keys == GLUT_KEY_DOWN:       # Se pressionar DOWN
        AvancaCampoDeVisao(-2)
    if a_keys == GLUT_KEY_LEFT:       # Se pressionar LEFT
        AnguloDoCampoDeVisao = AnguloDoCampoDeVisao + 2
    if a_keys == GLUT_KEY_RIGHT:      # Se pressionar RIGHT
        AnguloDoCampoDeVisao = AnguloDoCampoDeVisao - 2

    PosicionaTrianguloDoCampoDeVisao()

    glutPostRedisplay()

# ***********************************************************************************
#
# ***********************************************************************************
def mouse(button: int, state: int, x: int, y: int):
    global PontoClicado
    if (state != GLUT_DOWN): 
        return
    if (button != GLUT_RIGHT_BUTTON):
        return
    #print ("Mouse:", x, ",", y)
    # Converte a coordenada de tela para o sistema de coordenadas do 
    # universo definido pela glOrtho
    vport = glGetIntegerv(GL_VIEWPORT)
    mvmatrix = glGetDoublev(GL_MODELVIEW_MATRIX)
    projmatrix = glGetDoublev(GL_PROJECTION_MATRIX)
    realY = vport[3] - y
    worldCoordinate1 = gluUnProject(x, realY, 0, mvmatrix, projmatrix, vport)

    PontoClicado = Ponto (worldCoordinate1[0],worldCoordinate1[1], worldCoordinate1[2])
    PontoClicado.imprime("Ponto Clicado:")

    glutPostRedisplay()

# ***********************************************************************************
#
# ***********************************************************************************
def mouseMove(x: int, y: int):
    #glutPostRedisplay()
    return


# ***********************************************************************************
# Programa Principal
# ***********************************************************************************

glutInit(sys.argv)
glutInitDisplayMode(GLUT_RGBA)
# Define o tamanho inicial da janela grafica do programa
glutInitWindowSize(500, 500)
glutInitWindowPosition(100, 100)
wind = glutCreateWindow("Pontos no Triangulo")
glutDisplayFunc(display)
#glutIdleFunc(display)
glutReshapeFunc(reshape)
glutKeyboardFunc(keyboard)
glutSpecialFunc(arrow_keys)
glutMouseFunc(mouse)
init()

try:
    glutMainLoop()
except SystemExit:
    pass
