#!/bin/bash

function dep_install {
    yes| apt install -y wget curl gcc make
    yes| apt install -y zlib1g-dev
    yes| apt install -y libreadline-gplv2-dev
    yes| apt install -y libncurses5-dev
    yes| apt install -y libssl-dev
    yes| apt install -y libsqlite3-dev
    yes| apt install -y tk-dev
    yes| apt install -y libgdbm-dev
    yes| apt install -y libc6-dev
    yes| apt install -y libbz2-dev
    yes| apt install -y llvm
    yes| apt install -y libncurses5-dev
    yes| apt install -y xz-utils
    yes| apt install -y tk-dev
    yes| apt install -y libxml2-dev
    yes| apt install -y libxmlsec1-de
    mkdir -p $HOME/.sdkman/candidates/python/
    cd $HOME/.sdkman/candidates/python/ && wget https://bootstrap.pypa.io/get-pip.py
}

function install_eight {
    mkdir -p $HOME/.sdkman/candidates/python/3.8.15
    cd $HOME/.sdkman/candidates/python/3.8.15
    wget https://www.python.org/ftp/python/3.8.15/Python-3.8.15.tar.xz

    tar -xvf Python-3.8.15.tar.xz
    cd Python-3.8.15 && ./configure && make && make install && ./python $HOME/.sdkman/candidates/python/get-pip.py

    echo "#!/bin/bash" >> /bin/py_eight
    echo "$HOME/.sdkman/candidates/python/3.8.15/python $@" >> /bin/py_eight

    ln -s $HOME/.sdkman/candidates/python/3.8.15/ $HOME/.sdkman/candidates/python/current
    ln -s $HOME/.sdkman/candidates/python/current/python /bin/spy
}

function install_nine {
    mkdir -p $HOME/.sdkman/candidates/python/3.9.18
    cd $HOME/.sdkman/candidates/python/3.9.18
    wget https://www.python.org/ftp/python/3.9.18/Python-3.9.18.tar.xz

    tar -xvf Python-3.9.18.tar.xz
    cd Python-3.9.18 && ./configure && make && make install && ./python $HOME/.sdkman/candidates/python/get-pip.py

    echo "#!/bin/bash" >> /bin/py_nine
    echo "$HOME/.sdkman/candidates/python/3.9.18/python $@" >> /bin/py_nine

    ln -s $HOME/.sdkman/candidates/python/3.9.18/ $HOME/.sdkman/candidates/python/current
    ln -s $HOME/.sdkman/candidates/python/current/python /bin/spy
}

function install_ten {
    mkdir -p $HOME/.sdkman/candidates/python/3.10.13
    cd $HOME/.sdkman/candidates/python/3.10.13
    wget https://www.python.org/ftp/python/3.10.13/Python-3.10.13.tar.xz

    tar -xvf Python-3.10.13.tar.xz
    cd Python-3.10.13 && ./configure && make && make install && ./python $HOME/.sdkman/candidates/python/get-pip.py

    echo "#!/bin/bash" >> /bin/py_ten
    echo "$HOME/.sdkman/candidates/python/3.10.13/python $@" >> /bin/py_ten

    ln -s $HOME/.sdkman/candidates/python/3.10.13/ $HOME/.sdkman/candidates/python/current
    ln -s $HOME/.sdkman/candidates/python/current/python /bin/spy
}

function install_eleven {
    mkdir -p $HOME/.sdkman/candidates/python/3.11.6
    cd $HOME/.sdkman/candidates/python/3.11.6
    wget https://www.python.org/ftp/python/3.11.6/Python-3.11.6.tar.xz

    tar -xvf Python-3.11.6.tar.xz
    cd Python-3.11.6 && ./configure && make && make install && ./python $HOME/.sdkman/candidates/python/get-pip.py

    echo "#!/bin/bash" >> /bin/py_leven
    echo "$HOME/.sdkman/candidates/python/3.11.6/python $@" >> /bin/py_leven

    ln -s $HOME/.sdkman/candidates/python/3.11.6/ $HOME/.sdkman/candidates/python/current
    ln -s $HOME/.sdkman/candidates/python/current/python /bin/spy
}


# https://tldp.org/HOWTO/Bash-Prog-Intro-HOWTO-9.html#ss9.1
echo usage: $0 "all | eight | nine | ten | eleven"
OPTIONS="all eight nine ten eleven"
if [ -z "$1" ]; then 
    echo usage: $0 "all | eight | nine | ten | eleven"
    exit
fi

dep_install

if [ $1 == "eight" ] || [ $1 == "all" ]; then
echo "Installing python eight" && install_eight
fi

if [ $1 == "nine" ] || [ $1 == "all" ]; then
echo "Installing python nine" && install_nine
fi

if [ $1 == "ten" ] || [ $1 == "all" ]; then
echo "Installing python ten" && install_ten
fi

if [ $1 == "eleven" ] || [ $1 == "all" ]; then
echo "Installing python eleven" && install_eleven
fi

exit 0