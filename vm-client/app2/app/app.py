from typing import List, Dict
from flask import Flask
import mysql.connector
import requests
import json

SERVICES = ['app2_app_1', 'app2_db_1', 'cadvisor', 'node-exporter', 'prometheus']

app = Flask(__name__)

def request_cpu(vec_dicts):
    #carrega os segundos totals de cpu idle
    cpu_dict = {}
    response = requests.get('http://192.168.50.2:9090/api/v1/query',
         params={'query' : "node_cpu_seconds_total{mode='idle'}"})
    resp_dict = response.json()
    for resp in resp_dict['data']['result']:
        ip = resp['metric']['instance'].split(':')[0]+':8080' 
        #ja mapeia a porta do container configurado
        cpu_dict[ip] = resp['value'][1]

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
    
def request_mem(vec_dicts):    
    #carrega os segundos totals de cpu idle
    mem_dict = {}
    response = requests.get('http://192.168.50.2:9090/api/v1/query',
         params={'query' : "node_memory_MemTotal_bytes"})
    resp_dict = response.json()
    for resp in resp_dict['data']['result']:
        ip = resp['metric']['instance'].split(':')[0]+':8080' 
        #ja mapeia a porta do container configurado
        mem_dict[ip] = resp['value'][1]
    
    for item in mem_dict.items():
        print(item)
        
     #fills container name, container ID and cpu %
    response = requests.get('http://192.168.50.2:9090/api/v1/query',
         params={'query' : "container_memory_usage_bytes"})
    resp_dict = response.json()

    #for each result fills the dict with curresponding name and ID.
    #ignores nom named SERVICES for class example simplicity
    for resp in resp_dict['data']['result']:
        try:
            for i, d in enumerate(vec_dicts):
                if resp['metric']['id'] == d['cont_id']:                   
                    vec_dicts[i]['mem_usage'] = '{:.7f}'.format(float(resp['value'][1]) / float(mem_dict[resp['metric']['instance']]) * 100)
                    
        except:
            pass 


def request_rx(vec_dicts):    
    response = requests.get('http://192.168.50.2:9090/api/v1/query',
         params={'query' : "container_network_receive_packets_total"})
    resp_dict = response.json()
    #for each result fills the dict with curresponding 
    for resp in resp_dict['data']['result']:
        try:
            for i, d in enumerate(vec_dicts):
                print('metric id {} cont id {}'.format(resp['metric']['id'],d['cont_id']))
                if resp['metric']['id'] == d['cont_id']:                   
                    vec_dicts[i]['bytes_rx'] = resp['value'][1]                    
        except:
            pass 
def request_tx(vec_dicts):    
    response = requests.get('http://192.168.50.2:9090/api/v1/query',
         params={'query' : "container_network_transmit_packets_total"})
    resp_dict = response.json()
    #for each result fills the dict with curresponding 
    for resp in resp_dict['data']['result']:
        try:
            for i, d in enumerate(vec_dicts):
                print('metric id {} cont id {}'.format(resp['metric']['id'],d['cont_id']))
                if resp['metric']['id'] == d['cont_id']:                   
                    vec_dicts[i]['bytes_tx'] = resp['value'][1]                    
        except:
            pass 

def request_prom(insertions):    
    request_cpu(insertions)
    request_mem(insertions)
    request_rx(insertions)
    request_tx(insertions)
    #debug purps
    for ins in insertions:
        print("id: {} name: {} cpu: {} mem:{} rx:{} tx{}".format(ins['cont_id'], ins['cont_name'], ins['cpu_usage'], ins['mem_usage'], ins['bytes_rx'], ins['bytes_tx']))

def cadvisordb(insertions) -> List[Dict]:
    #insere e consulta base
       connection = mysql.connector.connect{
        'user': 'root',
        'password': 'root',
        'host': 'db',
        'port': '3306',
        'database': 'cadvisordb'
    }    
    cursor = connection.cursor(prepared=true)


    sql = """INSERT INTO prometheus (cont_id, cont_name, cpu_name, cpu_usage, mem_usage, bytes_rx, bytes_tx) VALUES (%s, %s, %s, %s, %s, %s, %s)"""
    val = [('dummy-container', 'cont_name', 'cpu_name', '47.212', '22.2', '123', '321'),
    ('dummy-container', 'cont_name', 'cpu_name', '47.212', '22.2', '123', '321'),
    ('dummy-container', 'cont_name', 'cpu_name', '47.212', '22.2', '123', '321')]
     
    r = cursor.executemany(sql, val)
    connection.commit()
    print(cursor.rowcount, "was inserted.") 



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
    insertions = []    
    request_prom(insertions)
    #dump mysql
    return json.dumps({'cadvisor': cadvisordb(insertions)})


if __name__ == '__main__':
    app.run(host='0.0.0.0')