from typing import List, Dict
from flask import Flask
#import mysql.connector
import requests
import json

SERVICES = ['app2_app_1', 'app2_db_1', 'cadvisor', 'node-exporter', 'prometheus']

app = Flask(__name__)

def request_cpu(vec_dicts):
    #carrega os segundos totals de cpu idle
    cpu_dict = {}
    response = requests.get('http://192.168.50.2:9090/api/v1/query',
         params={'query' : "node_memory_MemAvailable_bytes"})
    resp_dict = response.json()
    for resp in resp_dict['data']['result']:
        ip = resp['metric']['instance'].split(':')[0]+':8080' 
        #ja mapeia a porta do container configurado
        cpu_dict[ip] = resp['value'][1]
    
    for item in cpu_dict.items():
        print(item)

    #fills container name, container ID and cpu %
    response = requests.get('http://192.168.50.2:9090/api/v1/query',
         params={'query' : "container_cpu_usage_seconds_total"})
    resp_dict = response.json()

    #for each result fills the dict with curresponding name and ID.
    #ignores nom named SERVICES for class example simplicity
    for resp in resp_dict['data']['result']:
        try:
            if resp['metric']['name'] in SERVICES:
                d = {}
                d['cont_id'] = resp['metric']['id']
                d['cont_name'] = resp['metric']['name']
                d['cpu_name'] = resp['metric']['cpu']
                d['cpu_usage'] = '{:.7f}'.format(float(resp['value'][1]) / float(cpu_dict[resp['metric']['instance']]) * 100)
                vec_dicts.append(d)
        except:
            pass 
    

def request_prom():
    insertions = []    
    """response = requests.get('http://192.168.50.2:9090/api/v1/query',
         params={'query' : "container_memory_working_set_bytes{name='node-exporter'}"})
    dictio = response.json()
    for val in dictio['data']['result']:
        print('id: {} value: {}'.format(val['metric']['id'], val['value'][0]))
    result = response.json()
    return result"""
    request_cpu(insertions)
    #debug purps
    for ins in insertions:
        print("id: {} name: {} cpu: {}".format(ins['cont_id'], ins['cont_name'], ins['cpu_usage']))

""" def cadvisordb() -> List[Dict]:
    config = {
        'user': 'root',
        'password': 'root',
        'host': 'db',
        'port': '3306',
        'database': 'cadvisordb'
    }
    connection = mysql.connector.connect(**config)
    cursor = connection.cursor()
    cursor.execute('SELECT * FROM prometheus')
    results = [{'timestamp' : "{}-{}-{} {}:{}:{}".format(\
                    timestamp.day, timestamp.month, timestamp.year, timestamp.hour, timestamp.minute,timestamp.second),\
                'cont_id' : cont_id,\
                'cont_name' : cont_name,\
                'cpu_name' : cpu_name,\
                'cpu_usage' : cpu_usage,\
                'mem_usage' : mem_usage,\
                'bytes_rx' : bytes_rx,\
                'bytes_tx' : bytes_tx} for\
                (timestamp, cont_id, cont_name, cpu_name,\
                 cpu_usage,mem_usage,bytes_rx,bytes_tx) in cursor]
    cursor.close()
    connection.close()

    return results """


@app.route('/')
def index() -> str:
    #get jsons from prometheus server
    return json.dumps({'request' : request_prom()})
    #dump mysql
    #return json.dumps({'cadvisor': cadvisordb()})


if __name__ == '__main__':
    app.run(host='0.0.0.0')