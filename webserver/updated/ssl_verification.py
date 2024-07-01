# HTTPS ssl Certification
# Generating self-signed ssl certificate
# https://sourceforge.net/projects/gnuwin32/files/openssl/0.9.8h-1/

# openssl req -x509 -newkey rsa:4096 -keyout key.pem -out cert.pem -days 365

# Note: Unable to load config info from /usr/local/ssl/openssl.cnf
#   Solution: .\openssl-0.9.8h-1-bin\share\openssl.cnf needs to be placed in C:/usr/local/ssl/openssl.cnf


import ssl
def enable_ssl(httpd, server_address):
    if server_address[1] == 443:
        context = ssl.SSLContext(ssl.PROTOCOL_TLS_SERVER)
        context.load_cert_chain('cert.pem', 'key.pem')
        httpd.socket = context.wrap_socket(httpd.socket, server_side=True)
        return httpd

    # Deprecated Python
    #httpd.socket = ssl.wrap_socket(httpd.socket,
    #                                    server_side=True,
    #                                    certfile='cert.pem',
    #                                    keyfile='key.pem',
    #                                    ssl_version=ssl.PROTOCOL_TLS)



    # Self-signed ssl certificate causes invalid authority error for Google Chrome
    # NET::ERR_CERT_AUTHORITY_INVALID
    # https://letsencrypt.org/
    # https://community.letsencrypt.org/t/certbot-discontinuing-windows-beta-support-in-2024/208101
    # https://certifytheweb.com/
    # https://www.win-acme.com/