@echo off
cd /d C:\Users\quase\DOCUME~1\LIGAOE~1
title Progresso - Gemini Julho (feche a janela ou Ctrl+C para sair)
echo Mostrando as ultimas linhas de JULHO\log_execucao.txt e acompanhando ao vivo...
echo.
powershell -NoExit -Command "Get-Content -Path 'JULHO\log_execucao.txt' -Wait -Tail 40"
