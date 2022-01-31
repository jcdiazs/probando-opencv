import cv2 as cv
capturarVideo=cv.VideoCapture(0)
if not capturarVideo.isOpened():
    print("No se encontro una camara :c")
    exit()
while True:
    tipocamara, camara=capturarVideo.read()
#probando filtros xd
    grises=cv.cvtColor(camara, cv.COLOR_RGB2BGRA)

    cv.imshow("En vivo desde la camara :o", grises)
    if cv.waitKey(1)==ord("e"):
        break
capturarVideo.release()
cv.destroyAllWindows()
    

