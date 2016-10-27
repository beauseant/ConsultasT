from lib.DBConsultas import DB



if __name__ == "__main__":

	dbName = 'consultasT'
	host = 'vanir'
	user = 'consultas'
	pwd = 'teich:i6I'

	fich = 'data/camposYcategorias_v01.csv'


	dbT = DB ( dbName, host, user, pwd )

	dbT.cargarCategorias ( fich )	

	fichCat = 'data/consultas01.csv'
	dbT.cargarConsultas ( fichCat )