""" Programa principal """

import glfw
from OpenGL.GL import *
import OpenGL.GL.shaders
import numpy as np
import grafica.transformations as tr
import grafica.basic_shapes as bs
import grafica.performance_monitor as pm
import grafica.scene_graph as sg
from shapes import *
from math import *
import newLightShaders as nl
import shaders as sh
from obj_reader import *


class Controller:
    def __init__(self):
        self.camara = 0

        self.is_left_pressed = False
        self.is_right_pressed = False

        self.light = True

        self.slowmo = False

        self.auto = False


    def on_key(self, window, key, scancode, action, mods):

        if key == glfw.KEY_RIGHT:
            if action == glfw.PRESS:
                self.is_right_pressed = True
            elif action == glfw.RELEASE:
                self.is_right_pressed = False

        if key == glfw.KEY_LEFT:
            if action == glfw.PRESS:
                self.is_left_pressed = True
            elif action == glfw.RELEASE:
                self.is_left_pressed = False
        
        if key == glfw.KEY_TAB:
            if action == glfw.PRESS:
                self.light = not self.light
                if self.light:
                    print("(TAB) Cel Shading")
                else:
                    print("(TAB) Phong")
        
        if key == glfw.KEY_1:
            if action == glfw.PRESS:
                self.slowmo = not self.slowmo
                if self.slowmo:
                    print("(1) Cámara lenta")
                else:
                    print("(1) Velocidad normal")

        if key == glfw.KEY_2:
            if action == glfw.PRESS:
                self.auto = not self.auto
                if self.auto:
                    print("(2) Cámara automática")
                else:
                    print("(2) Cámara manual")

        if key == glfw.KEY_ESCAPE:
            if action == glfw.PRESS:
                glfw.set_window_should_close(window, True)


    #Funcion que recibe el input para manejar la camara
    def update_camera(self):
        if self.is_left_pressed:
            self.camara += 1

        if self.is_right_pressed:
            self.camara -= 1


#####################################################################

if __name__ == "__main__":

    # Initialize glfw
    if not glfw.init():
        glfw.set_window_should_close(window, True)

    width = 800
    height = 800
    title = "T2b - Bailando con Cel Shading"

    window = glfw.create_window(width, height, title, None, None)

    if not window:
        glfw.terminate()
        glfw.set_window_should_close(window, True)

    glfw.make_context_current(window)

    controller = Controller()
    # Connecting the callback function 'on_key' to handle keyboard events
    glfw.set_key_callback(window, controller.on_key)

     # Different shader programs for different lighting strategies
    phongPipeline = nl.MultiplePhongShaderProgram()

    celTexPipeline = sh.CelShading()
    phongTexPipeline = sh.MultipleTexturePhongShaderProgram()


    # Setting up the clear screen color
    glClearColor(0.85, 0.85, 0.85, 1.0)

    # As we work in 3D, we need to check which part is in front,
    # and which one is at the back
    glEnable(GL_DEPTH_TEST)

    # Creating shapes on GPU memory

    scene = createScene(celTexPipeline)

    ############################################

    # Montañas

    mountain = createTextureGPUShape(readOBJT(getAssetPath('mountain.obj')),celTexPipeline, "sprites/mountain.png")
    mountainNode = sg.SceneGraphNode("mountain")
    mountainNode.transform = tr.matmul([tr.translate(0,0,-5),tr.rotationX(pi/2),tr.scale(50,75,50)])
    mountainNode.childs = [mountain]
    
    ############################################

    # Mesa

    table = createTextureGPUShape(readOBJT(getAssetPath('table.obj')),celTexPipeline, "sprites/table.jpg")
    tableNode = sg.SceneGraphNode("table")
    tableNode.transform = tr.matmul([tr.translate(0,0,-5),tr.rotationX(pi/2),tr.uniformScale(0.035)])
    tableNode.childs = [table]
    
    ############################################

    # Arboles

    tree = createTextureGPUShape(readOBJT(getAssetPath('tree.obj')),celTexPipeline, "sprites/tree.png")
    treeNode = sg.SceneGraphNode("tree")
    treeNode.transform = tr.rotationX(pi/2)
    treeNode.childs = [tree]

    tree1 = sg.SceneGraphNode("tree1")
    tree1.transform = tr.matmul([tr.translate(25,30,-5),tr.rotationZ(1),tr.uniformScale(1.5)])
    tree1.childs = [treeNode]

    tree2 = sg.SceneGraphNode("tree2")
    tree2.transform = tr.matmul([tr.translate(-17,25,-5),tr.rotationZ(2),tr.uniformScale(1.75)])
    tree2.childs = [treeNode]

    tree3 = sg.SceneGraphNode("tree3")
    tree3.transform = tr.matmul([tr.translate(-13,-10,-5),tr.rotationZ(3),tr.uniformScale(3.5)])
    tree3.childs = [treeNode]

    tree4 = sg.SceneGraphNode("tree4")
    tree4.transform = tr.matmul([tr.translate(8,19,-5),tr.rotationZ(4),tr.uniformScale(2.75)])
    tree4.childs = [treeNode]

    tree5 = sg.SceneGraphNode("tree5")
    tree5.transform = tr.matmul([tr.translate(17,-21,-5),tr.rotationZ(5),tr.uniformScale(3.25)])
    tree5.childs = [treeNode]

    tree6 = sg.SceneGraphNode("tree6")
    tree6.transform = tr.matmul([tr.translate(21,0,-5),tr.rotationZ(6),tr.uniformScale(2.9)])
    tree6.childs = [treeNode]

    tree7 = sg.SceneGraphNode("tree7")
    tree7.transform = tr.matmul([tr.translate(-25,-2,-5),tr.rotationZ(7),tr.uniformScale(2.0)])
    tree7.childs = [treeNode]

    bosque = sg.SceneGraphNode("bosque")
    bosque.childs = [tree1, tree2, tree3, tree4, tree5, tree6, tree7]

    ############################################

    # Botella

    bottle = createTextureGPUShapeR(readOBJT(getAssetPath('botella.obj')),celTexPipeline, "sprites/botella.png")
    botella = sg.SceneGraphNode("botella")
    botella.transform = tr.matmul([tr.translate(-0.85,-3,-2.75),tr.rotationX(pi/2),tr.uniformScale(0.075)])
    botella.childs = [bottle]
    
    ############################################

    # Cielo

    skybox = createTextureGPUShape(createSkybox(),celTexPipeline, "sprites/night.jpg")
    skyboxNode = sg.SceneGraphNode("skybox")
    skyboxNode.transform = tr.matmul([tr.translate(0,0,0),tr.uniformScale(100)])
    skyboxNode.childs = [skybox]
    
    ############################################
 
    # Personaje
 
    cara = createTextureGPUShape(readOBJT(getAssetPath('world.obj')),celTexPipeline, "sprites/world.png")
    caraNode = sg.SceneGraphNode("cara")
    caraNode.transform = tr.matmul([tr.translate(0,5.5,0),tr.uniformScale(1.25)])
    caraNode.childs = [cara]

    headNode = sg.SceneGraphNode("head")
    headNode.childs = [caraNode]

    torso = createTextureGPUShapeR(readOBJT(getAssetPath('torso.obj')),celTexPipeline, "sprites/torso.jpg")
    torsoNode = sg.SceneGraphNode("torso")
    torsoNode.transform = tr.matmul([tr.translate(0,0,0),tr.uniformScale(1.0)])
    torsoNode.childs = [torso]

    arm = createTextureGPUShapeR(readOBJT(getAssetPath('arm1.obj')),celTexPipeline, "sprites/arm.jpg")
    arm2 = createTextureGPUShapeR(readOBJT(getAssetPath('arm2.obj')),celTexPipeline, "sprites/arm.jpg")
    armW = createTextureGPUShapeR(readOBJT(getAssetPath('armW.obj')),celTexPipeline, "sprites/armW.jpg")
    
    larm1Node = sg.SceneGraphNode("larm1")
    larm1Node.childs = [arm]   

    larm2rotNode = sg.SceneGraphNode("larm2rot")
    larm2rotNode.childs = [armW]

    larm2Node = sg.SceneGraphNode("larm2")
    larm2Node.transform = tr.matmul([tr.translate(0,-2,0),tr.rotationY(pi)])
    larm2Node.childs = [larm2rotNode]

    rarm1Node = sg.SceneGraphNode("rarm1")
    rarm1Node.childs = [arm]

    rarm2rotNode = sg.SceneGraphNode("rarm2rot")
    rarm2rotNode.childs = [arm2]
    
    rarm2Node = sg.SceneGraphNode("rarm2")
    rarm2Node.transform = tr.translate(0,-2,0)
    rarm2Node.childs = [rarm2rotNode]

    larm1rotNode = sg.SceneGraphNode("larm1rot")
    larm1rotNode.childs = [larm1Node ,larm2Node]

    rarm1rotNode = sg.SceneGraphNode("rarm1rot")
    rarm1rotNode.childs = [rarm1Node, rarm2Node]

    larm = sg.SceneGraphNode("larm")
    larm.transform = tr.translate(0,3.75,-1.75)
    larm.childs = [larm1rotNode]

    rarm = sg.SceneGraphNode("rarm")
    rarm.transform = tr.translate(0,3.75,1.75)
    rarm.childs = [rarm1rotNode]

    leg = createTextureGPUShapeR(readOBJT(getAssetPath('leg.obj')),celTexPipeline, "sprites/pant.png")
    
    lleg1Node = sg.SceneGraphNode("lleg1")
    lleg1Node.childs = [leg]

    lleg2rotNode = sg.SceneGraphNode("lleg2rot")
    lleg2rotNode.childs = [leg]

    lleg2Node = sg.SceneGraphNode("lleg2")
    lleg2Node.transform = tr.translate(0,-2.15,0)
    lleg2Node.childs = [lleg2rotNode]

    rleg1Node = sg.SceneGraphNode("rleg1") 
    rleg1Node.childs = [leg]

    rleg2rotNode = sg.SceneGraphNode("rleg2rot") 
    rleg2rotNode.childs = [leg]
    
    rleg2Node = sg.SceneGraphNode("rleg2")
    rleg2Node.transform = tr.translate(0,-2.15,0)
    rleg2Node.childs = [rleg2rotNode]

    lleg1rotNode = sg.SceneGraphNode("lleg1rot")
    lleg1rotNode.childs = [lleg1Node, lleg2Node]

    rleg1rotNode = sg.SceneGraphNode("rleg1rot")
    rleg1rotNode.childs = [rleg1Node, rleg2Node]

    lleg = sg.SceneGraphNode("lleg")
    lleg.transform = tr.translate(0,-4,-0.75)
    lleg.childs = [lleg1rotNode]

    rleg = sg.SceneGraphNode("rleg")
    rleg.transform = tr.translate(0,-4,0.75)
    rleg.childs = [rleg1rotNode]

    upperrotNode = sg.SceneGraphNode("upperrot")
    upperrotNode.childs = [headNode, torsoNode, larm, rarm]

    upper = sg.SceneGraphNode("upper")
    upper.transform = tr.translate(0,-3.5,0)
    upper.childs = [upperrotNode]

    cuerpo = sg.SceneGraphNode("cuerpo")
    cuerpo.transform = tr.matmul([tr.rotationX(pi/2),tr.uniformScale(0.45)])
    cuerpo.childs = [upper, lleg, rleg]
    
    dancer = sg.SceneGraphNode("dancer")
    dancer.childs = [cuerpo]

    ############################################

    # Luces

    blanco = createTextureGPUShapeR(readOBJT(getAssetPath('sphere1.obj')),celTexPipeline, "sprites/sphere1.png")
    amarillo = createTextureGPUShapeR(readOBJT(getAssetPath('sphere2.obj')),celTexPipeline, "sprites/sphere2.png")
    morado = createTextureGPUShapeR(readOBJT(getAssetPath('sphere3.obj')),celTexPipeline, "sprites/sphere3.png")

    bsphere = sg.SceneGraphNode("bsphere")
    bsphere.childs = [blanco]

    asphere = sg.SceneGraphNode("asphere")
    asphere.childs = [amarillo]

    msphere = sg.SceneGraphNode("msphere")
    msphere.childs = [morado]

    spheres = sg.SceneGraphNode("spheres")
    spheres.childs = [bsphere, asphere, msphere]

    ############################################

    # Referencias a nodos para aplicar transformaciones

    salto = sg.findNode(dancer, "dancer")

    espalda = sg.findNode(dancer, "upperrot")
    
    pizq1 = sg.findNode(dancer, "lleg1rot")
    pizq2 = sg.findNode(dancer, "lleg2rot")
    pder1 = sg.findNode(dancer, "rleg1rot")
    pder2 = sg.findNode(dancer, "rleg2rot")
    bizq1 = sg.findNode(dancer, "larm1rot")
    bizq2 = sg.findNode(dancer, "larm2rot")
    bder1 = sg.findNode(dancer, "rarm1rot")
    bder2 = sg.findNode(dancer, "rarm2rot")

    bder1.transform = tr.rotationZ(11*pi/20)
    bizq1.transform = tr.rotationZ(9*pi/20)

    bder2.transform = tr.rotationX(pi/2)
    bizq2.transform = tr.rotationX(pi/2)

    c1 = sg.findNode(spheres, "bsphere")
    c2 = sg.findNode(spheres, "asphere")
    c3 = sg.findNode(spheres, "msphere")

    ############################################

    # Curvas para las cámaras

    M = 500

    camara1 = catmull25(M)
    camara2 = catmull26(M)
    camara3 = catmull27(M)
    camara4 = catmull28(M)

    ############################################

    # Curvas para el modelo

    N = 100
    
    rodilla1 = catmull1(N)
    rodilla2 = catmull2(N)

    shin1 = catmull3(N)
    shin2 = catmull4(N)

    espalda1 = catmull3(N)
    espalda2 = catmull4(N)

    giro1cuerpo = catmull5(N)
    giro1b11 = catmull6(N)
    giro1b12 = catmull7(N)
    giro1b21 = catmull8(N)
    giro1b22 = giro1b12

    giro2cuerpo = catmull9(N)
    giro2b11 = catmull10(N)
    giro2b12 = catmull29(N)
    giro2b21 = catmull11(N)

    giro3cuerpo = catmull12(N)
    giro3b11Y = catmull13(N)
    giro3b11Z = catmull14(N)
    giro3b12 = catmull15(N)
    giro3b21X = catmull16(N)
    giro3b21Z = catmull17(N)

    giro4b11Y = catmull18(N)
    giro4b11Z = catmull19(N)
    giro4b12 = catmull20(N)
    giro4cuerpoY = catmull21(N)

    luces1 = catmull22(3*N)
    luces2 = catmull23(3*N)
    luces3 = catmull24(3*N)

    ############################################

    # Parámetros para las luces

    radio = 12.5

    luz0 = np.array([radio, 0, 10, 0.0])
    luz1 = luz0
    luz2 = luz0

    ############################################

    perfMonitor = pm.PerformanceMonitor(glfw.get_time(), 0.5)
    # glfw will swap buffers as soon as possible
    glfw.swap_interval(0)
    t0 = glfw.get_time()

    cont1 = 0
    cont4 = 0
    rot = 0

    movluces1 = 0

    intens = 1
    intens2 = 0

    # Application loop
    while not glfw.window_should_close(window):
        # Variables del tiempo
        t1 = glfw.get_time()
        delta = t1 -t0
        t0 = t1

        ############################################

        # Movimiento de las luces

        if controller.slowmo:
            speed = 50
        else:
            speed = 200
        
        rot += speed/150000  
        

        movluces1 += delta*speed
        movluces2 = int(movluces1)

              
        if movluces2 < 3*N:              
            posluz0 = tr.matmul([luz0,tr.rotationY(2*pi*luces3[movluces2][1]),tr.rotationZ(pi*luces1[movluces2][1] + t1*0.25)])
            posluz1 = tr.matmul([luz1,tr.rotationY(2*pi*luces3[movluces2][1]),tr.rotationZ(pi*luces1[movluces2][1] + t1*0.25 + pi*2/3)])
            posluz2 = tr.matmul([luz2,tr.rotationY(2*pi*luces3[movluces2][1]),tr.rotationZ(pi*luces1[movluces2][1] + t1*0.25 + pi*4/3)])

            c1.transform = tr.translate(posluz0[0],posluz0[1],posluz0[2])
            c2.transform = tr.translate(posluz1[0],posluz1[1],posluz1[2])
            c3.transform = tr.translate(posluz2[0],posluz2[1],posluz2[2])
     
        if movluces2 >= 3*N and movluces2 < 6*N:
            aux = movluces2%(3*N)
            posluz0 = tr.matmul([luz0,tr.rotationY(2*pi*luces3[aux][1]),tr.rotationZ(pi*luces1[aux][1] + t1*0.25)])
            posluz1 = tr.matmul([luz1,tr.rotationY(2*pi*luces3[aux][1]),tr.rotationZ(pi*luces1[aux][1] + t1*0.25 + pi*2/3)])
            posluz2 = tr.matmul([luz2,tr.rotationY(2*pi*luces3[aux][1]),tr.rotationZ(pi*luces1[aux][1] + t1*0.25 + pi*4/3)])

            c1.transform = tr.translate(posluz0[0],posluz0[1],posluz0[2])
            c2.transform = tr.translate(posluz1[0],posluz1[1],posluz1[2])
            c3.transform = tr.translate(posluz2[0],posluz2[1],posluz2[2])

        if movluces2 >= 6*N:
            movluces1 = 0
            movluces2 = movluces1

        ############################################

        # Movimiento del personaje
        # Por como funciona el baile, las piernas y brazos se animan por separado

        cont1 += delta*speed
        cont2 = int(cont1)
                
        salto.transform = tr.matmul([tr.translate(0,0,abs(sin(pi*cont2/N)/3)),tr.rotationZ(rot)])

        # Piernas

        cont3 = True
        
        if (cont2//N)%2 == 0:
            cont3 = False

        if cont3:
            pizq1.transform = tr.rotationZ(pi*rodilla1[cont2%N][1])
            pder1.transform = tr.rotationZ(pi*rodilla2[cont2%N][1])
            pizq2.transform = tr.rotationZ(-pi*shin1[cont2%N][1])
            pder2.transform = tr.rotationZ(-pi*shin2[cont2%N][1])
        else:
            pizq1.transform = tr.rotationZ(pi*rodilla2[cont2%N][1])
            pder1.transform = tr.rotationZ(pi*rodilla1[cont2%N][1])
            pizq2.transform = tr.rotationZ(-pi*shin2[cont2%N][1])
            pder2.transform = tr.rotationZ(-pi*shin1[cont2%N][1])

        # Brazos

        cont4 += delta*speed
        cont5 = int(cont4)
        
        if cont5 >= 5*N and cont5 < 6*N:
            espalda.transform = tr.matmul([tr.rotationX(pi*giro1cuerpo[cont5-5*N][1]),tr.rotationZ(pi*espalda1[cont5-5*N][1]*0.6)])
            bder1.transform = tr.rotationZ(pi*giro1b11[cont5-5*N][1])
            bder2.transform = tr.matmul([tr.rotationX(pi*giro1b12[cont5-5*N][1]),tr.rotationZ(-pi*giro2b21[cont5%N][1])])
            bizq1.transform = tr.rotationZ(pi*giro1b21[cont5-5*N][1])
            bizq2.transform = tr.rotationX(pi*giro1b22[cont5-5*N][1])
        if (cont5 >= 6*N and cont5 < 7*N) or (cont5 >= 8*N and cont5 < 9*N) or (cont5 >= 10*N and cont5 < 11*N):
            aux = cont5%N
            espalda.transform = tr.matmul([tr.rotationX(pi*giro2cuerpo[aux][1]),tr.rotationZ(pi*0.7*0.6)])
            bder1.transform = tr.rotationZ(pi*giro2b11[aux][1])
            bder2.transform = tr.rotationZ(pi*giro2b12[aux][1])
            bizq1.transform = tr.rotationZ(pi*giro2b21[aux][1])
            bizq2.transform = tr.rotationZ(-pi*giro2b12[N-1-cont5%N][1])
        if (cont5 >= 7*N and cont5 < 8*N) or (cont5 >= 9*N and cont5 < 10*N):
            aux = N-1-cont5%N
            espalda.transform = tr.matmul([tr.rotationX(pi*giro2cuerpo[aux][1]),tr.rotationZ(pi*0.7*0.6)])
            bder1.transform = tr.rotationZ(pi*giro2b11[aux][1])
            bder2.transform = tr.rotationZ(pi*giro2b12[aux][1])
            bizq1.transform = tr.rotationZ(pi*giro2b21[aux][1])
            bizq2.transform = tr.rotationZ(-pi*giro2b12[cont5%N][1])
        if cont5 >= 11*N and cont5 < 12*N:
            espalda.transform = tr.matmul([tr.rotationX(-pi*giro1cuerpo[11*N-cont5][1]),tr.rotationZ(pi*espalda2[cont5-11*N][1]*0.6)])
            bder1.transform = tr.rotationZ(pi*giro1b21[11*N-cont5][1])
            bder2.transform = tr.rotationX(pi*giro1b12[11*N-cont5][1])
            bizq1.transform = tr.rotationZ(pi*giro1b11[11*N-cont5][1])
            bizq2.transform = tr.matmul([tr.rotationX(pi*giro1b22[11*N-cont5][1]),tr.rotationZ(pi*giro2b21[N-1-cont5%N][1])])
        
        if cont5 >=14*N and cont5 < 15*N:
            espalda.transform = tr.rotationY(-pi*giro3cuerpo[cont5-14*N][1])
            
            bder1.transform = tr.matmul([tr.rotationY(-pi*giro3b11Y[cont5-14*N][1]),tr.rotationZ(pi*giro3b11Z[cont5-14*N][1])])
            bder2.transform = tr.rotationX(pi*giro3b12[cont5-14*N][1])
            bizq1.transform = tr.matmul([tr.rotationX(-pi*giro3b21X[cont5-14*N][1]),tr.rotationZ(pi*giro3b21Z[cont5-14*N][1])])
        
        if (cont5 >= 15*N and cont5 < 16*N) or (cont5 >= 17*N and cont5 < 18*N) or (cont5 >= 19*N and cont5 < 20*N):
            aux = cont5%N
            espalda.transform = tr.rotationY(-pi*giro4cuerpoY[aux][1])
            
            bder1.transform = tr.matmul([tr.rotationY(-pi*giro4b11Y[aux][1]),tr.rotationZ(pi*giro4b11Z[aux][1])])
            bder2.transform = tr.rotationX(pi*giro4b12[aux][1])

        if (cont5 >= 16*N and cont5 < 17*N) or (cont5 >= 18*N and cont5 < 19*N) or (cont5 >= 20*N and cont5 < 21*N):    
            aux = N-1-cont5%N
            espalda.transform = tr.rotationY(-pi*giro4cuerpoY[aux][1])
            
            bder1.transform = tr.matmul([tr.rotationY(-pi*giro4b11Y[aux][1]),tr.rotationZ(pi*giro4b11Z[aux][1])])
            bder2.transform = tr.rotationX(pi*giro4b12[aux][1])

        if cont5 >= 21*N and cont5 < 22*N:
            espalda.transform = tr.rotationY(-pi*giro3cuerpo[21*N-cont5][1])
            
            bder1.transform = tr.matmul([tr.rotationY(-pi*giro3b11Y[21*N-cont5][1]),tr.rotationZ(pi*giro3b11Z[21*N-cont5][1])])
            bder2.transform = tr.rotationX(pi*giro3b12[21*N-cont5][1])
            bizq1.transform = tr.matmul([tr.rotationX(-pi*giro3b21X[21*N-cont5][1]),tr.rotationZ(pi*giro3b21Z[21*N-cont5][1])])

        if cont5 >= 26*N: # Se reinician los contadores para las piernas y los brazos al mismo tiempo, para evitar descoordinaciones
            cont4 = 0
            cont5 = cont4
            cont1 = 0
            cont2 = cont1

        ############################################

        # Cambio en la intensidad de las luces

        intens2 += delta

        if (int(intens2) >= 0 and int(intens2) < 2) or (int(intens2) >= 4 and int(intens2) < 6):
            off = 0
            intens += 0.005
        if int(intens2) >= 2 and int(intens2) < 4:
            off = 0
            intens -= 0.004
        if int(intens2) == 10:
            off = 0
            intens2 = 0       
        if int(intens2) == 6 or int(intens2) == 8:
            off = 1
            intens = 10000
        if int(intens2) == 7 or int(intens2) == 9:
            off = 0
            intens = 1
        
        ######################################################

        # Cambio en la posicion de la camara

        controller.update_camera()

        posAuto1 = np.array([8*cos(t1),8*sin(t1),3])
        posAuto2 = np.array([0,0,0])
        posAuto3 = np.array([0,sin(0.2),cos(0.2)])
        autoMatrix = tr.lookAt(posAuto1,posAuto2,posAuto3)

        if controller.camara < 0:
            aux = abs(controller.camara)%(4*M)
            if aux < M:
                posView1 = np.array([camara4[M-1-aux][0],camara4[M-1-aux][1],camara4[M-1-aux][2]])
            if aux >= M and aux < 2*M:               
                posView1 = np.array([camara3[2*M-1-aux][0],camara3[2*M-1-aux][1],camara3[2*M-1-aux][2]])
            if aux >= 2*M and aux < 3*M:
                posView1 = np.array([camara2[3*M-1-aux][0],camara2[3*M-1-aux][1],camara2[3*M-1-aux][2]])
            if aux >= 3*M and aux < 4*M:
                posView1 = np.array([camara1[4*M-1-aux][0],camara1[4*M-1-aux][1],camara1[4*M-1-aux][2]])
        else:
            aux = (controller.camara)%(4*M)
            if aux < M:
                posView1 = np.array([camara1[aux][0],camara1[aux][1],camara1[aux][2]])
            if aux >= M and aux < 2*M:
                posView1 = np.array([camara2[aux-M][0],camara2[aux-M][1],camara2[aux-M][2]])
            if aux >= 2*M and aux < 3*M:
                posView1 = np.array([camara3[aux-2*M][0],camara3[aux-2*M][1],camara3[aux-2*M][2]])
            if aux >= 3*M and aux < 4*M:
                posView1 = np.array([camara4[aux-3*M][0],camara4[aux-3*M][1],camara4[aux-3*M][2]])

        posView2 = np.array([0,0,0])
        posView3 = np.array([0,sin(0.2),cos(0.2)])
        viewMatrix = tr.lookAt(posView1,posView2,posView3)

        ######################################################

        # Que camara se va a usar

        if controller.auto:
            Matrix = autoMatrix
        else:
            Matrix = viewMatrix  
        
        ######################################################

        # Using GLFW to check for input events
        glfw.poll_events()

        # Setting up the projection transform
        projection = tr.perspective(60, float(width) / float(height), 0.1, 200)

        # Clearing the screen in both, color and depth
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)

        ######################################################

        # Que shader se va a usar

        if controller.light:
            lightningPipeline = celTexPipeline
        else:
            lightningPipeline = phongTexPipeline
        
        glUseProgram(lightningPipeline.shaderProgram)

        ######################################################

        # Se definen parámetros distintos para cada grupo de objetos, y se dibujan respectivamente
 
        # Parámetros generales para las luces y el cielo, pues queremos que se iluminen de distinta manera

        glUniform3f(glGetUniformLocation(lightningPipeline.shaderProgram, "La"), 0.5, 0.5, 0.5)
        glUniform3f(glGetUniformLocation(lightningPipeline.shaderProgram, "Ld0"), 0.35, 0.35, 0.35)
        glUniform3f(glGetUniformLocation(lightningPipeline.shaderProgram, "Ld1"), 0.5, 0.3825, 0.0)
        glUniform3f(glGetUniformLocation(lightningPipeline.shaderProgram, "Ld2"), 0.6, 0.0, 0.0)
        glUniform3f(glGetUniformLocation(lightningPipeline.shaderProgram, "Ls0"), 0.7, 0.7, 0.7)
        glUniform3f(glGetUniformLocation(lightningPipeline.shaderProgram, "Ls1"), 1.0, 0.765, 0.0)
        glUniform3f(glGetUniformLocation(lightningPipeline.shaderProgram, "Ls2"), 1.0, 0.0, 0.0)

        glUniform3f(glGetUniformLocation(lightningPipeline.shaderProgram, "Ka"), 1.0, 1.0, 1.0)
        glUniform3f(glGetUniformLocation(lightningPipeline.shaderProgram, "Kd"), 0.1, 0.1, 0.1)
        glUniform3f(glGetUniformLocation(lightningPipeline.shaderProgram, "Ks"), 1.0, 1.0, 1.0)

        glUniform3f(glGetUniformLocation(lightningPipeline.shaderProgram, "lightPos0"), posluz0[0], posluz0[1], posluz0[2])
        glUniform3f(glGetUniformLocation(lightningPipeline.shaderProgram, "lightPos1"), posluz1[0], posluz1[1], posluz1[2])
        glUniform3f(glGetUniformLocation(lightningPipeline.shaderProgram, "lightPos2"), posluz2[0], posluz2[1], posluz2[2])
        glUniform3f(glGetUniformLocation(lightningPipeline.shaderProgram, "viewPosition"), 0, 0, 0)
        glUniform1ui(glGetUniformLocation(lightningPipeline.shaderProgram, "shininess"), off)
        
        glUniform1f(glGetUniformLocation(lightningPipeline.shaderProgram, "constantAttenuation"), 0.001)
        glUniform1f(glGetUniformLocation(lightningPipeline.shaderProgram, "linearAttenuation"), 0.015)
        glUniform1f(glGetUniformLocation(lightningPipeline.shaderProgram, "quadraticAttenuation"), 0.01)

        glUniformMatrix4fv(glGetUniformLocation(lightningPipeline.shaderProgram, "projection"), 1, GL_TRUE, projection)
        glUniformMatrix4fv(glGetUniformLocation(lightningPipeline.shaderProgram, "view"), 1, GL_TRUE, Matrix)
        glUniformMatrix4fv(glGetUniformLocation(lightningPipeline.shaderProgram, "model"), 1, GL_TRUE, tr.identity())

        sg.drawSceneGraphNode(spheres, lightningPipeline, "model")

        glUniform1ui(glGetUniformLocation(lightningPipeline.shaderProgram, "shininess"), int(intens))
        
        sg.drawSceneGraphNode(skyboxNode, lightningPipeline, "model")

        # Parámetros para el modelo

        glUniform3f(glGetUniformLocation(lightningPipeline.shaderProgram, "La"), 0.1, 0.1, 0.1)

        glUniform3f(glGetUniformLocation(lightningPipeline.shaderProgram, "Ka"), 0.5, 0.5, 0.5)
        glUniform3f(glGetUniformLocation(lightningPipeline.shaderProgram, "Kd"), 0.5, 0.5, 0.5)
        glUniform3f(glGetUniformLocation(lightningPipeline.shaderProgram, "Ks"), 0.6, 0.6, 0.6)

        sg.drawSceneGraphNode(dancer, lightningPipeline, "model")

        # Parámetros para la montaña y el suelo

        glUniform3f(glGetUniformLocation(lightningPipeline.shaderProgram, "Ka"), 0.9, 0.9, 0.9)
        glUniform3f(glGetUniformLocation(lightningPipeline.shaderProgram, "Kd"), 0.2, 0.2, 0.2)
        glUniform3f(glGetUniformLocation(lightningPipeline.shaderProgram, "Ks"), 1.0, 1.0, 1.0)

        sg.drawSceneGraphNode(mountainNode, lightningPipeline, "model")

        # Parámetros para la mesa y los árboles

        glUniform3f(glGetUniformLocation(lightningPipeline.shaderProgram, "Ka"), 0.8, 0.8, 0.8)
        glUniform3f(glGetUniformLocation(lightningPipeline.shaderProgram, "Kd"), 0.5, 0.5, 0.5)
        glUniform3f(glGetUniformLocation(lightningPipeline.shaderProgram, "Ks"), 0.7, 0.7, 0.7)

        sg.drawSceneGraphNode(tableNode, lightningPipeline, "model")
        sg.drawSceneGraphNode(bosque, lightningPipeline, "model")

        # Parámetros para la botella

        glUniform3f(glGetUniformLocation(lightningPipeline.shaderProgram, "Ka"), 0.215, 0.745, 0.215)
        glUniform3f(glGetUniformLocation(lightningPipeline.shaderProgram, "Kd"), 0.07568, 0.61424, 0.07568)
        glUniform3f(glGetUniformLocation(lightningPipeline.shaderProgram, "Ks"), 0.633, 0.727811, 0.633)

        sg.drawSceneGraphNode(botella, lightningPipeline, "model")

        
        # Once the drawing is rendered, buffers are swap so an uncomplete drawing is never seen.
        glfw.swap_buffers(window)


    glfw.terminate()