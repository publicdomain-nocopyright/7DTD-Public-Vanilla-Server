import a2s
import time

start_time = time.time()  # Record the program start time

last_check_time = last_fetch_time = fetched_time = 0

while True:
    try:
        current_time = time.time() - start_time  # Calculate current time since program start
        server_info = a2s.rules(("93.49.104.86", 26900))
        fetched = server_info.get("CurrentServerTime")
        
        if fetched is not None:
            fetched_time = int(fetched)
            if fetched_time > last_fetch_time:
                time_diff = current_time - last_check_time
                print(fetched, " ATime difference since last trigger:", time_diff)
                last_check_time = current_time
                last_fetch_time = fetched_time
                
        #print("Fetched time:", fetched_time, "Current time (seconds since program start):", current_time)
        print(fetched, " Time difference since last trigger:", current_time - last_check_time)
        time.sleep(1.1)
    except TimeoutError:
        print("Error: Connection timed out while fetching server rules.")
    except KeyError:
        print("Error: CurrentServerTime not found in server response.")
