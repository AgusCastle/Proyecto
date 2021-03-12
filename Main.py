
from Camara1_Entrada import ReconocimientoEntrada
from Camara2_Salida import ReconocimientoSalida
from CrearLista import CrearArchivoCSV
from TomarFotos import TomarFotografia
import cv2
from os import system

CrearArchivoCSV()

while True:

	system("cls")
	print(" [1] Camara Entrada \n [2] Camara Salida \n [3] Tomar Fotografia \n [4] Salir")
	Opcion = input("Seleccione una opcion: ")

	#print (Opcion)

	if Opcion == "1":
		system("cls")
		print("Camara Entrada")
		ReconocimientoEntrada()

	if Opcion == "2":
		system("cls")
		print("Camara Salida")
		ReconocimientoSalida()

	if Opcion == "3":
		system("cls")
		print("Tomar Fotografia")
		TomarFotografia()

	if Opcion == "4":
		system("cls")
		#print("Huevos")
		break




