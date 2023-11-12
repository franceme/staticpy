#!/bin/bash

#https://version.cs.vt.edu/rhunter/cs-linux-hardening-script/-/blob/master/linux_security_update.sh 

# Variables #
#pw_Age="730" # 2 Years
pw_Age="1825" # 5 Years

# Initial clear screen to keep things tidy.
clear

# OS Detection
OS_Detection() {
  echo
  echo -n "Detecting Operating System..."
  lsbTest=`which lsb_release 2> /dev/null`
  if [ -z "$lsbTest" ]; then
    yum -y install redhat-lsb-core &> /dev/null
  fi
  os_test=`lsb_release -d`
  OS_V=`lsb_release -r | sed -e "s/\..*//g" -e "s/.*\t//g"`
  os_ubuntu=`echo ${os_test} | grep -i ubuntu`
  os_centos=`echo ${os_test} | grep -i centos`
  if [ ! -z "${os_ubuntu}" ]; then
    OS="ubuntu"
  elif [ ! -z "${os_centos}" ]; then
    OS="centos"
  else
    echo "This script only supports ubuntu and centos."
    echo "We have detected you are running: $os_test"
    exit
  fi
  echo "$OS" "$OS_V"
}

# Firewall
check_Firewall() {
  echo
  echo -n "Checking Firewall..."
  if [ "$OS" == "ubuntu" ]; then
    ufw_test=`ufw status | grep inactive`
    if [ ! -z "$ufw_test" ]; then
      echo "Warning UFW is not running!"
      echo "Limiting SSH access on port 22"
      ufw limit ssh
      open_more=1
      while [ ! -z "$open_more" ]; do
        echo
        echo -n "If you have another port that need access enter the port number (Press Enter of none): "
        read open_more
        if [ ! -z "$open_more" ]; then
          ufw allow ${open_more}
        fi
      done
      ufw enable
    else
      echo "Firewall already exists"
      ufw status
    fi
  elif [ "$OS" == "centos" ]; then
    fwTest=`which firewall-cmd 2> /dev/null`
    if [ -z "$fwTest" ]; then
      echo "firewall-cmd not found.  Checking for iptables..."
      iptables -L
    else
      echo "firewalld found"
      echo -n "Firewalld State: "
      fwState=`firewall-cmd --state`
      # echo "$fwState"
      if [ "running" == "$fwState" ]; then
        open_more=1
        while [ ! -z "$open_more" ]; do
          echo
          echo -n "If you have another port that needs access enter the port number (Press Enter of none): "
          read open_more
          if [ ! -z "$open_more" ]; then
            firewall-cmd --permanent --zone=public --add-port=${open_more}
          fi
        done
        firewall-cmd --reload
        firewall-cmd --list-all
      else
        echo -n "Checking for IPTABLES: "
        iptfwState=`systemctl status iptables | grep dead`
        if [ -z "$iptfwState" ]; then
          echo "Running"
          echo "Listing your IPTABLES rules:"
          iptables -L
        else
          echo "FAILED!!!"
          echo "You do not appear to be running a firewall.  Please check and enable it, then re-run this script."
        fi 
      fi
    fi
  fi
}

# Password Length/Age/Complexity
check_PW_Complexity() {
  echo
  echo -n "Updating Password Complexity..."
  if [ "$OS" == "ubuntu" ]; then
    apt update &> /dev/null
    apt -y install libpam-pwquality &> /dev/null
    sed -e "s/pam_pwquality.so retry=3/pam_pwquality.so retry=4 minlen=8 minclass=3 difok=4 lcredit=-1 ucredit=-1 dcredit=-1 ocredit=-1 reject_username enforce_for_root/" -i /etc/pam.d/common-password
  elif [ "$OS" == "centos" ]; then
    if [ "$OS_V" == "7" ]; then
      authconfig --enablereqlower --enablerequpper --enablereqdigit --enablereqother --passminlen=8 --passminclass=3 --passmaxrepeat=4 --update 2> /dev/null
    else
      authconfig --enablereqlower --enablerequpper --enablereqdigit --enablereqother --passminlen=8 --passminclass=3 --passmaxrepeat=4 --update 2> /dev/null
    fi
  fi
  echo "Done"
}

check_PW_Age() {
  echo
  echo -n "Checking Password Age Rules..."
  age_Test=`grep "PASS_MAX_DAYS ${pw_Age}" /etc/login.defs`
  if [ -z "$age_Test" ]; then
    echo -n "Updating..."
    sed -e "s/^PASS_MAX_DAYS.*/PASS_MAX_DAYS ${pw_Age}/g" -e "s/^PASS_WARN_AGE.*/PASS_WARN_AGE 14/g" -i /etc/login.defs
  else
    echo -n "Already Configured..."
  fi
  echo "Done"
}

# Auto Patch
check_Auto_Updates() {
  echo
  echo -n "Checking for Automatic Updates..."
  if [ "$OS" == "ubuntu" ]; then
    if [ ! -f /etc/apt/apt.conf.d/50unattended-upgrades ]; then
      echo -n "Installing..."
      apt update &> /dev/null
      apt -y install unattended-upgrades &> /dev/null
      dpkg-reconfigure -fnoninteractive -plow unattended-upgrades
    else
      echo -n "Already Enabled..."
      daemonStatus=`systemctl status unattended-upgrades.service 2> /dev/null | grep running`
      if [ ! -z "$daemonStatus" ]; then
        echo -n "Running..."
      else
        echo "NOT Running!!!"
        echo "Try Enabling the service (service unattended-upgrades restart)"
        exit
      fi
    fi
  elif [ "$OS" == "centos" ]; then
    if [ "$OS_V" == "7" ]; then
      if [ ! -r /etc/yum/yum-cron.conf ]; then
        echo -n "Installing..."
        yum -y install yum-cron &> /dev/null
        autoTest=`grep "apply_updates = yes" /etc/yum/yum-cron.conf`
        if [ -z "$autoTest" ]; then
          echo -n "Configuring..."
          sed -e "s/update_cmd = default/update_cmd = security/g" -e "s/apply_updates = no/apply_updates = yes/g" -i /etc/yum/yum-cron.conf
        else
          echo -n "Already Configured..."
        fi
        systemctl enable yum-cron
        systemctl restart yum-cron
      else
        echo -n "Already Installed..."
      fi
    else
      if [ ! -r /etc/dnf/automatic.conf ]; then
        echo -n "installing dnf-automatic..."
        dnf -y install dnf-automatic &> /dev/null
      else
        echo -n "Already Installed..."
      fi
      dnf_Test=`grep "apply_updates = yes" /etc/dnf/automatic.conf`
      if [ -z "$dnf_Test" ]; then
        echo -n "Configuring..."
        sed -e "s/apply_updates = no/apply_updates = yes/" -i /etc/dnf/automatic.conf
      fi

    fi
  fi
  echo "Done"
}

# SSH disable root password
disableRootSSH() {
  echo
  echo -n "Checking SSH config: "
  sshRootCK=`grep -i "^PermitRootLogin" /etc/ssh/sshd_config`
  if [ -z "$sshRootCK" ]; then
    echo "Fixed"
    echo "PermitRootLogin without-password" >> /etc/ssh/sshd_config
    service sshd restart
  elif [ ! "$sshRootCK" == "PermitRootLogin without-password" ]; then
    echo "Fixed"
    sed -e "s/^PermitRootLogin.*/PermitRootLogin without-password/" -i /etc/ssh/sshd_config
    service sshd restart
  else
    echo "Already Configured"
  fi
}

installFail2Ban() {
  echo
  echo -n "Checking for Fail2Ban..."
  if [ "$OS" == "ubuntu" ]; then
    if [ -r /etc/fail2ban/fail2ban.conf ]; then
      echo -n "Already installed..."
    else
      echo -n " fail2ban..."
      DEBIAN_FRONTEND=noninteractive apt -y install fail2ban &> /dev/null
    fi
  else
    if [ -r /etc/fail2ban/fail2ban.conf ]; then
      echo -n "Already installed..."
    else
      echo -n "Installing EPEL"
      yum -y install epel-release &> /dev/null
      echo -n " fail2ban..."
      yum -y install fail2ban &> /dev/null
      echo -n "Enabling..."
      systemctl enable fail2ban &> /dev/null
      echo -n "Starting Service..."
      service restart fail2ban &> /dev/null
    fi
  fi
  echo "Done"
}

################
# Main Program #
################
OS_Detection
check_Firewall
check_PW_Complexity
check_PW_Age
check_Auto_Updates
disableRootSSH
installFail2Ban
