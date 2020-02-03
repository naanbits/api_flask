import psycopg2
import psycopg2.extras
'''
user="mauricio",
			password="",
			host="localhost",
			port="5432",
			database="postgres"

user="hlssatbqyqhgcu",
			password="91afc97b28dfdb603532c91116a0bbf105c781df8208bae5a20a5a2c96038ead",
			host="ec2-54-92-174-171.compute-1.amazonaws.com",
			port="5432",
			database="d528b4hs1njq1f"
'''
def getConexionPG():
	try:
		connection = psycopg2.connect(
			user="hlssatbqyqhgcu",
			password="91afc97b28dfdb603532c91116a0bbf105c781df8208bae5a20a5a2c96038ead",
			host="ec2-54-92-174-171.compute-1.amazonaws.com",
			port="5432",
			database="d528b4hs1njq1f")
	except:
		print('Error Conexion')
	return connection	

def getData(conexion, sql):
	if conexion:
		cur = conexion.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
		cur.execute(sql)
		data = cur.fetchall()
		return data
	return 'None'


#print(getConexionPG())
#for x in getData(getConexionPG(), 'SELECT * FROM mUSER'):
#	print(x)