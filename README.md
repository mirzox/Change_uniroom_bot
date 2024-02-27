systemctl daemon-reload
systemctl start unibot
systemctl enable unibot
systemctl status unibot

project service file location:
- /etc/systemd/system/unibot.service

python3 -m venv venv
source venv/bin/activate
pip3 install -r requirements.txt
source .env
venv/bin/python3 main.py