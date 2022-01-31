from cv2 import GaussianBlur, cv2
import  numpy as np
#se saca la imagen o no la reconoce

original=cv2.imread('monedas.jpg')
#original=cv2.imread('monedasPrueba3.jpg')
gris=cv2.cvtColor(original,cv2.COLOR_BGR2GRAY)

#valor de la matriz, siempre impares, con pares no me funciono

valorGauss=3
valorKernel=3
#usar suavizado con gauss, desenfoque
gauss=cv2.GaussianBlur(gris,(valorGauss, valorGauss),0 )
#segunda alineacion de ruidos con canny
canny=cv2.Canny(gauss, 60,100)

#matriz kernel de 3x3 de 8 bits de valor 
kernel=np.ones((valorKernel, valorKernel), np.uint8)
#https://docs.opencv.org/3.4/d9/d61/tutorial_py_morphological_ops.html
#uso el 4 para eliminar el ruido interior
cierre=cv2.morphologyEx(canny,cv2.MORPH_CLOSE,kernel )

contornos, jerarquia=cv2.findContours(cierre.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
print("Las cantidad de monedas que hay es de: {}".format(len(contornos)))
cv2.drawContours(original, contornos,-1, (0,0, 244), 2 )

#mostrar el res
'''
cv2.imshow('Grises',gris)
cv2.imshow('Grises con gauss',gauss)
cv2.imshow('Grises con canny',canny)'''
cv2.imshow('Cierre',cierre)
cv2.imshow('resultado', original) 
cv2.waitKey(0)


