@echo off
cd /d "C:\Users\D365\squishy-shop"
start "" http://localhost:5000/
start "" http://localhost:5000/admin
python server.py
pause
