#!/bin/bash
# Ansible - Automation engine
# Run Ansible playbooks and commands

PLAYBOOK="$2"
HOSTS="${3:-localhost}"
USER="${4:-root}"

usage() {
    cat << 'EOF'
Ansible - Automation Engine
Usage: ansible <command> [playbook] [hosts] [user]

Commands:
  ping <hosts>        Ping hosts
  list <hosts>        List hosts
  run <playbook>      Run playbook
  facts <hosts>       Gather facts
  copy <hosts>        Copy files
  command <hosts>     Run command
  reboot <hosts>      Reboot hosts

Examples:
  ansible ping all
  ansible run site.yml webserver
  ansible facts production
EOF
}

export ANSIBLE_HOST_KEY_CHECKING=False

case "$1" in
    ping)   ansible all -m ping -i "$HOSTS," ;;
    list)   ansible-inventory -i "$HOSTS," --list ;;
    run)    
        if [ -z "$PLAYBOOK" ]; then
            echo "Error: playbook required"
            exit 1
        fi
        ansible-playbook -i "$HOSTS," "$PLAYBOOK" ;;
    facts)  ansible "$HOSTS" -m setup ;;
    command) ansible "$HOSTS" -m command -a "$3" ;;
    copy)   
        SRC="$3"
        DST="$4"
        ansible "$HOSTS" -m copy -a "src=$SRC dest=$DST" ;;
    reboot) ansible "$HOSTS" -m reboot ;;
    *)      usage ;;
esac
