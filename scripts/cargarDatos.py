import sys

sys.path.insert(0, '../lib')
from DBConsultas import DB
import ConfigParser


if __name__ == "__main__":

	config = ConfigParser.ConfigParser()
	config.read('../web/consultas.cfg')


	dbT =  DB (dbName=config.get('DB','dbname'), host=config.get('DB','host'), user=config.get('DB','user'), pwd=config.get('DB','pwd'))	

	fich = '../data/camposYcategorias_v01.csv'

	dbT.cargarCategorias ( fich )	

	fichCat = '../data/consultas01.csv'
	dbT.cargarConsultas ( fichCat )