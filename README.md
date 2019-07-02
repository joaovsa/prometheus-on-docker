# prometheus-on-docker

### Trabalho Final: Prometheus

Com o `git` e o `vagrant` instalados, siga os passos a seguir:

### Passo 1

Se você já usou Vagrant antes, atualize seu box do ubuntu para não dar erro

```markdown
\$ sudo vagrant box update
```

### Passo 2

Você pode acessar o Prometheus pelo IP da VM master definido no Vagrantfile:

```markdown
192.168.50.2:9090
```

### Passo 3

Inicie as VMs usando o Vagrantfile

```markdown
\$ vagrant up
```

### Passo 4

Acesse cada uma das VMs utilizando dois terminais diferentes

```markdown
$ vagrant ssh master
$ vagrant ssh worker
```

### Passo 5

Na VM worker, você pode listar as imagens docker

```markdown
\$ docker images
```

### Passo 6

Iniciando a aplicação client do APP1

```markdown
\$ docker run -it app1/client
```

### Passo 7

No navegador, acesse o IP `192.168.50.3:5001` para verificar que ainda não existe arquivo no servidor.

### Passo 8

A aplicação cliente possui três opções:

```markdown
1. Get file
2. Post file
3. Exit
```

- Ao selecionar a opção 1, a aplicação cliente realiza um GET request para a aplicação servidor, que deve estar rodando no IP na porta 5001. O servidor deve responder com uma imagem de um cachorrinho bem fofo;

- Ao selecionar a opção 2, um POST request é feito para a aplicação servidor com uma imagem de um cachorrinho bem fofo. A imagem é guardada na pasta `files` e o servidor deve responder com uma mensagem de sucesso ou falha;

- A opção 3 finaliza a execuação da aplicação.

### Passo 9

No navegador, acesse o IP `192.168.50.3:5001` para verificar que agora existe o arquivo enviado pela aplicação client.

### Passo 10

Para construir a imagem do APP2 é necessário primeiro entrar na pasta

```markdown
cd prometheus-on-docker/vm-client/app2
```

E em seguida, construir a imagem

```markdown
sudo docker-compose build --no-cache
```

### Passo 11

Iniciando o APP2:

```markdown
sudo docker-compose up &
```

### Passo 12

Fazemos uma requisição para o APP2, onde é realizada uma requisição para a API do Prometheus que retorna as informações do container e salva em um arquivo JSON.

```markdown
curl http://0.0.0.0:5000 -o out.json
```

### Passo 13

Para verificar que tudo ocorreu conforme o esperado, podemos abrir o arquivo `out.json` e ver as informações que foram salvas

```markdown
sudo nano out.json
```

### Passo 14

Para construir a imagem do APP3 é necessário primeiro entrar na pasta

```markdown
cd ../app3
```

E em seguida, construir a imagem

```markdown
sudo docker-compose build --no-cache
```

### Passo 15

Iniciando o APP3:

```markdown
sudo docker-compose up &
```

### Passo 16

Fazemos uma requisição para o APP3, onde é realizada uma requisição para a API do Prometheus que retorna as informações da VM e salva em um arquivo JSON.

```markdown
curl http://0.0.0.0:5002 -o out.json
```

### Passo 17

Para verificar que tudo ocorreu conforme o esperado, podemos abrir o arquivo `out.json` e ver as informações que foram salvas

```markdown
sudo nano out.json
```

### Considerações e dificuldades

Este trabalho contribuiu imensamente com o nosso entendimento de criação de ambientes virtuais e conteinerização através do Vagrant e do Docker. Através dele conseguimos entender melhor o passo a passo de criação de um ambiente virtual e de aplicações que rodem dentro de containers.
