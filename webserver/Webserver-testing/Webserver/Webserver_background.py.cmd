@ECHO OFF
CD "%~DP0"
python "%~DP0\Webserver_background.py"
IF ERRORLEVEL 1 PAUSE
