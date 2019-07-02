from typing import List, Dict
from flask import Flask
import mysql.connector
import requests
import json

app = Flask(__name__)

def request_cpu(vec_dicts):
    #carrega os segundos totals de cpu idle
    cpu_dict = {}
    response = requests.get('http://192.168.50.2:9090/api/v1/query',
         params={'query' : "100 * (1 - avg by(instance)(irate(node_cpu_seconds_total{mode='idle'}[5m])))"})
    resp_dict = response.json()
    for resp in resp_dict['data']['result']:
        ip = resp['metric']['instance']
        #ja mapeia a porta do container configurado
        cpu_dict['name'] = ip
        cpu_dict['cpu_usage'] = resp['value'][1]
    
def request_prom(insertions):    
    request_cpu(insertions)
    #debug purps
    for ins in insertions:
        print("name: {} cpu: {} ".format(ins['cont_name'], ins['cpu_usage']))

def insertdb(argtuple):    
    connection = mysql.connector.connect(\
        user= 'root',\
        password= 'root',\
        host='db3',\
        port= '3306',\
        database='machines')  

    query = "INSERT INTO prometheus(name, cpu_usage, mem_usage, bytes_rx, bytes_tx, source) " \
            "VALUES(%s,%s,%s,%s,%s,%s)"    
 
    try:
        cursor = connection.cursor()
        cursor.execute(query, argtuple) 
        connection.commit()
    except Exception as e:
        print(e)
 
    finally:
        cursor.close()
        connection.close()

def machines() -> List[Dict]:
    #insere e consulta base
    connection = mysql.connector.connect(\
    user= 'root',\
    password= 'root',\
    host='db3',\
    port= '3306',\
    database='machines')
    cursor = connection.cursor()
    cursor.execute('SELECT * FROM prometheus')
    results = [{'timestamp' : "{}-{}-{} {}:{}:{}".format(\
                    timestamp.day, timestamp.month, timestamp.year, timestamp.hour, timestamp.minute,timestamp.second),\
                'name' : name,\
                'cpu_usage' : cpu_usage,\
                'mem_usage' : mem_usage,\
                'bytes_rx' : bytes_rx,\
                'bytes_tx' : bytes_tx,\
                'source' : source} for\
                (timestamp, name, cpu_usage,mem_usage,bytes_rx,bytes_tx, source) in cursor]
    cursor.close()
    connection.close()

    return results


@app.route('/')
def index() -> str:
    #get jsons from prometheus server
    insertions = []    
    request_prom(insertions)    
    insertdb( ('dummy-machine', '47.212', '22.2', '123', '321', 'sponge-bob'))
    #dump mysql
    return json.dumps({'machines': machines()})


if __name__ == '__main__':
    app.run(host='0.0.0.0', port='5002')