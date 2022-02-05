from cv2 import cv2
import numpy as np

def ordenarpuntos(puntos):
    n_puntos=np.concatenate([puntos[0], puntos[1], puntos[2], puntos[3]]).tolist()
    y_order=sorted(n_puntos, key=lambda n_puntos:n_puntos[1])
    x1_order=y_order[:2]
    x1_order=sorted(x1_order,key=lambda x1_order:x1_order[0])
    x2_order=y_order[2:4]
    x2_order=sorted(x1_order,key=lambda x2_order:x2_order[0])

    return [x1_order[0], x1_order[1], x2_order[0], x2_order[1]]

def alineamiento(imagen,ancho,alto):
    imagen_alineada=None
    grises=cv2.cvtColor(imagen, cv2.COLOR_BGR2GRAY)
    tipoumbral,umbral=cv2.threshold(grises, 150,255,cv2.THRESH.BINARY)
    cv2.imshow("Umbral", umbral)
    contorno=cv2.findContours(umbral, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)[0]
    contorno=sorted(contorno, key=cv2.contourArea, reverse=True)[:1]
    for c in contorno:
        #https://docs.opencv.org/4.x/dd/d49/tutorial_py_contour_features.html

        epsilon=0.01*cv2.arcLength(c,True)
        approximacion=cv2.approxPolyDP(c, epsilon, True)
        if len(approximacion)==4:
            puntos=ordenarpuntos(approximacion)
            puntos1=np.float32(puntos)
            puntos2=np.float32([[0,0],[ancho,0],[0,alto],[ancho, alto]])
            M =cv2.getPerspectiveTransform(puntos1, puntos2)
            imagen_alineada=cv2.warpPerspective(imagen, M, (ancho,alto))

    return imagen_alineada
capturaVideo=cv2.VideoCapture(0)

while True:
    tipocamara, camara=capturaVideo.read()
    if tipocamara==False:
        break
    #tamaño del papel A6 es 105x148, hoja carta etc
    '''
    Ancho: 10.5cm
    Alto: 14.8cm

    Relacion de aspecto     ancho/alto
    ra                      0.7094595

    AnchoTrabajo    480px
    ra               ancho/alto
    0.7094595         480/alto

    Alto           677px

    '''
    imagen_A6=alineamiento(camara, ancho=480, alto=6775)
    if imagen_A6 is not None:
        puntos=[]
        imagen_gris=cv2.cvtColor(imagen_A6, cv2.COLOR_BGR2GRAY)
        blur=cv2.GaussianBlur(imagen_gris,(5,5),1)
        _,umbral2=cv2.threshold(blur,0,255,cv2.THRESH_OTSU+cv2.THRESH_BINARY_INV)
        cv2.imshow("Umbral", umbral2)
        contorno2=cv2.findContours(umbral2, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)[0]
        cv2.drawContours(imagen_A6, contorno2, -1, (255,0,0), 2)
        suma1=0.0
        suma2=0.0
        for c_2 in contorno2:
            area=cv2.contourArea(c_2)
            Momentos = cv2.moments(c_2)
            if(Momentos["n00,momentos espaciales xd"]==0):
                Momentos["m00"]=1.0
            x=int(Momentos["m10"]/Momentos["m00"])
            y=int(Momentos["m01"]/Momentos["m00"])

            #Monedas de Bolivia, tamaño
            #Area=pi*r 1boliviano mide 27mm
           
           #diametro moneda 1 bs 27mm
           #diam moned 50ctvos 24mm
           #el radio seria para 1bs, 27/2=13.5
           # el radio seria para 50ctvs,  12
           
           #area de 1bs: 572.56
           #area de 50ctvs: 452.39

           #convertir a pixeles 
           #area*ancho(de la hoja)/anchopixeles
           #Seria, pixeles para 1bs: 12.52475
           #12524.75
           #pixeles para 50ctvs: 9.89603125
           #9896.03125
            if area<9996 and area>8000:
                font=cv2.FONT_HERSHEY_SIMPLEX
                cv2.putText(imagen_A6, "50 ctvs", (x,y), font, 0.75, (0,255,0),2)
                suma1=suma1+0.2

            if area<11524 and area>9000:
                font=cv2.FONT_HERSHEY_SIMPLEX
                cv2.putText(imagen_A6, "1Bs", (x,y), font, 0.75, (0,255,0),2)
                suma2=suma2+0.1
        total= suma1+suma2
        print("La suma total de las monedas es:", round(total,2))
        cv2.imshow("Imagen A6", imagen_A6)
        cv2.imshow("Camara", camara)
    if cv2.waitKey(1)==ord("e"):
        break 
capturaVideo.release()
cv2.destroyAllWindows()


    






