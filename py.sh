#!/bin/bash

function dep_install {
    yes|apt install wget curl zlib1g-dev libreadline-gplv2-dev libncurses5-dev libssl-dev libsqlite3-dev tk-dev libgdbm-dev libc6-dev libbz2-dev llvm libncurses5-dev xz-utils tk-dev libxml2-dev libxmlsec1-dev
    mkdir -p $HOME/.sdkman/candidates/python/
    cd $HOME/.sdkman/candidates/python/ && wget https://bootstrap.pypa.io/get-pip.py
}

function install_eight {
    cd $HOME/.sdkman/candidates/python/3.8.15
    wget https://www.python.org/ftp/python/3.8.15/Python-3.8.15.tar.xz

    tar -xvf Python-3.8.15.tar.xz
    cd Python-3.8.15 && ./configure && make && make install && ./python $HOME/.sdkman/candidates/python/get-pip.py

    echo "#!/bin/bash" >> /bin/py_eight
    echo "$HOME/.sdkman/candidates/python/3.8.15/python $@" >> /bin/py_eight
}

function install_nine {
    mkdir -p $HOME/.sdkman/candidates/python/3.9.18
    cd $HOME/.sdkman/candidates/python/3.9.18
    wget https://www.python.org/ftp/python/3.9.18/Python-3.9.18.tar.xz

    tar -xvf Python-3.9.18.tar.xz
    cd Python-3.9.18 && ./configure && make && make install && ./python $HOME/.sdkman/candidates/python/get-pip.py

    echo "#!/bin/bash" >> /bin/py_nine
    echo "$HOME/.sdkman/candidates/python/3.9.18/python $@" >> /bin/py_nine
}

function install_ten {
    mkdir -p $HOME/.sdkman/candidates/python/3.10.13
    cd $HOME/.sdkman/candidates/python/3.10.13
    wget https://www.python.org/ftp/python/3.10.13/Python-3.10.13.tar.xz

    tar -xvf Python-3.10.13.tar.xz
    cd Python-3.10.13 && ./configure && make && make install && ./python $HOME/.sdkman/candidates/python/get-pip.py

    echo "#!/bin/bash" >> /bin/py_ten
    echo "$HOME/.sdkman/candidates/python/3.10.13/python $@" >> /bin/py_ten
}

function install_eleven {
    mkdir -p $HOME/.sdkman/candidates/python/3.11.6
    cd $HOME/.sdkman/candidates/python/3.11.6
    wget https://www.python.org/ftp/python/3.11.6/Python-3.11.6.tar.xz

    tar -xvf Python-3.11.6.tar.xz
    cd Python-3.11.6 && ./configure && make && make install && ./python $HOME/.sdkman/candidates/python/get-pip.py

    echo "#!/bin/bash" >> /bin/py_leven
    echo "$HOME/.sdkman/candidates/python/3.11.6/python $@" >> /bin/py_leven
}


# https://tldp.org/HOWTO/Bash-Prog-Intro-HOWTO-9.html#ss9.1

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