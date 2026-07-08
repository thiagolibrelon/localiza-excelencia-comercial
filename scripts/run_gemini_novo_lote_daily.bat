@echo off
cd /d C:\Users\quase\DOCUME~1\LIGAOE~1
echo. >> resultados\gemini_novo_lote\log_execucao.txt
echo ===== Execucao agendada: %date% %time% ===== >> resultados\gemini_novo_lote\log_execucao.txt
"C:\Users\quase\AppData\Local\Microsoft\WindowsApps\python.exe" scripts\analisar_gemini_novo_lote.py >> resultados\gemini_novo_lote\log_execucao.txt 2>&1
"C:\Users\quase\AppData\Local\Microsoft\WindowsApps\python.exe" scripts\notificar_ntfy.py >> resultados\gemini_novo_lote\log_execucao.txt 2>&1
