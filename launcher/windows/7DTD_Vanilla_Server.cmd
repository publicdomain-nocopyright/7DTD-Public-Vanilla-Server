@ECHO OFF && TITLE 7 Days To Die Public Vanilla Server Launcher

WHERE curl
IF %ERRORLEVEL% NEQ 0 ECHO You need to download curl program for this launcher to work. && PAUSE && EXIT 

ECHO Receiving 7 Days To Die Public Vanilla Server information
CURL "https://raw.githubusercontent.com/publicdomain-nocopyright/ip-records/main/7dtd-public-vanilla-server.txt" > "%TEMP%\7dtd-public-vanilla-server.txt"
SET /P Server_IP= < "%TEMP%\7dtd-public-vanilla-server.txt"

:reconnect
curl -s %Server_IP%  
IF ERRORLEVEL 7 (
	
	ECHO 7DTD Vanilla Server is offline. 
	ECHO Trying to reconnect in...
	TIMEOUT /t 3
	CLS
	GOTO :reconnect
)
IF ERRORLEVEL 0 ECHO Vanilla Server is Online.


IF NOT "%Server_IP%" == "" (
	ECHO 7 Days To Die Public Vanilla Server IP: %Server_IP%
	ECHO You are about to try to connect to Vanilla Server
	REM EXPLORER steam://run/251570//+connect 51.178.20.227:62550 
	EXPLORER "steam://connect/%Server_IP%"
	REM TIMEOUT /t 15
) ELSE (
	CLS
	ECHO Failed to retrieve Public Vanilla Server IP.
	PAUSE
)
