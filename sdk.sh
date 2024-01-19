#!/bin/bash

function full_install {
    curl -s "https://get.sdkman.io" | bash
}

function sourcing {
    source "$HOME/.sdkman/bin/sdkman-init.sh"
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
}


# https://tldp.org/HOWTO/Bash-Prog-Intro-HOWTO-9.html#ss9.1

OPTIONS="all eight seven"
if [ -z "$1" ]; then 
    echo usage: $0 "all | eight | seven"
    exit
fi

if [ $1 == "all" ]; then
echo "Installing sdkman" && full_install
fi

if [ $1 == "seven" ] || [ $1 == "all" ]; then
echo "Installing jdk 7" && install_seven
fi

if [ $1 == "eight" ] || [ $1 == "all" ]; then
echo "Installing java jdk 8" && install_eight
fi

exit 0