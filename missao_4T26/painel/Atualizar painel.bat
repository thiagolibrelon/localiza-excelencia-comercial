@echo off
setlocal
rem ==========================================================================================
rem  Atualiza o painel: le o CSV exportado da consulta e grava dados.js na pasta do painel.
rem  Este arquivo fica no SEU computador, junto de atualizar_painel.py (nao na pasta compartilhada).
rem  Na primeira vez o script pergunta o CSV (ou a pasta de CSVs) e a pasta do painel; depois lembra.
rem ==========================================================================================
cd /d "%~dp0"
set "PY=python"
where python >nul 2>nul || set "PY=py -3"
%PY% "%~dp0atualizar_painel.py" %*
if errorlevel 1 goto erro
echo.
echo  Pronto. O OneDrive envia o dados.js em alguns segundos; quem abrir o painel ja ve o dia novo.
echo  (esta janela fecha sozinha)
timeout /t 15 >nul
exit /b 0

:erro
echo.
echo  Nao foi possivel atualizar o painel. Leia a mensagem acima.
echo  Se aparecer "python nao e reconhecido", instale o Python 3 e o pandas (veja o LEIA-ME).
echo.
pause
exit /b 1
