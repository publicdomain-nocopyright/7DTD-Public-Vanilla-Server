import psutil

def get_system_info():

    # Get CPU usage as a percentage
    cpu_percent = psutil.cpu_percent()

    # Get RAM usage in bytes
    ram_usage = psutil.virtual_memory()
    total_ram = ram_usage.total
    available_ram = ram_usage.available
    ram_percent = (total_ram - available_ram) / total_ram * 100

    return {
        "cpu_percent": cpu_percent,
        "ram_percent": ram_percent
    }

import sys
# Replace the module with the function
sys.modules[__name__] = get_system_info