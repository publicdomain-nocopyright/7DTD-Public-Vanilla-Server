# Webserver needs to execute steam game server data function every 20 seconds
# This can be done by measuring time and checking if time has come to fetch again.
# Also can be achieved by having separate thread running that executes function every 20 seconds.
# Also can be achieved by asynchronity and fetching by delay of 20 seconds.