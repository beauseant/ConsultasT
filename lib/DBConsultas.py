import csv
from pymongo import MongoClient


class DB (object):


	__host = 'localhost'
	__port = 2701

	__dbName = ''

	__pwd  = ''
	__user = ''
	__db = None
	__collectionCategorias = None
	__collectionConsultas = None
	__collectionUsers = None
	__conn = None


	__categoriesList = None
	


	def connect( self ):
		'''
			mongodb creates databases and collections automatically for you if they don't exist already. 
		'''		
		try:
			client = MongoClient( self.__host )
			client[ self.__dbName ].authenticate ( self.__user, self.__pwd )
			self.__db = client[ self.__dbName ]

			self.__collectionCategorias = self.__db [ 'categoria' ]
			self.__collectionConsultas = self.__db [ 'consulta' ]
			self.__collectionUser = self.__db [ 'user' ]

		except Exception as E:
			print ('fail to connect mongodb @ %s:%d, %s', self.__host, self.__port, str (E) )
			exit ()

		print ("connected to mongodb @ %s:[%s]", self.__host, self.__port)


	def __init__ ( self, dbName, host, user, pwd ):
		self.__dbName = dbName
		self.__pwd = pwd
		self.__user = user
		self.__host = host

		self.connect ()

	def cargarCategorias ( self, fich):

		print 'loading %s' % (fich)
		self.__collectionCategorias.remove({})

		with open(fich, 'rb') as f:
		    reader = csv.reader(f)
		    columns = list(zip(*reader))

		    catTotales = []
		    contador = 0
		    for col in columns:
		    	princ = col[0]
		    	for data in col[1:]:
		    		if not (data==''):		    			
		    			catTotales.append ({'categoria':data,'familia':princ,'catid':contador})
		    			contador += 1

		self.__collectionCategorias.insert ( catTotales )

	def cargarConsultas (self, fich):
		print 'loading %s' % (fich)
		self.__collectionConsultas.remove({})

		with open(fich, 'rb') as f:
		    reader = csv.reader(f)
		    col = list(zip(*reader))[0]

		    consultasTotales = []

		    for i, data in enumerate(col):
		    	if not (data == ''):
		    		consultasTotales.append ({'idconsulta':i,'consulta':data})

		self.__collectionConsultas.insert ( consultasTotales )


	def getUserPwd (self, user ):

		return (self.__collectionUser.find({'user':user},{'pwd':1}).limit(1))[0]['pwd']



	#categories = {'1.1. Informacion Practica':{0:'Movilidad en destino',1:'Accesibilidad del destino'},'1.4. Ocio':{2:'Ocio',3:'Atracciones'}}
	def getCategories ( self ):
		if not self.__categoriesList:
			catList = {}

			data = self.__collectionCategorias.find ({})

			for cat in data:
				try:
					catList [cat['familia']].update({cat['catid']:cat['categoria']})
				except:
					catList[cat['familia']]={}

			self.__categoriesList = catList


		return self.__categoriesList


	def getFinalCategories ( self ):
		return  (self.__collectionCategorias.find({},{'catid':1,'categoria':1}))

	def getConsulta ( self, all=False ):
		if all:			
			return  (self.__collectionConsultas.find({}))
		else:
			return  (self.__collectionConsultas.find({'categorias':{'$exists':False}}).limit(1)[0])
		
	def setCategoria (self, idconsulta, categorias ):
		self.__collectionConsultas.update ({'idconsulta':int(idconsulta)},{'$set':{'categorias':categorias}})
		#import ipdb ; ipdb.set_trace()









		    
		    


#admin xu#a0Io6s