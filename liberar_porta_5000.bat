@echo off
title LIBERAR PORTA 5000 - WINDOWS FIREWALL
echo ==========================================
echo  LIBERANDO PORTA TCP 5000 NO FIREWALL
echo ==========================================
echo.
netsh advfirewall firewall delete rule name="Flask Porta 5000" >nul 2>nul
netsh advfirewall firewall add rule name="Flask Porta 5000" dir=in action=allow protocol=TCP localport=5000
echo.
echo Regra criada. Verificando a porta:
netstat -ano | findstr :5000
echo.
echo Se aparecer 0.0.0.0:5000 LISTENING, o Flask esta aceitando conexoes externas.
echo.
pause
