from flask import Flask , jsonify , request
from flask_jwt_extended import (JWTManager, jwt_required, create_access_token,get_jwt_claims , get_jwt_identity)
from flask_jwt import JWT, current_identity
from werkzeug.security import safe_str_cmp
from flask_cors import CORS , cross_origin
import json
from datetime import datetime
#####my_modules#######
from Models.Usuario import *
from Models.Product import *
from Control.data_base import *
#----------CREACION DE OBJETO CONEXION PARA BD--------------
objConexion  = Conexion()
con          = objConexion.getConexionPG()
##--------------------------------------##
username_table = {u.username : u for u in objConexion.getUsers(User)}
userid_table = {u.id: u for u in objConexion.getUsers(User)}
#---------------JWT-----------------------##
def authenticate(username, password):    
    user = username_table.get(username, None)    
    if user and safe_str_cmp(user.password.encode('utf-8'), password.encode('utf-8')):        
        return user

def identity(payload):    
    user_id = payload['identity']
    return userid_table.get(user_id, None)
#-------------FLASK------------------------#
app = Flask(__name__)
app.debug = False
app.config['SECRET_KEY'] = 'super-secret'
CORS(app)
cors = CORS(app, resources={r"/*": {"origins": "*"}})

jwt = JWTManager(app)
#----------endpoints-----
@app.errorhandler(404) 
def not_found(e): 
  return 'Dirección incorrecta'

@app.route('/crear_token', methods=['POST'])

def crear_token():
    username = request.json.get('username', None)
    password = request.json.get('password', None)
    user = username_table.get(username, None)  
    print('st__', user.__str__())
    ret = {'access_token': create_access_token(username , fresh=False),
            'User':  user.getUser()
        }
    return ret
@app.route('/protected', methods= ['GET'])
@jwt_required
def protected():
    current_user = get_jwt_identity()
    if current_user:        
        return True
    else: 
        return False    

@app.route('/')
def index():    
        return '<h3> <b> Conociendo Python</b></h3><p> ABC Community </p>'    
#---------------------------CRUD PRODUCTS----------------------------
#-------------------OBTENER INFO DE PRODUCTOS---------------
@jwt_required
@app.route('/products_list/', methods=['GET','POST'])
def products_list():
    if request.method=='GET':                    
        if protected():
            data = getDataProducts('SELECT * FROM PRODUCT WHERE STATE = TRUE ')
            if data:
                return jsonify(data)
            else:
                return jsonify('SIN DATOS')

    else:        
        return 'IS NOT GET'
#---------------OBTENER INFO DE UN PRODUCTO MEDIANTE ID--------
@jwt_required
@app.route('/get_product/<string:id>',methods=['GET','POST','PUT','DELETE'])

def get_product(id):
    if request.method=='GET':                    
        if protected():        #si token es valido :)                                
            sql  = 'SELECT * FROM PRODUCT WHERE ID = '+id 
            data = getDataProducts(sql)            
            if data:                    
                return jsonify(data)
            else:
                return jsonify({'msg':'No existe producto con el id '+id})   
    else:                
        return 'Metodo debe ser GET'

#------------------ INSERTAR 1 PRODUCTO-------------------
@app.route('/insert_product', methods=['POST'])
def insert_product():
    if request.method=='POST' and protected():
        datosRecibidos      = request.get_json()
        PRINCIPAL_CODE      = datosRecibidos['PRINCIPAL_CODE']
        if len(PRINCIPAL_CODE) > 10:
            msg = {
                'msg':'PRINCIPAL_CODE DEBE SER DE MÁXIMO 10 DIGITOS'
            }
            return jsonify(msg) 
        else:
            DESCRIPTION         = datosRecibidos['DESCRIPTION']                
            PRICE               = datosRecibidos['PRICE']
            CREATEDAT           = datetime.today()
            msg = insert_table_product(DESCRIPTION , PRICE , CREATEDAT,PRINCIPAL_CODE)        
            if msg == True:
                return jsonify({'msg':'PRODUCTO CREADO CON ÉXITO' })
            return jsonify( {'msg':msg})
    
@app.route('/update_product/<id>',methods=['POST'])
def update_product(id):
    if request.method=='POST' and protected():
        datosRecibidos          = request.get_json()
        PRINCIPAL_CODE          = datosRecibidos['PRINCIPAL_CODE']
        if len(PRINCIPAL_CODE) > 10:
            msg = {
                'msg':'PRINCIPAL_CODE DEBE SER DE MÁXIMO 10 DIGITOS'
            }
            return jsonify(msg) 
        else:
            DESCRIPTION         = datosRecibidos['DESCRIPTION']                
            PRICE               = datosRecibidos['PRICE']
            UPDATEDAT           = datetime.today()         
            msg = update_table_product(id,DESCRIPTION,PRICE,UPDATEDAT,PRINCIPAL_CODE)
            if msg == True:
                return jsonify({'msg':'DATOS DEL PRODUCTO ACTUALIZADOS' })
            return jsonify( {'msg':msg})

@app.route('/delete_product/<id>', methods = ['GET'])
def delete_product(id):
    print('yes-delete')    
    if request.method == 'GET':                
        msg = delete_table_product(id)        
        if msg == True:
            return jsonify({'msg':'EL PRODUCTO SE ELIMINÓ CON ÉXITO.'})
    return jsonify({'msg':msg})
        
#------------------------------------------------------------
def insertarRegistro(id):
    cur = con.cursor()
    FECHA = datetime.today()
    query = "INSERT INTO REGISTRO (FECHA , ID_EMP )VALUES(%s,%s);"
    cur.execute(query,(FECHA , str(id)))
    con.commit()      

@app.route('/consulta_empleado/<codigo>', methods = ['GET'])
def consulta_usuario(codigo):
    if request.method=='GET':                            
        codigo = str(codigo)
        print(type(codigo))
        sql  = 'SELECT ID, NOMBRE FROM EMPLEADO WHERE CODIGO = '+str("'"+codigo+"'")
        data = objConexion.getData(sql)  
        if data:
            id = data[0]['id'] #id empleado
            #insertarRegistro(id)                                         
            empleado = str(data[0]['id'])+';'+ data[0]['nombre'] #orden id;empleado -> para leer desde esp y hacer split
            return jsonify(empleado)
        else:        
            return jsonify("0;0")
    else:                
        return 'Metodo debe ser GET'

if __name__ == '__main__':
    app.run()