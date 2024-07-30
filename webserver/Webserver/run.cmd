@ECHO OFF
REM start /B "" python webserver.py

REM TODO: Run webserver under cmd and exit the whole cmd if launched from fresh cmd.
REM Force kill the main thread.
python webserver.py
EXIT