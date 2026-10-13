@echo off
setlocal
rem ==========================================================================================
rem  Abre o painel de carga operacional (venda interna DVINT) e registra o acesso.
rem  Registro: data, hora, usuario do Windows e computador, em logs\<usuario>.csv
rem  (um arquivo por pessoa). Serve so para medir o uso; o painel mostra apenas contagens.
rem ==========================================================================================
set "PASTA=%~dp0"
rem Se este arquivo ficar FORA da pasta do painel (ex.: copiado para a area de trabalho),
rem troque a linha "set PASTA" acima pelo caminho da pasta sincronizada, terminando em \ . Exemplo:
rem set "PASTA=C:\Users\seu.usuario\Localiza\Excelencia Comercial - Documentos\Painel Carga Operacional\Gestao\"

if exist "%PASTA%painel.html" goto registrar
echo.
echo  Nao encontrei o painel.html nesta pasta:
echo  "%PASTA%"
echo.
echo  Confira se a pasta do painel esta sincronizada com o OneDrive
echo  (botao direito na pasta: "Sempre manter neste dispositivo").
echo.
pause
exit /b 1

:registrar
if not exist "%PASTA%logs" mkdir "%PASTA%logs" 2>nul
set "LOG=%PASTA%logs\%USERNAME%.csv"
if exist "%LOG%" goto gravar
2>nul >"%LOG%" echo data;hora;usuario;computador
:gravar
2>nul >>"%LOG%" echo %DATE%;%TIME%;%USERNAME%;%COMPUTERNAME%

start "" "%PASTA%painel.html"
exit /b 0
