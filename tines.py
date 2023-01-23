# from __future__ import print_function
import requests
import re

from subprocess import Popen, PIPE, STDOUT
"""Run `snort -A console` command using a pipe.
Warning! Alerts are delayed until snort's stdout buffer is flushed.
"""

#Insert Tines webhook URL here to send alerts to tines
tineswebhook = ''


def snort():
    # snort_process = Popen(['sudo','snort', '-b', '-l', '/var/log/snort/alert.log', '-c', '/usr/local/etc/snort/snort.lua' , '-R', '/usr/local/etc/rules/snort3-community.rules', '-i', 'ens18', ], #'-A', 'fast', '-l', '/var/log/snort/alert.log'],
    #                     stdout=PIPE, stderr=STDOUT, bufsize=1,
    #                     universal_newlines=True, close_fds=True)
    snort_process = Popen(['sudo','tail', '-f', '/var/log/snort/alert_fast.txt' ], #'-A', 'fast', '-l', '/var/log/snort/alert.log'],
                        stdout=PIPE, stderr=STDOUT, bufsize=1,
                        universal_newlines=True, close_fds=True)
    with snort_process.stdout:
        print('snort started')
        for line in iter(snort_process.stdout.readline, ''):
            #XXX run python script here:
            #    `subprocess.call([sys.executable or 'python', '-m', 'your_module'])`
            # alert = 
            if re.search(r'(0?[1-9]|[12][0-9]|3[01]).*[0-9]+(([+-]?(?=\.\d|\d)(?:\d+)?(?:\.?\d*))(?:[eE]([+-]?\d+))?(:([+-]?(?=\.\d|\d)(?:\d+)?(?:\.?\d*))(?:[eE]([+-]?\d+))?)+).*\[.*\].*\[.*\].*".*".*\[.*\].*\[.*\].*\{.*\}', line):
                send_tines(line)
    rc = snort_process.wait()


def send_tines(data):
   
    response = requests.post(
        tineswebhook,
        data=data,
    )

snort()

