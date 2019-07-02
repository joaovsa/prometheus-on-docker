
CREATE DATABASE machines;
use machines;

CREATE TABLE prometheus (
    timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    nome VARCHAR(200) DEFAULT 'no-name',
    cpu_name VARCHAR(10) DEFAULT 'cpu-main',
    cpu_usage VARCHAR(20) DEFAULT '0',
    mem_usage VARCHAR(20) DEFAULT '0',
    bytes_rx VARCHAR(40) DEFAULT '0',
    bytes_tx VARCHAR(30) DEFAULT '0',
    source VARCHAR(30) DEFAULT 'prometheus');

INSERT INTO prometheus
  (nome, cpu_name, cpu_usage, mem_usage, bytes_rx, bytes_tx, source)
VALUES
  ('dummy-machine', 'cpu_name', '47.212', '22.2', '123', '321', 'squidward')