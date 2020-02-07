from Control.data_base import *

objConexion = Conexion()
con = objConexion.getConexionPG()

def getDataProducts(sql):
    products = objConexion.getData(sql)
    data_products = []    
    if products:    
        for x in products:
            product = dict()
            if x['updatedat'] != None:
                x['updatedat'] = x['updatedat'].strftime('%d/%m/%Y')
                #----------------------------------------------------------#
            product = {
                    'ID': x['id'],
                    'PRINCIPAL_CODE': x['principal_code'],
                    'DESCRIPTION': x['description'],
                    'PRICE': float(x['price']),
                    'STATE': x['state'],
                    'CREATEDAT': x['createdat'].strftime('%d/%m/%Y'),
                    'UPDATEDAT': x['updatedat']
            }
            data_products.append(product)
        return data_products
    return False
def insert_table_product(DESCRIPTION , PRICE , CREATEDAT, PRINCIPAL_CODE):
    try:
        query_select    = 'SELECT * FROM PRODUCT WHERE STATE = TRUE'
        data_validate = getDataProducts(query_select)
        if validate_principal_code(data_validate , PRINCIPAL_CODE):        
            return 'YA EXISTE UN PRODUCTO CON ESE PRINCIPAL_CODE.'
        else:
            cur = con.cursor()
            query = "INSERT INTO PRODUCT (PRINCIPAL_CODE, DESCRIPTION , PRICE, STATE, CREATEDAT )VALUES(%s,%s,%s,%s,%s);"
            cur.execute(query,(PRINCIPAL_CODE, DESCRIPTION , PRICE, True, CREATEDAT))
            con.commit()               
            return True        
    except Exception as e:
        return str(e)

def update_table_product(ID, DESCRIPTION , PRICE ,UPDATEDAT , PRINCIPAL_CODE):
    _BAND = True
    try:
        data_select  =  query_not(ID)        
        query_select    = 'SELECT * FROM PRODUCT WHERE STATE = TRUE'
        data_exists = getDataProducts(query_select)
        if not data_exists:        
            return 'NO EXISTEN REGISTROS'
        else:        
            query_validate = 'SELECT * FROM PRODUCT WHERE STATE = TRUE AND ID = '+str(ID) 
            data_validate  =getDataProducts(query_validate)
            print('da',data_validate)
            if data_validate:
                if validate_principal_code(data_select , PRINCIPAL_CODE):
                    return 'PRINCIPAL_CODE YA EXISTE.'            
                else:
                    cur = con.cursor()
                    query_update = 'UPDATE PRODUCT SET DESCRIPTION = %s , PRICE =%s , UPDATEDAT = %s ,PRINCIPAL_CODE =%s  WHERE ID = %s '
                    cur.execute(query_update , (DESCRIPTION , PRICE , UPDATEDAT , PRINCIPAL_CODE, ID) )
                    con.commit()        
                    return True
            return 'NO EXISTE REGISTRO CON EL ID '+str(ID)
    except Exception as e:        
        return str(e)

def delete_table_product(ID):
    try:
        query_validate = 'SELECT * FROM PRODUCT WHERE STATE = TRUE AND ID = '+str(ID)         
        data_validate  =  getDataProducts(query_validate)
        print('dd.',data_validate)
        if data_validate:
            cur = con.cursor()
            query_delete = 'UPDATE PRODUCT SET STATE = %s WHERE ID = %s'
            cur.execute(query_delete,(False, ID) )
            con.commit()
            return True
        return 'NO EXISTE REGISTRO CON EL ID '+str(ID)
    except Exception as e:
        return str(e)

def query_not(ID):
    query_select = 'SELECT * FROM PRODUCT WHERE  STATE = TRUE AND  ID <> '+str(ID)        
    if query_select:
        return getDataProducts(query_select)
    return False

def validate_principal_code(data_list , value):
    print('Ingreso validate -- ', data_list , value)
    if data_list:
        for x in data_list:            
            if value == x['PRINCIPAL_CODE']:            
                return True        
    return False