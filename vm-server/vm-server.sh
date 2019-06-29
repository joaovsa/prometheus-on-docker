#!/bin/bash
#Script para configurar a VM Master

#Instalando o Docker
sudo apt -y install apt-transport-https ca-certificates curl gnupg-agent software-properties-common
curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo apt-key add -
sudo apt-key fingerprint 0EBFCD88
sudo add-apt-repository "deb [arch=amd64] https://download.docker.com/linux/ubuntu $(lsb_release -cs) stable"
sudo apt update
sudo apt -y install docker-ce docker-ce-cli containerd.io
sudo systemctl start docker
sudo systemctl enable docker
sudo apt -y upgrade
sudo gpasswd -a "${USER}" docker


#baixa repositorio e entra na pasta
git clone https://github.com/joaovsa/prometheus-on-docker
cd prometheus-on-docker/vm-server

#cria imagem docker do prometheus usando Dockerfile
sudo docker build -t my-prometheus .

#executa container prometheus
sudo docker run -p 9090:9090 --restart=always --detach=true --name=prometheus my-prometheus

#inicia container c/ node-exporter
sudo docker run -d --restart=always --net="host" --pid="host" --publish=9100:9100 --detach=true --name=node-exporter -v "/:/host:ro,rslave" quay.io/prometheus/node-exporter --path.rootfs /host

#inicia container c/ cAdvisor
sudo docker run --restart=always --volume=/:/rootfs:ro --volume=/var/run:/var/run:ro --volume=/sys:/sys:ro --volume=/var/lib/docker/:/var/lib/docker:ro --volume=/dev/disk/:/dev/disk:ro --publish=8080:8080 --detach=true --name=cadvisor google/cadvisor:latest