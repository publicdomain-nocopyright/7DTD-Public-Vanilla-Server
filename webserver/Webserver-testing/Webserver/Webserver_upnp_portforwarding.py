
import socket
import requests
import subprocess
import sys
import os

def install_upnpy():
    print("Attempting to install upnpy...")
    try:
        subprocess.check_call([sys.executable, "-m", "pip", "install", "upnpy"])
        print("upnpy has been successfully installed.")
        print("Restarting the script...")
        os.execv(sys.executable, ['python'] + sys.argv)
    except subprocess.CalledProcessError:
        print("Failed to install upnpy automatically.")
        print("Please try to install it manually using the following steps:")
        print("1. Open a command prompt or terminal.")
        print("2. Run the following command:")
        print("   pip install upnpy")
        print("3. If that doesn't work, try:")
        print("   python -m pip install upnpy")
        print("4. If you're using a virtual environment, make sure it's activated before installing.")
        sys.exit(1)
    except PermissionError:
        print("Permission error occurred while trying to install upnpy.")
        print("Try running the script with administrator privileges or use:")
        print("pip install upnpy --user")
        sys.exit(1)

try:
    import upnpy
    print("upnpy is already installed.")
except ModuleNotFoundError:
    print("ModuleNotFoundError: No module named 'upnpy'")
    install_upnpy()

class UPnPPortMapper:
    def __init__(self):
        self.upnp = upnpy.UPnP()
        self.device = None
        self.service = None
        self.external_ip = None

    def get_local_ip(self):
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        try:
            s.connect(('10.255.255.255', 1))
            IP = s.getsockname()[0]
        except Exception:
            IP = '127.0.0.1'
        finally:
            s.close()
        return IP

    def find_port_mapping_service(self):
        common_service_names = [
            'WANIPConn1',
            'WANIPConnection.1',
            'WANPPPConnection.1',
            'WANIPConnection',
            'WANPPPConnection'
        ]
        
        for service in self.device.get_services():
            if service.id in common_service_names:
                return service
        
        for service in self.device.get_services():
            if 'IPConn' in service.id or 'PPPConn' in service.id:
                return service
        
        return None

    def setup(self):
        print("Discovering UPnP devices...")
        devices = self.upnp.discover()
        
        if not devices:
            print("No UPnP devices found.")
            return False
        
        print(f"Found {len(devices)} device(s).")
        
        self.device = self.upnp.get_igd()
        print(f"Using IGD: {self.device.friendly_name}")
        
        self.service = self.find_port_mapping_service()
        if not self.service:
            print("Could not find a suitable port mapping service.")
            return False
        
        print(f"Using service: {self.service.id}")

        # Get external IP address
        try:
            self.external_ip = self.service.GetExternalIPAddress()['NewExternalIPAddress']
            print(f"External IP: {self.external_ip}")
        except Exception as e:
            print(f"Could not get external IP: {e}")
            return False

        return True

    def add_port_mapping(self, external_port, internal_port, protocol='TCP', description='UPnPy Mapping'):
        if not self.service:
            print("Service not set up. Run setup() first.")
            return False

        local_ip = self.get_local_ip()
        print(f"\nAttempting to add port mapping: External Port {external_port} -> {local_ip}:{internal_port}")
        
        try:
            result = self.service.AddPortMapping(
                NewRemoteHost='',
                NewExternalPort=external_port,
                NewProtocol=protocol,
                NewInternalPort=internal_port,
                NewInternalClient=local_ip,
                NewEnabled=1,
                NewPortMappingDescription=description,
                NewLeaseDuration=0
            )
            
            if result == {}:
                print("Port mapping added successfully.")
                return True
            else:
                print(f"Unexpected result when adding port mapping: {result}")
                return False
        except Exception as e:
            print(f"Error adding port mapping: {e}")
            return False

    def check_port_mapping(self, external_port, protocol='TCP'):
        if not self.service:
            print("Service not set up. Run setup() first.")
            return False

        print(f"\nChecking if port mapping exists for external port {external_port}...")
        try:
            result = self.service.GetSpecificPortMappingEntry(
                NewRemoteHost='',
                NewExternalPort=external_port,
                NewProtocol=protocol
            )
            print(f"Port mapping found: {result}")
            return True
        except Exception as e:
            if isinstance(e.args[0], tuple) and e.args[0][1] == 714:
                print(f"No port mapping exists for external port {external_port}.")
            else:
                print(f"Error checking port mapping: {e}")
            return False
            
    def remove_port_mapping(self, external_port, protocol='TCP'):
        if not self.service:
            print("Service not set up. Run setup() first.")
            return False

        print(f"\nRemoving port mapping for external port {external_port}...")
        try:
            self.service.DeletePortMapping(
                NewRemoteHost='',
                NewExternalPort=external_port,
                NewProtocol=protocol
            )
            print("Port mapping removed successfully.")
            return True
        except Exception as e:
            print(f"Error removing port mapping: {e}")
            return False

    def test_external_port(self, external_port, timeout=10):
        if not self.external_ip:
            print("External IP not available. Run setup() first.")
            return False

        print(f"\nTesting external port {external_port} using a custom check...")
        
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(timeout)
        
        try:
            result = sock.connect_ex((self.external_ip, external_port))
            if result == 0:
                print(f"Port {external_port} is open and accessible from the internet.")
                return True
            else:
                print(f"Port {external_port} appears to be closed or not accessible from the internet.")
                print(f"Error code: {result}")
                return False
        except socket.error as e:
            print(f"An error occurred while testing the port: {e}")
            return False
        finally:
            sock.close()
            
            
    def verify_external_port(self, port, timeout=10):
       """
       Verify if a port is open externally using multiple methods.
       
       :param port: The port number to test
       :param timeout: Timeout for connection attempts (default 10 seconds)
       :return: True if the port is open, False otherwise
       """
       if not self.external_ip:
           print("External IP not available. Run setup() first.")
           return False

       print(f"Verifying if port {port} is open on {self.external_ip}...")

       # Method 1: Direct socket connection
       try:
           with socket.create_connection((self.external_ip, port), timeout=timeout) as sock:
               print(f"Successfully connected to {self.external_ip}:{port}")
               return True
       except (socket.timeout, ConnectionRefusedError):
           print(f"Could not connect directly to {self.external_ip}:{port}")

       # Method 2: Using an external port checking service
       #try:
       #    response = requests.get(f"https://portchecker.co/check", params={
       #        "port": port,
       #        "ip": self.external_ip
       #    }, timeout=timeout)
       #    if "open" in response.text.lower():
       #        print(f"External service reports {self.external_ip}:{port} is open")
       #        return True
       #    else:
       #        print(f"External service reports {self.external_ip}:{port} is closed")
       #except requests.RequestException as e:
       #    print(f"Error checking port using external service: {e}")
#
       ## If both methods fail, consider the port closed
       #print(f"Port {port} appears to be closed on {self.external_ip}")
       #return False
            



def main():
    try:            
        mapper = UPnPPortMapper()
        if mapper.setup():
            mapper.verify_external_port(80)

        if mapper.setup():
            if mapper.test_external_port(80):
                print("Port 80 is verified as open externally.")
            else:
                print("Port 80 is mapped but not accessible externally.")
            #input("Press Enter to continue...")
            if mapper.check_port_mapping(80):
                print("Port mapping exists.")
                if mapper.test_external_port(80):
                    print("Port 80 is verified as open externally.")
                else:
                    print("Port 80 is mapped but not accessible externally.")
                mapper.remove_port_mapping(80)
                if not mapper.check_port_mapping(80):
                   print("Successfully removed.")
            else:
                print("Port mapping does not exist.")          
                if mapper.add_port_mapping(80, 80):
                    print("Adding port")
                    if mapper.test_external_port(80):
                        print("Port 80 is now verified as open externally.")
                    else:
                        print("Port 80 was mapped but is not accessible externally.")
                else:
                    print("Failed to add port mapping.")
                
    except Exception as e:
        print(f"Error: {e}")

            
                        
if __name__ == "__main__":
    main()