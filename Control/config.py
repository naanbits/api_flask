import json

def getDataJson():
    with open('Control/config.json') as file:
        data = json.load(file)
    return data['data_db_local'] , data['data_db_heroku']
