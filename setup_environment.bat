@echo off
conda create -n mti-chatbot python=3.11 -y
call conda activate mti-chatbot
pip install -r requirements.txt
pause
