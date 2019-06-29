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