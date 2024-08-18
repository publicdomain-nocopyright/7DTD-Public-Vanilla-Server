import socket
import time

def check_port_connectable(host='localhost', port=26900):
    while True:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(5)  # Set a timeout for the connection attempt
        result = sock.connect_ex((host, port))

        if result == 0:
            print(f"Server on port {port} is online.")
        else:
            print(f"Server on port {port} is offline.")
            # Uncomment the next lines to remove the file if the server is offline
            # import os
            # if os.path.exists('Webserver_player_status.json'):
            #     os.remove('Webserver_player_status.json')
            #     print("Webserver_player_status.json has been deleted.")

        sock.close()
        time.sleep(4)

# Example usage
check_port_connectable()
