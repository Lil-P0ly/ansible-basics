#!/usr/bin/env python3
""" Сценарий динамического инвентаря Vagrant для Ansible """

import argparse
import io
import json
import subprocess
import sys
import paramiko


def parse_args():
    """Обработка аргументов командной строки"""
    parser = argparse.ArgumentParser(description="Vagrant inventory script")
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument('--list', action='store_true', help="Получить список работающих хостов")
    group.add_argument('--host', help="Получить детали конкретного хоста")
    return parser.parse_args()


def list_running_hosts():
    """Возвращает список работающих хостов"""
    cmd = ["vagrant", "status", "--machine-readable"]
    status = subprocess.check_output(cmd).decode("utf-8")
    hosts = []
    for line in status.strip().splitlines():
        parts = line.split(',')
        if len(parts) >= 4:
            _, host, key, value = parts[:4]
            if key == 'state' and value == 'running':
                hosts.append(host)
    return hosts


def get_host_details(host):
    """Возвращает SSH-параметры хоста"""
    cmd = ["vagrant", "ssh-config", host]
    ssh_config = subprocess.check_output(cmd).decode("utf-8")
    config = paramiko.SSHConfig()
    config.parse(io.StringIO(ssh_config))
    host_config = config.lookup(host)
    return {
        'ansible_host': host_config['hostname'],
        'ansible_port': int(host_config['port']),
        'ansible_user': host_config['user'],
        'ansible_private_key_file': host_config['identityfile'][1]
    }


def main():
    args = parse_args()
    if args.list:
        hosts = list_running_hosts()
        inventory = {
            'vagrant': {
                'hosts': hosts,
                'vars': {}
            }
        }
        json.dump(inventory, sys.stdout, indent=2)
    else:
        details = get_host_details(args.host)
        json.dump(details, sys.stdout, indent=2)


if __name__ == '__main__':
    main()
