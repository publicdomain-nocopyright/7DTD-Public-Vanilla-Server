@ECHO OFF
REM python webserver.py
start "Webserver" python webserver.py < nul

REM TODO: Run webserver under cmd and exit the whole cmd if launched from fresh cmd.
REM Force kill the main thread.
