@echo off
cd /d C:\Users\quase\DOCUME~1\LIGAOE~1
if errorlevel 1 (
    echo ERRO: nao foi possivel localizar a pasta do projeto DOCUME~1\LIGAOE~1 1>&2
    exit /b 1
)
echo. >> JULHO\log_execucao.txt
echo ===== Execucao agendada: %date% %time% ===== >> JULHO\log_execucao.txt
"C:\Users\quase\AppData\Local\Microsoft\WindowsApps\python.exe" scripts\converter_julho.py >> JULHO\log_execucao.txt 2>&1
"C:\Users\quase\AppData\Local\Microsoft\WindowsApps\python.exe" scripts\notificar_inicio_ntfy.py >> JULHO\log_execucao.txt 2>&1
"C:\Users\quase\AppData\Local\Microsoft\WindowsApps\python.exe" scripts\analisar_gemini_julho.py >> JULHO\log_execucao.txt 2>&1
"C:\Users\quase\AppData\Local\Microsoft\WindowsApps\python.exe" scripts\consolidar_julho.py >> JULHO\log_execucao.txt 2>&1
echo -- Git commit/push do consolidado -- >> JULHO\log_execucao.txt
git add JULHO >> JULHO\log_execucao.txt 2>&1
git commit -m "Atualiza JULHO/consolidado (execucao automatica %date% %time%)" >> JULHO\log_execucao.txt 2>&1
git push >> JULHO\log_execucao.txt 2>&1
"C:\Users\quase\AppData\Local\Microsoft\WindowsApps\python.exe" scripts\notificar_ntfy.py JULHO\log_execucao.txt "Gemini Julho" >> JULHO\log_execucao.txt 2>&1
