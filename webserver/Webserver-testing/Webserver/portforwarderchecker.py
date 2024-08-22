import subprocess
import time
import socket
import os

def get_internal_ip():
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    try:
        s.connect(('8.8.8.8', 80))
        ip = s.getsockname()[0]
    finally:
        s.close()
    return ip

def check_port_forwarding():
    result = subprocess.run(
        ['upnpc-static', '-l'],
        capture_output=True,
        text=True,
        creationflags=subprocess.CREATE_NO_WINDOW
    )
    return '80->' in result.stdout

def add_port_forwarding():
    local_ip = get_internal_ip()
    subprocess.run(
        ['upnpc-static', '-a', local_ip, '80', '80', 'TCP'],
        creationflags=subprocess.CREATE_NO_WINDOW
    )
    subprocess.run(
        ['upnpc-static', '-a', local_ip, '80', '80', 'UDP'],
        creationflags=subprocess.CREATE_NO_WINDOW
    )

def main():
    while True:
        if check_port_forwarding():
            print("Port 80 is forwarded.")
        else:
            print("Port 80 is not forwarded. Adding the rule...")
            add_port_forwarding()
        
        print(get_internal_ip())
        time.sleep(5)

if __name__ == '__main__':
    main()
