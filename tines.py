# from __future__ import print_function
import requests
import re
import sys
from subprocess import Popen, PIPE, STDOUT
import socket
"""Run `snort -A console` command using a pipe.
Warning! Alerts are delayed until snort's stdout buffer is flushed.
"""





host = '192.168.3.110' # Change this to the IP address of the Raspberry Pi
port = 12345
buf = 1024
tines = '' #enter your tines webhook here


def snort():
    # snort_process = Popen(['sudo','snort', '-b', '-l', '/var/log/snort/alert.log', '-c', '/usr/local/etc/snort/snort.lua' , '-R', '/usr/local/etc/rules/snort3-community.rules', '-i', 'ens18', ], #'-A', 'fast', '-l', '/var/log/snort/alert.log'],
    #                     stdout=PIPE, stderr=STDOUT, bufsize=1,
    #                     universal_newlines=True, close_fds=True)
    snort_process = Popen(['sudo','tail', '-n0', '-f', '/var/log/snort/alert_fast.txt' ], #'-A', 'fast', '-l', '/var/log/snort/alert.log'],
                        stdout=PIPE, stderr=STDOUT, bufsize=1,
                        universal_newlines=True, close_fds=True)
    with snort_process.stdout:
        print('snort started')
        for line in iter(snort_process.stdout.readline, ''):
            #XXX run python script here:
            #    `subprocess.call([sys.executable or 'python', '-m', 'your_module'])`
            # alert = 
            if re.search(r'(0?[1-9]|[12][0-9]|3[01]).*[0-9]+(([+-]?(?=\.\d|\d)(?:\d+)?(?:\.?\d*))(?:[eE]([+-]?\d+))?(:([+-]?(?=\.\d|\d)(?:\d+)?(?:\.?\d*))(?:[eE]([+-]?\d+))?)+).*\[.*\].*\[.*\].*".*".*\[.*\].*\[.*\].*\{.*\}', line):
                if '{ICMP' not in line:
                    send_tines(line)
    rc = snort_process.wait()


def send_tines(data):
    print(data)
    response = requests.post(
        tines,
        data=data,
        )
    addr = (host, port)
    UDPSock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

    UDPSock.sendto(bytes("flash", "utf-8"), addr)
    UDPSock.close()

snort()

