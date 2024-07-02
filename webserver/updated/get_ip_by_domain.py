import socket

def get_ip_by_domain(domain):
    return socket.gethostbyname(domain)

# Example usage:
domain = "vanillaserver.eu"
ip_address = get_ip_by_domain(domain)
print(ip_address)
