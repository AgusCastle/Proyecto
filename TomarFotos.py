import cv2

def TomarFotografia():
    CamaraFotos = cv2.VideoCapture(0)
    #cv2.namedWindow("Camara")
    img_counter = 0

    while True:
        success, frame = CamaraFotos.read()
        if not success:
            print("No se detecta ninguna camara")
            break
        cv2.imshow('Tomar Fotografia', frame)

        k = cv2.waitKey(1)

        if k%256 == 27: #Cuando se presiona ESC se cierra la ventana
            break

        elif k%256 == 32: #Cuando se presiona espacio se toma una fotografia
            img_name = "Imagen_{}.jpg".format(img_counter)
            cv2.imwrite(img_name, frame)
            img_counter += 1

    CamaraFotos.release()
    cv2.destroyWindow('Tomar Fotografia')

#TomarFotografia()