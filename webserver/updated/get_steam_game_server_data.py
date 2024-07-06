import a2s
import socket

#TODO: Make default argument the public ip of current machine.

def get_steam_game_server_data(server_address = ("93.49.104.86", 26900)):
    try:
        rules = a2s.rules(server_address, timeout=3.0, encoding="utf-8")
    except socket.timeout:
        print("[Webserver] [a2s] [Error] Request timed out")
        return None
    except Exception as e:
        print("[Webserver] [a2s] [Error]", e)
        return None
    return rules

import sys, os
sys.modules[__name__] = get_steam_game_server_data # os.path.basename(__file__)[:-3]()


if __name__ == "__main__":
    # Code to execute only when run directly
    print("Script is running directly.")

    #print(get_steam_game_server_data()["CurrentServerTime"])
    #print(get_steam_game_server_data()["CurrentPlayers"])
    import time

    def get_value():
        return int(get_steam_game_server_data()["CurrentServerTime"])

    current_value = get_value()
    start_time = time.time()

    while True:
        #print(a2s.players(("93.49.104.86", 26900)))
        new_value = get_value()
        if new_value != current_value:
            end_time = time.time()
            print(f"Value changed after {end_time - start_time} seconds.")
            current_value = new_value
            start_time = end_time
        print(current_value)
        time.sleep(1)  

