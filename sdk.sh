#!/bin/bash

function full_install {
    curl -s "https://get.sdkman.io" | bash
}

function sourcing {
    full_install
    source "$HOME/.sdkman/bin/sdkman-init.sh"
    sdk update
}

function install_gradle {
    sourcing
    yes|sdk i gradle 6.0
}

function install_seven {
    sourcing

    IS_INSTALLED=$(sdk ls java|grep zulu|grep ' 7.0'|head -n 1)
    HAS_INSTALLED='installed'

    if echo "$IS_INSTALLED" | grep -q -E "$HAS_INSTALLED"; then
        echo "Java JDK Version already installed";
        exit 0
    fi

    VAR=$(sdk ls java|grep zulu|grep ' 7.0'|head -n 1|awk -F ' ' '{print $8}')
    yes|sdk i java $VAR
    export JAVA7_HOME="$HOME/.sdkman/candidates/java/$VAR/"
    echo "export JAVA7_HOME=$JAVA7_HOME" >> $HOME/.bashrc
    echo "JAVA7_HOME=$JAVA7_HOME" >> /opt/java.env
    echo "JAVA7_HOME=$JAVA7_HOME" >> $HOME/.sdkman/manual.env
    echo "export JAVA7_HOME=$JAVA7_HOME" >> $HOME/.bash_aliases
    echo "export JAVA7=$JAVA7_HOME/bin/java" >> $HOME/.bashrc
    echo "JAVA7=$JAVA7_HOME/bin/java" >> /opt/java.env
    echo "JAVA7=$JAVA7_HOME/bin/java" >> $HOME/.sdkman/manual.env
    echo "export JAVA7=$JAVA7_HOME/bin/java" >> $HOME/.bash_aliases


    #sudo echo "#!/usr/bin/env python" >> /bin/java_seven
    #sudo echo "import os,sys" >> /bin/java_seven
    #sudo echo "cmd = '$HOME/.sdkman/candidates/java/$VAR/bin/java ' + ' '.join(sys.argv)" >> /bin/java_seven
    #sudo echo "print(cmd);os.system(cmd)" >> /bin/java_seven
    ##sudo echo "$HOME/.sdkman/candidates/java/$VAR/bin/java $@" >> /bin/java_seven
    #sudo chmod 777 /bin/java_seven

    JPATH=/opt/java_seven

    echo "#!/bin/bash" >> $JPATH
    echo "$HOME/.sdkman/candidates/java/$VAR/bin/java $@" >> $JPATH
    chmod 777 $JPATH
}

function install_eight {
    sourcing

    IS_INSTALLED=$(sdk ls java|grep zulu|grep ' 8.0'|head -n 1)
    HAS_INSTALLED='installed'

    if echo "$IS_INSTALLED" | grep -q -E "$HAS_INSTALLED"; then
        echo "Java JDK Version already installed";
        exit 0
    fi

    VAR=$(sdk ls java|grep zulu|grep ' 8.0'|head -n 1|awk -F ' ' '{print $8}')
    yes|sdk i java $VAR
    export JAVA8_HOME="$HOME/.sdkman/candidates/java/$VAR/"
    echo "export JAVA8_HOME=$JAVA8_HOME" >> $HOME/.bashrc
    echo "JAVA8_HOME=$JAVA8_HOME" >> /opt/java.env
    echo "JAVA8_HOME=$JAVA8_HOME" >> $HOME/.sdkman/manual.env
    echo "export JAVA8_HOME=$JAVA8_HOME" >> $HOME/.bash_aliases
    echo "export JAVA8=$JAVA8_HOME/bin/java" >> $HOME/.bashrc
    echo "JAVA8=$JAVA8_HOME/bin/java" >> /opt/java.env
    echo "JAVA8=$JAVA8_HOME/bin/java" >> $HOME/.sdkman/manual.env
    echo "export JAVA8=$JAVA8_HOME/bin/java" >> $HOME/.bash_aliases

    JPATH=/opt/java_eight

    echo "#!/bin/bash" >> $JPATH
    echo "$HOME/.sdkman/candidates/java/$VAR/bin/java $@" >> $JPATH
    chmod 777 $JPATH
}

function install_leven {
    sourcing

    IS_INSTALLED=$(sdk ls java|grep zulu|grep '11.0'|head -n 1)
    HAS_INSTALLED='installed'

    if echo "$IS_INSTALLED" | grep -q -E "$HAS_INSTALLED"; then
        echo "Java JDK Version already installed";
        exit 0
    fi

    VAR=$(sdk ls java|grep zulu|grep '11.0'|head -n 1|awk -F ' ' '{print $8}')
    yes|sdk i java $VAR
    export JAVA11_HOME="$HOME/.sdkman/candidates/java/$VAR/"
    echo "export JAVA11_HOME=$JAVA11_HOME" >> $HOME/.bashrc
    echo "JAVA11_HOME=$JAVA11_HOME" >> /opt/java.env
    echo "JAVA11_HOME=$JAVA11_HOME" >> $HOME/.sdkman/manual.env
    echo "export JAVA11_HOME=$JAVA11_HOME" >> $HOME/.bash_aliases
    echo "export JAVA11=$JAVA11_HOME/bin/java" >> $HOME/.bashrc
    echo "JAVA11=$JAVA11_HOME/bin/java" >> /opt/java.env
    echo "JAVA11=$JAVA11_HOME/bin/java" >> $HOME/.sdkman/manual.env
    echo "export JAVA11=$JAVA11_HOME/bin/java" >> $HOME/.bash_aliases

    JPATH=/opt/java_leven

    echo "#!/bin/bash" >> $JPATH
    echo "$HOME/.sdkman/candidates/java/$VAR/bin/java $@" >> $JPATH
    chmod 777 $JPATH
}


# https://tldp.org/HOWTO/Bash-Prog-Intro-HOWTO-9.html#ss9.1
echo usage: $0 "all | eight | seven | eleven"
OPTIONS="all eight seven eleven"
if [ -z "$1" ]; then 
    echo usage: $0 "all | eight | seven | eleven"
    exit
fi

if [ $1 == "all" ]; then
echo "Installing sdkman" && full_install
echo "Installing Gradle" && install_gradle
fi

if [ $1 == "seven" ] || [ $1 == "all" ]; then
echo "Installing jdk 7" && install_seven
fi

if [ $1 == "eight" ] || [ $1 == "all" ]; then
echo "Installing java jdk 8" && install_eight
fi

if [ $1 == "eleven" ] || [ $1 == "all" ]; then
echo "Installing java jdk 11" && install_leven
fi

exit 0