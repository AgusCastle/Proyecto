import cv2
import numpy
import face_recognition
import os
from CrearLista import NombreArchivo
from datetime import datetime

NombreArc = NombreArchivo()

img_counter = 0
path = 'Rostros' #Ruta de donde estan las imagenes
Imagenes = []
ListaNombres = []
Lista = os.listdir(path)
#print(Lista) #Imprime los nombre que se encuentan en la imagenes junto con la extencion del archivo

def ReconocimientoSalida():

	for cl in Lista:
		ImagenActual = cv2.imread(f'{path}/{cl}')
		Imagenes.append(ImagenActual)
		ListaNombres.append(os.path.splitext(cl)[0])
	print(ListaNombres) #Imprime los nombres de la imagenes sin la extension

	def EncontrarRostrosGuardados(Imagenes): #Funcion para detectar las imagenes guardadas en la carpeta de Imagenes
		ListaRostrosEncontrados = []
		for Img in Imagenes:
			Img = cv2.cvtColor(Img, cv2.COLOR_BGR2RGB) #Combiar los colores a RGB
			Encode = face_recognition.face_encodings(Img)[0]
			ListaRostrosEncontrados.append(Encode)
		return ListaRostrosEncontrados

	def ListaAsistencia(Nombre):
		with open ('{}.csv'.format(NombreArc),'r+') as f:
			ListaDeAsistenciaSalida = f.readlines()
			ListaNombreAsistenciaSalida = []
			for line in ListaDeAsistenciaSalida:
				Entrada = line.split(',')
				ListaNombreAsistenciaSalida.append(Entrada[0])
			#if Nombre not in ListaNombreAsistenciaSalida:
			Acceso = datetime.now()
			Fecha = Acceso.strftime('%d-%m-%Y')
			Hora = Acceso.strftime('%H:%M:%S')
			TipoAcceso = "Salida"
			f.writelines(f'\n{Nombre},{Fecha},{Hora},{TipoAcceso}')


	ListaRostrosConocidos = EncontrarRostrosGuardados(Imagenes) 
	#print("Codificacion Completada.")

	CamaraSalida = cv2.VideoCapture(1) #Iniciamos la camara de entrada

	CamaraSalida.set(3,700) #Ajustamos el ancho que se va a mostrar de la camara
	CamaraSalida.set(4,500) #Ajustamos el alto que se va a mostrar de la camara


	
	while True:

		if not CamaraSalida:
			print ("No se detecta ninguna camara")
			break

		success, Img = CamaraSalida.read()
		ImgSmall = cv2.resize(Img,(0,0),None,0.25,0.25) #Reducimos el tamaño de la imagen de entrada para acelerar el proceso
		ImgSmall = cv2.cvtColor(ImgSmall, cv2.COLOR_BGR2RGB)

		RostrosTransmitidos = face_recognition.face_locations(ImgSmall)
		EncodeTransmitidos = face_recognition.face_encodings(ImgSmall,RostrosTransmitidos)

		for EncodeRostro, LocRostros in zip(EncodeTransmitidos,RostrosTransmitidos):
			Emparejamiento = face_recognition.compare_faces(ListaRostrosConocidos, EncodeRostro)
			Distancia_Rostro = face_recognition.face_distance(ListaRostrosConocidos, EncodeRostro)
			#print(Distancia_Rostro)
			MatchIndex = numpy.argmin(Distancia_Rostro)

			if Emparejamiento[MatchIndex]:
				Nombre = ListaNombres[MatchIndex].upper()
				#print(Nombre)
				y1,x2,y2,x1 = LocRostros
				y1,x2,y2,x1 = y1*4,x2*4,y2*4,x1*4
				cv2.rectangle(Img,(x1,y1),(x2,y2),(255,204,0),2)
				cv2.rectangle(Img,(x1,y2-35),(x2,y2),(255,204,0),cv2.FILLED)
				cv2.putText(Img,Nombre,(x1+6,y2-6),cv2.FONT_HERSHEY_COMPLEX,1,(255,255,255),2)
				ListaAsistencia(Nombre)
			else:
				y1,x2,y2,x1 = LocRostros
				y1,x2,y2,x1 = y1*4,x2*4,y2*4,x1*4
				cv2.rectangle(Img,(x1,y1),(x2,y2),(255,204,0),2)
				cv2.rectangle(Img,(x1,y2-35),(x2,y2),(255,204,0),cv2.FILLED)
				cv2.putText(Img,"DESCONOCIDO - Salida",(x1+6,y2-6),cv2.FONT_HERSHEY_COMPLEX,1,(255,255,255),2)
				ListaAsistencia("DESCONOCIDO")

		cv2.imshow('Camara Salida',Img) #Mostramos la transmision de la camara de entrada
		
		k = cv2.waitKey(1)

		if k%256 == 27: #Cuando se presiona ESC se cierra la ventana
			break

	CamaraSalida.release()
	cv2.destroyWindow('Camara Salida')

#ReconocimientoSalida()