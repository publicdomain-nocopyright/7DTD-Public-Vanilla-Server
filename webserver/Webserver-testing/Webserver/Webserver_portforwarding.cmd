@ECHO OFF
setlocal enabledelayedexpansion
IF NOT EXIST "%tmp%\upnpc-static.exe" (
	for /f delims^=^"^ tokens^=4 %%i in ('curl -s https://api.github.com/repos/miniupnp/miniupnp/releases/latest ^| findstr ^"browser_download_url.*zip^""
	') do (
	curl --location "%%i" > "%%~nxi"
	set "miniupnp_filename=%%~nxi"
	)
		echo !miniupnp_filename! sdc
	tar --extract --file=!miniupnp_filename! -C %tmp% upnpc-static.exe
	del "!miniupnp_filename!"

)



REM Portforwards Telnet access and Web Dashboard if enabled.
%tmp%\upnpc-static.exe -d 80 tcp
%tmp%\upnpc-static.exe -d 80 udp


set ip_address_string="IPv4 Address"
rem Uncomment the following line when using older versions of Windows without IPv6 support (by removing "rem")
rem set ip_address_string="IP Address"
for /f "usebackq tokens=2 delims=:" %%f in (`ipconfig ^| findstr /c:%ip_address_string%`) do (
    echo Your IP Address is: %%f
    set "ip_address=%%f"

)

%tmp%\upnpc-static.exe -a %ip_address% 80 80 tcp
%tmp%\upnpc-static.exe -a %ip_address% 80 80 udp



PAUSE