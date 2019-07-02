# prometheus-on-docker

Se você já usou Vagrant antes, atualize seu box do ubuntu, senão vai dar merda!

```markdown
$ sudo vagrant box update
```

Beleza, até agora o Prometheus tá funcionando no. Pelo Browser, acesse o IP da VM master definido no Vagrantfile:

```markdown
192.168.50.2:9090
```
Conectar cadvisor e node-exporter da VM-Worker já deu certo:
talvez o cadvisor procure o server prometheus da mesma subrede. Tá ai, de graça! 

Chique. Próximos passos: 
- testar acesso da API HTTP do vagrant. 
- Desenvolver 1 APP flask se comunicando com a API

Inicie as VMs usando o Vagrantfile

```markdown
$ vagrant up
```

Acesse cada uma das VMs utilizando dois terminais diferentes

```markdown
$ vagrant ssh master
$ vagrant ssh worker
```

Na VM worker, você pode listar as imagens docker

```markdown
$ docker images
```

Inicie o container que possui a aplicação cliente

```markdown
$ docker run -it app1/client
```

A aplicação cliente possui três opções:

```markdown
1. Get file
2. Post file
3. Exit
```

- Ao selecionar a opção 1, a aplicação cliente realiza um GET request para a aplicação servidor, que deve estar rodando no IP na porta 5001. O servidor deve responder com uma imagem de um cachorrinho bem fofo;

- Ao selecionar a opção 2, um POST request é feito para a aplicação servidor com uma imagem de um cachorrinho bem fofo. A imagem é guardada na pasta `files` e o servidor deve responder com uma mensagem de sucesso ou falha;

- A opção 3 finaliza a execuação da aplicação.
