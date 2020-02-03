from flask import Flask , jsonify , request
from flask_jwt_extended import (
    JWTManager, jwt_required, create_access_token,
    get_jwt_claims , get_jwt_identity
)
from flask_jwt import JWT, current_identity
from werkzeug.security import safe_str_cmp

#--------------------
from flask_cors import CORS
import json
from datetime import datetime
#####my_modules#######
from data_base import * 

_miConexion =  getConexionPG()
class User(object):
    def __init__(self, id, username, password, first_name , last_name, email):
        self.id = id
        self.username   = username
        self.password   = password
        self.first_name = first_name
        self.last_name  = last_name
        self.email      = email

    def __str__(self):
        data =  "User{id:"+str(self.id)+" ,nombre:"+self.first_name+"}"
        return data

    def getUser(self):# return data user
        User = dict()
        User ={
            'id'            : str(self.id),
            'userame'       : str(self.username),
            'first_name'    : str(self.first_name),
            'last_name'     : str(self.last_name),
            'email'         : str(self.email)
        }        
        return User

############### GET USERS DB ##############
def getUsers():
    queryUsers = 'SELECT * FROM mUSER'
    dataUsers  = getData(_miConexion , queryUsers)
    if len(dataUsers)>0:
        users = list()
        for x in dataUsers:        
            newUser = User(x['id'], x['username'] ,
                        x ['psw'] , x['first_name'],
                        x['last_name'], x['email'])
            users.append(newUser)
    return users
##--------------------------------------##
username_table = {u.username : u for u in getUsers()}
userid_table = {u.id: u for u in getUsers()}
#--------------------------------------##
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
def getDataProducts():
    sql = 'SELECT * FROM PRODUCT'
    products  = getData(_miConexion , sql)
    data_products = []
    for x in products:
        product = dict()                
        if x['updatedat'] != None:
           print('yes')
           x['updatedat'] =  x['updatedat'].strftime('%d/%m/%Y')
        #----------------------------------------------------------#
        product = {
            'ID'                : x['id'],
            'PRINCIPAL_CODE'    : x['principal_code'],
            'DESCRIPTION'       : x['description'],
            'PRICE'             : float(x['price']),
            'STATE'             : x['state'],
            'CREATEDAT'         : x['createdat'].strftime('%d/%m/%Y') ,
            'UPDATEDAT'         : x['updatedat']
        }    
        data_products.append(product)
    return data_products
#-------------------OBTENER INFO DE PRODUCTOS---------------
@jwt_required
@app.route('/products_list/', methods=['GET','POST'])
def products_list():
    if request.method=='GET':                    
        if protected():        #si token es valido :)
            return jsonify(getDataProducts())
    else:        
        return 'IS NOT GET'
#------------------ INSERTAR 1 PRODUCTO-------------------
@app.route('/insert_product', methods=['POST'])
def insert_product():
    if request.method=='POST' and protected():
        datosRecibidos      = request.get_json()
        PRINCIPAL_CODE      = datosRecibidos['PRINCIPAL_CODE']
        print(len(PRINCIPAL_CODE))
        if len(PRINCIPAL_CODE) > 10:
            msg = {
                'Error':'PRINCIPAL_CODE DEBE SER DE MÁXIMO 10 DIGITOS'
            }
            return jsonify(msg) 
        else:
            DESCRIPTION         = datosRecibidos['DESCRIPTION']                
            PRICE               = datosRecibidos['PRICE']
            CREATEDAT           = datetime.today()
            cur = _miConexion.cursor()
            query = "INSERT INTO PRODUCT (PRINCIPAL_CODE, DESCRIPTION , PRICE, STATE, CREATEDAT )VALUES(%s,%s,%s,%s,%s);"
            cur.execute(query,(PRINCIPAL_CODE, DESCRIPTION , PRICE, True, CREATEDAT))
            _miConexion.commit()               
            return 'PRODUCTO CREADO CON ÉXITO'
if __name__ == '__main__':
    app.run()