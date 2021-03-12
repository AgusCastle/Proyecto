import cv2
import numpy
import face_recognition
import os
from CrearLista import NombreArchivo
from datetime import datetime

NombreArc = NombreArchivo()

path = 'Rostros' #Ruta de donde estan las imagenes
Imagenes = []
ListaNombres = []
Lista = os.listdir(path) #Creamos una lista con los nombres de los archivos que se encuentran en el path
#print(Lista) #Imprime los nombre que se encuentan en la imagenes junto con la extencion del archivo

def ReconocimientoEntrada():

	for cl in Lista:
		ImagenActual = cv2.imread(f'{path}/{cl}')
		Imagenes.append(ImagenActual)
		ListaNombres.append(os.path.splitext(cl)[0])
	print(ListaNombres) #Imprime los nombres de la imagenes sin la extension

	def EncontrarRostrosGuardados(Imagenes): #Funcion para detectar las imagenes guardadas en la carpeta de Imagenes
		ListaRostrosEncontrados = []
		for Img in Imagenes:
			Img = cv2.cvtColor(Img, cv2.COLOR_BGR2RGB) #Combiar los colores a RGB
			Encode = face_recognition.face_encodings(Img)[0] #Buscamos si en las imagenes se encuentra algun candito a rostro
			ListaRostrosEncontrados.append(Encode) #Si se encuentra un candidato a rostros este se guarda en un lista
		return ListaRostrosEncontrados


	def ListaAsistencia(Nombre):
		with open ('{}.csv'.format(NombreArc),'r+') as f:
			ListaDeAsistencia = f.readlines()
			ListaNombreAsistencia = []
			for line in ListaDeAsistencia:
				Entrada = line.split(',')
				ListaNombreAsistencia.append(Entrada[0])
			#if Nombre not in ListaNombreAsistencia:
			Acceso = datetime.now()
			Fecha = Acceso.strftime('%d-%m-%Y')
			Hora = Acceso.strftime('%H:%M:%S')
			TipoAcceso = "Entrada"
			f.writelines(f'\n{Nombre},{Fecha},{Hora},{TipoAcceso}')


	ListaRostrosConocidos = EncontrarRostrosGuardados(Imagenes) 
	#print("Codificacion Completada.")

	CamaraEntrada = cv2.VideoCapture(0) #Iniciamos la camara de entrada

	CamaraEntrada.set(3,700) #Ajustamos el ancho que se va a mostrar de la camara
	CamaraEntrada.set(4,500) #Ajustamos el alto que se va a mostrar de la camara



	while True:

		if not CamaraEntrada:
			print ("No se detecta ninguna camara")
			break

		success, Img = CamaraEntrada.read()
		ImgSmall = cv2.resize(Img,(0,0),None,0.25,0.25) #Reducimos el tamaño de la imagen de entrada para acelerar el proceso
		ImgSmall = cv2.cvtColor(ImgSmall, cv2.COLOR_BGR2RGB) #Converimos el video transmitido a RGB

		RostrosTransmitidos = face_recognition.face_locations(ImgSmall) #Generamos un array de cuadros limitadores de los rostros encontrados en la transmision
		EncodeTransmitidos = face_recognition.face_encodings(ImgSmall,RostrosTransmitidos)  #Buscamos si en las imagenes se encuentra algun candito a rostro

		for EncodeRostro, LocRostros in zip(EncodeTransmitidos,RostrosTransmitidos):
			Emparejamiento = face_recognition.compare_faces(ListaRostrosConocidos, EncodeRostro) #Comparamos la lista de los rostros conocidos con el candidato a rostro en la transmision
			Distancia_Rostro = face_recognition.face_distance(ListaRostrosConocidos, EncodeRostro) #Se comparan las distancias de los componentes de los rostros con los rostros en la transmision
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
				cv2.putText(Img,"DESCONOCIDO - Entrada",(x1+6,y2-6),cv2.FONT_HERSHEY_COMPLEX,1,(255,255,255),2)
				ListaAsistencia("DESCONOCIDO")
		
		cv2.imshow('Camara Entrada',Img) #Mostramos la transmision de la camara de entrada
		
		k = cv2.waitKey(1)

		if k%256 == 27: #Cuando se presiona ESC se cierra la ventana
			break

	CamaraEntrada.release()
	cv2.destroyWindow('Camara Entrada')

#ReconocimientoEntrada()