@echo off
rem Starts a dedicated server
rem
rem -quit, -batchmode, -nographics: Unity commands
rem -configfile			  : Allows server settings to be set up in an xml config file. Use no path if in same dir or full path.
rem -dedicated                    : Has to be the last option to start the dedicated server.

set LOGTIMESTAMP=


IF EXIST 7DaysToDieServer.exe (
	set GAMENAME=7DaysToDieServer
	set LOGNAME=output_log_dedi
) ELSE (
	set GAMENAME=7DaysToDie
	set LOGNAME=output_log
)

:: --------------------------------------------
:: REMOVE OLD LOGS (only keep latest 20)

for /f "tokens=* skip=19" %%F in ('dir %GAMENAME%_Data\%LOGNAME%*.txt /o-d /tc /b') do del %GAMENAME%_Data\%%F



:: --------------------------------------------
:: BUILDING TIMESTAMP FOR LOGFILE

:: Check WMIC is available
WMIC.EXE Alias /? >NUL 2>&1 || GOTO s_start

:: Use WMIC to retrieve date and time
FOR /F "skip=1 tokens=1-6" %%G IN ('WMIC Path Win32_LocalTime Get Day^,Hour^,Minute^,Month^,Second^,Year /Format:table') DO (
	IF "%%~L"=="" goto s_done
	Set _yyyy=%%L
	Set _mm=00%%J
	Set _dd=00%%G
	Set _hour=00%%H
	Set _minute=00%%I
	Set _second=00%%K
)
:s_done

:: Pad digits with leading zeros
Set _mm=%_mm:~-2%
Set _dd=%_dd:~-2%
Set _hour=%_hour:~-2%
Set _minute=%_minute:~-2%
Set _second=%_second:~-2%

Set LOGTIMESTAMP=__%_yyyy%-%_mm%-%_dd%__%_hour%-%_minute%-%_second%

:s_start


:: --------------------------------------------
:: STARTING SERVER


echo|set /p="251570" > steam_appid.txt
set SteamAppId=251570
set SteamGameId=251570

set LOGFILE=%~dp0\%GAMENAME%_Data\%LOGNAME%%LOGTIMESTAMP%.txt


echo Writing log file to: %LOGFILE%

start %GAMENAME% -logfile "%LOGFILE%" -quit -batchmode -nographics "-configfile=%~DP0serverconfig.xml" -dedicated


echo Starting server ...
REM timeout 15

cls

echo.
echo Server running in background, you can close this window.
echo You can check the task manager if the server process is really running.
echo.
echo.

REM pause
