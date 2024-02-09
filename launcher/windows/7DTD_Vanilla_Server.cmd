@ECHO OFF && TITLE 7 Days To Die Public Vanilla Server Launcher

ECHO 1. Checking if your Windows Operating System have curl preinstalled. 
ECHO    (It's available starting with Windows 10)
WHERE curl >nul 2>nul
IF %ERRORLEVEL% NEQ 0 (COLOR 0c && ECHO You need to download curl program for this launcher to work or ask BoQsc for bitsadmin support: Windows >7. && PAUSE && EXIT ) ELSE ( ECHO OK curl was found)
ECHO.

ECHO 2. Receiving 7 Days To Die Public Vanilla Server information
CURL "https://raw.githubusercontent.com/publicdomain-nocopyright/ip-records/main/7dtd-public-vanilla-server.txt" > "%TEMP%\7dtd-public-vanilla-server.txt"
SET /P Server_IP= < "%TEMP%\7dtd-public-vanilla-server.txt"

IF "%Server_IP%" == "" (
	CLS
	COLOR 0c
	ECHO [curl] Failed to retrieve Public Vanilla Server IP.
	PAUSE
	EXIT
) ELSE (
	ECHO [curl] 7 Days To Die Public Vanilla Server IP: %Server_IP%
)
ECHO.

:reconnect
ECHO 3. Checking if Vanilla Server is alive before trying to connect.
curl -s %Server_IP%  
IF ERRORLEVEL 7 (
	COLOR 0A
	ECHO [curl] 7DTD Vanilla Server is offline. 
	ECHO Trying to reconnect in...
	TIMEOUT /t 3
	CLS
	GOTO :reconnect
)
IF ERRORLEVEL 0 ECHO Vanilla Server is Online. && 
ECHO.

IF NOT "%Server_IP%" == "" (
	ECHO 4. You are about to try to connect to Vanilla Server
	REM EXPLORER steam://run/251570//+connect 51.178.20.227:62550 
	EXPLORER "steam://connect/%Server_IP%"
	REM TIMEOUT /t 15
) 
