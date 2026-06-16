@echo off
:: discover_projector.bat – scans the local /24 subnet for hosts with port 5555 open.
:: Prints each IP on its own line.

:: Get the first non-loopback IPv4 address
for /f "tokens=2 delims=: " %%A in ('ipconfig ^| findstr /R /C:"IPv4 Address"') do (
    set "LOCAL=%%A"
    goto :found
)
:found
if "%LOCAL%"=="" (
    exit /b 0
)

:: Strip spaces
set "LOCAL=%LOCAL: =%"

:: Extract first three octets
for /f "tokens=1-4 delims=." %%a in ("%LOCAL%") do (
    set "BASE=%%a.%%b.%%c."
)

:: Loop 1-254 and test port 5555 using PowerShell Test-NetConnection
for /L %%i in (1,1,254) do (
    powershell -NoProfile -Command "if (Test-NetConnection -ComputerName %BASE%%%i -Port 5555 -InformationLevel Quiet) { Write-Host '%BASE%%%i' }"
)
