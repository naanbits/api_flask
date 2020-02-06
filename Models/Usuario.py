from Control.data_base import *

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
    