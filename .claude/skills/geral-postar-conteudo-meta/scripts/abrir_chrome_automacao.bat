@echo off
setlocal

if "%~1"=="" (
    echo Uso: abrir_chrome_automacao.bat NOME_CLIENTE
    echo.
    echo   NOME_CLIENTE   o mesmo nome usado no setup_perfil_automacao.bat pra esse cliente
    echo.
    echo Exemplo: abrir_chrome_automacao.bat ClienteExemplo
    echo.
    echo Se ainda nao existe perfil de automacao pra esse cliente, rode primeiro:
    echo   setup_perfil_automacao.bat NOME_CLIENTE "NOME_DO_PERFIL_CHROME_JA_LOGADO"
    exit /b 1
)

set CLIENTE=%~1
set DEST=C:\Users\%USERNAME%\AppData\Local\ChromeAutomationProfile_%CLIENTE%

if not exist "%DEST%" (
    echo Nao existe perfil de automacao para "%CLIENTE%" ainda.
    echo Rode primeiro: setup_perfil_automacao.bat %CLIENTE% "NOME_DO_PERFIL_CHROME_JA_LOGADO"
    exit /b 1
)

echo Fechando Chrome existente...
taskkill /F /IM chrome.exe >nul 2>&1
timeout /t 2 /nobreak >nul

REM NAO ressincroniza do perfil real aqui: esse perfil de automacao ja tem login
REM proprio (feito uma vez via setup_perfil_automacao.bat). Ressincronizar
REM sobrescreveria a sessao logada. Pra recriar do zero, rode setup de novo.

echo Abrindo Chrome com debug remoto (porta 9222) no perfil de automacao de %CLIENTE%...
start "" "C:\Program Files\Google\Chrome\Application\chrome.exe" --remote-debugging-port=9222 --user-data-dir="%DEST%" --profile-directory="Default" --no-first-run "https://business.facebook.com/latest/content_calendar"

echo.
echo Chrome abrindo no perfil de automacao de %CLIENTE%. Confira se a pagina/conta certa
echo do Meta Business Suite esta selecionada antes de rodar postar_conteudo.py.
pause
