@echo off
setlocal
title Rathyon - Instalar Extensao VS Code

set "SRC=%~dp0"
set "SRC=%SRC:~0,-1%"
set "VER=0.2.0"
set "DEST=%USERPROFILE%\.vscode\extensions\fumiko0701.rathyon-%VER%"

if not exist "%SRC%\package.json" (
    powershell -NoProfile -Command "Add-Type -AssemblyName PresentationFramework; [System.Windows.MessageBox]::Show('Coloque este .bat dentro da pasta vscode-rathyon.','Rathyon','OK','Error')"
    exit /b 1
)

if exist "%DEST%" (
    powershell -NoProfile -Command "Add-Type -AssemblyName PresentationFramework; [System.Windows.MessageBox]::Show('Extensao ja instalada em:%0D%0A%DEST%0D%0A%0D%0ARemova a pasta manualmente para reinstalar.','Rathyon','OK','Warning')"
    exit /b 1
)

if not exist "%USERPROFILE%\.vscode\extensions" mkdir "%USERPROFILE%\.vscode\extensions"

xcopy /E /I /Y "%SRC%" "%DEST%" >nul
if errorlevel 1 (
    powershell -NoProfile -Command "Add-Type -AssemblyName PresentationFramework; [System.Windows.MessageBox]::Show('Falha ao copiar a extensao. Verifique permissoes.','Rathyon','OK','Error')"
    exit /b 1
)

powershell -NoProfile -Command "Add-Type -AssemblyName PresentationFramework; [System.Windows.MessageBox]::Show('Extensao instalada. Feche o VS Code por completo e reabra.','Rathyon','OK','Information')"

endlocal