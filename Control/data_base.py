import psycopg2
import psycopg2.extras
from Control.config import *

class Conexion(object):
	def __init__(self):
		self.dataBD = getDataJson()[1]  
	
	def getConexionPG(self):
		try:
			connection = psycopg2.connect(
				user      =   self.dataBD['user'],
				password  =   self.dataBD['psw'],
				host      =   self.dataBD['host'],
				port	  =   self.dataBD['port'],
				database  =   self.dataBD['db'])
			print('yes')
		except:
			print('Error Conexion')
		return connection	

	def getData(self, sql):
		if self.getConexionPG():						
			print('sel')
			try:
				cur = self.getConexionPG().cursor(cursor_factory=psycopg2.extras.RealDictCursor)
				cur.execute(sql)
				data = cur.fetchall()
			except Exception as e:
				data = False
				print('error',e)
			return data
		return 'None'

	def getUsers(self, User):
	    queryUsers = 'SELECT * FROM mUSER'
	    dataUsers  = self.getData(queryUsers)
	    if dataUsers:
        	users = list()
	        for x in dataUsers:
                    newUser = User(x['id'], x['username'] ,x ['psw'] , x['first_name'],x['last_name'], x['email'])
                    users.append(newUser)
	        return users
	    return False

	def insert_table_product(DESCRIPTION , PRICE , CREATEDAT, PRINCIPAL_CODE):
		try:
			cur = con.cursor()
			query = "INSERT INTO PRODUCT (PRINCIPAL_CODE, DESCRIPTION , PRICE, STATE, CREATEDAT )VALUES(%s,%s,%s,%s,%s);"
			cur.execute(query,(PRINCIPAL_CODE, DESCRIPTION , PRICE, True, CREATEDAT))
			con.commit()               
			return True
		except Exception as e:
			print(e)
			return False
