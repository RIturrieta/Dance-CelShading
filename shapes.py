""" Funciones para crear distintas figuras y escenas en 3D """

import numpy as np
import math
from OpenGL.GL import *
import grafica.basic_shapes as bs
import grafica.easy_shaders as es
import grafica.transformations as tr
import grafica.scene_graph as sg



#########################################################################

def createGPUShape(pipeline, shape):
    gpuShape = es.GPUShape().initBuffers()
    pipeline.setupVAO(gpuShape)
    gpuShape.fillBuffers(shape.vertices, shape.indices, GL_STATIC_DRAW)
    return gpuShape

def createTextureGPUShape(shape, pipeline, path):
    # Funcion Conveniente para facilitar la inicializacion de un GPUShape con texturas
    gpuShape = es.GPUShape().initBuffers()
    pipeline.setupVAO(gpuShape)
    gpuShape.fillBuffers(shape.vertices, shape.indices, GL_STATIC_DRAW)
    gpuShape.texture = es.textureSimpleSetup(
        path, GL_CLAMP_TO_EDGE, GL_CLAMP_TO_EDGE, GL_NEAREST, GL_NEAREST)
    return gpuShape

#########################################################################
# La misma función, pero con GL_REPEAT

def createTextureGPUShapeR(shape, pipeline, path):
    # Funcion Conveniente para facilitar la inicializacion de un GPUShape con texturas
    gpuShape = es.GPUShape().initBuffers()
    pipeline.setupVAO(gpuShape)
    gpuShape.fillBuffers(shape.vertices, shape.indices, GL_STATIC_DRAW)
    gpuShape.texture = es.textureSimpleSetup(
        path, GL_REPEAT, GL_REPEAT, GL_NEAREST, GL_NEAREST)
    return gpuShape    

#########################################################################

def createScene(pipeline):

    gpuRedCube = createGPUShape(pipeline, bs.createColorNormalsCube(1, 0, 0))
    gpuGreenCube = createGPUShape(pipeline, bs.createColorNormalsCube(0, 1, 0))
    gpuGrayCube = createGPUShape(pipeline, bs.createColorNormalsCube(0.7, 0.7, 0.7))
    gpuWhiteCube = createGPUShape(pipeline, bs.createColorNormalsCube(1, 1, 1))

    redCubeNode = sg.SceneGraphNode("redCube")
    redCubeNode.childs = [gpuRedCube]

    greenCubeNode = sg.SceneGraphNode("greenCube")
    greenCubeNode.childs = [gpuGreenCube]

    grayCubeNode = sg.SceneGraphNode("grayCube")
    grayCubeNode.childs = [gpuGrayCube]

    whiteCubeNode = sg.SceneGraphNode("whiteCube")
    whiteCubeNode.childs = [gpuWhiteCube]

    rightWallNode = sg.SceneGraphNode("rightWall")
    rightWallNode.transform = tr.translate(1, 0, 0)
    rightWallNode.childs = [redCubeNode]

    leftWallNode = sg.SceneGraphNode("leftWall")
    leftWallNode.transform = tr.translate(-1, 0, 0)
    leftWallNode.childs = [greenCubeNode]

    backWallNode = sg.SceneGraphNode("backWall")
    backWallNode.transform = tr.translate(0,-1, 0)
    backWallNode.childs = [grayCubeNode]

    lightNode = sg.SceneGraphNode("lightSource")
    lightNode.transform = tr.matmul([tr.translate(0, 0, -0.4), tr.scale(0.12, 0.12, 0.12)])
    lightNode.childs = [grayCubeNode]

    ceilNode = sg.SceneGraphNode("ceil")
    ceilNode.transform = tr.translate(0, 0, 1)
    ceilNode.childs = [grayCubeNode, lightNode]

    floorNode = sg.SceneGraphNode("floor")
    floorNode.transform = tr.translate(0, 0, -1)
    floorNode.childs = [grayCubeNode]

    sceneNode = sg.SceneGraphNode("scene")
    sceneNode.transform = tr.matmul([tr.translate(0, 0, 0), tr.scale(5, 5, 5)])
    sceneNode.childs = [rightWallNode, leftWallNode, backWallNode, ceilNode, floorNode]

    trSceneNode = sg.SceneGraphNode("tr_scene")
    trSceneNode.childs = [sceneNode]

    return trSceneNode

#########################################################################

def createSkybox():

    # Defining locations,texture coordinates and normals for each vertex of the shape  
    vertices = [
    #   positions            tex coords   normals
    # Z+
        -0.5, -0.5,  0.5,    0, 1,        0,0,1,
        0.5, -0.5,  0.5,    1, 1,        0,0,1,
        0.5,  0.5,  0.5,    1, 0,        0,0,1,
        -0.5,  0.5,  0.5,    0, 0,        0,0,1,   
    # Z-          
        -0.5, -0.5, -0.5,    0, 1,        0,0,-1,
        0.5, -0.5, -0.5,    1, 1,        0,0,-1,
        0.5,  0.5, -0.5,    1, 0,        0,0,-1,
        -0.5,  0.5, -0.5,    0, 0,        0,0,-1,
    
    # X+          
        0.5, -0.5, -0.5,    0, 1,        1,0,0,
        0.5,  0.5, -0.5,    1, 1,        1,0,0,
        0.5,  0.5,  0.5,    1, 0,        1,0,0,
        0.5, -0.5,  0.5,    0, 0,        1,0,0,   
    # X-          
        -0.5, -0.5, -0.5,    1, 0,        -1,0,0,
        -0.5,  0.5, -0.5,    0, 0,        -1,0,0,
        -0.5,  0.5,  0.5,    0, 1,        -1,0,0,
        -0.5, -0.5,  0.5,    1, 1,        -1,0,0,   
    # Y+          
        -0.5,  0.5, -0.5,    0, 0,        0,1,0,
        0.5,  0.5, -0.5,    0, 1,        0,1,0,
        0.5,  0.5,  0.5,    1, 1,        0,1,0,
        -0.5,  0.5,  0.5,    1, 0,        0,1,0,   
    # Y-          
        -0.5, -0.5, -0.5,    1, 1,        0,-1,0,
        0.5, -0.5, -0.5,    1, 0,        0,-1,0,
        0.5, -0.5,  0.5,    0, 0,        0,-1,0,
        -0.5, -0.5,  0.5,    0, 1,        0,-1,0
        ]   

    # Defining connections among vertices
    # We have a triangle every 3 indices specified
    indices = [
        0, 1, 2, 2, 3, 0, # Z+
        7, 6, 5, 5, 4, 7, # Z-
        8, 9,10,10,11, 8, # X+
        15,14,13,13,12,15, # X-
        19,18,17,17,16,19, # Y+
        20,21,22,22,23,20] # Y-

    return bs.Shape(vertices, indices)

#########################################################################

# Funciones y curvas usadas en el programa

def catmullMatrix(P0, P1, P2, P3):

    # Generate a matrix concatenating the columns
    G = np.concatenate((P0, P1, P2, P3), axis=1)
    
    # La matriz base de Catmull-rom es constante
    Mc = np.array([[0, -0.5, 1, -0.5], [1, 0, -2.5, 1.5], [0, 0.5, 2, -1.5], [0, 0, -0.5, 0.5]])    
    
    return np.matmul(G, Mc)

def generateT(t):
    return np.array([[1, t, t**2, t**3]]).T

def catmull1(N): 
    # Puntos de Control
    
    P0 = np.array([[1.5, -1.0, 0.0]]).T
    P1 = np.array([[0.0, 0.5, 0.0]]).T
    P2 = np.array([[1.0, 0.5, 0.0]]).T
    P3 = np.array([[0.0, 0.4, 0.0]]).T
    
    # Matriz de Catmull-rom
    C_M = catmullMatrix(P0, P1, P2, P3)

    # Arreglo de numeros entre 0 y 1
    ts = np.linspace(0.0, 1.0, N)
    
    # The computed value in R3 for each sample will be stored here
    curve = np.ndarray(shape=(len(ts), 3), dtype=float)
    
    # Se llenan los puntos de la curva
    for i in range(len(ts)):
        T = generateT(ts[i])
        curve[i, 0:3] = np.matmul(C_M, T).T

    return curve

def catmull2(N): 
    # Puntos de Control
    
    P0 = np.array([[1.0, 0.4, 0.0]]).T
    P1 = np.array([[0.0, 0.5, 0.0]]).T
    P2 = np.array([[1.0, 0.5, 0.0]]).T
    P3 = np.array([[-0.5,-1.0, 0.0]]).T
    
    # Matriz de Catmull-rom
    C_M = catmullMatrix(P0, P1, P2, P3)

    # Arreglo de numeros entre 0 y 1
    ts = np.linspace(0.0, 1.0, N)
    
    # The computed value in R3 for each sample will be stored here
    curve = np.ndarray(shape=(len(ts), 3), dtype=float)
    
    # Se llenan los puntos de la curva
    for i in range(len(ts)):
        T = generateT(ts[i])
        curve[i, 0:3] = np.matmul(C_M, T).T

    return curve

def catmull3(N): 
    # Puntos de Control
    
    P0 = np.array([[0.5, -1.0, 0.0]]).T
    P1 = np.array([[0.0, 0.0, 0.0]]).T
    P2 = np.array([[1.0, 0.7, 0.0]]).T
    P3 = np.array([[6.0, 0.7, 0.0]]).T
    
    # Matriz de Catmull-rom
    C_M = catmullMatrix(P0, P1, P2, P3)

    # Arreglo de numeros entre 0 y 1
    ts = np.linspace(0.0, 1.0, N)
    
    # The computed value in R3 for each sample will be stored here
    curve = np.ndarray(shape=(len(ts), 3), dtype=float)
    
    # Se llenan los puntos de la curva
    for i in range(len(ts)):
        T = generateT(ts[i])
        curve[i, 0:3] = np.matmul(C_M, T).T

    return curve

def catmull4(N): 
    # Puntos de Control
    
    P0 = np.array([[-5.0, 0.7, 0.0]]).T
    P1 = np.array([[0.0, 0.7, 0.0]]).T
    P2 = np.array([[1.0, 0.0, 0.0]]).T
    P3 = np.array([[0.5, -1.0, 0.0]]).T
    
    # Matriz de Catmull-rom
    C_M = catmullMatrix(P0, P1, P2, P3)

    # Arreglo de numeros entre 0 y 1
    ts = np.linspace(0.0, 1.0, N)
    
    # The computed value in R3 for each sample will be stored here
    curve = np.ndarray(shape=(len(ts), 3), dtype=float)
    
    # Se llenan los puntos de la curva
    for i in range(len(ts)):
        T = generateT(ts[i])
        curve[i, 0:3] = np.matmul(C_M, T).T

    return curve

def catmull5(N): 
    # Puntos de Control
    
    P0 = np.array([[-0.5, -0.5, 0.0]]).T
    P1 = np.array([[-0.5, 0.0, 0.0]]).T
    P2 = np.array([[0.5, 0.1, 0.0]]).T
    P3 = np.array([[1.0, 0.1, 0.0]]).T
    
    # Matriz de Catmull-rom
    C_M = catmullMatrix(P0, P1, P2, P3)

    # Arreglo de numeros entre 0 y 1
    ts = np.linspace(0.0, 1.0, N)
    
    # The computed value in R3 for each sample will be stored here
    curve = np.ndarray(shape=(len(ts), 3), dtype=float)
    
    # Se llenan los puntos de la curva
    for i in range(len(ts)):
        T = generateT(ts[i])
        curve[i, 0:3] = np.matmul(C_M, T).T

    return curve

def catmull6(N): 
    # Puntos de Control
    
    P0 = np.array([[-0.5, -0.5, 0.0]]).T
    P1 = np.array([[-0.5, 0.55, 0.0]]).T
    P2 = np.array([[0.5, -0.5, 0.0]]).T
    P3 = np.array([[0.5, -5.0, 0.0]]).T
    
    # Matriz de Catmull-rom
    C_M = catmullMatrix(P0, P1, P2, P3)

    # Arreglo de numeros entre 0 y 1
    ts = np.linspace(0.0, 1.0, N)
    
    # The computed value in R3 for each sample will be stored here
    curve = np.ndarray(shape=(len(ts), 3), dtype=float)
    
    # Se llenan los puntos de la curva
    for i in range(len(ts)):
        T = generateT(ts[i])
        curve[i, 0:3] = np.matmul(C_M, T).T

    return curve

def catmull7(N): 
    # Puntos de Control
    
    P0 = np.array([[-1.0, 0.5, 0.0]]).T
    P1 = np.array([[-0.5, 0.5, 0.0]]).T
    P2 = np.array([[0.5, 0.0, 0.0]]).T
    P3 = np.array([[0.5, -1.0, 0.0]]).T
    
    # Matriz de Catmull-rom
    C_M = catmullMatrix(P0, P1, P2, P3)

    # Arreglo de numeros entre 0 y 1
    ts = np.linspace(0.0, 1.0, N)
    
    # The computed value in R3 for each sample will be stored here
    curve = np.ndarray(shape=(len(ts), 3), dtype=float)
    
    # Se llenan los puntos de la curva
    for i in range(len(ts)):
        T = generateT(ts[i])
        curve[i, 0:3] = np.matmul(C_M, T).T

    return curve

def catmull8(N): 
    # Puntos de Control
    
    P0 = np.array([[-2.0, 0.0, 0.0]]).T
    P1 = np.array([[-0.5, 0.45, 0.0]]).T
    P2 = np.array([[0.5, 0.0, 0.0]]).T
    P3 = np.array([[0.5, -1.2, 0.0]]).T
    
    # Matriz de Catmull-rom
    C_M = catmullMatrix(P0, P1, P2, P3)

    # Arreglo de numeros entre 0 y 1
    ts = np.linspace(0.0, 1.0, N)
    
    # The computed value in R3 for each sample will be stored here
    curve = np.ndarray(shape=(len(ts), 3), dtype=float)
    
    # Se llenan los puntos de la curva
    for i in range(len(ts)):
        T = generateT(ts[i])
        curve[i, 0:3] = np.matmul(C_M, T).T

    return curve

def catmull9(N): 
    # Puntos de Control
    
    P0 = np.array([[-0.5, -0.5, 0.0]]).T
    P1 = np.array([[-0.5, 0.1, 0.0]]).T
    P2 = np.array([[0.5, -0.1, 0.0]]).T
    P3 = np.array([[0.5, 0.5, 0.0]]).T
    
    # Matriz de Catmull-rom
    C_M = catmullMatrix(P0, P1, P2, P3)

    # Arreglo de numeros entre 0 y 1
    ts = np.linspace(0.0, 1.0, N)
    
    # The computed value in R3 for each sample will be stored here
    curve = np.ndarray(shape=(len(ts), 3), dtype=float)
    
    # Se llenan los puntos de la curva
    for i in range(len(ts)):
        T = generateT(ts[i])
        curve[i, 0:3] = np.matmul(C_M, T).T

    return curve

def catmull10(N): 
    # Puntos de Control
    
    P0 = np.array([[-0.5, -2.0, 0.0]]).T
    P1 = np.array([[-0.5,-0.35, 0.0]]).T
    P2 = np.array([[0.5, 0.0, 0.0]]).T
    P3 = np.array([[2.0, 0.0, 0.0]]).T
    
    # Matriz de Catmull-rom
    C_M = catmullMatrix(P0, P1, P2, P3)

    # Arreglo de numeros entre 0 y 1
    ts = np.linspace(0.0, 1.0, N)
    
    # The computed value in R3 for each sample will be stored here
    curve = np.ndarray(shape=(len(ts), 3), dtype=float)
    
    # Se llenan los puntos de la curva
    for i in range(len(ts)):
        T = generateT(ts[i])
        curve[i, 0:3] = np.matmul(C_M, T).T

    return curve

def catmull11(N): 
    # Puntos de Control
    
    P0 = np.array([[-2.0, 0.0, 0.0]]).T
    P1 = np.array([[-0.5, 0.0, 0.0]]).T
    P2 = np.array([[0.5, -0.35, 0.0]]).T
    P3 = np.array([[0.5, -2.0, 0.0]]).T
    
    # Matriz de Catmull-rom
    C_M = catmullMatrix(P0, P1, P2, P3)

    # Arreglo de numeros entre 0 y 1
    ts = np.linspace(0.0, 1.0, N)
    
    # The computed value in R3 for each sample will be stored here
    curve = np.ndarray(shape=(len(ts), 3), dtype=float)
    
    # Se llenan los puntos de la curva
    for i in range(len(ts)):
        T = generateT(ts[i])
        curve[i, 0:3] = np.matmul(C_M, T).T

    return curve

def catmull12(N): 
    # Puntos de Control
    
    P0 = np.array([[-2.0, 0.2, 0.0]]).T
    P1 = np.array([[-0.5, 0.0, 0.0]]).T
    P2 = np.array([[0.5, 0.1, 0.0]]).T
    P3 = np.array([[2.0, 0.0, 0.0]]).T
    
    # Matriz de Catmull-rom
    C_M = catmullMatrix(P0, P1, P2, P3)

    # Arreglo de numeros entre 0 y 1
    ts = np.linspace(0.0, 1.0, N)
    
    # The computed value in R3 for each sample will be stored here
    curve = np.ndarray(shape=(len(ts), 3), dtype=float)
    
    # Se llenan los puntos de la curva
    for i in range(len(ts)):
        T = generateT(ts[i])
        curve[i, 0:3] = np.matmul(C_M, T).T

    return curve

def catmull13(N): 
    # Puntos de Control
    
    P0 = np.array([[-1.0, 0.0, 0.0]]).T
    P1 = np.array([[-0.5, 0.0, 0.0]]).T
    P2 = np.array([[0.5, 0.6, 0.0]]).T
    P3 = np.array([[0.5, 3.5, 0.0]]).T
    
    # Matriz de Catmull-rom
    C_M = catmullMatrix(P0, P1, P2, P3)

    # Arreglo de numeros entre 0 y 1
    ts = np.linspace(0.0, 1.0, N)
    
    # The computed value in R3 for each sample will be stored here
    curve = np.ndarray(shape=(len(ts), 3), dtype=float)
    
    # Se llenan los puntos de la curva
    for i in range(len(ts)):
        T = generateT(ts[i])
        curve[i, 0:3] = np.matmul(C_M, T).T

    return curve

def catmull14(N): 
    # Puntos de Control
    
    P0 = np.array([[-0.5, 1.0, 0.0]]).T
    P1 = np.array([[-0.5, 0.55, 0.0]]).T
    P2 = np.array([[0.5, 0.6, 0.0]]).T
    P3 = np.array([[0.5, 3.5, 0.0]]).T
    
    # Matriz de Catmull-rom
    C_M = catmullMatrix(P0, P1, P2, P3)

    # Arreglo de numeros entre 0 y 1
    ts = np.linspace(0.0, 1.0, N)
    
    # The computed value in R3 for each sample will be stored here
    curve = np.ndarray(shape=(len(ts), 3), dtype=float)
    
    # Se llenan los puntos de la curva
    for i in range(len(ts)):
        T = generateT(ts[i])
        curve[i, 0:3] = np.matmul(C_M, T).T

    return curve

def catmull15(N): 
    # Puntos de Control
    
    P0 = np.array([[-0.5, 1.5, 0.0]]).T
    P1 = np.array([[-0.5, 0.5, 0.0]]).T
    P2 = np.array([[0.5, 0.1, 0.0]]).T
    P3 = np.array([[0.5, -0.5, 0.0]]).T
    
    # Matriz de Catmull-rom
    C_M = catmullMatrix(P0, P1, P2, P3)

    # Arreglo de numeros entre 0 y 1
    ts = np.linspace(0.0, 1.0, N)
    
    # The computed value in R3 for each sample will be stored here
    curve = np.ndarray(shape=(len(ts), 3), dtype=float)
    
    # Se llenan los puntos de la curva
    for i in range(len(ts)):
        T = generateT(ts[i])
        curve[i, 0:3] = np.matmul(C_M, T).T

    return curve

def catmull16(N): 
    # Puntos de Control
    
    P0 = np.array([[-0.5, 0.5, 0.0]]).T
    P1 = np.array([[-0.5, 0.0, 0.0]]).T
    P2 = np.array([[0.5, -0.25, 0.0]]).T
    P3 = np.array([[0.5, -0.5, 0.0]]).T
    
    # Matriz de Catmull-rom
    C_M = catmullMatrix(P0, P1, P2, P3)

    # Arreglo de numeros entre 0 y 1
    ts = np.linspace(0.0, 1.0, N)
    
    # The computed value in R3 for each sample will be stored here
    curve = np.ndarray(shape=(len(ts), 3), dtype=float)
    
    # Se llenan los puntos de la curva
    for i in range(len(ts)):
        T = generateT(ts[i])
        curve[i, 0:3] = np.matmul(C_M, T).T

    return curve

def catmull17(N): 
    # Puntos de Control
    
    P0 = np.array([[-0.5, 1.0, 0.0]]).T
    P1 = np.array([[-0.5, 0.5, 0.0]]).T
    P2 = np.array([[0.5, 0.0, 0.0]]).T
    P3 = np.array([[0.5, -0.5, 0.0]]).T
    
    # Matriz de Catmull-rom
    C_M = catmullMatrix(P0, P1, P2, P3)

    # Arreglo de numeros entre 0 y 1
    ts = np.linspace(0.0, 1.0, N)
    
    # The computed value in R3 for each sample will be stored here
    curve = np.ndarray(shape=(len(ts), 3), dtype=float)
    
    # Se llenan los puntos de la curva
    for i in range(len(ts)):
        T = generateT(ts[i])
        curve[i, 0:3] = np.matmul(C_M, T).T

    return curve

def catmull18(N): 
    # Puntos de Control
    
    P0 = np.array([[-1.0, 0.0, 0.0]]).T
    P1 = np.array([[-0.5, 0.6, 0.0]]).T
    P2 = np.array([[0.5, -0.1, 0.0]]).T
    P3 = np.array([[2.0, 0.5, 0.0]]).T
    
    # Matriz de Catmull-rom
    C_M = catmullMatrix(P0, P1, P2, P3)

    # Arreglo de numeros entre 0 y 1
    ts = np.linspace(0.0, 1.0, N)
    
    # The computed value in R3 for each sample will be stored here
    curve = np.ndarray(shape=(len(ts), 3), dtype=float)
    
    # Se llenan los puntos de la curva
    for i in range(len(ts)):
        T = generateT(ts[i])
        curve[i, 0:3] = np.matmul(C_M, T).T

    return curve

def catmull19(N): 
    # Puntos de Control
    
    P0 = np.array([[-1.0, 0.25, 0.0]]).T
    P1 = np.array([[-0.5, 0.6, 0.0]]).T
    P2 = np.array([[0.5, 0.25 , 0.0]]).T
    P3 = np.array([[1.0, 0.5, 0.0]]).T
    
    # Matriz de Catmull-rom
    C_M = catmullMatrix(P0, P1, P2, P3)

    # Arreglo de numeros entre 0 y 1
    ts = np.linspace(0.0, 1.0, N)
    
    # The computed value in R3 for each sample will be stored here
    curve = np.ndarray(shape=(len(ts), 3), dtype=float)
    
    # Se llenan los puntos de la curva
    for i in range(len(ts)):
        T = generateT(ts[i])
        curve[i, 0:3] = np.matmul(C_M, T).T

    return curve

def catmull20(N): 
    # Puntos de Control
    
    P0 = np.array([[-2.5, 0.7, 0.0]]).T
    P1 = np.array([[-0.5, 0.1, 0.0]]).T
    P2 = np.array([[0.5, 0.6 , 0.0]]).T
    P3 = np.array([[1.5, 0.2, 0.0]]).T
    
    # Matriz de Catmull-rom
    C_M = catmullMatrix(P0, P1, P2, P3)

    # Arreglo de numeros entre 0 y 1
    ts = np.linspace(0.0, 1.0, N)
    
    # The computed value in R3 for each sample will be stored here
    curve = np.ndarray(shape=(len(ts), 3), dtype=float)
    
    # Se llenan los puntos de la curva
    for i in range(len(ts)):
        T = generateT(ts[i])
        curve[i, 0:3] = np.matmul(C_M, T).T

    return curve

def catmull21(N): 
    # Puntos de Control
    
    P0 = np.array([[-2.0, 0.1, 0.0]]).T
    P1 = np.array([[-0.5, 0.1, 0.0]]).T
    P2 = np.array([[0.5, -0.1 , 0.0]]).T
    P3 = np.array([[2.0, -0.1, 0.0]]).T
    
    # Matriz de Catmull-rom
    C_M = catmullMatrix(P0, P1, P2, P3)

    # Arreglo de numeros entre 0 y 1
    ts = np.linspace(0.0, 1.0, N)
    
    # The computed value in R3 for each sample will be stored here
    curve = np.ndarray(shape=(len(ts), 3), dtype=float)
    
    # Se llenan los puntos de la curva
    for i in range(len(ts)):
        T = generateT(ts[i])
        curve[i, 0:3] = np.matmul(C_M, T).T

    return curve

def catmull22(N): 
    # Puntos de Control
    
    P0 = np.array([[-2.5, 2.0, 0.0]]).T
    P1 = np.array([[-0.5, 0.0, 0.0]]).T
    P2 = np.array([[0.5, 0.0 , 0.0]]).T
    P3 = np.array([[2.0, -6.0, 0.0]]).T
    
    # Matriz de Catmull-rom
    C_M = catmullMatrix(P0, P1, P2, P3)

    # Arreglo de numeros entre 0 y 1
    ts = np.linspace(0.0, 1.0, N)
    
    # The computed value in R3 for each sample will be stored here
    curve = np.ndarray(shape=(len(ts), 3), dtype=float)
    
    # Se llenan los puntos de la curva
    for i in range(len(ts)):
        T = generateT(ts[i])
        curve[i, 0:3] = np.matmul(C_M, T).T

    return curve
    
def catmull23(N): 
    # Puntos de Control
    
    P0 = np.array([[-0.5, 1.0, 0.0]]).T
    P1 = np.array([[-0.5, 0.0, 0.0]]).T
    P2 = np.array([[0.5, 0.0 , 0.0]]).T
    P3 = np.array([[2.0, -6.0, 0.0]]).T
    
    # Matriz de Catmull-rom
    C_M = catmullMatrix(P0, P1, P2, P3)

    # Arreglo de numeros entre 0 y 1
    ts = np.linspace(0.0, 1.0, N)
    
    # The computed value in R3 for each sample will be stored here
    curve = np.ndarray(shape=(len(ts), 3), dtype=float)
    
    # Se llenan los puntos de la curva
    for i in range(len(ts)):
        T = generateT(ts[i])
        curve[i, 0:3] = np.matmul(C_M, T).T

    return curve

def catmull24(N): 
    # Puntos de Control
    
    P0 = np.array([[-0.5, -2.0, 0.0]]).T
    P1 = np.array([[-0.5, 0.0, 0.0]]).T
    P2 = np.array([[0.5, 0.0 , 0.0]]).T
    P3 = np.array([[0.5, 2.0, 0.0]]).T
    
    # Matriz de Catmull-rom
    C_M = catmullMatrix(P0, P1, P2, P3)

    # Arreglo de numeros entre 0 y 1
    ts = np.linspace(0.0, 1.0, N)
    
    # The computed value in R3 for each sample will be stored here
    curve = np.ndarray(shape=(len(ts), 3), dtype=float)
    
    # Se llenan los puntos de la curva
    for i in range(len(ts)):
        T = generateT(ts[i])
        curve[i, 0:3] = np.matmul(C_M, T).T

    return curve

def catmull25(N): 
    # Puntos de Control
    
    P0 = np.array([[12.5, -1.0, 0.0]]).T
    P1 = np.array([[-3.0, 7.5, -2.5]]).T
    P2 = np.array([[-12.5, 0.0 , 0.0]]).T
    P3 = np.array([[2.0, -15.5, 2.5]]).T
    
    # Matriz de Catmull-rom
    C_M = catmullMatrix(P0, P1, P2, P3)

    # Arreglo de numeros entre 0 y 1
    ts = np.linspace(0.0, 1.0, N)
    
    # The computed value in R3 for each sample will be stored here
    curve = np.ndarray(shape=(len(ts), 3), dtype=float)
    
    # Se llenan los puntos de la curva
    for i in range(len(ts)):
        T = generateT(ts[i])
        curve[i, 0:3] = np.matmul(C_M, T).T

    return curve

def catmull26(N): 
    # Puntos de Control
    
    P0 = np.array([[-3.0, 7.5, -2.5]]).T
    P1 = np.array([[-12.5, 0.0 , 0.0]]).T
    P2 = np.array([[2.0, -15.5, 2.5]]).T
    P3 = np.array([[12.5, -1.0, 0.0]]).T
    
    # Matriz de Catmull-rom
    C_M = catmullMatrix(P0, P1, P2, P3)

    # Arreglo de numeros entre 0 y 1
    ts = np.linspace(0.0, 1.0, N)
    
    # The computed value in R3 for each sample will be stored here
    curve = np.ndarray(shape=(len(ts), 3), dtype=float)
    
    # Se llenan los puntos de la curva
    for i in range(len(ts)):
        T = generateT(ts[i])
        curve[i, 0:3] = np.matmul(C_M, T).T

    return curve

def catmull27(N): 
    # Puntos de Control
    
    P0 = np.array([[-12.5, 0.0 , 0.0]]).T
    P1 = np.array([[2.0, -15.5, 2.5]]).T
    P2 = np.array([[12.5, -1.0, 0.0]]).T
    P3 = np.array([[-3.0, 7.5, -2.5]]).T
    
    # Matriz de Catmull-rom
    C_M = catmullMatrix(P0, P1, P2, P3)

    # Arreglo de numeros entre 0 y 1
    ts = np.linspace(0.0, 1.0, N)
    
    # The computed value in R3 for each sample will be stored here
    curve = np.ndarray(shape=(len(ts), 3), dtype=float)
    
    # Se llenan los puntos de la curva
    for i in range(len(ts)):
        T = generateT(ts[i])
        curve[i, 0:3] = np.matmul(C_M, T).T

    return curve

def catmull28(N): 
    # Puntos de Control
    
    P0 = np.array([[2.0, -15.5, 2.5]]).T
    P1 = np.array([[12.5, -1.0, 0.0]]).T
    P2 = np.array([[-3.0, 7.5, -2.5]]).T
    P3 = np.array([[-12.5, 0.0 , 0.0]]).T
    
    # Matriz de Catmull-rom
    C_M = catmullMatrix(P0, P1, P2, P3)

    # Arreglo de numeros entre 0 y 1
    ts = np.linspace(0.0, 1.0, N)
    
    # The computed value in R3 for each sample will be stored here
    curve = np.ndarray(shape=(len(ts), 3), dtype=float)
    
    # Se llenan los puntos de la curva
    for i in range(len(ts)):
        T = generateT(ts[i])
        curve[i, 0:3] = np.matmul(C_M, T).T

    return curve

def catmull29(N): 
    # Puntos de Control
    
    P0 = np.array([[-3.0, 0.0, 0.0]]).T
    P1 = np.array([[-0.5, 0.2, 0.0]]).T
    P2 = np.array([[0.5, 0.0, 0.0]]).T
    P3 = np.array([[1.0, 0.2 , 0.0]]).T
    
    # Matriz de Catmull-rom
    C_M = catmullMatrix(P0, P1, P2, P3)

    # Arreglo de numeros entre 0 y 1
    ts = np.linspace(0.0, 1.0, N)
    
    # The computed value in R3 for each sample will be stored here
    curve = np.ndarray(shape=(len(ts), 3), dtype=float)
    
    # Se llenan los puntos de la curva
    for i in range(len(ts)):
        T = generateT(ts[i])
        curve[i, 0:3] = np.matmul(C_M, T).T

    return curve
