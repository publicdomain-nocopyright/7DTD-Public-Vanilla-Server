import a2s

def get_steam_game_server_data(server_address = ("93.49.104.86", 26900)):
    rules = a2s.rules(server_address)
    return rules

import sys
# Replace the module with the function
sys.modules[__name__] = get_steam_game_server_data()