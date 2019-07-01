from typing import List, Dict
from flask import Flask
import mysql.connector
import requests
import json

app = Flask(__name__)

def request_prom():
    response = requests.get('http://192.168.50.2:9090/api/v1/query',
         params={'query' : "container_memory_working_set_bytes{name='node-exporter'}"})
    dictio = response.json()
    for val in dictio['data']['result']:
        print('id: {} value: {}'.format(val['metric']['id'], val['value'][0]))
    result = response.json()
    return result

def cadvisordb() -> List[Dict]:
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

    return results


@app.route('/')
def index() -> str:
    #get jsons from prometheus server
    return json.dumps({'request' : request_prom()})
    #dump mysql
    return json.dumps({'cadvisor': cadvisordb()})


if __name__ == '__main__':
    app.run(host='0.0.0.0')