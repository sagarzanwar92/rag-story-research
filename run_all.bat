@echo off
title RAG Story Researcher Launcher

echo [1/3] Activating ai_master environment...
:: This moves up one level to find ai_master and activates it
call ..\ai_master\Scripts\activate

echo [2/3] Starting Backend (FastAPI)...
:: 'start' opens a new terminal window for the backend
start "RAG BACKEND" cmd /k "..\ai_master\Scripts\activate && python backend.py"

echo Waiting for backend to warm up...
timeout /t 5

echo [3/3] Starting Frontend (Streamlit)...
start "RAG FRONTEND" cmd /k "..\ai_master\Scripts\activate && streamlit run frontend.py"

echo.
echo ======================================================
echo  SYSTEM ONLINE: Backend and Frontend are launching.
echo  Keep the other windows open while chatting!
echo ======================================================
pause