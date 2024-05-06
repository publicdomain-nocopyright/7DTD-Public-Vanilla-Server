
from http.server import HTTPServer, BaseHTTPRequestHandler
import requests

class RedirectHandler(BaseHTTPRequestHandler):
    def get_system_info(self):
        import psutil
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



    log_file = open("server_log.txt", "a")  # Open the log file in append mode

    def log_message(self, format, *args):
        self.log_file.write("%s - - [%s] %s\n" %
                            (self.address_string(),
                            self.log_date_time_string(),
                            format % args))
        self.log_file.flush()

    def do_GET(self):
        self.log_message("GET %s", self.path)  # Log the incoming request
        
        import a2s
        import json
        if self.path == '/data':

            # Define the server address
            server_address = ("93.49.104.86", 26900)
            rules = a2s.rules(server_address)

            ticks_per_day = 24000
            total_ticks = int(rules["CurrentServerTime"])
            total_days = total_ticks // ticks_per_day
            remaining_ticks = total_ticks % ticks_per_day
            hours = remaining_ticks // 1000
            minutes = (remaining_ticks % 1000) * 60 // 1000
            rules["CurrentServerTime_formatted"] = f"Day {total_days}, {hours:02d}:{minutes:02d}"
            rules["CurrentServerTime_houronly"] = f"{hours:02d}"
            rules["CurrentServerTime_minutesonly"] = f"{minutes:02d}"
            rules["CurrentServerTime_dayonly"] = f"{total_days}"

            data = {
                "currentPlayers": rules.get("CurrentPlayers", 0),
                "maxPlayers": rules.get("MaxPlayers", 0),
                "serverVersion": rules.get("ServerVersion", ""),
                "gameHost": rules.get("GameHost", ""),
                "ip": rules.get("IP", ""),
                "port": rules.get("Port", ""),
                "levelName": rules.get("LevelName", ""),
                "gameName": rules.get("GameName", ""),
                "currentservertime": rules.get("CurrentServerTime", ""),
                "currentservertime_formatted": rules.get("CurrentServerTime_formatted", ""),
                "currentservertime_houronly": rules.get("CurrentServerTime_houronly", ""),
                "currentservertime_minutesonly": rules.get("CurrentServerTime_minutesonly", ""),
                "currentservertime_dayonly": rules.get("CurrentServerTime_dayonly", "")
            }

            system_info = self.get_system_info()
            data.update(system_info)
            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.send_header('Access-Control-Allow-Origin', '*')  # Allow requests from any origin
            self.end_headers()
            self.wfile.write(json.dumps(data).encode())  # Encode data as JSON
        elif self.path == '/':
            # Fetch public IP address
            public_ip = self.get_public_ip()
            if public_ip:
                html_content = f"""
                <html>
                <head>
                    <title>Vanilla Server 7 Days To Die (7DTD)</title>
                    <link rel="icon" type="image/x-icon" href="https://github.com/publicdomain-nocopyright/7DTD-Public-Vanilla-Server/releases/download/in-game-server-info-background/Vanila_Server_Logo.png">
                    <script>

                        // Function to redirect to Steam
                        function redirectToSteam() {{
                            window.location.href = 'steam://connect/{public_ip}:26900';
                            // Redirect to GitHub after a short delay

                        }}
                        //setTimeout(redirectToSteam, 500); // 5 seconds delay
                   
                    </script>
                </head> 
                <body>
                    
    <img src="https://github.com/publicdomain-nocopyright/7DTD-Public-Vanilla-Server/blob/main/splashscreen/website_logo_Vanilla Server Recreation logoxcf.png?raw=true">
    <h2>7 Days To Die Vanilla Public Server</h2>
    <img height="100px" src="https://github.com/publicdomain-nocopyright/7DTD-Public-Vanilla-Server/blob/main/splashscreen/output-onlinegiftools.gif?raw=true">
    <p>Accept request to join the server.</p>
    <a href="steam://connect/{public_ip}:26900"><p>Click here to join the server</p></a>

    <style> 
        body {{
            font-family: "Open Sans", Arial, Helvetica, sans-serif;
            background-image: url('https://github.com/publicdomain-nocopyright/7DTD-Public-Vanilla-Server/blob/main/splashscreen/website_background_Vanilla Server Recreation logoxcf.png?raw=true');
            background-attachment: fixed;
            background-position: center center;
            background-size: cover; 
        }}
        
        p, h2 {{   
            text-align: center;      
            color: #e8e8e8;
            text-shadow: #222222 1px 0 10px;
        }}
       
        img {{ 
            display: block;
            margin-left: auto;
            margin-right: auto;
        }}
    </style>


                    <script>
                            (async () => {{
                            console.log('Started');
                            while (true) {{
  
              async function fetchData() {{
    try {{
        const response = await fetch('/data');
        const data = await response.json();
        console.log("Fetching data _______________-");
        window.dataglobal = data;
        document.getElementById('currentPlayers').innerText = data.currentPlayers;
        document.getElementById('maxPlayers').innerText = data.maxPlayers;
        document.getElementById('serverVersion').innerText = data.serverVersion;
        document.getElementById('gameHost').innerText = data.gameHost;
        document.getElementById('ip').innerText = data.ip;
        document.getElementById('port').innerText = data.port;
        document.getElementById('levelName').innerText = data.levelName;
        document.getElementById('gameName').innerText = data.gameName;
        document.getElementById('currentservertime_formatted').innerText = data.currentservertime_formatted;
        window.current_ticks = data.currentservertime;
    }} catch (error) {{
        console.error('Error fetching data:', error);
    }}
}}

// Call the function to fetch data
await fetchData();


                                    //Timer counting and recallibration with the server time.
                                    for (let i = 0; i < 5; i++) {{
                                    console.log("Simulating time _______________-")
                                    await new Promise((res) => {{
                                        setTimeout(() => {{
                                        


                                    let data = window.dataglobal;
                                    function updateFormattedTime() {{

                                        let ticks_per_day = 24000;
                                        let timeElement = document.getElementById('currentservertime');

                                        let total_days = Math.floor(window.current_ticks / ticks_per_day);
                                        let remaining_ticks = window.current_ticks % ticks_per_day;
                                        let hours = Math.floor(remaining_ticks / 1000);
                                        let minutes = Math.floor((remaining_ticks % 1000) / (1000 / 60));
                                        let formatted = 'Day ' + total_days + ', ' + hours.toString().padStart(2, '0') + ':' + minutes.toString().padStart(2, '0');
                                        timeElement.innerText = formatted;
                                        console.log(" trying to update formatted time");
                                    }}

                                    
                                    

                                  
                              
                                        console.log(" current ticks: ",window.current_ticks);
                                        if (data && data.currentservertime) {{
                                        if (window.previousfetch < data.currentservertime) {{
                                            current_ticks = data.currentservertime;
                                        }}
                                        
                                        window.previousfetch = data.currentservertime;
                                        }}


                                        // Initial update
                                        window.current_ticks = parseInt(window.current_ticks) + parseInt(6);
                                        console.log(" after ticks: ",window.current_ticks);
                                        updateFormattedTime();

                                    
                                      res();
        }}, 2000);
      }});
    }}


  }}
}})();


                    
                   
            
                        
              
                                    
                                    
                              




                               
                     
                 
                    </script>
                    <p>Current Players: <span id="currentPlayers"></span></p>
                    <p>Max Players: <span id="maxPlayers"></span></p>
                    <p>Server Version: <span id="serverVersion"></span></p>
                    <p>Game Host: <span id="gameHost"></span></p>
                    <p>IP: <span id="ip"></span></p>
                    <p>Port: <span id="port"></span></p>
                    <p>Level Name: <span id="levelName"></span></p>
                    <p>Game Name: <span id="gameName"></span></p>
                    <p>Current Server Time: <span id="currentservertime_formatted"></span></p>
                    <p>Active Server Time: <span id="currentservertime"></span></p>
                </body>
                </html>
                """
                self.send_response(200)
                self.send_header('Content-type', 'text/html')
                self.end_headers()
                self.wfile.write(html_content.encode('utf-8'))
            else:
                self.send_response(500)
                self.end_headers()
                self.wfile.write(b'Internal Server Error')
        else:
            self.send_response(404)
            self.end_headers()
            self.wfile.write(b'404 Not Found')

    def get_public_ip(self):
        try:
            response = requests.get('https://api.ipify.org')
            if response.status_code == 200:
                return response.text
            else:
                return None
        except Exception as e:
            self.log_message("Error fetching public IP: %s", e)
            return None

def run(server_class=HTTPServer, handler_class=RedirectHandler, port=80):
    server_address = ('', port)
    httpd = server_class(server_address, handler_class)
    print('Server started at localhost:' + str(port))
    httpd.serve_forever()

if __name__ == '__main__':
    run()
