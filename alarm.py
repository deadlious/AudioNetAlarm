"""
This script will play a sound once connection to a certain host is restored.

Usage: python alarm.py [--host <host_name>] [--alarm-sound <path_to_file>] [-t <timeout_in_secs>] [-v]
or   : alarm.exe [--host <host_name>] [--alarm-sound <path_to_file>] [-t <timeout_in_secs>] [-v]


Command line options
    --host <host>       : hostname to ping (default: google.com)
    --alarm-sound <path>: Path to an MP3 or WAV file (default: first mp3 file in the same folder)
    -t <timeout>        : timeout between pings (default 5 secs)
    -v                  : verbose output
    --help, -h          : print this information
"""

import os
import sys
import platform    # For getting the operating system name
import subprocess  # For executing a shell command
from time import sleep
from playsound import playsound


def ping(_host, _count_param, _timeout, _debug):
    print(f"Pinging host {_host}...")

    while p := subprocess.run(['ping', _count_param, '1', _host], capture_output=True):
        if p.returncode == 0 and p.stdout.decode().find('unreachable') == -1:
            break
        if _debug:
            print(p.stdout.decode())
        sleep(_timeout)
        print(f"Host {_host} is unreachable...")

    if _debug:
        print(p.stdout.decode())

    print(f'Host {_host} is online...')


if __name__ == '__main__':
    if '--help' in sys.argv or '-h' in sys.argv:
        print(__doc__)
    else:
        if platform.system().lower() == 'windows':
            count_param = '-n'
            press_any_cmd = 'pause'
        else:
            count_param = '-c'
            press_any_cmd = 'read -p "Press any key to continue..." -n 1 -s && echo'
        host = sys.argv[sys.argv.index('--host')+1] if '--host' in sys.argv else 'google.com'
        timeout = int(sys.argv[sys.argv.index('-t')+1]) if '-t' in sys.argv else 5
        if '--alarm-sound' in sys.argv:
            alarm_sound = [sys.argv[sys.argv.index('--alarm-sound')+1]]
        else:
            alarm_sound = [_ for _ in os.listdir() if _.casefold().find('.mp3') > -1]
        debug = '-v' in sys.argv

        ping(host, count_param, timeout, debug)

        if alarm_sound:
            playsound(alarm_sound[0], block=False)
        else:
            print("No sound file found... Running in silent mode.")

        subprocess.run([press_any_cmd], shell=True)
