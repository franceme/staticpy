#!/bin/bash

function full_install {
    curl -s "https://get.sdkman.io" | bash
}

function sourcing {
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

    echo "#!/bin/bash" >> /bin/java_seven
    echo "$HOME/.sdkman/candidates/java/$VAR/bin/java $@" >> /bin/java_seven
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

    echo "#!/bin/bash" >> /bin/java_eight
    echo "$HOME/.sdkman/candidates/java/$VAR/bin/java $@" >> /bin/java_eight
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

    echo "#!/bin/bash" >> /bin/java_leven
    echo "$HOME/.sdkman/candidates/java/$VAR/bin/java $@" >> /bin/java_leven
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