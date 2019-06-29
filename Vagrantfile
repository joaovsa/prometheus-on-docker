# -*- mode: ruby -*-
# vi: set ft=ruby :

# All Vagrant configuration is done below. The "2" in Vagrant.configure
# configures the configuration version (we support older styles for
# backwards compatibility). Please don't change it unless you know what
# you're doing.
Vagrant.configure(2) do |config|
    config.vm.define "master" do |master|

        master.vm.box = "ubuntu/bionic64"
        master.vm.network "forwarded_port", guest: 5000, host: 9003
        master.vm.network "private_network", ip: "192.168.50.2"
        master.vm.hostname = "master"
        master.vm.provider "virtualbox" do |vb|
                vb.memory = "4096"
                vb.name = "master"
        end
        master.vm.provision "shell" do |s|
            s.path = "vm-server/vm-server.sh"	
        end  
    end

    config.vm.define "worker" do |worker|

        worker.vm.box = "ubuntu/bionic64"
        worker.vm.network "private_network", ip: "192.168.50.3"
        worker.vm.hostname = "worker"
        worker.vm.provider "virtualbox" do |vb|
                vb.memory = "4096"
                vb.name = "worker"
        end
        worker.vm.provision "shell" do |s|
            s.path = "vm-client/vm-client.sh"	
        end  
    end
end
