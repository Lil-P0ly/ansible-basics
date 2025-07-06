# -*- mode: ruby -*-
# vi: set ft=ruby :

# All Vagrant configuration is done below. The "2" in Vagrant.configure
# configures the configuration version (we support older styles for
# backwards compatibility). Please don't change it unless you know what
# you're doing.


Vagrant.configure("2") do |config|
  # The most common configuration options are documented and commented below.
  # For a complete reference, please see the online documentation at
  # https://docs.vagrantup.com.

  # Every Vagrant development environment requires a box. You can search for
  # boxes at https://vagrantcloud.com/search.

  ### CHAPTER - 3
  # config.vm.box = "ubuntu/focal64"
  # config.vm.hostname = "testserver"
  # config.vm.network "forwarded_port", id: 'ssh', guest: 22, host: 2202, host_ip: "127.0.0.1", auto_correct: false
  # config.vm.network "forwarded_port", id: 'http', guest: 80, host: 8080, host_ip: "127.0.0.1"
  # config.vm.network "forwarded_port", id: 'https', guest: 443, host: 8443, host_ip: "127.0.0.1"
  # if Vagrant.has_plugin?("vagrant-vbguest")
  #   config.vbguest.auto_update = false
  # end
  # config.vm.provider "virtualbox" do |virtualbox|
  #   virtualbox.name = "ch03"
  # end
  ### END CHAPTER - 3 

  ### CHAPTER - 4
  # Использовать один и тот же ключ для всех машин
  config.ssh.insert_key = false

  config.vm.define "ubuntu_2404" do |ubuntu_2404|
    config.vm.box = "ubuntu_bento-24.04"
    # config.vm.box_url = "https://app.vagrantup.com/generic/boxes/ubuntu2404"

    ubuntu_2404.vm.network "forwarded_port", guest: 80, host: 8080
    ubuntu_2404.vm.network "forwarded_port", guest: 443, host: 8443



     # Add public key
     # ssh-keygen -t ed25519 -f ~/.ssh/runner_vagrant_key
  config.vm.provision "shell", env: {
    "RUNNER_PUBKEY" => File.read(File.expand_path("~/.ssh/runner_vagrant_key.pub")).strip
  }, inline: <<-SHELL
    set -eux

    # Установка нужных пакетов
    apt-get update
    apt-get install -y nginx curl jq

    # Создание пользователя runner
    groupadd -f runner
    useradd -m -g runner -G sudo -s /bin/bash runner
    echo 'runner:superpassword' | chpasswd

    # SSH-доступ по ключу
    mkdir -p /home/runner/.ssh
    echo "$RUNNER_PUBKEY" > /home/runner/.ssh/authorized_keys
    chmod 700 /home/runner/.ssh
    chmod 600 /home/runner/.ssh/authorized_keys
    chown -R runner:runner /home/runner/.ssh

    # Создание скрипта weather.sh
    cat > /home/runner/weather.sh << 'EOF'
#!/bin/bash
CITY=$1
echo "<HTML><BODY>"
date
curl -s https://wttr.in/${CITY}?format=j1 | jq '.["current_condition"][0] | .temp_C,.humidity'
echo "</BODY></HTML>"
EOF

    chmod +x /home/runner/weather.sh
    chown runner:runner /home/runner/weather.sh

    # Разрешение runner писать в index.nginx-debian.html
    chmod a+w /var/www/html/index.nginx-debian.html

    # Добавление задания в crontab от имени runner
    echo '* * * * * /home/runner/weather.sh Samara > /var/www/html/index.nginx-debian.html 2>/home/runner/weather.err' > /tmp/runner_cron
    crontab -u runner /tmp/runner_cron

    # Перезапуск служб
    systemctl restart cron
    systemctl restart nginx
  SHELL

  end

  # config.vm.define "vagrant1" do |vagrant1|
  #   vagrant1.vm.box = "ubuntu/focal64"
  #   vagrant1.vm.network "forwarded_port", guest: 80, host: 8080
  #   vagrant1.vm.network "forwarded_port", guest: 443, host: 8443
  # end

  # config.vm.define "vagrant2" do |vagrant2|
  # vagrant2.vm.box = "ubuntu/focal64"
  #   vagrant2.vm.network "forwarded_port", guest: 80, host: 8081
  #   vagrant2.vm.network "forwarded_port", guest: 443, host: 8444
  # end

  # config.vm.define "vagrant3" do |vagrant3|
  #   vagrant3.vm.box = "centos/stream8"
  #   vagrant3.vm.box_url = "https://cloud.centos.org/centos/8/vagrant/x86_64/images/CentOS-8-Vagrant-8.4.2105-20210603.0.x86_64.vagrant-virtualbox.box"

  #   vagrant3.vm.network "forwarded_port", guest: 80, host: 8082
  #   vagrant3.vm.network "forwarded_port", guest: 443, host: 8445
  # end
  ### END CHAPTER - 4
  # Disable automatic box update checking. If you disable this, then
  # boxes will only be checked for updates when the user runs
  # `vagrant box outdated`. This is not recommended.
  # config.vm.box_check_update = false

  # Create a forwarded port mapping which allows access to a specific port
  # within the machine from a port on the host machine. In the example below,
  # accessing "localhost:8080" will access port 80 on the guest machine.
  # NOTE: This will enable public access to the opened port
  # config.vm.network "forwarded_port", guest: 80, host: 8080

  # Create a forwarded port mapping which allows access to a specific port
  # within the machine from a port on the host machine and only allow access
  # via 127.0.0.1 to disable public access
  # config.vm.network "forwarded_port", guest: 80, host: 8080, host_ip: "127.0.0.1"

  # Create a private network, which allows host-only access to the machine
  # using a specific IP.
  # config.vm.network "private_network", ip: "192.168.33.10"

  # Create a public network, which generally matched to bridged network.
  # Bridged networks make the machine appear as another physical device on
  # your network.
  # config.vm.network "public_network"

  # Share an additional folder to the guest VM. The first argument is
  # the path on the host to the actual folder. The second argument is
  # the path on the guest to mount the folder. And the optional third
  # argument is a set of non-required options.
  # config.vm.synced_folder "../data", "/vagrant_data"

  # Disable the default share of the current code directory. Doing this
  # provides improved isolation between the vagrant box and your host
  # by making sure your Vagrantfile isn't accessable to the vagrant box.
  # If you use this you may want to enable additional shared subfolders as
  # shown above.
  # config.vm.synced_folder ".", "/vagrant", disabled: true

  # Provider-specific configuration so you can fine-tune various
  # backing providers for Vagrant. These expose provider-specific options.
  # Example for VirtualBox:
  #
  # config.vm.provider "virtualbox" do |vb|
  #   # Display the VirtualBox GUI when booting the machine
  #   vb.gui = true
  #
  #   # Customize the amount of memory on the VM:
  #   vb.memory = "1024"
  # end
  #
  # View the documentation for the provider you are using for more
  # information on available options.

  # Enable provisioning with a shell script. Additional provisioners such as
  # Ansible, Chef, Docker, Puppet and Salt are also available. Please see the
  # documentation for more information about their specific syntax and use.
  # config.vm.provision "shell", inline: <<-SHELL
  #   apt-get update
  #   apt-get install -y apache2
  # SHELL
end
