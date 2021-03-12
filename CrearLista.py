import os
from datetime import datetime
import csv

Acesso = datetime.now()
Fecha = Acesso.strftime('%d_%m_%Y')

def NombreArchivo():
	Nombre_Archivo = 'Lista_E_S_{}'.format(Fecha)
	return Nombre_Archivo

def CrearArchivoCSV():
	Lista_E_S = open('Lista_E_S_{}.csv'.format(Fecha),'w')
