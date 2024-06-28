
import requests


def get_public_ip():
    try:
        response = requests.get('https://api.ipify.org')
        if response.status_code == 200:
            return response.text
        else:
            return "Failed to retrieve public IP"
    except Exception as e:
        return "Error: " + str(e)
    

import sys
# Replace the module with the function
sys.modules[__name__] = get_public_ip