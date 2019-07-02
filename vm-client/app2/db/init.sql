
CREATE DATABASE cadvisordb;
use cadvisordb;

CREATE TABLE prometheus (
    timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    cont_id VARCHAR(200) DEFAULT 'no-id',
    cont_name VARCHAR(20) DEFAULT 'no-name',
    cpu_name VARCHAR(10) DEFAULT 'cpu-none',
    cpu_usage VARCHAR(20) DEFAULT '0',
    mem_usage VARCHAR(20) DEFAULT '0',
    bytes_rx VARCHAR(40) DEFAULT '0',
    bytes_tx VARCHAR(30) DEFAULT '0'
);

INSERT INTO prometheus
  (cont_id, cont_name, cpu_name, cpu_usage, mem_usage, bytes_rx, bytes_tx)
VALUES
  ('dummy-container', 'cont_name', 'cpu_name', '47.212', '22.2', '123', '321')