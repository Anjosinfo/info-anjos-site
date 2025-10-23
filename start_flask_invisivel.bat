@echo off
REM Caminho do seu ambiente virtual
SET VENV_PYTHON=C:\Users\Jessica Anjos\Documents\info-anjos-site\venv\Scripts\pythonw.exe

REM Caminho do seu app.py
SET APP_PATH=C:\Users\Jessica Anjos\Documents\info-anjos-site\app.py

REM Caminho do log de erros
SET LOG_PATH=C:\Users\Jessica Anjos\Documents\info-anjos-site\flask_errors.log

REM Rodar Flask invisível sem abrir CMD, enviando erros para log
"%VENV_PYTHON%" "%APP_PATH%" 2>> "%LOG_PATH%"
