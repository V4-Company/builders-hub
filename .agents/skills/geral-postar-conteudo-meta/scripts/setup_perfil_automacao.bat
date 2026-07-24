@echo off
setlocal

if "%~1"=="" (
    echo Uso: setup_perfil_automacao.bat NOME_CLIENTE PERFIL_CHROME_ORIGEM
    echo.
    echo   NOME_CLIENTE         nome livre pra identificar esse cliente ^(ex: ClienteExemplo^)
    echo   PERFIL_CHROME_ORIGEM nome da pasta do perfil do Chrome ja logado nesse cliente
    echo                        ^(ver em chrome://version, campo "Profile Path" - pegue so a
    echo                        ultima pasta do caminho, ex: "Profile 10" ou "Default"^)
    echo.
    echo Exemplo: setup_perfil_automacao.bat ClienteExemplo "Profile 10"
    exit /b 1
)
if "%~2"=="" (
    echo Falta o segundo parametro: nome do perfil Chrome de origem. Veja o uso acima.
    exit /b 1
)

set CLIENTE=%~1
set PERFIL_ORIGEM=%~2
set DEST=C:\Users\%USERNAME%\AppData\Local\ChromeAutomationProfile_%CLIENTE%
set ORIGEM=C:\Users\%USERNAME%\AppData\Local\Google\Chrome\User Data\%PERFIL_ORIGEM%

echo Cliente: %CLIENTE%
echo Perfil de origem: %ORIGEM%
echo Perfil de automacao (destino): %DEST%\Default
echo.
echo ATENCAO: isso cria (ou recria do zero) o perfil de automacao deste cliente.
echo Se ja existir e tiver login funcionando, isso vai te obrigar a logar de novo.
pause

taskkill /F /IM chrome.exe >nul 2>&1
timeout /t 2 /nobreak >nul

echo Copiando dados essenciais do perfil de origem (sem cache)...
robocopy "%ORIGEM%" "%DEST%\Default" /E /R:1 /W:1 /NFL /NDL /NJH /XD "Cache" "Code Cache" "GPUCache" "DawnWebGPUCache" "Service Worker" "Shared Dictionary" "Extensions" "Local Extension Settings" "Extension State" "DNR Extension Rules" "shared_proto_db"
copy /Y "C:\Users\%USERNAME%\AppData\Local\Google\Chrome\User Data\Local State" "%DEST%\Local State"

echo Abrindo Chrome com debug remoto (porta 9222) no perfil de automacao de %CLIENTE%...
start "" "C:\Program Files\Google\Chrome\Application\chrome.exe" --remote-debugging-port=9222 --user-data-dir="%DEST%" --profile-directory="Default" --no-first-run "https://business.facebook.com/latest/content_calendar"

echo.
echo Se pedir login (normal ao recriar o perfil), faca uma vez so.
echo Confirme tambem que a pagina/conta do Meta Business Suite certa (%CLIENTE%) esta selecionada.
echo Das proximas vezes, use: abrir_chrome_automacao.bat %CLIENTE%
pause
